<script setup>
import { ref, provide } from 'vue';
const isSidenavVisibleBis = ref(false);
const headerItems = ref([]);

const toggleNav = () => {
  isSidenavVisibleBis.value = !isSidenavVisibleBis.value;
};

</script>

<template>
  <div>
    <!-- Sidenav -->
    <CommonSidenavView :isSidenavVisibleBis="isSidenavVisibleBis" />

    <!-- Header -->
    <div id="main-content">
      <CommonHeaderView @toggle-sidenav="toggleNav" />

      <!-- Page to display -->
      <NuxtPage />

    </div>
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
};
</script>
