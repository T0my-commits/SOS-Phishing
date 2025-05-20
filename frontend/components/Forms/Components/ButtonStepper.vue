<template>
  <div class="mt-3">
    <div v-if="prevBtn !== 'true'" class="flex justify-content-end">
      <Button label="Next"
        icon="pi pi-arrow-right" iconPos="right"
        @click="$emit('stepForward')" />
    </div>

    <div v-else class="flex justify-content-between">
      <Button label="Back" severity="secondary"
        icon="pi pi-arrow-left"
        @click="$emit('stepBackward')" />
      <Button v-if="nextBtn === 'true'"
        label="Next"
        icon="pi pi-arrow-right" iconPos="right"
        @click="$emit('stepForward')" />
      <Button v-if="nextBtn === 'submit'"
        label="Submit"
        icon="pi pi-check" iconPos="right"
        @click="$emit('stepForward')" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'FormsComponentsButtonStepper',
  props: ['prevBtn', 'nextBtn']
};
</script>

