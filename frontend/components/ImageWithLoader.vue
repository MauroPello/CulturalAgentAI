<template>
  <div class="relative">
    <div
      v-if="loading"
      class="absolute inset-0 flex items-center justify-center bg-gray-200 dark:bg-gray-700 rounded"
      :style="{ width: width + 'px', height: height + 'px' }"
    >
      <!-- Simple Spinner -->
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 dark:border-gray-100"/>
    </div>
    <NuxtImg
      v-bind="$attrs"
      :width="width"
      :height="height"
      class="transition-opacity duration-300 ease-in-out"
      :class="{ 'opacity-0': loading, 'opacity-100': !loading }"
      @load="onImageLoad"
      @error="onImageError"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  width?: number | string
  height?: number | string
}

withDefaults(defineProps<Props>(), {
  width: 'auto',
  height: 'auto',
})

const loading = ref(true)

const onImageLoad = () => {
  loading.value = false
}

const onImageError = () => {
  loading.value = false
  console.error("Failed to load image")
}
</script>
