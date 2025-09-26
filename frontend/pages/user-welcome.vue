<template>
  <UContainer>
    <div class="py-10">
      <h1 class="text-3xl font-bold text-center">
        Welcome back!
      </h1>
      <p class="text-lg text-center text-gray-500 mt-2">
        What would you like to do today?
      </p>
    </div>

    <div class="space-y-12">

      <!-- Latest Plans -->
      <div>
        <div class="flex items-center gap-x-2 mb-4">
          <UIcon name="i-heroicons-document-text-20-solid" class="w-6 h-6 text-blue-500" />
          <h2 class="text-2xl font-semibold">
            Latest Plans
          </h2>
        </div>
        <UCard>
          <div class="space-y-2 max-h-64 overflow-y-auto">
            <NuxtLink
              v-for="plan in latestPlans"
              :key="plan.id"
              :to="`/plans/${plan.id}`"
              class="flex items-center gap-x-3 p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800"
            >
              <UIcon name="i-heroicons-document-20-solid" class="w-5 h-5 text-gray-400" />
              <div class="flex-1">
                <h3 class="font-semibold">
                  {{ plan.project_name }}
                </h3>
                <p class="text-sm text-gray-500 line-clamp-1">
                  {{ plan.project_description }}
                </p>
              </div>
            </NuxtLink>
          </div>
        </UCard>
      </div>

      <!-- Quick Actions -->
      <div>
        <div class="flex items-center gap-x-2 mb-4">
          <UIcon name="i-heroicons-bolt-20-solid" class="w-6 h-6 text-yellow-500" />
          <h2 class="text-2xl font-semibold">
            Quick Actions
          </h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <NuxtLink
            v-for="card in cards"
            :key="card.to"
            :to="card.to"
            class="block"
          >
            <UCard
              class="h-full cursor-pointer transition-all duration-200 transform hover:scale-105 hover:ring-2 hover:ring-primary-500 dark:hover:ring-primary-400"
            >
              <template #header>
                <div class="flex justify-between items-center">
                  <h3 class="text-xl font-semibold">
                    {{ card.title }}
                  </h3>
                  <UIcon name="i-heroicons-arrow-right-20-solid" class="w-5 h-5 text-gray-400 dark:text-gray-500" />
                </div>
              </template>
              <p class="text-gray-600 dark:text-gray-300">
                {{ card.description }}
              </p>
            </UCard>
          </NuxtLink>
        </div>
      </div>

      <!-- Latest Chats -->
      <div>
        <div class="flex items-center gap-x-2 mb-4">
          <UIcon name="i-heroicons-chat-bubble-left-right-20-solid" class="w-6 h-6 text-green-500" />
          <h2 class="text-2xl font-semibold">
            Latest Chats
          </h2>
        </div>
        <UCard>
          <div class="space-y-2 max-h-64 overflow-y-auto">
            <div v-for="chat in latestChats" :key="chat.id" class="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-x-3">
                  <UIcon name="i-heroicons-chat-bubble-left-20-solid" class="w-5 h-5 text-gray-400" />
                  <p class="font-semibold">
                    {{ chat.title }}
                  </p>
                </div>
                <NuxtLink to="/chat-review" class="text-primary-500 hover:underline text-sm">
                  Continue to Chat
                </NuxtLink>
              </div>
            </div>
          </div>
        </UCard>
      </div>

      <!-- Latest Documents -->
      <div>
        <div class="flex items-center gap-x-2 mb-4">
          <UIcon name="i-heroicons-folder-20-solid" class="w-6 h-6 text-purple-500" />
          <h2 class="text-2xl font-semibold">
            Latest Documents
          </h2>
        </div>
        <UCard>
          <div class="space-y-2 max-h-64 overflow-y-auto">
            <div v-for="doc in latestDocuments" :key="doc.id" class="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-x-3">
                  <UIcon name="i-heroicons-document-20-solid" class="w-5 h-5 text-gray-400" />
                  <p class="font-semibold">
                    {{ doc.name }}
                  </p>
                </div>
                <NuxtLink :to="doc.url" target="_blank" class="text-primary-500 hover:underline text-sm">
                  View
                </NuxtLink>
              </div>
            </div>
          </div>
        </UCard>
      </div>
    </div>
  </UContainer>
</template>

<script setup lang="ts">
import { usePlans } from '~/composables/usePlans';

const { plans } = usePlans();
const latestPlans = computed(() => plans.value.slice(0, 3));

const cards = [
  {
    title: 'My Plans',
    description: 'View and manage your existing cultural integration plans.',
    to: '/my-plans',
  },
  {
    title: 'Create a New Plan',
    description: 'Start a new cultural integration plan from scratch.',
    to: '/new-plan',
  },
  {
    title: 'Review Chats',
    description: 'Review chats and flag messages that may not be appropriate for the language it\'s being spoken in.',
    to: '/chat-review',
  },
  {
    title: 'AI Chat',
    description: 'Interact with the AI to get insights and suggestions.',
    to: '/ai-chat',
  },
  {
    title: 'Library',
    description: 'Browse the library of cultural resources and information.',
    to: '/library',
  },
  {
    title: 'Upload Document',
    description: 'Upload documents to the library.',
    to: '/library',
  },
]

const latestChats = [
  { id: 1, title: 'Meeting Reschedule' },
  { id: 2, title: 'Document Request' },
  { id: 3, title: 'Project Question' },
]
const latestDocuments = [
  { id: 1, name: 'Project Proposal.pdf', url: '#' },
  { id: 2, name: 'Meeting Notes.docx', url: '#' },
  { id: 3, name: 'Budget Spreadsheet.xlsx', url: '#' },
]
</script>

