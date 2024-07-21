<script setup lang="ts">
import DataTable from "../components/DataTable.vue";
</script>
<template>
    <div class="text-center mb-4">
        <h1 class="about text-center mb-4 mt-4 text-4xl font-extrabold">Datasets for bioacoustics</h1>
        <p>This is a list of datasets that are applicable for work within bioacoustics and machine learning.</p>
        <p><b>Want to contribute?</b> Open a pull request that adds a JSON-file that describes the dataset(s) you want
            to add.</p>
    </div>
    <DataTable></DataTable>
</template>