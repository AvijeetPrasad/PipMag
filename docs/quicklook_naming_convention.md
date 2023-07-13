# Quicklook Movie Filename Convention

To ensure a standardized and comprehensible naming of quicklook movies, we recommend the following convention:

The filename should be a string formatted as follows:

```
Date_Time_Observable_Instrument_Wavelength.jpg
```

Below is a brief description of each component in the filename:

| Component | Description | Format/Example |
| --- | --- | --- |
| `Date` | The date the observation was made | `YYYY-MM-DD` |
| `Time` | The time the observation was made | `HH-MM-SS` |
| `Observable` | The physical quantity being observed | intensity, linear polarization (LP), total polarization (TP), etc. |
| `Instrument` | The instrument used for the observation | HMIAIA, CRISP, CHROMIS, IRIS-SJI, etc. |
| `Wavelength` | The wavelength of the filter used for the observation | 6173, 171, 8542, etc. |

## Example

A movie generated from the CRISP instrument, observing the intensity at 8542 Å, taken on 2022-07-07 at 16:06:50, would be named as follows:

```
2022-07-07_16-06-50_Intensity_CRISP_8542.jpg
```

## Multi-Observable Movies

In the case where a movie consists of two subplots, the filename should include information about both observables, both with their corresponding instruments and wavelengths, separated by an underscore:

```
Date_Time_Observable1_Instrument1_Wavelength1_Observable2_Instrument2_Wavelength2.jpg
```

For instance, a movie with two subplots, the first showing the HMI intensity at 6173 Å and the second showing the CRISP Vlos at 8542 Å, taken on 2022-07-07 at 16:06:50, would be named:

```
2022-07-07_16-06-50_Intensity_HMI_6173_Vlos_CRISP_8542.jpg
```

This convention ensures that the filename provides a clear and quick overview of the content of the movie.