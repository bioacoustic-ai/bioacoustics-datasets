# Bioacoustics datasets

Note: the webapp is not published yet, and will be very soon!

## Introduction
This repository gathers the list of online publicly available bioacoustics datasets that can be used together with deep learning. You can visualise this table at the following url: *Coming Soon*. This list aims at providing an overview of what data is currently accessible to train and evaluate models. We aim at keeping this list up-to-date, and you can contribute by opening a pull request to add new datasets. The procedure to add a new dataset is explained in the next section.

## Want to contribute?
That's great! You can contribute in two ways. The first way to contribute is to add more information on the already listed datasets, or add another dataset. In order to modify the existing datasets, you only need to modify its json file, located in the directory `datasets_json`. To add a new dataset, download the file called `dataset_template.json`. Then, open it and fill as many fields as possible. We recommend to fill at least the fields `authors`, `description`, `url`, `version`, and `license`. You will find a description of each of the fields below. You can also open a github issue to refer us to a new dataset if you do not wish to fill the information yourself.

The second way to contribute is to make the webapp better, either by proposing improvements in github issues, or by implementing them directly. Read the README file in the `frontend` folder to run the webapp locally.

## Description of the fields

You can find an explanation of each field in alphabetical order below. You can also look at other `json` files in the `datasets_json` folder for more examples.

| Field                      | Description                                                                                                                                                                  | Examples                                                                             |
|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| additionalDescription      | Complementary information.                                                                                                                                                   |                                                                                      |
| annotationsType            | The information that has been annotated.                                                                                                                                     | "Species, vocalisation type"                                                         |
| captureDevice              | Hardware used to record the vocalisations. Write "Various" if several devices have been used.                                                                                | "Lavalier microphone"                                                                |
| continent                  | See https://ac.tdwg.org/termlist/#dwc_continent                                                                                                                              | "Europe"                                                                             |
| countryCode                | ISO 3166-1 alpha-2 code of the country. For states or provinces, use preferably the codes defined in the standard ISO 3166-2                                                 | One country: "FR",<br>One province: "CN-AH",<br>Several places: ["FR", "CN-AH"]      |
| creators                   | List of the dataset's authors.                                                                                                                                               | ['John Doe']                                                                         |
| datePublished              | Date when this version of the dataset was published, in the ISO 8601 format.                                                                                                 | "2021-06-18T06:26:56.891644+00:00", or "2021-06-18"                                  |
| description                | Description of the dataset.                                                                                                                                                  |                                                                                      |
| labellingLevel             | Whether the dataset is strongly labelled (with precise time annotations), or weakly labelled (without time annotations)                                                      | "Strong", "Weak"                                                                     |
| license                    | The license under which this dataset is distributed, either as its name, or as a link.                                                                                       | "cc-by-4.0", "https://creativecommons.org/licenses/by/4.0/legalcode"                 |
| lifeStage                  | See https://ac.tdwg.org/termlist/#dwc_lifeStage. The current categories include Juvenile and Adult.                                                                          | "Adult", "All"                                                                       |
| locality                   | See https://ac.tdwg.org/termlist/#dwc_locality. Contains specific geographical information if available.                                                                     | "703 nest sites in Wytham Woods, Oxfordshire (51°46 N, 1°20 W)"                      |
| minAndMaxRecordingDuration | The minimum and maximum time duration of the recordings in seconds. If all the recordings have the same duration, write the same value for the minimum and maximum duration. | "60 - 60"                                                                            |
| name                       | Name of the dataset.                                                                                                                                                         | "NIPS4Bplus"                                                                         |
| numAnnotations             | The number of annotations in the dataset.                                                                                                                                    | 598                                                                                  |
| numAudioFiles              | The number of audio files in the dataset.                                                                                                                                    | 3403                                                                                 |
| numClasses                 | If applicable, the number of classes of interest in the dataset.                                                                                                             | 40                                                                                   |
| numSpecies                 | The number of species that this dataset targets.                                                                                                                             | 23                                                                                   |
| paperLink                  | If applicable, the link of the paper which introduces the dataset.                                                                                                           | "https://link.to.paper"                                                              |
| physicalSetting            | See https://ac.tdwg.org/termlist/#ac_physicalSetting.                                                                                                                        | "Natural", "Artificial"                                                              |
| provider                   | The institution providing the dataset.                                                                                                                                       |                                                                                      |
| recordingPeriod            | The period of time when the data was recorded.                                                                                                                               | "late March to mid-May during the breeding seasons of 2020 from 5 to 7 AM each day." |
| recordingType              | Describes whether the recordings consist of edited clips, or are continuous. Constrained vocabulary with choices 'Clips', or 'Continuous'.                                   | "Clips"                                                                              |
| sampleRate                 | The sample rate at which the data was recorded, in kHz.                                                                                                                      | 48.0                                                                                 |
| sizeInGb                   | The size of the dataset in GB.                                                                                                                                               | 10.2                                                                                 |
| taxonomicClass             | The taxonomix classes of the species in the dataset.                                                                                                                         | "Aves"                                                                               |
| totalDuration              | The duration of the whole dataset, in hours.                                                                                                                                 | 7.8                                                                                  |
| url                        | Link to the dataset.                                                                                                                                                         | "https://link.to.dataset"                                                            |
| version                    | The version of the dataset.                                                                                                                                                  | 5                                                                                    |
