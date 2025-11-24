# Buried_Volume_and_Bite_Angle_Calculation_Using_Morfeus
This project provides a streamlined workflow for extracting and analyzing geometric descriptors of metal complexes, starting from Gaussian output files and ending with quantitative steric and geometric parameters.

---

# Geometry Analysis Toolkit for Metal Complexes

## 1. Overview

This repository provides a compact workflow for analyzing **steric and geometric parameters** of metal complexes using the **Morfeus** library.
It consists of two Python scripts:

1. **`log_to_xyz.py`** – Extracts molecular coordinates from Gaussian `.log` files and converts them to standard `.xyz` format.
2. **`xyz.py`** – Processes `.xyz` structures to compute:

   * **Buried Volume** and **%V<sub>bur</sub>**
   * **Free volume** and **distal volume**
   * **Bite angle** between donor atoms and the metal center

All results are compiled into a single CSV file for efficient downstream analysis.

This toolkit is particularly suited for:

* Steric profiling of ligands
* High-throughput screening campaigns
* Structure–reactivity & structure–selectivity studies
* Automated post-processing of Gaussian calculations

---

## 2. Script Descriptions

### **2.1 `log_to_xyz.py` — Gaussian Log → XYZ Converter**

**Purpose:**
Extracts molecular geometry from the `Input orientation` block found in Gaussian `.log` files and generates clean `.xyz` coordinate files.

**Features:**

* Automatically scans the working directory for `.log` files.
* Converts atomic numbers to element symbols using a full periodic table.
* Produces XYZ files in the format:

```
N
Generated from Gaussian log file
El   x   y   z
...
```

**Use Case:**
Standardizes geometries for subsequent Morfeus analysis.

---

### **2.2 `xyz.py` — Steric & Geometric Analysis for XYZ Files**

**Purpose:**
Computes steric descriptors (%V<sub>bur</sub>, buried volume, free volume, distal volume) and geometric descriptors (bite angle) for each `.xyz` structure using Morfeus.

**Key Capabilities:**

#### **(1) XYZ Parsing**

* Loads atoms and Cartesian coordinates using a custom XYZ reader.
* Assumes the **last atom is the metal center** (1-based index).

#### **(2) Automatic Donor Atom Detection**

* Predefined metal list:

  ```
  {"Pd", "Pt", "Ni", "Co", "Rh", "Ir", "Fe", "Cu", "Zn", "Au", "Ag"}
  ```
* Selects the **first two non-metal atoms** as donor atoms for bite angle calculations.

#### **(3) Buried Volume Analysis**

For each radius in `RADII = [3.0, 4.0, 5.0]`, the script computes:

* `%Vbur`
* `buried_volume`
* `free_volume`
* `distal_volume`

using the `morfeus.BuriedVolume` class.

#### **(4) Bite Angle Calculation**

Using `morfeus.BiteAngle`, the script computes:

* Donor–Metal–Donor **bite angle**
* **Inversion flag** indicating a flipped ligand geometry

#### **(5) Unified CSV Output**

All results are merged into:

```
combined_vbur_biteangle_results.csv
```

with columns for:

* file name
* %V<sub>bur</sub> and volumetric descriptors for each radius
* bite angle & inversion status

---

## 3. Workflow

### **Step 1 — Convert Gaussian Logs**

Place `log_to_xyz.py` in the directory containing `.log` files:

```bash
python log_to_xyz.py
```

Each `.log` will produce a corresponding `.xyz`.

---

### **Step 2 — Analyze Steric and Geometric Parameters**

Install Morfeus:

```bash
pip install morfeus-ml
```

Run the analysis:

```bash
python xyz.py
```

Output:
`combined_vbur_biteangle_results.csv`

---

## 4. Dependencies

* Python 3.x
* Packages:

  * `morfeus-ml` (steric and geometric analysis)
  * Standard libraries: `os`, `csv`

Recommended installation (Conda):

```bash
conda activate chem
pip install morfeus-ml
```

---

## 5. References

### **Morfeus Library**

Official documentation:
🔗 [https://digital-chemistry-laboratory.github.io/morfeus/](https://digital-chemistry-laboratory.github.io/morfeus/)

GitHub repository:
🔗 [https://github.com/digital-chemistry-laboratory/morfeus](https://github.com/digital-chemistry-laboratory/morfeus)

### **Primary Literature**

Please cite the Morfeus methodology if used in scientific publications:

1. **Falivene, L.; Cao, Z.; Petta, A.; Serra, L.; Poater, A.; Oliva, R.; Scarano, V.; Cavallo, L.**
   *Towards the online computer-aided design of catalytic pockets.*
   **Nat. Chem.** 2019, 11, 872–879.
   [https://doi.org/10.1038/s41557-019-0319-5](https://doi.org/10.1038/s41557-019-0319-5)

2. **Falivene, L.; Cao, Z.; Petta, A.; Serra, L.; Poater, A.; Cavallo, L.**
   *Buried Volume Analysis for Phosphine and N-Heterocyclic Carbene Ligands.*
   **Organometallics** 2016, 35, 2286–2293.
   [https://doi.org/10.1021/acs.organomet.6b00371](https://doi.org/10.1021/acs.organomet.6b00371)

3. **Digital Chemistry Laboratory, EPFL.**
   *Morfeus: A Python library for molecular shape and steric analysis.*
   (software documentation and implementation details).

---

## 6. License

You may include your preferred license here, e.g.:

```
MIT License
```

---

## 7. Contact

For questions, improvements, or feature requests, feel free to open an issue or contact the repository maintainer.


