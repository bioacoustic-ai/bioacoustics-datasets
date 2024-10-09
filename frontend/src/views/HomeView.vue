<script setup lang="ts">
import DataTable from "../components/DataTable.vue";
</script>
<!--  TODO: use the createLink function -->
<template>
    <div class="flow-root">  
        <div>
            <!--
            Cool and practical way to set the source of images dynamically:
            https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture
            -->
            <picture>
                <source srcset=".././assets/BiocAI_image.png" media="(prefers-color-scheme: light)"/>
                <source srcset=".././assets/BiocAI_image_dark.png"  media="(prefers-color-scheme: dark)"/>
                <!--The source here is the "default", i.e. the normal version of the logo.-->
                <img width="100" class="h-auto max-w-xs float-left" src=".././assets/BiocAI_image.png"/>
            </picture>
        </div>
        <img class="h-auto max-w-xs rounded-lg float-right" src=".././assets/EU.png" width=90 alt="EU flag">
    </div>
    <div class="text-center mb-4">
        <h1 class="about text-center mb-4 mt-4 text-4xl font-extrabold">Datasets for bioacoustics</h1>
        <p>This table presents publicly available bioacoustic datasets that can be used with machine learning.</p>
        <p><b>Want to add a dataset?</b> Follow the instructions of this <a target="_blank" class="underline text-blue-800 dark:text-blue-400" href="https://github.com/Cangonin/bioacoustics-datasets">README file.</a></p>
        <p><b>Want to contribute to make this list better?</b> Open a pull request on <a target="_blank" class="underline text-blue-800 dark:text-blue-400" href="https://github.com/Cangonin/bioacoustics-datasets">this github repo!</a> 
        </p>
    </div>
    <DataTable></DataTable>
</template>