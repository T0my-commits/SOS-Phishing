<template>
  <div>
     <div class="block text-800 font-medium text-left mb-3">Compromissions by category</div>
     <Chart type="pie" :data="chartData" :options="chartOptions" class="w-full" />
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import { getCompromiseByCategory } from '@/composables/campaigns';
import { useRoute } from 'vue-router';

const route = useRoute();

onMounted(async () => {
    chartData.value = await setChartData();
    chartOptions.value = setChartOptions();
});

const chartData = ref();
const chartOptions = ref();

const setChartData = async () => {
    let documentStyle = getComputedStyle(document.documentElement);

    // fetch data from API
    const url_id = route.params.url_id;
    const res = await getCompromiseByCategory(url_id);

    const labels = res.labels;
    const dataPerJobType = res.data;

    // Initialiser le total par catégorie à 0
    const totals = new Array(labels.length).fill(0);

    // Additionner les valeurs pour chaque type d'action
    dataPerJobType.forEach(jobType => {
        jobType.job_type_data.forEach((value, index) => {
            totals[index] += value;
        });
    });

    console.log(labels);
    console.log(totals);

    return {
        labels: labels,
        datasets: [
            {
                data: totals,
                backgroundColor: [
                    documentStyle.getPropertyValue('--indigo-500'),
                    documentStyle.getPropertyValue('--purple-500'),
                    documentStyle.getPropertyValue('--teal-500'),
                    documentStyle.getPropertyValue('--cyan-500'),
                    documentStyle.getPropertyValue('--pink-500'),
                    documentStyle.getPropertyValue('--yellow-500'),
                    documentStyle.getPropertyValue('--green-500'),
                    documentStyle.getPropertyValue('--blue-500'),
                    documentStyle.getPropertyValue('--bluegray-500'),
                    documentStyle.getPropertyValue('--red-500'),
                    documentStyle.getPropertyValue('--orange-500'),
                    documentStyle.getPropertyValue('--primary-500'),
                    documentStyle.getPropertyValue('--gray-500')
                ],
                hoverBackgroundColor: [
                    documentStyle.getPropertyValue('--indigo-400'),
                    documentStyle.getPropertyValue('--purple-400'),
                    documentStyle.getPropertyValue('--teal-400'),
                    documentStyle.getPropertyValue('--cyan-400'),
                    documentStyle.getPropertyValue('--pink-400'),
                    documentStyle.getPropertyValue('--yellow-400'),
                    documentStyle.getPropertyValue('--green-400'),
                    documentStyle.getPropertyValue('--blue-400'),
                    documentStyle.getPropertyValue('--bluegray-400'),
                    documentStyle.getPropertyValue('--red-400'),
                    documentStyle.getPropertyValue('--orange-400'),
                    documentStyle.getPropertyValue('--primary-400'),
                    documentStyle.getPropertyValue('--gray-400')
                ]
            }
        ]
    };
};

const setChartOptions = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color');
    // let textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
    // let surfaceBorder = documentStyle.getPropertyValue('--surface-border');

    return {
        plugins: {
            legend: {
                labels: {
                    usePointStyle: true,
                    color: textColor
                }
            }
        }
    };
};
</script>

