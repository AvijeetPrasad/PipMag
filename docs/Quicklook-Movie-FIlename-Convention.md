# Quicklook Movie Filename Convention

The Quicklook movie filenames in PipMag follow a specific naming convention to provide a standardized and comprehensible way of identifying the details of each movie. Each filename is structured to contain information about the date, time, observable, instrument, and wavelength of the observation.

Here's the recommended format for the filenames:

```
Date_Time_Observable_Instrument_Wavelength.jpg
```

The table below explains what each component represents:

| Component | Description | Format/Examples |
| --- | --- | --- |
| `Date` | The date when the observation was made | `YYYY-MM-DD`, e.g., `2022-07-07` |
| `Time` | The time when the observation was made | `HH-MM-SS`, e.g., `16-06-50` |
| `Observable` | The physical quantity that was observed | `Intensity`, `LP` (Linear Polarization), `TP` (Total Polarization), etc. |
| `Instrument` | The instrument used for the observation | `HMIAIA`, `CRISP`, `CHROMIS`, `IRIS-SJI`, etc. |
| `Wavelength` | The wavelength of the filter used for the observation | `6173`, `171`, `8542`, etc. |

For instance, a movie generated from the CRISP instrument, observing the intensity at 8542 Å, taken on 2022-07-07 at 16:06:50, would be named:

```
2022-07-07_16-06-50_Intensity_CRISP_8542.jpg
```

In cases where the movie consists of two subplots, the filename should include information about both observables, their corresponding instruments, and wavelengths, separated by an underscore. The format is:

```
Date_Time_Observable1_Instrument1_Wavelength1_Observable2_Instrument2_Wavelength2.jpg
```

For example, a movie with two subplots—first showing the HMI intensity at 6173 Å and second showing the CRISP Vlos at 8542 Å, taken on 2022-07-07 at 16:06:50—would be named:

```
2022-07-07_16-06-50_Intensity_HMI_6173_Vlos_CRISP_8542.jpg
```

This convention ensures that the filenames provide a clear and quick overview of the content of the movie, facilitating efficient organization and retrieval of movies.