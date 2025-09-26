<script setup lang="ts">
import type { Message } from "~/types/chat";

const messages = ref<Message[]>([
  {
    id: 1,
    text: "Hello! I am an AI expert in foreign market expansion. How can I help you today?",
    isUser: false,
  },
  {
    id: 2,
    text: "I want to create a plan to expand my business into a new country.",
    isUser: true,
  },
  {
    id: 3,
    text: "Excellent! To create a successful expansion plan, we need to consider several factors. Which country are you considering for expansion?",
    isUser: false,
  },
]);

const newMessage = ref("");
const isModalOpen = ref(false);

const { createPlan } = usePlans();

function sendMessage() {
  if (newMessage.value.trim() === "") return;

  messages.value.push({
    id: messages.value.length + 1,
    text: newMessage.value,
    isUser: true,
  });

  // Simulate a response from the LLM
  setTimeout(() => {
    messages.value.push({
      id: messages.value.length + 1,
      text: "That's a great choice. Let's start by analyzing the market size and growth potential in that country.",
      isUser: false,
    });
  }, 1000);

  newMessage.value = "";
}

function confirmBuildPlan() {
  const newPlan = createPlan(
    "New Market Expansion Plan",
    "A plan to expand the business into a new country."
  );
  navigateTo(`/plans/${newPlan.id}`);
}
</script>

<template>
  <div class="flex flex-col h-screen">
    <AppHeader />
    <main
      class="flex-1 overflow-y-auto p-4 flex flex-col items-center justify-center"
    >
      <div class="text-center mb-4">
        <h1 class="text-2xl font-bold">Define a Market Expansion Plan</h1>
        <p class="text-gray-500 dark:text-gray-400">
          Chat with our AI expert to create a plan for entering a new foreign
          market.
        </p>
      </div>
      <UCard
        class="p-1 h-full min-h-[40rem] w-full max-w-7xl"
        :ui="{
          body: { padding: 'p-0 sm:p-0' },
          divide: 'divide-y-0',
          ring: 'ring-0',
        }"
      >
        <div class="flex flex-col h-full">
          <div class="flex-1 space-y-4 overflow-y-auto p-4">
            <div
              v-for="message in messages"
              :key="message.id"
              class="flex w-full"
              :class="message.isUser ? 'justify-end' : 'justify-start'"
            >
              <div
                class="max-w-xs break-words rounded-lg p-3"
                :class="{
                  'bg-primary-500 text-white': message.isUser,
                  'bg-gray-200 text-gray-900': !message.isUser,
                }"
              >
                {{ message.text }}
              </div>
            </div>
          </div>
          <div class="flex w-full flex-col gap-3 justify-center items-center border-t p-4">
            <div class="flex w-full items-center gap-2">
              <UInput
                v-model="newMessage"
                size="xl"
                class="flex-1 text-base"
                placeholder="Type a message..."
                @keyup.enter="sendMessage"
              />
              <UButton
                size="xl"
                label="Send"
                variant="soft"
                icon="i-heroicons-paper-airplane"
                class="ml-2"
                @click="sendMessage"
              />
              <UButton
                size="xl"
                color="primary"
                variant="solid"
                label="Build Plan"
                icon="i-heroicons-document-plus"
                :trailing="false"
                @click="isModalOpen = true"
              />
            </div>
            <div class="flex w-full flex-row gap-2 items-center justify-center">
              <p>Are you satisfied with the Plan?</p>
              <UButton
                size="xl"
                color="primary"
                :padded="false"
                variant="link"
                class="font-bold"
                label="Build It!"
                @click="isModalOpen = true"
              />
            </div>
          </div>
        </div>
      </UCard>
      <UModal v-model="isModalOpen">
        <UCard
          :ui="{
            ring: '',
            divide: 'divide-y divide-gray-100 dark:divide-gray-800',
          }"
        >
          <template #header>
            <div class="flex items-center justify-between">
              <h3
                class="text-base font-semibold leading-6 text-gray-900 dark:text-white"
              >
                Confirm Plan Creation
              </h3>
              <UButton
                color="gray"
                variant="ghost"
                icon="i-heroicons-x-mark-20-solid"
                class="-my-1"
                @click="isModalOpen = false"
              />
            </div>
          </template>

          <p>Are you sure you want to create a new plan?</p>

          <template #footer>
            <div class="flex justify-end gap-2">
              <UButton color="gray" variant="ghost" @click="isModalOpen = false"
                >Cancel</UButton
              >
              <UButton @click="confirmBuildPlan">Create Plan</UButton>
            </div>
          </template>
        </UCard>
      </UModal>
    </main>
  </div>
</template>
