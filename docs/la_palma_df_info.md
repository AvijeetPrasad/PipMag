# Outline of the La Palma Data Frame

The data frame is structured with the following columns:

| Column Name | Description | Possible Values |
| --- | --- | --- |
| `Target` | Lists the various phenomena or regions on the Sun that were the target of the observation | Active Region (AR), Sunspot, Light Bridge, Flare, Burst, UV Burst, Ellerman Bombs, Penumbral Ellerman Bombs (PEB), Surges, Flux Emergence, Pores, Faculae/Plage, Filament, Quiet Sun (QS), Coronal Bright Point, Coronal Hole, Magnetic Bright Points, Spicules, Prominences (off-limb filaments), Review |
| `Instruments` | Specifies which instruments were used for the observation | CRISP, CHROMIS, IRIS |
| `Polarimetry` | Indicates whether polarimetry was used in the observation | True, False |
| `Comments` | Can include any other additional information or notes regarding the observation | |
| `Mosaic` | Specifies whether the observation was a mosaic, and if so, whether it was at the disk center or the limb of the Sun | Disk Center, Limb |
| `Seeing` | Provides a qualitative assessment of the atmospheric conditions during the observation | Bad, Ok, Good, Excellent |
| `Science Ready` | Indicates whether the observation is ready for scientific analysis | True, False |
| `Line` | Specifies the spectral line for the observation. This can be obtained from the calibrations from the webpage | (Can be obtained from the calibrations from the webpage) |

---