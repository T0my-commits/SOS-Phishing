<script setup>
import { ref, provide } from 'vue';
const isSidenavVisibleBis = ref(false);
const headerItems = ref([]);

const toggleNav = () => {
  isSidenavVisibleBis.value = !isSidenavVisibleBis.value;
};

const setHeaderItems = (items) => {
  this.headerItems.value = {};
  if (items) {
    this.headerItems.value = items;
  }
  this.headerItems.value = items;
};

// Provide it for children
// provide('setHeaderItems', setHeaderItems);
</script>

<template>
  <div>
    <!-- Sidenav -->
    <CommonSidenavView :isSidenavVisibleBis="isSidenavVisibleBis" />

    <!-- Header -->
    <div id="main-content">
      <CommonHeaderView headerItems="" @toggle-sidenav="toggleNav" />

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
