🇳🇬 Nigeria Renewable Energy GIS Suitability Project

Solar • Wind • Hydro | QGIS + Python + GDAL Workflow

This repository contains a complete GIS-based suitability analysis workflow for renewable energy development in Nigeria.
The project integrates solar, wind, and hydro suitability using QGIS, GDAL, raster processing, multi-criteria decision analysis (MCDA), and geospatial modelling.

🔍 Project Purpose

To create spatially accurate, data-driven suitability maps for supporting renewable energy planning in Nigeria.

The project outputs:

🌞 Solar Suitability Map

🌬️ Wind Suitability Map

💧 Hydro Suitability Map

⚡ Combined Renewable Energy Suitability Index

📍 Candidate Sites / Priority Zones


📁 Project Folder Structure
Nigeria_Renewable_Suitability/
│
├── data_raw/                     # Untouched source data
│   ├── dem/
│   ├── landcover/
│   ├── solar_GHI/
│   ├── wind/
│   ├── hydro/
│   ├── grid_network/
│   └── roads/
│
├── data_processed/               # Cleaned / clipped / reprojected datasets
│
├── analysis/                     # Scripts, MCDA weights, QGIS models
│   ├── solar_suitability.py
│   ├── wind_suitability.py
│   ├── hydro_suitability.py
│   ├── qgis_model.model3
│   ├── utils_raster.py
│   └── weights.xlsx
│
├── outputs/                      # Final suitability results
│   ├── solar_suitability.tif
│   ├── wind_suitability.tif
│   ├── hydro_suitability.tif
│   ├── combined_suitability.tif
│   └── site_candidates.shp
│
├── maps/                         # Printable layouts
│   ├── suitability_map.pdf
│   └── aoi_map.qgz
│
├── docs/                         # Documentation
│   ├── methodology.md
│   ├── workflow_diagram.png
│   └── references.md
│
├── logs/                         # Runtime logs and metadata
│
├── Nigeria_Renewable.qgz         # QGIS project file
└── README.md

🗂️ Datasets Used
Raster Data

Digital Elevation Model (DEM)

Landcover (ESA WorldCover / Copernicus)

Global Horizontal Irradiance (GHI)

Wind Speed (ERA5 / Global Wind Atlas)

Hydro layers (flow accumulation, slope, rivers)

Roads & grid network

Vector Data

State boundaries (GADM, OCHA)

Hydrology (rivers, catchments)

Transmission lines & substations


⚙️ Processing Workflow

The GIS workflow includes:

1. Data Acquisition

Download raw datasets into data_raw/.

2. Preprocessing

Reproject all rasters to WGS84 / UTM

Clip to Nigeria AOI

Resample layers to common resolution

Convert vector → raster where needed

Build landmask

3. Criteria Computation

Solar:

GHI reclassification

Slope constraints

Land cover restrictions

Wind:

Wind speed at 100m

Roughness / surface friction

Distance to grid

Hydro:

Flow accumulation

Stream network extraction

Head & slope constraints

4. Multi-Criteria Decision Analysis (MCDA)

Weights stored in:
analysis/weights.xlsx


5. Weighted Overlay

Each suitability index is generated:

Suitability = Σ (Weight × Normalized_Criterion)

6. Output Generation

Stored in /outputs/:

Raster suitability maps

Classes (0–5)

Candidate site shapefiles


🧰 Tools & Software
Component	Version	Notes
QGIS	3.34+	Core GIS processing
GDAL	3.10+	Raster reprojection, warp
Python	3.10+	Automated processing
NumPy	–	Raster math
QGIS Model Builder	–	Automated pipelines

▶️ How to Run the Scripts
1. Activate your environment
conda activate gis_env   # or your environment name

2. Run solar suitability
python analysis/solar_suitability.py

3. Run wind suitability
python analysis/wind_suitability.py

4. Run hydro suitability
python analysis/hydro_suitability.py


📊 Results

The project produces:

Final suitability raster maps

Classification maps (e.g., Very High, High, Moderate…)

renewable energy zones

GIS-ready outputs for reports and dashboards


🤝 Contributing

You are welcome to contribute by:

Adding datasets

Improving model weights

Adding Python modules

Enhancing cartographic outputs

🔒 Data Notice

Large raw datasets (DEM, GHI, wind speed, etc.) are not stored in the repository.
To avoid large file sizes and licensing issues, use your own copies inside /data_raw/.

📜 License

MIT License — free to use, modify, and distribute.

📧 Contact

If you’d like help running the pipeline or applying it to another country, contact:

Bayodele Famuyide
(famuyideb@gmail.com)