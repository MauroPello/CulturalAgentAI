<template>
  <div class="container mx-auto p-4">
    <UCard>
      <template #header>
        <h1 class="text-2xl font-bold">Upload Document</h1>
      </template>
      <div class="flex w-full items-center justify-center">
        <label
          for="dropzone-file"
          class="dark:hover:bg-bray-800 flex h-64 w-full cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 hover:bg-gray-100 dark:border-gray-600 dark:bg-gray-700 dark:hover:border-gray-500 dark:hover:bg-gray-600"
        >
          <div class="flex flex-col items-center justify-center pb-6 pt-5">
            <UIcon name="i-heroicons-cloud-arrow-up" class="mb-4 h-8 w-8" />
            <p class="mb-2 text-sm text-gray-500 dark:text-gray-400">
              <span class="font-semibold">Click to upload</span> or drag and
              drop
            </p>
            <p class="text-xs text-gray-500 dark:text-gray-400">
              PDF, DOC, or DOCX
            </p>
          </div>
          <input
            id="dropzone-file"
            type="file"
            class="hidden"
            accept=".pdf,.doc,.docx"
            @change="handleFileChange"
          >
        </label>
      </div>
      <div v-if="selectedFile" class="mt-4">
        <p>Selected file: {{ selectedFile.name }}</p>
        <UButton class="mt-2" @click="uploadFile"> Upload </UButton>
      </div>
    </UCard>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const selectedFile = ref<File | null>(null);

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    const file = target.files[0];
    const allowedTypes = [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];
    if (file && allowedTypes.includes(file.type)) {
      selectedFile.value = file;
    } else {
      alert("Please select a valid file type (PDF, DOC, DOCX).");
      target.value = "";
    }
  }
};

const uploadFile = () => {
  if (selectedFile.value) {
    console.log("Uploading file:", selectedFile.value.name);
    // Here you would typically use a library like Axios to send the file to your backend
  }
};
</script>

<style scoped>
/* Add any additional styles here */
</style>
