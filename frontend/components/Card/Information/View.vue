<template>
  <div class="information-card">
    <transition name="fade">
      <div v-if="!isLoading" class="mb-0">
        <div class="flex justify-content-between mb-3">
          <div>
            <span class="block text-800 font-medium text-left mb-3">{{ title }}</span>
            <div class="text-900 font-bold text-3xl">
              <span class="information-card-nb">{{ text_big }}</span>
              <span v-if="text_medium" class="font-bold text-xl">{{ text_medium }}</span>
              <span v-if="text_small" class="font-normal text-base">{{ text_small }}</span>
            </div>
          </div>
          <div class="flex text-3xl h-full align-items-center justify-content-center icon-bg">
            <i :class="icon" class="icon-shape"></i>
          </div>
        </div>
        <div v-if="subtitle_nb || subtitle_text" class="w-full text-left text-sm">
          <span :class="subtitle_nb_color" class="font-medium">{{ subtitle_nb }}</span>
          <span class="text-500">{{ subtitle_text }}</span>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="isLoading" class="w-full flex flex-column gap-3">
        <Skeleton />
        <Skeleton height="2rem" width="8rem" />
        <Skeleton />
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'CardInformationView',
  props: [
    'isLoading',
    'title',
    'text_big',
    'text_medium',
    'text_small',
    'subtitle_nb',
    'subtitle_text',
    'subtitle_nb_color',
    'icon'
  ]
}
</script>

<style scoped>
img {
  margin-top: -25px;
  margin-left: 34px;
}
</style>
