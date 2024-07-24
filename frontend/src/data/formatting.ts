import moment from "moment";
import { type DataEntryType } from "./index";
type DataEntryKey = keyof DataEntryType;

// TODO: actually finish this.
var nameLookup: { [key: string]: string } = {
    "additionalDescription": "Additional description",
    "annotationsType": "annotationsType",
    "captureDevice": "captureDevice",
    "citeAs": "citeAs",
    "continent": "continent",
    "countryCode": "countryCode",
    "creators": "creators",
    "datePublished": "datePublished",
    "description": "description",
    "labellingLevel": "labellingLevel",
    "license": "license",
    "lifeStage": "lifeStage",
    "locality": "locality",
    "minAndMaxRecordingDuration": "minAndMaxRecordingDuration",
    "name": "name",
    "numAnnotations": "numAnnotations",
    "numAudioFiles": "numAudioFiles",
    "numClasses": "numClasses",
    "numSpecies": "numSpecies",
    "paperLink": "paperLink",
    "physicalSetting": "physicalSetting",
    "provider": "provider",
    "recordingPeriod": "recordingPeriod",
    "recordingType": "recordingType",
    "sampleRate": "sampleRate",
    "sizeInGb": "sizeInGb",
    "species": "species",
    "taxonomicClass": "taxonomicClass",
    "totalDuration": "totalDuration",
    "url": "url",
    "version": "version"
};

function formatDate(value: Date | undefined) {
    if (!value) {
        return "";
    }
    return moment(String(value)).format('MM/DD/YYYY')
}

// In some cases, we might need to process the data before showing it. (i.e. parse dates)
// In these cases, define the function here, by keying it with the prop name.
var functionLookup: { [key: string]: Function } = {
    "creators": (data: string[]) => { return data ? (data as string[]).join("; ") : "" },
    "datePublished": formatDate
};
var functionKeys = Object.keys(functionLookup);

// Actually returns a string!
function getData(entry: DataEntryType, key: string): any {
    if (!entry) {
        return "";
    }

    var propData = entry[key as DataEntryKey];
    if (functionKeys.includes(key)) {
        propData = functionLookup[key](propData);
    }
    return propData;
}

export { functionKeys, functionLookup, getData, nameLookup };

