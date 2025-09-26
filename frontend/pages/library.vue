<template>
  <div class="p-4 sm:p-6 lg:p-8">
    <h1 class="text-2xl font-bold mb-4">Library</h1>
    <p class="mb-8 text-gray-500">Manage your documents, upload new ones, and query their content.</p>

    <div class="space-y-8">

      <!-- Upload Card -->
      <UCard>
        <template #header>
          <h2 class="text-xl font-bold">Upload New Document</h2>
        </template>

        <div class="flex w-full items-center justify-center">
          <label
            for="dropzone-file"
            class="dark:hover:bg-bray-800 flex h-64 w-full cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 hover:bg-gray-100 dark:border-gray-600 dark:bg-gray-700 dark:hover:border-gray-500 dark:hover:bg-gray-600"
          >
            <div class="flex flex-col items-center justify-center pb-6 pt-5">
              <UIcon name="i-heroicons-cloud-arrow-up" class="mb-4 h-8 w-8" />
              <p class="mb-2 text-sm text-gray-500 dark:text-gray-400">
                <span class="font-semibold">Click to upload</span> or drag and drop
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
              multiple
              @change="handleFileChange"
            >
          </label>
        </div>
        <div v-if="selectedFiles.length > 0" class="mt-4">
          <p>Selected files:</p>
          <ul class="list-disc pl-5">
            <li v-for="file in selectedFiles" :key="file.name">{{ file.name }}</li>
          </ul>
          <UButton
            class="mt-2"
            :loading="isUploading"
            :disabled="isUploading"
            @click="uploadFile"
          >
            {{ isUploading ? 'Uploading...' : `Upload ${selectedFiles.length} file(s)` }}
          </UButton>
        </div>
        <UAlert
          v-if="uploadStatus"
          :title="uploadStatus.includes('successfully') ? 'Success' : 'Error'"
          :description="uploadStatus"
          :color="uploadStatus.includes('successfully') ? 'green' : 'red'"
          variant="subtle"
          class="mt-4"
        />
      </UCard>

      <!-- Query Card -->
      <UCard>
        <template #header>
          <div class="flex justify-between items-center">
            <h2 class="text-xl font-bold">Query Documents</h2>
            <UButton v-if="queryResult" variant="ghost" icon="i-heroicons-x-mark" @click="clearQuery" />
          </div>
        </template>

        <div class="space-y-4">
          <p>Ask a question about the documents you've uploaded. The system will retrieve relevant information.</p>
          <div class="flex gap-2">
            <UInput
              v-model="query"
              type="text"
              placeholder="e.g., What was our revenue last quarter?"
              class="flex-grow"
              :disabled="isQuerying"
              @keyup.enter="submitQuery"
            />
            <UButton :loading="isQuerying" @click="submitQuery">
              Ask
            </UButton>
          </div>

          <UAlert
            v-if="queryError"
            title="Error"
            :description="queryError"
            color="red"
            variant="subtle"
          />
        </div>
      </UCard>

      <!-- Results / Document List -->
      <div>
        <!-- Query Result View -->
        <div v-if="queryResult" class="space-y-4">
          <UCard v-if="queryResult.answer">
            <template #header>
              <h3 class="font-bold">AI Answer</h3>
            </template>
            <div class="prose dark:prose-invert">
              {{ queryResult.answer }}
            </div>
          </UCard>

          <UAlert
            v-if="queryResult.error"
            title="LLM Error"
            :description="queryResult.error"
            color="red"
            variant="subtle"
          />

          <UCard>
            <template #header>
              <h3 class="font-bold">Retrieved Chunks (Context)</h3>
            </template>
            <div class="prose dark:prose-invert max-w-none">
              <p v-if="queryResult.retrieved_chunks.length === 0">No relevant chunks found.</p>
              <ul v-else class="list-disc space-y-2 pl-5">
                <li v-for="(chunk, index) in queryResult.retrieved_chunks" :key="index" class="bg-gray-50 dark:bg-gray-800 p-2 rounded">
                  "{{ chunk }}"
                </li>
              </ul>
            </div>
          </UCard>
        </div>

        <!-- Default Document List View -->
        <UCard v-else>
          <template #header>
            <h2 class="text-xl font-bold">All Documents</h2>
          </template>
          <UTable :rows="documents" :columns="columns">
            <template #status-data="{ row }">
              <UBadge
                :color="row.status === 'completed' ? 'green' : 'orange'"
                variant="subtle"
              >
                {{ row.status }}
              </UBadge>
            </template>
          </UTable>
        </UCard>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

// Common interface for documents
interface Document {
  id: number;
  name: string;
  status: "processing" | "completed";
}

interface QueryResult {
  answer?: string;
  error?: string;
  retrieved_chunks: string[];
  prepared_prompt?: string;
}

// --- Documents List ---
const columns = [
  { key: "name", label: "Document Name" },
  { key: "status", label: "Status" },
];
const documents = ref<Document[]>([
  { id: 1, name: "Document 1.pdf", status: "completed" },
  { id: 2, name: "Document 2.docx", status: "processing" },
  { id: 3, name: "Another document.txt", status: "completed" },
]);
// TODO: Fetch documents from an API onMounted

// --- Upload ---
const selectedFiles = ref<File[]>([]);
const isUploading = ref(false);
const uploadStatus = ref<string>("");

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    const files = Array.from(target.files);
    const allowedTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      "application/vnd.ms-excel",
      "text/plain",
    ];

    const validFiles = files.filter(file => allowedTypes.includes(file.type));

    if (validFiles.length !== files.length) {
      uploadStatus.value = "Upload failed: Some files have invalid types. Only PDF, DOCX, XLSX, XLS, TXT are allowed.";
      // Keep only valid files, or clear all? For now, let's just warn and not add any.
      target.value = ""; // Clear the input
      selectedFiles.value = [];
    } else {
      selectedFiles.value = validFiles;
      uploadStatus.value = "";
    }
  }
};

const uploadFile = async () => {
  if (selectedFiles.value.length === 0) return;

  isUploading.value = true;
  uploadStatus.value = "";
  const uploadResults: string[] = [];

  for (const file of selectedFiles.value) {
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/process-document/", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        uploadResults.push(`SUCCESS: '${file.name}' processed (${result.chunks_added} chunks created).`);
      } else {
        const errorData = await response.json().catch(() => ({ detail: "Unknown error" }));
        uploadResults.push(`ERROR: Upload failed for '${file.name}': ${errorData.detail}`);
      }
    } catch (error) {
      uploadResults.push(`ERROR: Network error for '${file.name}': ${error instanceof Error ? error.message : "Unknown"}`);
    }
  }

  isUploading.value = false;
  uploadStatus.value = uploadResults.join("\n");
  selectedFiles.value = [];
  const fileInput = document.getElementById("dropzone-file") as HTMLInputElement;
  if (fileInput) fileInput.value = "";
  // TODO: Refresh the document list
};

// --- Query ---
const query = ref('');
const queryResult = ref<QueryResult | null>(null);
const isQuerying = ref(false);
const queryError = ref<string | null>(null);

const submitQuery = async () => {
  if (!query.value.trim()) {
    queryError.value = 'Please enter a query.';
    return;
  }

  isQuerying.value = true;
  queryResult.value = null;
  queryError.value = null;

  try {
    const response = await fetch('http://127.0.0.1:8000/query/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query.value, n_results: 3 }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'An error occurred while fetching data.');
    }

    queryResult.value = await response.json();
  } catch (err) {
    if (err instanceof Error) {
      queryError.value = err.message;
    } else {
      queryError.value = 'An unknown error occurred.';
    }
  } finally {
    isQuerying.value = false;
  }
};

const clearQuery = () => {
  query.value = '';
  queryResult.value = null;
  queryError.value = null;
};

</script>

<style scoped>
/* You can add page-specific styles here */
</style>
