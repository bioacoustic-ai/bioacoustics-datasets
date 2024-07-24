<script setup lang="ts">
import { FwbButton, FwbModal } from 'flowbite-vue';
import { defineExpose, ref } from 'vue';
import { type DataEntryType } from "../data";
import { getData, nameLookup } from "../data/formatting";
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


defineExpose({ showModal });

var nameKeys = Object.keys(nameLookup);

</script>

<template>
    <fwb-modal v-if="isShowModal" @close="closeModal" size="5xl">
        <template #header>
            <div class="flex items-center text-lg">
                {{ data?.name }}
            </div>
        </template>
        <template #body>
            <div v-for="key in nameKeys" v-if="data">
                <DataGroup v-bind:title="nameLookup[key]" v-bind:content="getData(data, key)">
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
<style>

</style>../data/formatting