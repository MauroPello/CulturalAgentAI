<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import type { Message } from "~/types/chat";

interface Chat {
  id: number;
  title: string;
  messages: Message[];
}

const route = useRoute();
const router = useRouter();

const isSidebarCollapsed = ref(false);
const newMessage = ref("");
const activeChat = ref<Chat | null>(null);
const previousChats = ref<Chat[]>([]);

// Simulate fetching all chat sessions
async function fetchPreviousChats() {
  console.log("Fetching previous chats...");
  return new Promise<Chat[]>((resolve) => {
    setTimeout(() => {
      resolve([
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
        {
          id: 2,
          title: "European Expansion",
          messages: [
            {
              id: 1,
              text: "Let's discuss European expansion.",
              isUser: true,
            },
          ],
        },
      ]);
    }, 500);
  });
}

// Simulate fetching a single chat
async function fetchChat(id: number) {
  console.log(`Fetching chat ${id}...`);
  const chats = await fetchPreviousChats();
  return chats.find((chat) => chat.id === id) || null;
}

async function createNewChat() {
  // In a real app, this would be a POST request to the backend
  const newId = Math.max(...previousChats.value.map((c) => c.id)) + 1;
  const newChat: Chat = {
    id: newId,
    title: `New Chat ${newId}`,
    messages: [],
  };
  previousChats.value.push(newChat);
  router.push(`/ai-chat/${newChat.id}`);
}

function loadChat(chat: Chat) {
  router.push(`/ai-chat/${chat.id}`);
}

async function deleteChat(chatId: number) {
  // In a real app, this would be a DELETE request
  const chatIndex = previousChats.value.findIndex((chat) => chat.id === chatId);
  if (chatIndex === -1) return;

  previousChats.value.splice(chatIndex, 1);

  // If the deleted chat was the active one, navigate to another chat
  if (activeChat.value?.id === chatId) {
    const nextChat = previousChats.value[0];
    if (nextChat) {
      router.push(`/ai-chat/${nextChat.id}`);
    } else {
      router.push("/ai-chat"); // Or a dedicated 'no chats' page
    }
  }
}

async function sendMessage() {
  if (newMessage.value.trim() === "" || !activeChat.value) return;

  const messageText = newMessage.value;
  newMessage.value = "";

  // Optimistic update
  activeChat.value.messages.push({
    id: Date.now(), // Temporary ID
    text: messageText,
    isUser: true,
  });

  // Simulate backend call
  await new Promise((resolve) => setTimeout(resolve, 1000));

  if (activeChat.value) {
    activeChat.value.messages.push({
      id: Date.now() + 1,
      text: "Excellent question. I'll analyze the key market entry strategies for that region.",
      isUser: false,
    });
  }
}

// Fetch chats when component mounts
onMounted(async () => {
  previousChats.value = await fetchPreviousChats();
  const chatId = Number(route.params.id);
  if (chatId) {
    activeChat.value = await fetchChat(chatId);
  }
});

// Watch for route changes to load new chat data
watch(
  () => route.params.id,
  async (newId) => {
    if (newId) {
      activeChat.value = await fetchChat(Number(newId));
    }
  },
);
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
                :class="{ 'bg-gray-200': activeChat?.id === chat.id }"
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
          v-if="activeChat"
          class="flex flex-col transition-all duration-300"
          :class="isSidebarCollapsed ? 'w-full' : 'w-2/3'"
        >
          <!-- Messages -->
          <div class="flex-1 space-y-4 overflow-y-auto p-4">
            <div
              v-for="message in activeChat.messages"
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
        <div v-else class="flex-1 flex items-center justify-center">
          <p>Select a chat or create a new one to start.</p>
        </div>
      </div>
    </UCard>
  </div>
</template>
