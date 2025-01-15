<template>
    <v-row>
        <VuePlotly :data="formattedData" :layout="layout" :display-mode-bar="false"></VuePlotly>
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
                    l: 3,
                    r: 3,
                    b: 10,
                    t: 10,
                    pad: 2
                }
            },
            formattedData: []
        }
    },
    methods: {
        mapCategoriesToNumbers(categories) {
            const categoryMap = {};
            let counter = 0;

            return categories.map(category => {
                if (!(category in categoryMap)) {
                    categoryMap[category] = counter++;
                }
                return categoryMap[category];
            });
        },
    },
    mounted() {
        console.log(this.plotData)
        let categories = []
        if (Object.hasOwnProperty.call(this.plotData, 'selected_classification')) {
            categories = this.mapCategoriesToNumbers(this.plotData.selected_classification)
        }

        this.formattedData = [
            {
                x: this.plotData.x,
                y: this.plotData.y,
                z: this.plotData.z,
                mode: 'markers+text',
                type: 'scatter3d',
                text: this.plotData.labels,
                marker: {
                    size: 5,
                    color: categories,
                    colorscale: 'Viridis',
                    opacity: 0.8
                }
            }
        ]
    }
}
</script>


<style scoped>
.js-plotly-plot,
.plot-container {
    height: 80vh;
    width: 100%;
    padding-top: 10;
}
</style>