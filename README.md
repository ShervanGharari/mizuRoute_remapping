# Remapping File Creation for mizuRoute

This repository provides tools and guidance for creating remapping files for use with the [mizuRoute](https://github.com/NCAR/mizuRoute) hydrological routing model. These remapping files are essential for linking model runoff outputs (e.g., from land surface or hydrologic models) to the routing units (HRUs or subbasins) used by mizuRoute.

## 📌 Overview

The remapping process establishes spatial correspondence between source runoff fields (e.g., gridded model output or shapefiles) and the routing elements used in mizuRoute. There are **two primary ways** to handle this remapping, each with different levels of integration with mizuRoute.

---

## 🔁 Remapping Approaches

### ✅ Option 1: Pre-remapped Runoff Field (No mizuRoute Internal Remapping)

In this approach, the runoff data is **pre-remapped** from the source format (e.g., gridded or other shapefile than routing HRUs or subbasins) to the routing HRUs or subbasins **before** running mizuRoute.

- **Advantages:**
  - mizuRoute reads the runoff field directly without needing an internal remapping step.
  - Offers complete control over the remapping method and accuracy.

- **Requirements:**
  - You must perform the spatial remapping externally (e.g., using a script or GIS tool - We use [easymore](https://github.com/ShervanGharari/easymore)).
  - The remapped runoff field must match the structure and IDs of the routing units used in mizuRoute.
  - **No remapping file is needed for mizuRoute** in this case.

---

### ✅ Option 2: Use mizuRoute's Internal Remapping Capability

In this approach, you provide a **remapping file** to mizuRoute along with the original runoff field (gridded or shapefile). mizuRoute will then internally map the runoff to its routing units using the provided mapping file.

- **Advantages:**
  - Simplifies workflow by allowing mizuRoute to handle the remapping internally.
  - Maintains separation between runoff model output and routing setup.

- **Requirements:**
  - You must generate a valid **remapping file** that links source cells or features to routing HRUs or subbasins.
  - The runoff field must retain its original spatial structure (e.g., latitude/longitude grid).
  - mizuRoute must be configured to use the internal remapping.

---

## 🛠 Requirements

- Python 3.x
- `geopandas`, `shapely`, `numpy`, `pandas`, `xarray`
- GIS tools (optional, for visualization)

---

## 📖 References

- **mizuRoute** documentation: [https://github.com/NCAR/mizuRoute](https://github.com/NCAR/mizuRoute)
- Gharari et al. (2024): *A Flexible Framework for Simulating the Water Balance of Lakes and Reservoirs From Local to Global Scales: mizuRoute‐Lake*. [https://doi.org/10.1029/2022WR032400](https://doi.org/10.1029/2022WR032400)

---

## 📬 Citation

If you use the tools or methods in this repository for your work, please consider citing:

**Gharari, S., Vanderkelen, I., Tefs, A., Mizukami, N., Kluzek, E., Stadnyk, T., Lawrence, D., & Clark, M. P. (2024).**  
*A Flexible Framework for Simulating the Water Balance of Lakes and Reservoirs From Local to Global Scales: mizuRoute‐Lake*.  
Water Resources Research, 60, e2022WR032400. [https://doi.org/10.1029/2022WR032400](https://doi.org/10.1029/2022WR032400)

---