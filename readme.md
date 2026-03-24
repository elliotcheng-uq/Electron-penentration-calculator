# ⚛ Electron Penetration Calculator

> Monte Carlo Simulation (MCS) of electron penetration depth for 100 / 120 / 200 kV beams across selectable elements.

---

## Overview

This tool simulates the penetration depth of high-energy electrons into a target material using a **single-scattering Monte Carlo approach** combined with **Bethe continuous energy loss**. It is useful in electron microscopy, materials science, and radiation physics to estimate interaction volumes.

Two versions are available:

| Version | File | Description |
|---|---|---|
| Desktop (Python) | `Z range MCS.py` | Tkinter GUI, reads `.dat` trajectory files |
| Web | `electron-penetration-calculator.html` | Runs fully in the browser, no install needed |

---

## Web Version Features

- **Element selection by Z number** — choose from 34 common elements (Z 1–82) via dropdown
- **Three beam voltages** — 100 kV, 120 kV, 200 kV
- **Configurable simulation** — set number of electrons (50–1000) and max steps per trajectory
- **Live histogram** — Z-range distribution chart rendered with Chart.js
- **Summary statistics** — average penetration depth, absolute max, standard deviation
- **Trajectory log** — scrollable per-electron depth readout with inline bar chart
- **CSV export** — download all trajectory data and stats
- **Background color picker** — customise via colour wheel or hex input

---

## Physics

### Kanaya–Okayama Range (analytical estimate)

The K-O formula gives an empirical estimate of the electron range in µm:

```
R = (0.0276 · A · E₀^1.67) / (ρ · Z^0.89)
```

Where:
- `A` = atomic mass (g/mol)
- `E₀` = beam energy (keV)
- `ρ` = material density (g/cm³)
- `Z` = atomic number

This is used to set the simulation step size as a fraction of the estimated range.

### Monte Carlo Simulation

Each electron trajectory follows these steps:

1. **Initialisation** — electron starts at the surface (z = 0) travelling in the −z direction
2. **Scattering** — at each step, a polar scattering angle is sampled from the **screened Rutherford cross-section**:

   ```
   cos θ = 1 − (2α · ξ) / (1 + α − ξ)
   ```

   where `α = 3.4×10⁻³ · Z^0.67 / E` is the screening parameter and `ξ` is a uniform random number.

3. **Direction update** — the new direction vector is calculated from the scattering angles using a rotation matrix
4. **Energy loss** — continuous slowing down via the **Bethe formula**:

   ```
   dE/ds = (78500 · Z) / (A · E) · ln(1.166 · E / J) · ρ × 10⁻⁷
   ```

   where `J = (9.76Z + 58.5 · Z^-0.19) × 10⁻³` keV is the mean ionisation potential.

5. **Termination** — trajectory ends when the electron backscatters (z > 0.5 nm) or drops below 0.5 keV

The maximum z-depth reached by each trajectory is recorded as its **Z-range** (penetration depth).

---

## Desktop Version (Python)

### Requirements

```
python >= 3.8
matplotlib
tkinter (usually bundled with Python)
```

Install dependencies:

```bash
pip install matplotlib
```

### Usage

```bash
python "Z range MCS.py"
```

The app will open a GUI where you can:

1. Click **Select .data File** to load a trajectory file (`.dat` or `.*`)
2. View per-trajectory Z-range values and summary statistics
3. See a bar chart of the results
4. Export results to CSV

### Input File Format

The `.dat` trajectory files should follow this structure:

```
Trajectory 1
X    Y    Z
0.0  0.0  0.00
0.1  0.0  -12.3
...

Trajectory 2
X    Y    Z
...
```

Each trajectory block begins with `Trajectory N`, followed by a header row starting with `X`, then data rows with at least 3 columns (X, Y, Z positions in nm).

---

## Output

| Field | Description |
|---|---|
| Max Z Range (per trajectory) | Largest depth reached by that electron |
| Average Max Z Range | Mean across all trajectories |
| Absolute Max Z Range | Overall deepest penetration |
| Std Deviation | Spread of penetration depths |

---

## Example Results

| Element | Z | Voltage | Avg Depth (approx.) |
|---|---|---|---|
| Carbon | 6 | 100 kV | ~1200 nm |
| Aluminium | 13 | 100 kV | ~550 nm |
| Copper | 29 | 200 kV | ~180 nm |
| Gold | 79 | 100 kV | ~60 nm |

*Results are stochastic — values will vary slightly between runs.*

---

## File Structure

```
Electron-penentration-calculator/
├── Z range MCS.py                        # Desktop Python GUI
├── electron-penetration-calculator.html  # Web version (standalone)
├── LICENSE                               # GPL-3.0
└── README.md                             # This file
```

---

## License

This project is licensed under the **GNU General Public License v3.0** — see [LICENSE](LICENSE) for details.

---

## Author

**Elliot Cheng** · University of Queensland  
Created: April 2025
