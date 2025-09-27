<script setup lang="ts">
import type { Message, ChatCompletionResponse } from "~/types/chat";
import MarkdownIt from "markdown-it";

// Type for the make_plan API response
interface MakePlanResponse {
  success: boolean;
  gantt_plan?: {
    project_name: string;
    project_description: string;
    [key: string]: any;
  };
  error?: string;
  processing_time_seconds?: number;
  timestamp?: string;
}

const md = new MarkdownIt();

const messages = ref<Message[]>([
  {
    content: "Hello! I am an AI expert in foreign market expansion. How can I help you today?",
    role: "assistant",
  }
]);

const newMessage = ref("");
const isModalOpen = ref(false);
const isLoading = ref(false);

const { createPlan } = usePlans();

async function sendMessage() {
  if (newMessage.value.trim() === "") return;

  const userMessage = newMessage.value;
  
  // Add user message to chat
  messages.value.push({
    content: userMessage,
    role: "user",
  });

  newMessage.value = "";
  isLoading.value = true;

  try {
    // Call the chat completion API
    const response = await $fetch<ChatCompletionResponse>('/chat-completion', {
      method: 'POST',
      baseURL: 'http://localhost:8000',
      body: {
        messages: messages.value.map(msg => ({
          role: msg.role,
          content: msg.content
        })),
        temperature: 0.1,
        max_tokens: 1000
      }
    });

    // Add AI response to chat
    if (response.choices && response.choices[0] && response.choices[0].message) {
      messages.value.push({
        content: response.choices[0].message.content,
        role: "assistant",
      });
    }
  } catch (error) {
    console.error('Error calling chat completion:', error);
    // Add error message to chat
    messages.value.push({
      content: "Sorry, I encountered an error. Please try again.",
      role: "assistant",
    });
  } finally {
    isLoading.value = false;
  }
}

async function confirmBuildPlan() {
  isLoading.value = true;
  
  try {
    // Call the make_plan endpoint with the current chat history
    const response = await $fetch<MakePlanResponse>('/make_plan', {
      method: 'POST',
      baseURL: 'http://localhost:8000',
      body: {
        messages: messages.value.map(msg => ({
          role: msg.role,
          content: msg.content
        })),
        project_name: "New Market Expansion Plan"
      }
    });

    console.log('Make Plan Response:', response);
    if (response.success && response.gantt_plan) {
      console.log(response.gantt_plan);
      // Create a plan using the generated Gantt data
      const newPlan = createPlan(
        response.gantt_plan.project_name || "New Market Expansion Plan",
        response.gantt_plan.project_description || "A plan generated from chat conversation"
      );
      
      // Update the plan with the Gantt data
      Object.assign(newPlan, response.gantt_plan);
      
      // Close modal and navigate to the new plan
      isModalOpen.value = false;
      navigateTo(`/plans/${newPlan.id}`);
    } else {
      console.error('Failed to generate plan:', response.error);
      // You might want to show an error message to the user here
    }
  } catch (error) {
    console.error('Error calling make_plan endpoint:', error);
    // You might want to show an error message to the user here
  } finally {
    isLoading.value = false;
  }
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
              v-for="(message, index) in messages"
              :key="index"
              class="flex w-full"
              :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
            >
              <div
                class="prose max-w-xs break-words rounded-lg p-3"
                :class="{
                  'bg-primary-500 text-white prose-invert': message.role === 'user',
                  'bg-gray-200 text-gray-900': message.role === 'assistant',
                }"
                v-html="md.render(message.content)"
              />
            </div>
            <!-- Loading indicator -->
            <div v-if="isLoading" class="flex w-full justify-start">
              <div class="max-w-xs break-words rounded-lg p-3 bg-gray-200 text-gray-900">
                <div class="flex space-x-1">
                  <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                  <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                  <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                </div>
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
                :disabled="isLoading"
                @keyup.enter="sendMessage"
              />
              <UButton
                size="xl"
                :label="isLoading ? 'Processing...' : 'Send'"
                variant="soft"
                :icon="isLoading ? 'i-heroicons-arrow-path' : 'i-heroicons-paper-airplane'"
                class="ml-2"
                :loading="isLoading"
                :disabled="isLoading"
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

          <div v-if="isLoading" class="flex items-center space-x-3">
            <UIcon name="i-heroicons-arrow-path" class="animate-spin text-primary-500" />
            <p>Generating your personalized plan from the chat conversation...</p>
          </div>
          <p v-else>Are you sure you want to create a new plan based on your conversation?</p>

          <template #footer v-if="!isLoading">
            <div class="flex justify-end gap-2">
              <UButton color="gray" variant="ghost" size="xl" @click="isModalOpen = false"
                >Cancel</UButton
              >
              <UButton size="xl" @click="confirmBuildPlan">Create Plan</UButton>
            </div>
          </template>
        </UCard>
      </UModal>
    </main>
  </div>
</template>
