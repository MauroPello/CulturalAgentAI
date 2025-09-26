<template>
  <div class="p-4 sm:p-6 lg:p-8">
    <h1 class="text-2xl font-bold mb-4">Library</h1>
    <p class="mb-8 text-gray-500">Here is a list of all uploaded documents.</p>
    <UCard>
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
</template>

<script setup lang="ts">
import { ref } from "vue";

interface Document {
  id: number;
  name: string;
  status: "processing" | "completed";
}

const columns = [
  {
    key: "name",
    label: "Document Name",
  },
  {
    key: "status",
    label: "Status",
  },
];

const documents = ref<Document[]>([
  { id: 1, name: "Document 1.pdf", status: "completed" },
  { id: 2, name: "Document 2.docx", status: "processing" },
  { id: 3, name: "Another document.txt", status: "completed" },
]);

// In a real application, you would fetch this data from an API.
// e.g., onMounted(async () => {
//   documents.value = await fetch('/api/documents').then(res => res.json());
// });
</script>

<style scoped>
/* You can add page-specific styles here */
</style>
