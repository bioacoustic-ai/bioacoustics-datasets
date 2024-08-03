<script setup lang="ts">
import DataTable from "../components/DataTable.vue";
</script>
<template>
    <div class="flow-root">  
        <img class="h-auto max-w-xs float-left" src=".././assets/BiocAI_image.png" width=100 alt="Logo of the BiocAI project">
        <img class="h-auto  max-w-xs rounded-lg float-right" src=".././assets/EU.png" width=90 alt="EU flag">
    </div>
    <div class="text-center mb-4">
        <h1 class="about text-center mb-4 mt-4 text-4xl font-extrabold">Datasets for bioacoustics</h1>
        <p>This table presents publicly available bioacoustic datasets that can be used with machine learning.</p>
        <p><b>Want to add a dataset?</b> Follow the instructions of this <a href="https://github.com/Cangonin/bioacoustics-datasets">README</a>file.</p>
        <p><b>Want to contribute to make this list better?</b> Open a pull request on <a href="https://github.com/Cangonin/bioacoustics-datasets">this github repo!</a> 
        </p>
    </div>
    <DataTable></DataTable>
</template>