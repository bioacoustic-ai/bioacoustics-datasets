<script setup lang="ts">
import DataModal from "@/components/DataModal.vue";
import { ref } from "vue";
import objects, { type DataEntryType } from "../data";
import { getData, nameLookup } from "../data/formatting";

var nameKeys = Object.keys(nameLookup);
var visibleKeys = ref(["name", "datePublished"]);

var currentData: DataEntryType | null = null;
const modalRef = ref();

function openModal(entry: DataEntryType) {
    currentData = entry;
    modalRef.value.showModal(entry);
}

function updateChecked(key: string) {
    if (visibleKeys.value.includes(key) && visibleKeys.value.length > 1) {
        visibleKeys.value.splice(visibleKeys.value.indexOf(key), 1);
    } else {
        visibleKeys.value.push(key);
    }
    console.log(visibleKeys);
}


</script>

<template>
    <div class="max-h-32 overflow-y-scroll mb-5">
        <div class="flex flex-wrap place-content-center">
            <div v-for="key in nameKeys"
                class="flex items-center p-4 border border-gray-200 rounded xs:w-1/4 sm:w-1/5 lg:w-1/6 xl:w-1/6 m-1 h-6 cursor-pointer">
                <input v-bind:id="key" v-bind:checked="visibleKeys.includes(key)" @change="updateChecked(key)"
                    type="checkbox" v-bind:value="key" v-bind:name="key"
                    class="w-3 h-3 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 cursor-pointer">
                <label v-bind:for="key"
                    class="w-full h-auto py-4 ms-2 text-xs font-medium text-gray-900 overflow-hidden text-ellipsis cursor-pointer">
                    {{ nameLookup[key] }}
                </label>
            </div>
        </div>
    </div>

    <div class="data-table overflow-hidden">
        <DataModal ref="modalRef" v-bind:data="currentData"></DataModal>
        <table class="w-full text-sm text-left text-gray-500">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50">
                <tr>
                    <th v-for="key in visibleKeys" scope="col" class="px-6 py-3 max-w-6 overflow-x-auto text-ellipsis">
                        {{ nameLookup[key] }}
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="entry in objects" v-on:click="openModal(entry)"
                    class="bg-white border-b hover:bg-gray-100 cursor-pointer">
                    <th v-for="key in visibleKeys" scope="row"
                        class="px-6 py-4 font-medium  max-w-6 text-ellipsis overflow-x-hidden text-gray-900 whitespace-nowrap">
                        {{ getData(entry, key) }}
                    </th>
                </tr>
            </tbody>
        </table>
    </div>
</template>
<style>
.data-table {
    height: 550px;
    overflow-y: scroll;
}
</style>