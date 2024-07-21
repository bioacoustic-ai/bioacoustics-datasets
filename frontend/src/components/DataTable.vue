<script setup lang="ts">
import DataModal from "@/components/DataModal.vue";
import moment from "moment";
import { ref } from "vue";
import objects, { type DataEntryType } from "../data";

var currentData: DataEntryType | null = null;
const modalRef = ref();

function formatDate(value: Date) {
    return moment(String(value)).format('MM/DD/YYYY')
}

function openModal(entry: DataEntryType) {
    currentData = entry;
    modalRef.value.showModal(entry);
}
</script>

<template>
    <div>
        <DataModal ref="modalRef" v-bind:data="currentData"></DataModal>
        <div class="relative overflow-x-auto">
            <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
                <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                    <tr>
                        <th scope="col" class="px-6 py-3">
                            Name
                        </th>
                        <th scope="col" class="px-6 py-3">
                            Date published
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="entry in objects" v-on:click="openModal(entry)"
                        class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                        <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                            {{ entry.name }}
                        </th>
                        <td class="px-6 py-4">
                            {{ formatDate(entry.datePublished) }}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
