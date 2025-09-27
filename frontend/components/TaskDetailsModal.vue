<template>
  <UModal v-model="isOpen" :ui="{ width: 'sm:max-w-2xl' }">
    <UCard>
      <template #header>
        <div class="flex justify-between items-start">
          <div class="flex items-center gap-4">
            <UIcon name="i-heroicons-document-text" class="h-8 w-8 text-primary-500" />
            <h2 class="text-2xl font-bold text-gray-800">{{ task.name }}</h2>
          </div>
          <UButton color="gray" variant="ghost" icon="i-heroicons-x-mark-20-solid" class="-my-1" @click="isOpen = false" />
        </div>
      </template>

      <div class="space-y-6">
        <!-- Description -->
        <div class="flex items-start">
          <UIcon name="i-heroicons-bars-3-bottom-left" class="h-6 w-6 text-gray-500 mr-4 mt-1" />
          <div>
            <p class="text-sm font-medium text-gray-500">Description</p>
            <p class="text-gray-800">{{ task.description || 'No description provided.' }}</p>
          </div>
        </div>

        <!-- Status -->
        <div class="flex items-center">
          <UIcon name="i-heroicons-information-circle" class="h-6 w-6 text-gray-500 mr-4" />
          <div>
            <p class="text-sm font-medium text-gray-500">Status</p>
            <UBadge :color="statusColor" variant="subtle" size="lg">{{ task.status }}</UBadge>
          </div>
        </div>

        <!-- Dates -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div class="flex items-center">
            <UIcon name="i-heroicons-calendar-days" class="h-6 w-6 text-gray-500 mr-4" />
            <div>
              <p class="text-sm font-medium text-gray-500">Start Date</p>
              <p class="text-lg font-semibold text-gray-800">{{ formatDate(task.start_date) }}</p>
            </div>
          </div>
          <div class="flex items-center">
            <UIcon name="i-heroicons-calendar" class="h-6 w-6 text-gray-500 mr-4" />
            <div>
              <p class="text-sm font-medium text-gray-500">End Date</p>
              <p class="text-lg font-semibold text-gray-800">{{ formatDate(task.end_date) }}</p>
            </div>
          </div>
        </div>

        <!-- Progress -->
        <div>
          <div class="flex items-center mb-2">
            <UIcon name="i-heroicons-chart-pie" class="h-6 w-6 text-gray-500 mr-4" />
            <div>
              <p class="text-sm font-medium text-gray-500">Progress</p>
              <p class="text-lg font-semibold text-gray-800">{{ task.progress }}%</p>
            </div>
          </div>
          <UProgress :value="task.progress" size="lg" />
        </div>
      </div>
    </UCard>
  </UModal>
</template>

<script setup lang="ts">
import type { Task } from '~/types/plan';
import { computed } from 'vue';

const props = defineProps<{
  modelValue: boolean;
  task: Task;
}>();

const emit = defineEmits(['update:modelValue']);

const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const statusColor = computed(() => {
  switch (props.task.status?.toLowerCase()) {
    case 'completed':
      return 'green';
    case 'in progress':
      return 'blue';
    case 'not started':
      return 'gray';
    default:
      return 'black';
  }
});

function formatDate(dateString: string) {
  if (!dateString) return 'N/A';
  const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
}
</script>
