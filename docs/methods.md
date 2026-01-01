2. Methods
2.1 Study Area
The study covers the entire land area of Nigeria, West Africa. Nigeria spans diverse climatic and physiographic zones, ranging from arid and semi-arid regions in the north to humid tropical conditions in the south. This diversity makes the country suitable for comparative assessment of solar, wind, and hydropower potential at national and sub-national scales.

2.2 Data Sources
Multiple geospatial datasets were integrated to evaluate renewable energy suitability (Table 1). These include remotely sensed and global modeled datasets commonly used in renewable energy assessments, ensuring consistency and comparability with prior studies.
Table 1. Summary of datasets used in the analysis.
DatasetSourceDescriptionDigital Elevation Model (DEM)NASA SRTM30 m resolution elevationSolar Resource (GHI)Global Solar AtlasAnnual mean Global Horizontal IrradianceWind SpeedGlobal Wind AtlasMean wind speed at 100 m hub heightHydrological DataHydroSHEDSFlow accumulation and river networksLand CoverESA WorldCoverLand use and exclusion constraintsAdministrative BoundariesGADMState-level boundaries
2.3 Data Pre-processing
All datasets were harmonized to ensure spatial consistency prior to analysis. First, all raster and vector layers were reprojected to a common projected coordinate reference system (UTM Zone 32N, EPSG:32632). Datasets were clipped to Nigeria’s national boundary and resampled to a uniform spatial resolution of 30 m.
Land-use and water-body masks were applied to exclude areas unsuitable for energy infrastructure development. Continuous raster variables were normalized to a 0–1 scale to enable comparability across indicators and technologies.

2.4 Renewable Energy Suitability Modeling
2.4.1 Solar Suitability
Solar suitability was derived primarily from normalized Global Horizontal Irradiance (GHI). Terrain slope and land-use constraints were incorporated to penalize or exclude unsuitable locations. Higher suitability scores correspond to areas with high solar resource availability and favorable terrain conditions.
2.4.2 Wind Suitability
Wind suitability was computed using mean wind speed at 100 m hub height. Wind speed values were normalized and adjusted using terrain and land-use constraints. Areas with higher wind speeds and minimal physical constraints were assigned higher suitability scores.
2.4.3 Hydropower Suitability
Hydropower suitability was assessed using hydrological and topographic proxies. Flow accumulation was used as an indicator of potential stream power, while terrain slope was incorporated to reflect constructability and feasibility considerations. These factors were combined into a continuous hydropower suitability index.

2.5 Continuous Suitability Indices
For each renewable energy source, a continuous suitability raster was produced with values ranging from 0 (least suitable) to 1 (most suitable). This approach preserves spatial variability and allows for detailed interpretation of suitability gradients across the country.

2.6 Suitability Classification
Continuous suitability indices were reclassified into five ordinal classes to facilitate interpretation and reporting:
1. Very Low
2. Low
3. Medium
4. High
5. Very High
This classification scheme enables comparison across renewable energy technologies and administrative units.

2.7 Zonal Statistics and State-Level Indices
State-level zonal statistics were computed using classified suitability rasters. For each state, the proportion of land area falling within each suitability class was calculated. Resource-specific indices (solar, wind, and hydropower) were derived as weighted combinations of the High and Very High suitability classes, emphasizing areas most suitable for development.
An example formulation is:
I=0.6×PVH+0.4×PHI = 0.6 \times P_{VH} + 0.4 \times P_{H}I=0.6×PVH?+0.4×PH? 
where PVHP_{VH}PVH? and PHP_{H}PH? represent the percentage of Very High and High suitability areas, respectively.

2.8 Combined Renewable Energy Index
To support integrated renewable energy planning, individual solar, wind, and hydropower indices were normalized using min–max scaling. A combined renewable energy index was then calculated as the arithmetic mean of the normalized indices:
CI=Isolar+Iwind+Ihydro3CI = \frac{I_{solar} + I_{wind} + I_{hydro}}{3}CI=3Isolar?+Iwind?+Ihydro?? 
This composite indicator provides a holistic measure of overall renewable energy potential at the state level.

2.9 Outputs and Visualization
The analysis produced continuous and classified suitability maps for each renewable energy source, state-level zonal statistics in tabular format, and ranking charts illustrating comparative renewable energy potential across Nigerian states. These outputs support both spatial interpretation and policy-relevant decision-making.

