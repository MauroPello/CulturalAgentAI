<script setup lang="ts">
import type { Message } from '~/types/chat'

const messages = ref<Message[]>([
  { id: 1, text: 'Hello! How can I help you today?', isUser: false },
  { id: 2, text: 'I want to know more about the cultural impact of AI.', isUser: true },
  { id: 3, text: 'That\'s a great question! The cultural impact of AI is vast and multifaceted. It affects everything from art and music to language and social norms. Do you have a specific area of interest?', isUser: false },
])

const newMessage = ref('')

function sendMessage() {
  if (newMessage.value.trim() === '') return

  messages.value.push({
    id: messages.value.length + 1,
    text: newMessage.value,
    isUser: true,
  })

  // Simulate a response from the LLM
  setTimeout(() => {
    messages.value.push({
      id: messages.value.length + 1,
      text: 'That\'s an interesting point. Let me think about that for a moment...',
      isUser: false,
    })
  }, 1000)

  newMessage.value = ''
}
</script>

<template>
  <div class="flex flex-col h-screen">
    <AppHeader />
    <main class="flex-1 overflow-y-auto p-4">
      <UCard class="h-full">
        <div class="flex flex-col h-full">
          <div class="flex-1 space-y-4 overflow-y-auto">
            <div
              v-for="message in messages"
              :key="message.id"
              class="flex"
              :class="{ 'justify-end': message.isUser }"
            >
              <div
                class="p-2 rounded-lg max-w-xs"
                :class="{
                  'bg-primary text-white': message.isUser,
                  'bg-gray-200 dark:bg-gray-700': !message.isUser,
                }"
              >
                {{ message.text }}
              </div>
            </div>
          </div>
          <div class="mt-4 flex items-center">
            <UInput
              v-model="newMessage"
              class="flex-1"
              placeholder="Type a message..."
              @keyup.enter="sendMessage"
            />
            <UButton class="ml-2" @click="sendMessage">
              Send
            </UButton>
          </div>
        </div>
      </UCard>
    </main>
  </div>
</template>
