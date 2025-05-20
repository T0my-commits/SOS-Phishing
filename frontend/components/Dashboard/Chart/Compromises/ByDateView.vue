<template>
  <div>
     <div class="flex align-items-start justify-content-between mb-6">
        <span class="block text-800 font-medium text-left mb-3">Activities overview</span>
        <div class="p-dropdown p-component p-inputwrapper p-inputwrapper-filled w-10rem h-1" data-pc-name="dropdown" data-pc-section="root" id="pv_id_2">
           <span class="p-dropdown-label p-inputtext" tabindex="0" role="combobox" aria-label="Last Week" aria-haspopup="listbox" aria-expanded="false" aria-controls="pv_id_2_list" aria-disabled="false" data-pc-section="input">Last Week</span>
           <div class="p-dropdown-trigger" data-pc-section="trigger">
              <i class="pi pi-angle-down"></i>
           </div>
        </div>
     </div>
     <!-- <div class="p-chart" style="position: relative;" data-pc-name="chart" data-pc-section="root"> -->
     <!--    <canvas data-pc-section="canvas" style="box-sizing: border-box; display: block; height: 300px; width: 1144px;" width="1144" height="300"></canvas> -->
     <!-- </div> -->
     <Chart type="line" :data="chartData" :options="chartOptions" class="h-30rem"  />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getActivityTimeline } from '@/composables/campaigns';
import { useRoute } from 'vue-router';

const route = useRoute();

onMounted(async () => {
    chartData.value = await setChartData();
    chartOptions.value = setChartOptions();
});

const chartData = ref();
const chartOptions = ref();

const setChartData = async () => {
    // get values from CSS
    const documentStyle = getComputedStyle(document.documentElement);

    // fetch data from API
    const url_id = route.params.url_id;
    const data = await getActivityTimeline(url_id);

    return {
        labels: data["labels"],
        datasets: [
            {
                label: 'Compromises',
                backgroundColor: documentStyle.getPropertyValue('--pink-500'),
                borderColor: documentStyle.getPropertyValue('--pink-500'),
                data: data["data_compromises"],
                borderRadius: 5,
                barThickness: 16,
                maxBarThickness: 20,
            },
            {
                label: 'Clicks',
                backgroundColor: documentStyle.getPropertyValue('--orange-500'),
                borderColor: documentStyle.getPropertyValue('--orange-500'),
                data: data["data_clicks"],
                borderRadius: 5,
                barThickness: 16,
                maxBarThickness: 20,
            },
            {
                label: 'Signalisations',
                backgroundColor: documentStyle.getPropertyValue('--yellow-500'),
                borderColor: documentStyle.getPropertyValue('--yellow-500'),
                data: data["data_signalisations"],
                borderRadius: 5,
                barThickness: 16,
                maxBarThickness: 20,
            },
            {
                label: 'Download attachment',
                backgroundColor: documentStyle.getPropertyValue('--purple-500'),
                borderColor: documentStyle.getPropertyValue('--purple-500'),
                data: data["data_download_attachment"],
                borderRadius: 5,
                barThickness: 16,
                maxBarThickness: 20,
            },
            {
                label: 'Open attachment',
                backgroundColor: documentStyle.getPropertyValue('--pink-300'),
                borderColor: documentStyle.getPropertyValue('--pink-300'),
                data: data["data_open_attachment"],
                borderRadius: 5,
                barThickness: 16,
                maxBarThickness: 20,
            },
            {
                label: 'Credentials leak',
                backgroundColor: documentStyle.getPropertyValue('--green-600'),
                borderColor: documentStyle.getPropertyValue('--green-600'),
                data: data["data_creds_leak"],
                borderRadius: 5,
                barThickness: 16,
                maxBarThickness: 20,
            }
        ]
    };
};
const setChartOptions = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color');
    const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
    const surfaceBorder = documentStyle.getPropertyValue('--surface-border');

    return {
        maintainAspectRatio: false,
        aspectRatio: 0.8,
        plugins: {
            legend: {
                labels: {
                    color: textColor
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: textColorSecondary,
                    font: {
                        weight: 500
                    }
                },
                grid: {
                    display: false,
                    drawBorder: false
                }
            },
            y: {
                ticks: {
                    color: textColorSecondary
                },
                grid: {
                    color: surfaceBorder,
                    drawBorder: false
                }
            }
        }
    };
}
</script>

