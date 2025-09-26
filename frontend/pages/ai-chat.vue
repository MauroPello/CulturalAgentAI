<script setup lang="ts">
import { ref } from "vue";
import type { Message } from "~/types/chat";

const isSidebarCollapsed = ref(false);
const newMessage = ref("");
const messages = ref<Message[]>([]);

const previousChats = ref([
  {
    id: 1,
    title: "Asian Market Strategy",
    messages: [
      {
        id: 1,
        text: "Hello! I am an AI expert in international business and consulting. How can I help you today?",
        isUser: false,
      },
      {
        id: 2,
        text: "I want to know more about expanding my business into the Asian market.",
        isUser: true,
      },
      {
        id: 3,
        text: "That's a great goal! The Asian market is diverse and offers many opportunities. To give you the best advice, could you tell me a bit more about your business and which countries you are considering?",
        isUser: false,
      },
    ],
  },
]);

let chatCounter = 2;

function createNewChat() {
  const newChat = {
    id: chatCounter++,
    title: `New Chat ${chatCounter}`,
    messages: [],
  };
  previousChats.value.push(newChat);
  messages.value = newChat.messages;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function loadChat(chat: any) {
  messages.value = chat.messages;
}

function deleteChat(chatId: number) {
  const chatIndex = previousChats.value.findIndex((chat) => chat.id === chatId);
  if (chatIndex === -1) return;

  // If the deleted chat is currently active, clear the messages
  if (messages.value === previousChats.value[chatIndex]?.messages) {
    messages.value = [];
  }

  previousChats.value.splice(chatIndex, 1);
}

function sendMessage() {
  if (newMessage.value.trim() === "") return;

  messages.value.push({
    id: messages.value.length + 1,
    text: newMessage.value,
    isUser: true,
  });

  setTimeout(() => {
    messages.value.push({
      id: messages.value.length + 1,
      text: "Excellent question. I'll analyze the key market entry strategies for that region.",
      isUser: false,
    });
  }, 1000);

  newMessage.value = "";
}
</script>

<template>
  <div class="flex h-full flex-col items-center justify-center">
    <!-- Outer container -->
    <UCard
      class="p-1 h-full min-h-[40rem] w-full max-w-7xl"
      :ui="{
        body: { padding: 'p-0 sm:p-0' },
        divide: 'divide-y-0',
        ring: 'ring-0',
      }"
    >
      <div class="flex h-full w-full">
        <aside
          class="relative border-r border-gray-200 bg-gray-50 p-4 transition-all duration-300"
          :class="isSidebarCollapsed ? 'w-16' : 'w-1/3 min-w-[250px]'"
        >
          <div
            class="flex items-center mb-4"
            :class="
              isSidebarCollapsed ? 'justify-center' : 'justify-between'
            "
          >
            <h2
              v-if="!isSidebarCollapsed"
              class="mb-0 text-lg font-semibold"
            >
              Previous Chats
            </h2>
            <UButton
              :icon="
                isSidebarCollapsed
                  ? 'i-heroicons-chevron-double-right'
                  : 'i-heroicons-chevron-double-left'
              "
              variant="ghost"
              @click="isSidebarCollapsed = !isSidebarCollapsed"
            />
          </div>

          <div v-if="!isSidebarCollapsed">
            <!-- New Chat Button -->
            <UButton
              label="New Chat"
              icon="i-heroicons-plus"
              block
              class="text-base mb-4"
              size="lg"
              @click="createNewChat"
            />

            <!-- Chat List -->
            <ul class="space-y-2">
              <li
                v-for="chat in previousChats"
                :key="chat.id"
                class="group flex cursor-pointer items-center justify-between rounded-md p-2 hover:bg-gray-200"
                @click="loadChat(chat)"
              >
                <span class="flex-1 truncate">{{ chat.title }}</span>
                <UButton
                  icon="i-heroicons-trash"
                  color="red"
                  variant="ghost"
                  class="invisible group-hover:visible"
                  @click.stop="deleteChat(chat.id)"
                />
              </li>
            </ul>
          </div>
        </aside>

        <!-- 💬 Chat area -->
        <div
          class="flex flex-col transition-all duration-300"
          :class="isSidebarCollapsed ? 'w-full' : 'w-2/3'"
        >
          <!-- Messages -->
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

          <!-- Input bar -->
          <div class="flex items-center gap-2 border-t p-4">
            <UInput
              v-model="newMessage"
              placeholder="Type your message..."
              class="flex-1"
              @keyup.enter="sendMessage"
            />
            <UButton
              label="Send"
              icon="i-heroicons-paper-airplane"
              @click="sendMessage"
            />
          </div>
        </div>
      </div>
    </UCard>
  </div>
</template>
