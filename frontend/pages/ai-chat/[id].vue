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
const isLoading = ref(false);
const editingChatId = ref<number | null>(null);
const editingTitle = ref("");

// LocalStorage key for chats
const CHATS_STORAGE_KEY = 'ai-chats';

// Load chats from localStorage
function loadChatsFromStorage(): Chat[] {
  if (typeof window === 'undefined') return [];
  
  try {
    const stored = localStorage.getItem(CHATS_STORAGE_KEY);
    if (stored) {
      return JSON.parse(stored);
    }
  } catch (error) {
    console.error('Error loading chats from localStorage:', error);
  }
  
  // Return default chats if nothing in storage
  return [
    {
      id: 1,
      title: "Asian Market Strategy",
      messages: [
        {
          id: 1,
          text: "Hello! I am an AI expert in international business and consulting. How can I help you today?",
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
          text: "Hello! I am an AI expert in international business and consulting. How can I help you today?",
          isUser: false,
        },
      ],
    },
  ];
}

// Save chats to localStorage
function saveChatsToStorage(chats: Chat[]) {
  if (typeof window === 'undefined') return;
  
  try {
    localStorage.setItem(CHATS_STORAGE_KEY, JSON.stringify(chats));
  } catch (error) {
    console.error('Error saving chats to localStorage:', error);
  }
}

// Fetch all chat sessions (now from localStorage)
async function fetchPreviousChats() {
  console.log("Loading chats from localStorage...");
  return loadChatsFromStorage();
}

// Fetch a single chat (now from localStorage)
async function fetchChat(id: number) {
  console.log(`Loading chat ${id} from localStorage...`);
  // Find the chat in the already loaded previousChats array first
  const existingChat = previousChats.value.find((chat) => chat.id === id);
  if (existingChat) {
    return existingChat;
  }
  
  // If not found in memory, load from localStorage
  const chats = loadChatsFromStorage();
  return chats.find((chat) => chat.id === id) || null;
}

async function createNewChat() {
  // Calculate new ID safely, defaulting to 1 if no chats exist
  const newId = previousChats.value.length > 0 
    ? Math.max(...previousChats.value.map((c) => c.id)) + 1 
    : 1;
    
  const newChat: Chat = {
    id: newId,
    title: `New Chat ${newId}`,
    messages: [
      {
        id: 1,
        text: "Hello! I am an AI expert in international business and consulting. How can I help you today?",
        isUser: false,
      },
    ],
  };
  
  // Add to chat list and set as active
  previousChats.value.push(newChat);
  activeChat.value = newChat;
  
  // Save to localStorage
  saveChatsToStorage(previousChats.value);
  
  // Navigate to the new chat
  router.push(`/ai-chat/${newChat.id}`);
}

function loadChat(chat: Chat) {
  // Set the active chat directly from the previousChats array
  activeChat.value = previousChats.value.find(c => c.id === chat.id) || chat;
  router.push(`/ai-chat/${chat.id}`);
}

async function deleteChat(chatId: number) {
  // Find and remove chat
  const chatIndex = previousChats.value.findIndex((chat) => chat.id === chatId);
  if (chatIndex === -1) return;

  previousChats.value.splice(chatIndex, 1);
  
  // Save to localStorage
  saveChatsToStorage(previousChats.value);

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
  if (newMessage.value.trim() === "" || !activeChat.value || isLoading.value) return;

  const messageText = newMessage.value;
  newMessage.value = "";
  isLoading.value = true;

  // Add user message
  const userMessage: Message = {
    id: Date.now(),
    text: messageText,
    isUser: true,
  };
  activeChat.value.messages.push(userMessage);

  // Save updated chat to localStorage immediately
  saveChatsToStorage(previousChats.value);

  try {
    // Call the ask endpoint with conversation context
    const conversationHistory = activeChat.value.messages
      .filter(msg => msg.id !== userMessage.id) // Exclude current message
      .map(msg => `${msg.isUser ? 'Human' : 'AI'}: ${msg.text}`)
      .join('\n');
    
    const queryWithContext = conversationHistory 
      ? `Previous conversation:\n${conversationHistory}\n\nCurrent question: ${messageText}`
      : messageText;

    const response = await $fetch('http://127.0.0.1:8000/ask', {
      method: 'POST',
      body: {
        query: queryWithContext
      }
    });

    // Add AI response
    if (activeChat.value) {
      activeChat.value.messages.push({
        id: Date.now() + 1,
        text: response.answer,
        isUser: false,
      });
      
      // Update chat title based on first user message if it's still the default
      if (activeChat.value.title.startsWith('New Chat') && activeChat.value.messages.length >= 3) {
        // Generate a title from the first user message (truncated)
        const firstUserMessage = activeChat.value.messages.find(msg => msg.isUser);
        if (firstUserMessage) {
          activeChat.value.title = firstUserMessage.text.slice(0, 30) + 
            (firstUserMessage.text.length > 30 ? '...' : '');
        }
      }
      
      // Save updated chat to localStorage
      saveChatsToStorage(previousChats.value);
    }
  } catch (error) {
    console.error('Error calling AI:', error);
    // Add error message
    if (activeChat.value) {
      activeChat.value.messages.push({
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        isUser: false,
      });
      
      // Save even error messages to localStorage
      saveChatsToStorage(previousChats.value);
    }
  } finally {
    isLoading.value = false;
  }
}

function startEditingTitle(chat: Chat) {
  editingChatId.value = chat.id;
  editingTitle.value = chat.title;
}

function cancelEditingTitle() {
  editingChatId.value = null;
  editingTitle.value = "";
}

function saveEditedTitle(chatId: number) {
  if (!editingTitle.value.trim()) return;
  
  const chat = previousChats.value.find(c => c.id === chatId);
  if (chat) {
    chat.title = editingTitle.value.trim();
    saveChatsToStorage(previousChats.value);
  }
  
  editingChatId.value = null;
  editingTitle.value = "";
}

// Fetch chats when component mounts
onMounted(async () => {
  previousChats.value = await fetchPreviousChats();
  const chatId = Number(route.params.id);
  if (chatId) {
    // Find the chat in the loaded previousChats array
    const foundChat = previousChats.value.find(chat => chat.id === chatId);
    if (foundChat) {
      activeChat.value = foundChat;
    } else {
      activeChat.value = await fetchChat(chatId);
    }
  }
});

// Watch for route changes to load new chat data
watch(
  () => route.params.id,
  async (newId) => {
    if (newId) {
      const chatId = Number(newId);
      // Find the chat in the loaded previousChats array first
      const foundChat = previousChats.value.find(chat => chat.id === chatId);
      if (foundChat) {
        activeChat.value = foundChat;
      } else {
        activeChat.value = await fetchChat(chatId);
      }
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
              >
                <!-- Chat title - editable or clickable -->
                <div 
                  v-if="editingChatId === chat.id"
                  class="flex-1 flex items-center gap-2"
                  @click.stop
                >
                  <UInput
                    v-model="editingTitle"
                    class="flex-1 text-sm"
                    size="sm"
                    @keyup.enter="saveEditedTitle(chat.id)"
                    @keyup.escape="cancelEditingTitle"
                    @blur="saveEditedTitle(chat.id)"
                    autofocus
                  />
                </div>
                <span
                  v-else
                  class="flex-1 truncate"
                  @click="loadChat(chat)"
                >
                  {{ chat.title }}
                </span>
                
                <!-- Action buttons -->
                <div class="flex items-center gap-1">
                  <UButton
                    v-if="editingChatId !== chat.id"
                    icon="i-heroicons-pencil"
                    color="gray"
                    variant="ghost"
                    size="sm"
                    class="invisible group-hover:visible"
                    @click.stop="startEditingTitle(chat)"
                  />
                  <UButton
                    v-if="editingChatId === chat.id"
                    icon="i-heroicons-check"
                    color="green"
                    variant="ghost"
                    size="sm"
                    @click.stop="saveEditedTitle(chat.id)"
                  />
                  <UButton
                    v-if="editingChatId === chat.id"
                    icon="i-heroicons-x-mark"
                    color="red"
                    variant="ghost"
                    size="sm"
                    @click.stop="cancelEditingTitle"
                  />
                  <UButton
                    v-if="editingChatId !== chat.id"
                    icon="i-heroicons-trash"
                    color="red"
                    variant="ghost"
                    size="sm"
                    class="invisible group-hover:visible"
                    @click.stop="deleteChat(chat.id)"
                  />
                </div>
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
            
            <!-- Loading indicator -->
            <div v-if="isLoading" class="flex">
              <div class="p-3 rounded-lg max-w-xs bg-gray-200 text-gray-900">
                <div class="flex space-x-1">
                  <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                  <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                  <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Input bar -->
          <div class="flex items-center gap-2 border-t p-4">
            <UInput
              v-model="newMessage"
              placeholder="Type your message..."
              class="flex-1"
              :disabled="isLoading"
              @keyup.enter="sendMessage"
            />
            <UButton
              :label="isLoading ? 'Sending...' : 'Send'"
              icon="i-heroicons-paper-airplane"
              :disabled="isLoading || newMessage.trim() === ''"
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
