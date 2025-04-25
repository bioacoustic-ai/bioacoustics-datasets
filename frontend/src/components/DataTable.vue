<script setup lang="ts">
import DataModal from "@/components/DataModal.vue";
import { ref } from "vue";
import objects, { type DataEntryType } from "../data";
import { getData, nameLookup } from "../data/formatting";
type DataEntryKey = keyof DataEntryType;


var dataEntries = ref(objects);

var nameKeys = Object.keys(nameLookup);
var visibleKeys = ref(["name", "title", "taxonomicClass", "totalDuration", "locality"]);
var hiddenKeys = ["url"];

var currentData = ref<DataEntryType>(objects[0]);

enum SortDirection {
    Ascending = 0,
    Descending = 1
}

const modalRef = ref();

var sortBy = ref({
    key: "",
    sortDirection: SortDirection.Ascending
});

function openModal(entry: DataEntryType, $event: MouseEvent) {
    if ($event.target instanceof Element && $event.target.tagName.toLowerCase() === "a") {
        return;
    } 
    currentData.value = entry;
    modalRef.value.showModal();
}

function updateChecked(key: string) {
    if (visibleKeys.value.includes(key) && visibleKeys.value.length > 1) {
        visibleKeys.value.splice(visibleKeys.value.indexOf(key), 1);
    } else {
        visibleKeys.value.push(key);
    }
}

function updateSort(key: string) {
    if (key === sortBy.value.key) {
        sortBy.value.sortDirection = (sortBy.value.sortDirection + 1) % 2;
    } else {
        sortBy.value = {
            key: key,
            sortDirection: SortDirection.Ascending
        };
    }
    sorted(sortBy.value.key as DataEntryKey, sortBy.value.sortDirection as number);
}

function sorted(prop: DataEntryKey, ascending: SortDirection) {
    // TODO: explain this
    var mult = ascending === SortDirection.Ascending ? -1 : 1;
    // TODO: sort correctly for all cases (string | number | Date | string[] | undefined) (and not as any)
    dataEntries.value.sort(function (a, b) {
        var aVal = a[prop] as any;
        var bVal = b[prop] as any;
        if (aVal > bVal) {
            return 1 * mult;
        }
        if (aVal < bVal) {
            return -1 * mult;
        }
        return 0;
    });
}


</script>

<template>
    <div class="max-h-32 overflow-y-scroll mb-5">
        <div class="flex flex-wrap place-content-center">
            <div v-for="key in nameKeys.filter(x => !hiddenKeys.includes(x))"
                class="flex items-center p-4 border border-gray-200 rounded xs:w-1/4 sm:w-1/5 lg:w-1/6 xl:w-1/6 m-1 h-6 cursor-pointer">
                <input v-bind:id="key" v-bind:checked="visibleKeys.includes(key)" @change="updateChecked(key)"
                    type="checkbox" v-bind:value="key" v-bind:name="key"
                    class="w-3 h-3 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 cursor-pointer">
                <label v-bind:for="key"
                    class="w-full h-auto py-4 ms-2 text-xs font-medium overflow-hidden text-ellipsis cursor-pointer">
                    {{ nameLookup[key] }}
                </label>
            </div>
        </div>
    </div>

    <div class="data-table overflow-hidden">
        <DataModal ref="modalRef" v-bind:data="currentData"></DataModal>
        <table class="w-full text-sm text-left">
            <thead class="text-xs text-gray-700 dark:text-gray-1000 uppercase bg-gray-50 dark:bg-slate-300">
                <tr>
                    <th @click="updateSort(key)" v-for="key in visibleKeys" scope="col"
                        class="px-6 py-3 max-w-6 overflow-x-auto text-ellipsis select-none cursor-pointer">
                        {{ nameLookup[key] }}
                        <svg class="w-3 h-2.5 inline-block mb-0.5 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M8.574 11.024h6.852a2.075 2.075 0 0 0 1.847-1.086 1.9 1.9 0 0 0-.11-1.986L13.736 2.9a2.122 2.122 0 0 0-3.472 0L6.837 7.952a1.9 1.9 0 0 0-.11 1.986 2.074 2.074 0 0 0 1.847 1.086Zm6.852 1.952H8.574a2.072 2.072 0 0 0-1.847 1.087 1.9 1.9 0 0 0 .11 1.985l3.426 5.05a2.123 2.123 0 0 0 3.472 0l3.427-5.05a1.9 1.9 0 0 0 .11-1.985 2.074 2.074 0 0 0-1.846-1.087Z"/>
                        </svg>
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="entry in dataEntries" v-on:click="openModal(entry, $event)"
                    class="border-b dark:hover:bg-gray-700 hover:bg-gray-100 cursor-pointer">
                    <th v-for="key in visibleKeys" scope="row"
                        class="px-6 py-4 font-medium max-w-6 whitespace-nowrap">
                        <div class="truncate" v-html="getData(entry, key)"></div>
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
