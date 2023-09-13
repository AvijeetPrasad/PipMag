# La Palma Data Frame Structure

The La Palma Data Frame serves as the central repository for storing the solar observations data gathered by the Swedish Solar Telescope (SST). The data frame's architecture is designed to provide a comprehensive overview of each observation, making it easy for users to understand the specifics.

Below is the structure of the data frame along with a brief description and possible values for each column:

| Column Name   | Description                                                           | Possible Values                                       |
| ------------- | --------------------------------------------------------------------- | ----------------------------------------------------- |
| `date_time`   | The date and time when the observation was made                       | Timestamp format (YYYY-MM-DD HH:MM:SS)                |
| `year`        | The year of the observation                                           | Any valid year                                        |
| `month`       | The month of the observation                                          | 1 to 12                                               |
| `day`         | The day of the observation                                            | 1 to 31                                               |
| `time`        | The time when the observation was made                                | Time format (HH:MM:SS)                                |
| `instruments` | Specifies which instruments were used for the observation              | CRISP, CHROMIS, IRIS                                  |
| `target`      | Lists the various phenomena or regions on the Sun targeted            | Active Region (AR), Sunspot, Light Bridge, Flare, Burst, UV Burst, Ellerman Bombs, Penumbral Ellerman Bombs (PEB), Surges, Flux Emergence, Pores, Faculae/Plage, Filament, Quiet Sun (QS), Coronal Bright Point, Coronal Hole, Magnetic Bright Points, Spicules, Prominences (off-limb filaments), Review      |
| `comments`    | Can include any other additional information or notes                  | Free text                                             |
| `video_links` | URLs of video files related to the observation                         | URLs                                                  |
| `image_links` | URLs of image files related to the observation                         | URLs                                                  |
| `links`       | Aggregated URLs of all related files                                  | URLs                                                  |
| `num_links`   | The number of links associated with the observation                    | Any integer value                                     |
| `polarimetry` | Indicates whether polarimetry was used in the observation              | True, False                                           |

This structured format allows for efficient querying and data extraction based on various observation parameters. For more information on interacting with the data frame, refer to the 'Working with the Data Frame' section of this wiki
