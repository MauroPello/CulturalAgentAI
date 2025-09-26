<template>
  <div class="container mx-auto p-4">
    <UCard>
      <template #header>
        <h1 class="text-2xl font-bold">Review Chat</h1>
      </template>
      <p class="mb-4">
        Paste a collection of messages and emails to get an LLM evaluation on their cultural and linguistic appropriateness.
      </p>
      <div class="flex flex-col items-start">
        <UTextarea
          v-model="textInput"
          class="w-full"
          placeholder="Paste your messages here..."
          :rows="10"
        />
        <UButton class="mt-4" @click="analyzeText" :disabled="loading"> Analyze </UButton>
        <p v-if="error" class="text-red-500 mt-2">{{ error }}</p>
      </div>
      <div v-if="loading" class="mt-4">
        <p>Loading...</p>
      </div>
      <div v-if="analysisResult" class="mt-8">
        <h2 class="text-xl font-bold mb-2">Analysis Result</h2>
        <pre class="whitespace-pre-wrap">{{ analysisResult }}</pre>
      </div>
    </UCard>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const textInput = ref("");
const analysisResult = ref("");
const loading = ref(false);
const error = ref<string | null>(null);

const analyzeText = async () => {
  if (!textInput.value.trim()) {
    error.value = "Please paste some text to analyze.";
    analysisResult.value = "";
    return;
  }

  loading.value = true;
  analysisResult.value = "";
  error.value = null;

  try {
    const response = await $fetch<{ answer: string }>("http://127.0.0.1:8000/ask", {
      method: "POST",
      body: {
        query: textInput.value,
      },
    });
    analysisResult.value = response.answer;
  } catch (e: any) {
    error.value = "An error occurred while analyzing the text. Please try again.";
    console.error(e);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* You can add additional styles here if needed */
</style>
