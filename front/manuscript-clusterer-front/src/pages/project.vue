<template>
    <v-container>
        <v-row align="center" justify="center" class="mb-10">
            <h1>Standard projection</h1>
        </v-row>
        <v-card class="mb-10" align="justify">
            <v-card-text>
                <p>
                    This projection relies on the profile method (CPM) as defined by Wisse.
                    The manuscripts are projected using a Machine Learning so that manuscripts with close profiles are
                    grouped together, and only
                    considers
                    readings as selected by the CPM.

                    The coloration according to the groups is based on the classification scheme selected :

                <ul>
                    <li><strong>custom-profiles:</strong> based on the profile method</li>
                    <li><strong>custom-all-text:</strong> based on the entire text</li>
                    <li><strong>wisse:</strong> based on the Wisse classification</li>
                    <li><strong>von-soden:</strong> based on the Von Soden classification</li>
                    <li><strong>text-type:</strong> based on the text type</li>
                    <li><strong>aland-cat:</strong> based on the Aland categories</li>
                </ul>
                </p>
            </v-card-text>
        </v-card>
        <v-row>
            <p v-for="classification in classification_schemes" @input="getProjection()" class="mr-2">
                <input type="radio" :value=classification v-model="selected_classification" />
                <label for="one">{{ classification }}</label>
            </p>
        </v-row>

        <v-row>
            <v-col>
                <Projector :plotData="plotData" :key="plotData"></Projector>
            </v-col>
            <v-col cols="4">
                <v-card>
                    <v-card-title>Classification details</v-card-title>
                    <v-card-text>
                        <div v-if="homogeneityLoaded" v-for="(value, name, index) in homogeneity" :key="homogeneityLoaded">
                            {{ name }}: {{ value }}
                        </div>
                    </v-card-text>
                </v-card>
                <v-card class="mt-2">
                    <v-card-title>Manuscript details</v-card-title>
                    <v-card-text>
                        <v-select label="Select" :items="plotData.labels" v-model="selectedMS"
                            @update:modelValue="getInfo()">
                        </v-select>
                        <div v-if="MSInfo.length > 0" v-for="info in MSInfo">
                            <div v-for="(value, name, index) in info">
                                <b>{{ name }}</b>: {{ value }}
                            </div>
                        </div>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
        <v-row class="mb-2">
            <h2>Wisse profiles</h2>
        </v-row>
        <v-row>
            <HeatMap :plotData="heatMapData" :key="heatMapData"></HeatMap>
        </v-row>

    </v-container>
</template>

<script>
import Projector from '../components/Projector.vue'
import HeatMap from '../components/HeatMap.vue';


export default {
    data() {
        return {
            classification_schemes: ["clustered-profile", "clustered-content", "wisse", "von-soden", "text-type", 'aland-cat', 'date'],
            selected_classification: "clustered_profile",
            projectionsList: [],
            plotData: {},
            selectedMS: "",
            MSInfo: [],
            heatMapData: {},
            homogeneity: {},
            homogeneityLoaded: false
        }
    },
    created() {
        this.axios
            .get('/manuscripts/transform/projections/?all_manuscripts=true&experimental=false')
            .then((response) => {
                this.plotData = response.data
            })
        this.axios
            .get('/manuscripts/profiles/?format_heatmap=true')
            .then((response) => {
                this.heatMapData = response.data
            })

        this.axios
            .get("/manuscripts/transform/homogeneity/")
            .then((response) => {
                this.homogeneity = response.data
                this.homogeneityLoaded = true
                console.log(this.homogeneityLoaded)
            })
    },
    methods: {
        getProjection() {
            this.axios
                .get('/manuscripts/transform/projections/?all_manuscripts=true&experimental=false')
                .then((response) => {
                    this.plotData = response.data
                    this.plotData["selected_classification"] = this.plotData[this.selected_classification]
                    console.log(this.plotData)
                })

            console.log(this.plotData.selected_classification)
        },
        getInfo() {
            this.axios
                .get('/manuscript/' + this.selectedMS + '/info')
                .then((response) => {
                    this.MSInfo = response.data
                })
        }
    },
}
</script>