<template>
  <div class="container mx-auto p-4">
    <UCard>
      <template #header>
        <h1 class="text-2xl font-bold">
          Chat Review
        </h1>
      </template>
      <p class="mb-4">
        Paste a collection of messages and emails to get an LLM evaluation.
      </p>
      <div class="flex flex-col items-start">
        <UTextarea
          v-model="textInput"
          class="w-full"
          placeholder="Paste your messages here..."
          :rows="10"
        />
        <UButton
          class="mt-4"
          @click="analyzeText"
        >
          Analyze
        </UButton>
      </div>
      <div v-if="analysisResult" class="mt-8">
        <h2 class="text-xl font-bold mb-2">
          Analysis Result
        </h2>
        <pre class="whitespace-pre-wrap">{{ analysisResult }}</pre>
      </div>
    </UCard>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const textInput = ref('')
const analysisResult = ref('')

const analyzeText = async () => {
  // This is where the API call will be made.
  // For now, we'll just simulate a result.
  analysisResult.value = 'This is a placeholder for the LLM evaluation result.'
}
</script>

<style scoped>
/* You can add additional styles here if needed */
</style>
