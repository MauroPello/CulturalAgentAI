<script setup lang="ts">
import { ref } from 'vue'
import type { Message } from '~/types/chat'

const newMessage = ref('')
const messages = ref<Message[]>([])

const previousChats = ref([
  {
    id: 1,
    title: 'Asian Market Strategy',
    messages: [
      { id: 1, text: 'Hello! I am an AI expert in international business and consulting. How can I help you today?', isUser: false },
      { id: 2, text: 'I want to know more about expanding my business into the Asian market.', isUser: true },
      { id: 3, text: 'That\'s a great goal! The Asian market is diverse and offers many opportunities. To give you the best advice, could you tell me a bit more about your business and which countries you are considering?', isUser: false },
    ],
  },
])

let chatCounter = 2

function createNewChat() {
  const newChat = {
    id: chatCounter++,
    title: `New Chat ${chatCounter}`,
    messages: [],
  }
  previousChats.value.push(newChat)
  messages.value = newChat.messages
}

function loadChat(chat) {
  messages.value = chat.messages
}

function sendMessage() {
  if (newMessage.value.trim() === '') return

  messages.value.push({
    id: messages.value.length + 1,
    text: newMessage.value,
    isUser: true,
  })

  setTimeout(() => {
    messages.value.push({
      id: messages.value.length + 1,
      text: 'Excellent question. I\'ll analyze the key market entry strategies for that region.',
      isUser: false,
    })
  }, 1000)

  newMessage.value = ''
}
</script>

<template>
  <div class="flex h-screen items-center justify-center bg-gray-50 p-4">
    <!-- Outer container -->
    <UCard class="h-full w-full max-w-6xl rounded-lg overflow-hidden">
      <div class="flex h-full w-full">


        <aside class="w-1/3 bg-gray-100 border-r p-4 overflow-y-auto">
  <h2 class="text-lg font-semibold mb-4">Previous Chats</h2>

  <!-- New Chat Button -->
  <button
    @click="createNewChat"
    class="mb-4 w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
  >
    + New Chat
  </button>

  <!-- Chat List -->
  <ul class="space-y-2">
    <li
      v-for="chat in previousChats"
      :key="chat.id"
      @click="loadChat(chat)"
      class="cursor-pointer p-2 rounded hover:bg-gray-200"
    >
      {{ chat.title }}
    </li>
  </ul>
</aside>


        <!-- 💬 Chat area (2/3) -->
        <div class="w-2/3 flex flex-col">
          <UCard class="flex flex-col h-full rounded-none shadow-none">

            <!-- Messages -->
            <div class="flex-1 overflow-y-auto p-4 space-y-4">
              <div
                v-for="message in messages"
                :key="message.id"
                class="flex w-full"
                :class="message.isUser ? 'justify-end' : 'justify-start'"
              >
                <div
                  class="p-3 rounded-lg max-w-xs break-words"
                  :class="message.isUser ? 'bg-blue-600 text-white' : 'bg-gray-200 text-black'"
                >
                  {{ message.text }}
                </div>
              </div>
            </div>

            <!-- Input bar -->
            <div class="border-t p-4 flex gap-2">
            <input
              v-model="newMessage"
              type="text"
              placeholder="Type your message..."
              class="flex-1 p-3 border rounded-lg focus:outline-none"
            />
            <button
              @click="sendMessage"
              class="p-3 bg-blue-600 text-white rounded-lg w-32"
            >
              Send
            </button>
          </div>


          </UCard>
        </div>
      </div>
    </UCard>
  </div>
</template>
