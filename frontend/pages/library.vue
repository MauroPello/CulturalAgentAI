<template>
  <UContainer>
    <div class="py-10">
      <h1 class="text-2xl font-bold mb-4">Library</h1>
      <p class="mb-8 text-gray-500">
        Manage your documents, upload new ones, and query their content.
      </p>

      <div class="space-y-8">
        <!-- Upload Card -->
        <UCard>
          <template #header>
            <h2 class="text-xl font-bold">Upload New Document</h2>
          </template>

          <div class="flex w-full items-center justify-center">
            <label
              for="dropzone-file"
              class="dark:hover:bg-bray-800 flex h- w-full cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 hover:bg-gray-100 dark:border-gray-600 dark:bg-gray-700 dark:hover:border-gray-500 dark:hover:bg-gray-600"
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
                multiple
                @change="handleFileChange"
              >
            </label>
          </div>
          <div v-if="selectedFiles.length > 0" class="mt-4">
            <p>Selected files:</p>
            <ul class="list-disc pl-5">
              <li v-for="file in selectedFiles" :key="file.name">
                {{ file.name }}
              </li>
            </ul>
            <UButton
              class="mt-2"
              :loading="isUploading"
              :disabled="isUploading"
              @click="uploadFile"
            >
              {{
                isUploading
                  ? "Uploading..."
                  : `Upload ${selectedFiles.length} file(s)`
              }}
            </UButton>
          </div>
          <UAlert
            v-if="uploadStatus"
            :title="uploadStatus.includes('✅') && !uploadStatus.includes('❌') ? 'Success' : uploadStatus.includes('❌') && !uploadStatus.includes('✅') ? 'Error' : 'Mixed Results'"
            :description="uploadStatus"
            :color="uploadStatus.includes('✅') && !uploadStatus.includes('❌') ? 'green' : uploadStatus.includes('❌') && !uploadStatus.includes('✅') ? 'red' : 'yellow'"
            variant="subtle"
            class="mt-4"
          />
        </UCard>

        <!-- Results / Document List -->
        <div>
          <!-- Default Document List View -->
          <UCard>
            <template #header>
              <h2 class="text-xl font-bold">All Documents</h2>
            </template>
            <UAlert
              v-if="deleteError"
              title="Error Deleting Document"
              :description="deleteError"
              color="red"
              variant="subtle"
              class="mb-4"
              :close-button="{
                icon: 'i-heroicons-x-mark-20-solid',
                color: 'red',
                variant: 'ghost',
              }"
              @close="deleteError = null"
            />
            <div v-if="isLoadingDocuments" class="flex justify-center py-6">
              <div class="flex items-center gap-2">
                <UIcon name="i-heroicons-arrow-path" class="w-5 h-5 animate-spin" />
                <span>Loading documents...</span>
              </div>
            </div>
            <UAlert
              v-else-if="documentError"
              title="Error Loading Documents"
              :description="documentError"
              color="red"
              variant="subtle"
              class="mb-4"
              :close-button="{
                icon: 'i-heroicons-x-mark-20-solid',
                color: 'red',
                variant: 'ghost',
              }"
              @close="documentError = null"
            />
            <UTable v-else :rows="documents" :columns="columns">
              <template #empty-state>
                <div class="flex flex-col items-center justify-center py-6 gap-3">
                  <UIcon name="i-heroicons-document-text" class="w-10 h-10" />
                  <p class="text-sm text-gray-500">No documents uploaded yet.</p>
                  <p class="text-sm text-gray-500">
                    Upload a document to get started.
                  </p>
                </div>
              </template>
              <template #file_size-data="{ row }">
                {{ formatFileSize(row.file_size) }}
              </template>
              <template #actions-data="{ row }">
                <div class="flex justify-end">
                  <UButton
                    icon="i-heroicons-trash"
                    size="sm"
                    color="red"
                    variant="ghost"
                    :loading="isDeleting"
                    @click="() => handleDelete(row)"
                  />
                </div>
              </template>
            </UTable>
          </UCard>
        </div>
      </div>

      <!-- Delete Confirmation Modal -->
      <UModal v-model="isDeleteModalOpen">
        <UCard>
          <template #header>
            <h3
              class="text-base font-semibold leading-6 text-gray-900 dark:text-white"
            >
              Confirm Deletion
            </h3>
          </template>

          <p>Are you sure you want to delete "{{ documentToDelete?.filename }}"?</p>

          <template #footer>
            <div class="flex justify-end gap-2">
              <UButton
                color="gray"
                variant="ghost"
                size="xl"
                @click="isDeleteModalOpen = false"
              >
                Cancel
              </UButton>
              <UButton color="red" size="xl" :loading="isDeleting" @click="confirmDelete">
                Delete
              </UButton>
            </div>
          </template>
        </UCard>
      </UModal>
    </div>
  </UContainer>
</template>

<script setup lang="ts">
import { ref } from "vue";

// Common interface for documents
interface Document {
  id: number;
  name: string;
  status: "processing" | "completed";
}

// --- Documents List ---
const columns = [
  { key: "filename", label: "Document Name" },
  { key: "file_type", label: "Type" },
  { key: "file_size", label: "Size" },
  { key: "actions", label: "Actions", class: "text-right" },
];

interface DocumentFile {
  filename: string
  file_size: number
  upload_time: number
  file_path: string
  file_type: string
}

const documents = ref<DocumentFile[]>([]);
const isLoadingDocuments = ref(false);
const documentError = ref<string | null>(null);

// Function to refresh document list
const refreshDocumentList = async () => {
  isLoadingDocuments.value = true;
  documentError.value = null;
  
  try {
    const { getFiles } = useApiCall();
    const result = await getFiles();
    documents.value = result.files;
  } catch (error) {
    documentError.value = error instanceof Error ? error.message : 'Failed to load documents';
    console.error('Error loading documents:', error);
  } finally {
    isLoadingDocuments.value = false;
  }
};

// Load documents on component mount
onMounted(async () => {
  await refreshDocumentList();
});

// Helper function to format file sizes
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return 'Processed'; // Changed for processed documents
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
};

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

    const validFiles = files.filter((file) => allowedTypes.includes(file.type));

    if (validFiles.length !== files.length) {
      uploadStatus.value =
        "Upload failed: Some files have invalid types. Only PDF, DOCX, XLSX, XLS, TXT are allowed.";
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

  try {
    const { uploadDocuments } = useApiCall();
    const result = await uploadDocuments(selectedFiles.value);
    
    // Check if we have any successful uploads
    const hasSuccess = result.processed_files && result.processed_files.length > 0;
    const hasErrors = result.errors && result.errors.length > 0;
    
    if (hasSuccess && !hasErrors) {
      // Only successful uploads
      const successMessages = result.processed_files.map(file => 
        `✅ '${file.filename}' processed successfully (${file.chunks_added} chunks created)`
      );
      uploadStatus.value = successMessages.join("\n");
    } else if (hasSuccess && hasErrors) {
      // Mixed results
      const successMessages = result.processed_files.map(file => 
        `✅ '${file.filename}' processed successfully (${file.chunks_added} chunks created)`
      );
      const errorMessages = result.errors.map(error =>
        `❌ Upload failed for '${error.filename}': ${error.error}`
      );
      uploadStatus.value = [...successMessages, ...errorMessages].join("\n");
    } else if (!hasSuccess && hasErrors) {
      // Only errors
      const errorMessages = result.errors.map(error =>
        `❌ Upload failed for '${error.filename}': ${error.error}`
      );
      uploadStatus.value = errorMessages.join("\n");
    }
    
    // Refresh the document list
    await refreshDocumentList();
    
  } catch (error) {
    uploadStatus.value = `❌ Upload error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`;
  } finally {
    isUploading.value = false;
    selectedFiles.value = [];
    const fileInput = document.getElementById("dropzone-file") as HTMLInputElement;
    if (fileInput) fileInput.value = "";
  }
};

// --- Delete ---
const isDeleting = ref(false);
const deleteError = ref<string | null>(null);
const isDeleteModalOpen = ref(false);
const documentToDelete = ref<DocumentFile | null>(null);

const handleDelete = (document: DocumentFile) => {
  documentToDelete.value = document;
  isDeleteModalOpen.value = true;
};

const confirmDelete = async () => {
  if (documentToDelete.value) {
    await deleteDocument(documentToDelete.value.filename);
  }
  isDeleteModalOpen.value = false;
};

const deleteDocument = async (filename: string) => {
  isDeleting.value = true;
  deleteError.value = null;
  try {
    const { deleteDocument } = useApiCall();
    await deleteDocument(filename);
    
    // Refresh the document list
    await refreshDocumentList();
    
  } catch (err) {
    if (err instanceof Error) {
      deleteError.value = err.message;
    } else {
      deleteError.value = "An unknown error occurred during deletion.";
    }
  } finally {
    isDeleting.value = false;
  }
};
</script>

<style scoped>
/* You can add page-specific styles here */
</style>
