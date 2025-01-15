<template>
    <v-container>
        <v-row align="center" justify="center" class="mb-10">
            <h1>Exprimental projector</h1>
        </v-row>
        <v-card class="mb-10" align="center">
            <v-card-text>
                <p>
                    The experimental projector consists in using the whole text of the manuscripts for the projection (instead of individual readings)
                    and perform the clustering based on the similarity of the texts.
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
    </v-container>
</template>

<script>
import Projector from '../components/Projector.vue'


export default {
    data() {
        return {
            classification_schemes: ["clustered-profile", "clustered-content", "wisse", "von-soden", "text-type", 'aland-cat','date'],
            selected_classification: "clustered_profile",
            projectionsList: [],
            plotData: {},
            selectedMS: "",
            MSInfo: [],
            homogeneity: {},
            homogeneityLoaded: false
        }
    },
    created() {
        this.axios
            .get('/manuscripts/transform/projections/?all_manuscripts=true&experimental=true')
            .then((response) => {
                this.plotData = response.data
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
                .get('/manuscripts/transform/projections/?all_manuscripts=true&experimental=true')
                .then((response) => {
                    this.plotData = response.data
                    this.plotData["selected_classification"] = this.plotData[this.selected_classification]
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