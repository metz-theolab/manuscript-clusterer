<template>
    <v-row>
        <VuePlotly :data="formattedData" :layout="layout"></VuePlotly>
    </v-row>
</template>

<script>
import { VuePlotly } from 'vue3-plotly'


export default {
    components: {
        VuePlotly
    },
    props: {
        plotData: Object,
    },
    data() {
        return {
            layout: {
                margin: {
                    // l: 3,
                    // r: 3,
                    b: 80,
                    t: 10,
                    pad: 4
                },
                yaxis: { type: 'category' },
                xaxis: { type: 'category'},
            },
            formattedData: []
        }
    },
    mounted() {
        this.formattedData = [
            {
                z: this.plotData.z,
                x: this.plotData.x,
                y: this.plotData.y,
                type: 'heatmap',
                hoverongaps: false,
                showscale: false
            }
        ];
    }
}
</script>

<style scoped>
.js-plotly-plot,
.plot-container {
    height: 50vh;
    width: 100%;
    padding-top: 20px;
}
</style>