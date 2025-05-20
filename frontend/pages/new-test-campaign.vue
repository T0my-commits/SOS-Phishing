<script setup>
definePageMeta({
  middleware: 'auth'
})
</script>

<template>
  <div>
    <h2>Start new campaign</h2>
    <FormsNewCampaignView />
  </div>
</template>

