Methodology – Renewable Energy Suitability Assessment for Nigeria

## 1. 	Overview

	This study applies a standardized, GIS-based multi-criteria decision analysis (MCDA) framework to assess solar, wind, and 	hydropower 	suitability across Nigeria. Continuous suitability indices were developed for each renewable resource, 	classified into suitability classes, and aggregated at state level using zonal statistics. A combined renewable 	energy index was subsequently constructed to support comparative state-level ranking and strategic energy planning.


## 2. 	Data Sources
	Dataset	Source	Description
	Digital Elevation Model (DEM)	NASA SRTM	30 m resolution elevation data
	Global Horizontal Irradiance (GHI)	Global Solar Atlas	Annual mean solar resource
	Wind Speed	Global Wind Atlas	100 m hub-height wind speed
	Land Cover	ESA WorldCover	Land use / land cover constraints
	River Network & Flow Accumulation	HydroSHEDS	Hydropower proxy indicators
	Roads	OpenStreetMap	Accessibility constraints
	Transmission Grid	WRI / EnergyData	Proximity to grid infrastructure
	Administrative Boundaries	GADM	State-level boundaries


## 3. 	Data Pre-processing

	All datasets were standardized using the following steps:

	Coordinate Reference System (CRS):
	All layers were reprojected to a common projected CRS (UTM Zone 32N, EPSG:32632).

	Spatial Extent:
	Datasets were clipped to Nigeria’s national boundary.

	Spatial Resolution:
	Raster layers were resampled to a common spatial resolution (30 m) using bilinear or nearest-neighbor interpolation as 	appropriate.

	Masking & Exclusion:
	Non-developable areas (e.g., water bodies, protected areas, unsuitable land cover) were excluded using binary masks.

	Normalization:
	All continuous suitability layers were normalized to a 0–1 scale, where higher values indicate higher suitability.



4. 	Suitability Modeling
## 4.1 	Solar Suitability

	Solar suitability was derived primarily from normalized Global Horizontal Irradiance (GHI), adjusted for terrain slope and 	land-use constraints. Areas with steep slopes or incompatible land cover were penalized or excluded.

##4.2  	Wind Suitability

	Wind suitability was computed using normalized wind speed at 100 m hub height, adjusted for terrain constraints and 	exclusion zones. 	Higher wind speeds correspond to higher suitability scores.

## 4.	3 Hydropower Suitability

	Hydropower suitability was derived from flow accumulation, terrain slope, and elevation proxies. Flow accumulation served as 	an indicator of potential stream power, with terrain constraints applied to avoid unsuitable locations.

## 5. 	Continuous Suitability Indices

	For each renewable source, a continuous suitability raster was produced with values 	ranging from 0 (unsuitable) to 1 	(highly suitable). These continuous surfaces allow for nuanced spatial interpretation beyond binary or categorical maps.



## 6. 	Classification of Suitability

	Continuous suitability indices were reclassified into five ordinal classes:

	Class	Description
	1	Very Low
	2	Low
	3	Medium
	4	High
	5	Very High

	This classification facilitates interpretation, reporting, and comparison across regions.



## 7. 	Zonal Statistics and State-Level Analysis

	State boundaries were used to compute zonal statistics for each classified suitability 	raster. For each state:

	Pixel counts per suitability class were calculated

	Percentage area per class was derived

	A resource-specific index was computed as a weighted combination of High and Very High 	suitability classes

	Example (hydropower index):

	Hydro Index = 0.6 × (% Very High) + 0.4 × (% High)



## 8. Combined Renewable Energy Index

	To support integrated planning, solar, wind, and hydropower indices were:

	Min-max normalized to ensure comparability

	Combined using equal weighting:

	Combined Index = (Solar_norm + Wind_norm + Hydro_norm) / 3


	This produced a single composite indicator representing overall renewable energy 	potential per state.



## 9. 	Outputs

	The workflow produced the following outputs:

	Continuous suitability rasters (solar, wind, hydro)

	Classified suitability maps

	State-level zonal statistics (CSV)

	Individual and combined renewable energy rankings

	Publication-ready charts and maps



##  10. Limitations

	Data resolution and temporal variability may affect accuracy

	Socio-economic, policy, and grid-capacity factors were not explicitly modeled

	Hydropower potential is represented by proxy indicators rather than detailed 	hydrological simulations

---

## 11. References

	[1]     Energy Commission of Nigeria, Federal Ministry of Science, Technology and 	Innovation, 	Federal Republic of Nigeria. 	National Energy Master Plan.
        https://www.energy.gov.ng/Energy_Policies_Plan/APPROVED_NEMP_2022.pdf.

	[2] 	Challenges and Opportunities in Nigeria's Renewable Energy Policy and 	Legislation, 	World Journal of Advanced 	Research and Reviews, 2024, 23(02), 	2354–2372,
        https://doi.org/10.30574/wjarr.2024.23.2.2391
	
[3]	Global Solar Atlas: 
        https://globalsolaratlas.info/map?c=9.123792,8.701172,  5&r=NGA

[4] 	 Global Wind Atlas:
	 https://globalwindatlas.info/en/area/Nigeria

[5]	https://data.humdata.org/dataset/nigeria-water-	courses-			    	cod/resource/9df5fb63-28ef-465b-9520-75fddbfd5356

[6]	https://energydata.info/dataset/nigeria-electricity-	transmission-		    	network-2015






