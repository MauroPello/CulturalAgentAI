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
              <h2 class="text-xl font-semibold">
                {{ card.title }}
              </h2>
              <UIcon name="i-heroicons-arrow-right-20-solid" class="w-5 h-5 text-gray-400 dark:text-gray-500" />
            </div>
          </template>

          <p class="text-gray-600 dark:text-gray-300">
            {{ card.description }}
          </p>
        </UCard>
      </NuxtLink>
    </div>
  </UContainer>
</template>

<script setup lang="ts">
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
]
</script>

