<template>
    <v-container>
        <v-row align="center" justify="center" class="mb-10">
            <h1>Manuscript classifier</h1>
        </v-row>
        <v-card class="mb-10" align="center">
            <v-card-text>
                <p>
                    This is a tool for vizualizing New Testament manuscripts based on their content. 
                    It relies on Machine Learning approaches to project texts.
                    Two classificat
                </p>
            </v-card-text>
        </v-card>
        <v-row align="center" justify="center">
            <v-btn href="/project" class="mr-2">Standard Projector</v-btn>
            <v-btn href="/experimental" class="mr-2">Experimental Projector</v-btn>
            <v-btn href="/comparator">Comparator</v-btn>
        </v-row>
    </v-container>
</template>