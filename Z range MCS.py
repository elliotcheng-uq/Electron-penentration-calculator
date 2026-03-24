# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 13:58:58 2025

@author: uqhche13
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import re
import csv
import statistics
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def parse_trajectories(file_path):
    z_ranges = {}
    current_traj = None
    collecting = False
    z_values = []

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()

            match = re.match(r'Trajectory\s+(\d+)', line)
            if match:
                if current_traj is not None and z_values:
                    z_ranges[current_traj] = max(z_values) - min(z_values)
                current_traj = int(match.group(1))
                z_values = []
                collecting = False
                continue

            if line.startswith('X'):
                collecting = True
                continue
            elif collecting and line == '':
                collecting = False
                continue

            if collecting:
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        z = float(parts[2])
                        z_values.append(z)
                    except ValueError:
                        pass

        if current_traj is not None and z_values:
            z_ranges[current_traj] = max(z_values) - min(z_values)

    return z_ranges

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Data files", "*.dat"), ("All files", "*.*")])
    if file_path:
        result_box.delete("1.0", tk.END)
        clear_plot()
        try:
            z_ranges = parse_trajectories(file_path)

            if not z_ranges:
                result_box.insert(tk.END, "No trajectory data found.\n")
                return

            for traj, z_range in z_ranges.items():
                result_box.insert(tk.END, f"Trajectory {traj}: Max Z Range = {z_range:.2f}\n")

            # Summary stats
            
            all_ranges = list(z_ranges.values())
            avg_range = statistics.mean(all_ranges)
            max_range = max(all_ranges)
            result_box.insert(tk.END, f"\nAverage Max Z Range: {avg_range:.2f}\n")
            result_box.insert(tk.END, f"Absolute Max Z Range: {max_range:.2f}\n")

            export_button.config(state=tk.NORMAL)
            export_button.z_ranges = z_ranges
            export_button.stats = {'average': avg_range, 'max': max_range}
            
            show_plot(z_ranges)
            # print avg and max range
            print('average Z')
            print(avg_range)
            print('max Z')
            print(max_range)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file:\n{e}")

def export_to_csv():
    z_ranges = export_button.z_ranges
    stats = export_button.stats
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
    if save_path:
        with open(save_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Trajectory", "Max Z Range"])
            for traj, z_range in z_ranges.items():
                writer.writerow([traj, z_range])
            writer.writerow([])
            writer.writerow(["Average Max Z Range", stats['average']])
            writer.writerow(["Absolute Max Z Range", stats['max']])
        messagebox.showinfo("Export Complete", f"Results saved to:\n{save_path}")

def show_plot(z_ranges):
    fig, ax = plt.subplots(figsize=(6, 3))
    traj_ids = list(z_ranges.keys())
    ranges = list(z_ranges.values())

    ax.bar(traj_ids, ranges, color='skyblue')
    ax.set_title("Max Z Range per Trajectory")
    ax.set_xlabel("Trajectory ID")
    ax.set_ylabel("Z Range")

    # Embed the plot in tkinter
    global canvas
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def clear_plot():
    global canvas
    for widget in plot_frame.winfo_children():
        widget.destroy()
    canvas = None

# GUI setup
root = tk.Tk()
root.title("Trajectory Z Range Calculator")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

btn = tk.Button(frame, text="Select .data File", command=browse_file)
btn.pack()

result_box = tk.Text(frame, width=60, height=15)
result_box.pack(pady=10)

export_button = tk.Button(frame, text="Export to CSV", command=export_to_csv, state=tk.DISABLED)
export_button.pack(pady=5)

plot_frame = tk.Frame(root)
plot_frame.pack()

canvas = None

root.mainloop()
