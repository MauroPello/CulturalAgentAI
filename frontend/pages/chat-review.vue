<template>
  <UContainer>
    <div class="py-10">
      <UCard>
        <template #header>
          <h1 class="text-2xl font-bold">Review Chat</h1>
        </template>
        <p class="mb-4">
          Paste a collection of messages and emails to get an LLM evaluation on
          their cultural and linguistic appropriateness.
        </p>
        <div class="flex flex-col items-start">
          <UTextarea
            v-model="textInput"
            class="w-full"
            placeholder="Paste your messages here..."
            :rows="10"
          />
          <UButton class="mt-4" @click="analyzeText"> Analyze </UButton>
        </div>
        <div v-if="analysisResult" class="mt-8">
          <h2 class="text-xl font-bold mb-2">Analysis Result</h2>
          <pre class="whitespace-pre-wrap">{{ analysisResult }}</pre>
        </div>
      </UCard>
    </div>
  </UContainer>
</template><script setup lang="ts">
import { ref } from "vue";

const textInput = ref("");
const analysisResult = ref("");

const analyzeText = async () => {
  // This is where the API call will be made.
  // For now, we'll just simulate a result.
  analysisResult.value = "This is a placeholder for the LLM evaluation result.";
};
</script>

<style scoped>
/* You can add additional styles here if needed */
</style>
