import moment from "moment";
import { type DataEntryType } from "./index";
type DataEntryKey = keyof DataEntryType;

// TODO: actually finish this.
var nameLookup: { [key: string]: string } = {
    "additionalDescription": "Additional description",
    "annotationsType": "annotationsType",
    "captureDevice": "captureDevice",
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
    "taxonomicClass": "taxonomicClass",
    "totalDuration": "totalDuration",
    "url": "url",
    "version": "version"
};

function formatDate(entry: DataEntryType, key: string) {
    var value = entry[key as DataEntryKey];
    if (!value) {
        return "";
    }
    return moment(String(value)).format('YYYY-MM-DD')
}

// The point of this function is to return a standardized link.
// The thing was that there were more than one entry that needed a link, and so 
// it was not that nice to have multiple link templates essentially doing the same thing.
function createLink(href: string | undefined, text: string | undefined) {
    return `<a target="_blank" class="underline text-blue-800" href="${href}">${text}</a>`;
}


// In some cases, we might need to process the data before showing it. (i.e. parse dates)
// In these cases, define the function here, by keying it with the prop name.
var functionLookup: { [key: string]: Function } = {
    "creators": (entry: DataEntryType, key: string) => {
        var data = entry[key as DataEntryKey] as string[];
        return data ? (data as string[]).join("; ") : "";
    },
    "datePublished": formatDate,
    "name": (entry: DataEntryType, key: string) => {
        return createLink(entry["url" as DataEntryKey]?.toString(), entry["name" as DataEntryKey]?.toString())
    },
    "paperLink": (entry: DataEntryType, key: string) => { return entry["paperLink"] == null ? "" : createLink(entry["paperLink" as DataEntryKey]?.toString(), "paper link"); }
};


var functionKeys = Object.keys(functionLookup);

// Actually returns a string!
function getData(entry: DataEntryType, key: string): any {
    if (!entry) {
        return "";
    }

    var propData = entry[key as DataEntryKey];
    if (functionKeys.includes(key)) {
        propData = functionLookup[key](entry, key);
    }
    return propData;
}

export { functionKeys, functionLookup, getData, nameLookup };

