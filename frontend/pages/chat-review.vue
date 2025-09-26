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
            size="xl"
            autoresize
          />
          <UButton class="mt-4" size="xl" @click="analyzeText"> Analyze </UButton>
        </div>
        <div v-if="analysisResult" class="mt-8">
          <h2 class="text-xl font-bold mb-2">Analysis Result</h2>
          <pre class="whitespace-pre-wrap">{{ analysisResult }}</pre>
        </div>
        <div v-else-if="loading" class="mt-8 text-center">
          <p>Analyzing...</p>
        </div>
        <div v-else-if="error" class="mt-8 text-center text-red-500">
          <p>{{ error }}</p>
        </div>
      </UCard>
    </div>
  </UContainer>
</template><script setup lang="ts">
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
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
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
