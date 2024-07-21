interface DataEntry {
    additionalDescription: string;
    annotationsType: string;
    captureDevice: string;
    citeAs: string | undefined;
    continent: string;
    countryCode: string;
    creators: string[];
    datePublished: Date;
    description: string;
    labellingLevel: string;
    license: string;
    lifeStage: string;
    locality: string;
    minAndMaxRecordingDuration: string;
    name: string;
    numAnnotations: number;
    numAudioFiles: number;
    numClasses: number;
    numSpecies: number;
    paperLink: string;
    physicalSetting: string;
    provider: string;
    recordingPeriod: string;
    recordingType: string;
    sampleRate: number;
    sizeInGb: number;
    species: string;
    taxonomicClass: string;
    totalDuration: number;
    url: string;
    version: number;
}

export type { DataEntry as DataEntryType };

const files = (import.meta.glob('../../../datasets_json/*.json', { eager: true }) as unknown) as DataEntry[];
var objects: DataEntry[] = [];
for (let key in files) {
    objects.push(files[key]);
}

export default objects;