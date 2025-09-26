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
              PDF, DOCX, XLSX, XLS, or TXT
            </p>
          </div>
          <input
            id="dropzone-file"
            type="file"
            class="hidden"
            accept=".pdf,.docx,.xlsx,.xls,.txt"
            @change="handleFileChange"
          >
        </label>
      </div>
      <div v-if="selectedFile" class="mt-4">
        <p>Selected file: {{ selectedFile.name }}</p>
        <UButton 
          class="mt-2" 
          :loading="isUploading"
          :disabled="isUploading"
          @click="uploadFile"
        > 
          {{ isUploading ? 'Uploading...' : 'Upload' }}
        </UButton>
      </div>
      <div v-if="uploadStatus" class="mt-4">
        <p 
          :class="{
            'text-green-600': uploadStatus.includes('successfully'),
            'text-red-600': uploadStatus.includes('failed')
          }"
        >
          {{ uploadStatus }}
        </p>
      </div>
    </UCard>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const selectedFile = ref<File | null>(null);
const isUploading = ref(false);
const uploadStatus = ref<string>("");

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    const file = target.files[0];
    const allowedTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      "application/vnd.ms-excel",
      "text/plain",
    ];
    if (file && allowedTypes.indexOf(file.type) !== -1) {
      selectedFile.value = file;
      uploadStatus.value = "";
    } else {
      alert("Please select a valid file type (PDF, DOCX, XLSX, XLS, TXT).");
      target.value = "";
    }
  }
};

const uploadFile = async () => {
  if (!selectedFile.value) {
    return;
  }

  isUploading.value = true;
  uploadStatus.value = "";

  try {
    const formData = new FormData();
    formData.append("file", selectedFile.value);

    const response = await fetch("http://localhost:8000/process-document/", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const result = await response.json();
      uploadStatus.value = `Document processed successfully! ${result.chunks_added} chunks created. Total documents in store: ${result.total_documents_in_store}`;
      console.log("Upload successful:", result);
      
      // Reset the form
      selectedFile.value = null;
      const fileInput = document.getElementById("dropzone-file") as HTMLInputElement;
      if (fileInput) {
        fileInput.value = "";
      }
    } else {
      const errorData = await response.json().catch(() => ({ detail: "Upload failed" }));
      uploadStatus.value = `Upload failed: ${errorData.detail || "Unknown error"}`;
      console.error("Upload failed:", errorData);
    }
  } catch (error) {
    uploadStatus.value = `Upload failed: ${error instanceof Error ? error.message : "Network error"}`;
    console.error("Upload error:", error);
  } finally {
    isUploading.value = false;
  }
};
</script>

<style scoped>
/* Add any additional styles here */
</style>
