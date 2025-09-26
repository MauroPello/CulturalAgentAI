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
          <div class="flex items-center gap-2 border-t p-4">
            <UInput
              v-model="newMessage"
              class="flex-1"
              placeholder="Type a message..."
              @keyup.enter="sendMessage"
            />
            <UButton
              label="Send"
              icon="i-heroicons-paper-airplane"
              class="ml-2"
              @click="sendMessage"
            />
          </div>
        </div>
      </UCard>
    </main>
  </div>
</template>
