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
              icon="i-heroicons-arrow-up-tray"
              size="lg"
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
          <UAlert color="yellow" class="hidden"/>
          <UAlert color="red" class="hidden"/>
          <UAlert
            v-if="uploadStatus"
            :title="uploadStatusType === 'success' ? 'Success' : (uploadStatusType === 'warning' ? 'Warning' : 'Error')"
            :description="uploadStatus"
            :color="uploadStatusType === 'success' ? 'green' : (uploadStatusType === 'warning' ? 'yellow' : 'red')"
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
            <!-- Scrollable table container -->
            <div class="max-h-96 overflow-y-auto">
              <UTable :rows="documents" :columns="columns" :loading="isLoadingDocuments">
                <template #empty-state>
                  <div class="flex flex-col items-center justify-center py-6 gap-3">
                    <UIcon name="i-heroicons-document-text" class="w-10 h-10 text-gray-400" />
                    <p class="text-sm text-gray-500">No documents uploaded yet.</p>
                    <p class="text-sm text-gray-500">
                      Upload a document to get started.
                    </p>
                  </div>
                </template>
                <template #status-data="{ row }">
                  <UBadge
                    :color="row.status === 'completed' ? 'green' : 'orange'"
                    variant="subtle"
                  >
                    {{ row.status === 'completed' ? 'Processed' : 'Processing' }}
                  </UBadge>
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
            </div>
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

          <p>Are you sure you want to delete "{{ documentToDelete?.name }}"?</p>

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
import { useDocuments } from '~/composables/useDocuments';

const { documents, isLoadingDocuments, fetchDocuments } = useDocuments();

// Enhanced Document interface to match backend response
interface Document {
  id: number;
  name: string;
  size: string;
  upload_date: string;
  status: "processing" | "completed";
  file_id: string; // Add file_id for delete functionality
}

// --- Documents List ---
const columns = [
  { key: "name", label: "Document Name" },
  { key: "size", label: "Size" },
  { key: "upload_date", label: "Upload Date" },
  { key: "status", label: "Status" },
  { key: "actions", label: "Actions", class: "text-right" },
];

// --- Upload ---
const selectedFiles = ref<File[]>([]);
const isUploading = ref(false);
const uploadStatus = ref<string>("");
const uploadStatusType = ref<"success" | "warning" | "error">("success");

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
  uploadStatusType.value = "success"; // Default to success

  const formData = new FormData();
  selectedFiles.value.forEach(file => {
    formData.append("files", file);
  });

  try {
    const response = await fetch("http://localhost:8000/process-documents/", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    
    // Debug logging to help troubleshoot
    console.log('Upload response:', { status: response.status, result });

    const statusMessages: string[] = [];
    
    // Handle different response formats from backend
    let hasSuccess = false;
    let hasDuplicates = false;
    let hasErrors = false;
    
    if (response.ok) {
      // Standard success response format
      hasSuccess = result.processed_files && result.processed_files.length > 0;
      hasDuplicates = result.duplicates && result.duplicates.length > 0;
      hasErrors = result.errors && result.errors.length > 0;
    } else if (response.status === 409 && result.detail) {
      // Duplicate files response format
      hasDuplicates = result.detail.duplicates && result.detail.duplicates.length > 0;
      hasErrors = result.detail.errors && result.detail.errors.length > 0;
    }
    
    // Debug logging
    console.log('Detection results:', { hasSuccess, hasDuplicates, hasErrors });

    if (response.ok || response.status === 409) { // Handle success and partial success
      if (hasSuccess) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const fileNames = result.processed_files.map((f: any) => `'${f.filename}'`).join(', ');
        statusMessages.push(`Successfully uploaded and processed: ${fileNames}.`);
      }

      if (hasDuplicates) {
        // Handle different duplicate response formats
        let duplicateNames = '';
        if (response.status === 409 && result.detail && result.detail.duplicates) {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          duplicateNames = result.detail.duplicates.map((d: any) => `'${d.filename}'`).join(', ');
        } else if (result.duplicates) {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          duplicateNames = result.duplicates.map((d: any) => `'${d.filename || d.name}'`).join(', ');
        }
        statusMessages.push(`These files already exist and were not re-uploaded: ${duplicateNames}.`);
      }

      if (hasErrors) {
        // Handle different error response formats
        let errorDetails = '';
        if (response.status === 409 && result.detail && result.detail.errors) {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          errorDetails = result.detail.errors.map((e: any) => `'${e.filename}': ${e.error}`).join('; ');
        } else if (result.errors) {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          errorDetails = result.errors.map((e: any) => `'${e.filename}': ${e.error}`).join('; ');
        }
        statusMessages.push(`Errors occurred with some files: ${errorDetails}.`);
      }

      // Set status type based on what happened
      if (hasSuccess && !hasDuplicates && !hasErrors) {
        uploadStatusType.value = "success";
      } else if (hasDuplicates && !hasErrors) {
        uploadStatusType.value = "warning";  // Pure duplicates should show warning
      } else if (hasSuccess && hasDuplicates) {
        uploadStatusType.value = "warning";  // Mixed success and duplicates should show warning
      } else if (hasSuccess && hasErrors) {
        uploadStatusType.value = "warning";  // Mixed success and errors should show warning
      } else {
        uploadStatusType.value = "error";    // Pure errors should show error
      }

      uploadStatus.value = statusMessages.join('\n');
      
      // Debug logging for final result
      console.log('Final upload result:', { 
        statusType: uploadStatusType.value, 
        message: uploadStatus.value 
      });

    } else { // Handle other errors (400, 500, etc.)
      uploadStatusType.value = "error";
      if (result.detail) {
        uploadStatus.value = `Upload failed: ${result.detail.message || result.detail}`;
      } else {
        uploadStatus.value = "An unknown error occurred during upload.";
      }
    }
  } catch (error) {
    uploadStatusType.value = "error";
    uploadStatus.value = `Network error: ${error instanceof Error ? error.message : "Unknown"}`;
  } finally {
    isUploading.value = false;
    selectedFiles.value = [];
    const fileInput = document.getElementById("dropzone-file") as HTMLInputElement;
    if (fileInput) fileInput.value = "";
    await fetchDocuments();
  }
};

// --- Delete ---
const isDeleting = ref(false);
const deleteError = ref<string | null>(null);
const isDeleteModalOpen = ref(false);
const documentToDelete = ref<Document | null>(null);

const handleDelete = (document: Document) => {
  documentToDelete.value = document;
  isDeleteModalOpen.value = true;
};

const confirmDelete = async () => {
  if (documentToDelete.value) {
    await deleteDocument(documentToDelete.value.file_id);
  }
  isDeleteModalOpen.value = false;
  documentToDelete.value = null;
};

const deleteDocument = async (fileId: string) => {
  isDeleting.value = true;
  deleteError.value = null;
  try {
    const response = await fetch(
      `http://localhost:8000/uploaded-files/${fileId}`,
      {
        method: "DELETE",
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to delete document.");
    }

    // Refresh the document list after successful deletion
    await fetchDocuments();
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
