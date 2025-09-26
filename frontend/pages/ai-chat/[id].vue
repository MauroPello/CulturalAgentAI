<script setup lang="ts">
import { ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import type { Message, Chat } from "~/types/chat";
import { useChats } from "~/composables/useChats";

const route = useRoute();
const router = useRouter();

const {
  chats,
  createNewChat: createChatInComposable,
  deleteChat: deleteChatInComposable,
} = useChats();

const isSidebarCollapsed = ref(false);
const newMessage = ref("");
const isLoading = ref(false);
const editingChatId = ref<number | null>(null);
const editingTitle = ref("");

const activeChat = computed(() => {
  const chatId = Number(route.params.id);
  return chats.value.find((chat) => chat.id === chatId) || null;
});

const previousChats = computed(() => chats.value);

async function createNewChat() {
  const newChat = createChatInComposable();
  router.push(`/ai-chat/${newChat.id}`);
}

function loadChat(chat: Chat) {
  router.push(`/ai-chat/${chat.id}`);
}

async function deleteChat(chatId: number) {
  deleteChatInComposable(chatId);

  if (activeChat.value?.id === chatId) {
    const nextChat = previousChats.value[0];
    if (nextChat) {
      router.push(`/ai-chat/${nextChat.id}`);
    } else {
      router.push("/ai-chat");
    }
  }
}

async function sendMessage() {
  if (newMessage.value.trim() === "" || !activeChat.value || isLoading.value)
    return;

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

  try {
    // Call the ask endpoint with conversation context
    const conversationHistory = activeChat.value.messages
      .filter((msg) => msg.id !== userMessage.id) // Exclude current message
      .map((msg) => `${msg.isUser ? "Human" : "AI"}: ${msg.text}`)
      .join("\n");

    const queryWithContext = conversationHistory
      ? `Previous conversation:\n${conversationHistory}\n\nnCurrent question: ${messageText}`
      : messageText;

    const response = await $fetch<{ answer: string }>("http://127.0.0.1:8000/ask", {
      method: "POST",
      body: {
        query: queryWithContext,
      },
    });

    // Add AI response
    if (activeChat.value) {
      activeChat.value.messages.push({
        id: Date.now() + 1,
        text: response.answer,
        isUser: false,
      });

      // Update chat title based on first user message if it's still the default
      if (
        activeChat.value.title.startsWith("New Chat") &&
        activeChat.value.messages.length >= 3
      ) {
        // Generate a title from the first user message (truncated)
        const firstUserMessage = activeChat.value.messages.find(
          (msg) => msg.isUser
        );
        if (firstUserMessage) {
          activeChat.value.title = `${firstUserMessage.text.slice(0, 30)}...`;
        }
      }
    }
  } catch (error) {
    console.error("Error calling AI:", error);
    // Add error message
    if (activeChat.value) {
      activeChat.value.messages.push({
        id: Date.now() + 1,
        text: "Sorry, I encountered an error. Please try again.",
        isUser: false,
      });
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

  const chat = chats.value.find((c) => c.id === chatId);
  if (chat) chat.title = editingTitle.value.trim();

  editingChatId.value = null;
  editingTitle.value = "";
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
            :class="isSidebarCollapsed ? 'justify-center' : 'justify-between'"
          >
            <h2 v-if="!isSidebarCollapsed" class="mb-0 text-lg font-semibold">
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
                    autofocus
                    @keyup.enter="saveEditedTitle(chat.id)"
                    @keyup.escape="cancelEditingTitle"
                    @blur="saveEditedTitle(chat.id)"
                  />
                </div>
                <span v-else class="flex-1 truncate" @click="loadChat(chat)">
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
                  <div
                    class="w-2 h-2 bg-gray-500 rounded-full animate-bounce"
                  />
                  <div
                    class="w-2 h-2 bg-gray-500 rounded-full animate-bounce"
                    style="animation-delay: 0.1s"
                  />
                  <div
                    class="w-2 h-2 bg-gray-500 rounded-full animate-bounce"
                    style="animation-delay: 0.2s"
                  />
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
