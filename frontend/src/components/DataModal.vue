<script setup lang="ts">
import { FwbButton, FwbModal } from 'flowbite-vue';
import moment from "moment";
import { defineExpose, ref } from 'vue';
import { type DataEntryType } from "../data";
import DataGroup from "./DataGroup.vue";



const isShowModal = ref(false);

var data: DataEntryType | null = null;

function closeModal() {
    isShowModal.value = false
}
function showModal(newData: any) {
    data = newData;

    isShowModal.value = true
}
function formatDate(value: Date | undefined) {
    if (!value) {
        return "";
    }
    return moment(String(value)).format('MM/DD/YYYY')
}

defineExpose({ showModal });

// TODO: consider moving this to separate JSON file/storage
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

// In some cases, we might need to process the data before showing it. (i.e. parse dates)
// In these cases, define the function here, by keying it with the prop name.
var functionLookup: { [key: string]: Function } = {
    "creators": (data: string[]) => (data as string[]).join("; "),
    "datePublished": formatDate
}

var nameKeys = Object.keys(nameLookup);
var functionKeys = Object.keys(functionLookup);
type DataEntryKey = keyof DataEntryType;

// Actually returns a string!
function getData(key: string): any {
    if (!data) {
        return "";
    }

    var propData = data[key as DataEntryKey];
    if (functionKeys.includes(key)) {
        propData = functionLookup[key](propData);
    }

    return propData;
}


</script>

<template>
    <fwb-modal v-if="isShowModal" @close="closeModal">
        <template #header>
            <div class="flex items-center text-lg">
                {{ data?.name }}
            </div>
        </template>
        <template #body>
            <!--TODO: some smarter stuff here maybe-->
            <!--TODO: also order these better later-->
            <div v-for="key in nameKeys">
                <DataGroup v-bind:title="nameLookup[key]" v-bind:content="getData(key)">
                </DataGroup>
            </div>

        </template>
        <template #footer>
            <div class="flex justify-between">
                <fwb-button @click="closeModal" color="alternative">
                    Close
                </fwb-button>
            </div>
        </template>
    </fwb-modal>
</template>
