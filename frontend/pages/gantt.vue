<template>
  <div class="container mx-auto p-4">
    <UCard>
      <template #header>
        <h1 class="text-2xl font-bold">Test Gantt Convert Endpoint</h1>
      </template>
      <p class="mb-4">
        Enter a project name and description to generate a Gantt chart plan from the `convert` endpoint.
      </p>
      <div class="flex flex-col space-y-4">
        <UInput v-model="projectName" placeholder="Project Name" />
        <UTextarea v-model="projectDescription" placeholder="Project Description" :rows="5" />
        <UButton @click="generatePlan" :loading="loading">Generate Plan</UButton>
      </div>

      <div v-if="error" class="mt-4 p-4 bg-red-100 text-red-700 rounded">
        <p><strong>Error:</strong></p>
        <pre class="whitespace-pre-wrap">{{ error }}</pre>
      </div>

      <div v-if="result" class="mt-4">
        <h2 class="text-xl font-bold mb-2">Generated Plan (JSON Response)</h2>
        <pre class="p-4 bg-gray-100 rounded whitespace-pre-wrap">{{ JSON.stringify(result, null, 2) }}</pre>
      </div>
    </UCard>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const projectName = ref('');
const projectDescription = ref('');
const result = ref<any>(null);
const loading = ref(false);
const error = ref<string | null>(null);

const generatePlan = async () => {
  if (!projectName.value || !projectDescription.value) {
    error.value = 'Please provide both a project name and a description.';
    return;
  }

  loading.value = true;
  error.value = null;
  result.value = null;

  try {
    // Assuming the Gantt API is running at this address
    const response = await $fetch('http://127.0.0.1:8000/convert', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: {
        project_name: projectName.value,
        description: projectDescription.value,
      },
    });
    result.value = response;
  } catch (e: any) {
    console.error(e);
    error.value = e.data?.detail || e.message || 'An unknown error occurred.';
  } finally {
    loading.value = false;
  }
};
</script>