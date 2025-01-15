<template>
    <v-container class="fluid">
        <v-row align="center" justify="center" class="mb-10">
            <h1>Compare the distances between manuscripts using different schemes</h1>
        </v-row>
        <v-card class="mb-10" align="center">
            <v-card-text>
                <p>
                    The comparator allows to compare the global distances between manuscripts as well as between verses.
                </p>
            </v-card-text>
        </v-card>
        <v-tabs v-model="tab" align-tabs="center" color="deep-purple-accent-4">
            <v-tab :value="1">All text</v-tab>
            <v-tab :value="2">Verses</v-tab>
        </v-tabs>
        <v-tabs-window v-model="tab">
      <v-tabs-window-item :value="1">

        <v-row>
            <v-col>
                <h2>Wisse profiles</h2>
                <HeatMap :plotData="heatMapDataWisse" :key="heatMapDataWisse"></HeatMap>
            </v-col>
            <v-col>
                <h2>Using all text</h2>
                <HeatMap :plotData="heatMapDataAll" :key="heatMapDataAll"></HeatMap>
            </v-col>
        </v-row>
        </v-tabs-window-item>
        
        <v-tabs-window-item :value="2">

        <v-row class="mb-2" justify="center" align="center">
            <v-select label="MS1" :items="manuscriptsList" v-model="selectedMS1" max-width="20%" class="mx-auto">
            </v-select>
            <v-select label="MS2" :items="manuscriptsList" v-model="selectedMS2" max-width="20%" class="mx-auto">
            </v-select>
        </v-row>

        <v-row justify="center" align="center">
            <v-btn @click="compareVerses()">Compare</v-btn>
        </v-row>
        <v-row>
            <v-col cols="6">
                <h2>Comparison of content</h2>
                <HeatMap :plotData="heatMapVerses" :key="heatMapVerses"></HeatMap>
            </v-col>
            <v-col cols="6">
                <h2>Comparison of Wisse</h2>
                <HeatMap :plotData="heatMapVersesProfile" :key="heatMapVersesProfile"></HeatMap>
            </v-col>

        </v-row>
        <v-row class="my-10">
            <v-select label="Verses" :items="verseList" v-model="selectedVerse" @update:modelValue="getCollation()">
            </v-select>
        </v-row>
        <v-row class="my-auto mx-auto" style="overflow-x: scroll;">
            <div v-html="collation">
            </div>
        </v-row>
        <v-row class="my-5 mx-auto">
            <div v-html="readingsTable">
            </div>
        </v-row>
        </v-tabs-window-item>
    </v-tabs-window>
    </v-container>
</template>

<script>
export default {
    data() {
        return {
            heatMapDataWisse: {},
            heatMapDataAll: {},
            heatMapDataWisseReadings: {},
            heatMapVerses: {},
            heatMapVersesProfile: {},
            heatMapDataAllText: {},
            manuscriptsList: [],
            selectedMS1: "20001",
            selectedMS2: "20002",
            selectedVerse: "1",
            verseList: [],
            collation: "",
            readingsTable: "",
            tab: "1"
        }
    },
    methods: {
        compare() {
            this.axios
                .get('/manuscripts/transform/distances/?manuscript1=' + this.selectedMS1 + '&manuscript2=' + this.selectedMS2 + '&distance_scheme=wisse&format_heatmap=true')
                .then((response) => {
                    this.heatMapDataWisseReadings = response.data
                })
        },
        compareVerses() {
            this.axios
                .get('/manuscripts/transform/versedistances/?manuscript_1=' + this.selectedMS1 + '&manuscript_2=' + this.selectedMS2 + '&format_heatmap=true')
                .then((response) => {
                    this.heatMapVerses = response.data
                    console.log(this.heatMapVerses)
                })
            this.axios
                .get('/manuscripts/transform/profiles/?manuscript_1=' + this.selectedMS1 + '&manuscript_2=' + this.selectedMS2 + '&format_heatmap=true')
                .then((response) => {
                    this.heatMapVersesProfile = response.data
                })
        },
        getCollation() {
            // http://localhost:8000/manuscripts/collation/?manuscript_1=20001&manuscript_2=20002&verse=1
            this.axios
                .get('/manuscripts/collation/?manuscript_1=' + this.selectedMS1 + '&manuscript_2=' + this.selectedMS2 + '&verse=' + this.selectedVerse)
                .then((response) => {
                    this.collation = response.data
                })

        }
    },
    created() {
        this.axios
            .get('/manuscripts/transform/distances/?all_manuscripts=true&distance_scheme=wisse&format_heatmap=true')
            .then((response) => {
                this.heatMapDataWisse = response.data
            })

        this.axios
            .get('/manuscripts/transform/distances/?all_manuscripts=true&distance_scheme=all&format_heatmap=true')
            .then((response) => {
                this.heatMapDataAll = response.data
            })


        this.axios
            .get('/manuscripts/')
            .then((response) => {
                this.manuscriptsList = response.data
            })

        this.axios
            .get('/manuscript/' + this.selectedMS1 + '/verses')
            .then((response) => {
                this.verseList = response.data
                console.log(this.verseList)
            })

        this.axios
            .get("/manuscripts/transform/wissereadings")
            .then((response) => {
                this.readingsTable = response.data
            })
    }
}
</script>