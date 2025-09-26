<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useChats } from '~/composables/useChats'

const router = useRouter()
const { chats, createNewChat } = useChats()

onMounted(() => {
  if (chats.value && chats.value.length > 0 && chats.value[0]) {
    router.push(`/ai-chat/${chats.value[0].id}`)
  }
  else {
    const newChat = createNewChat()
    router.push(`/ai-chat/${newChat.id}`)
  }
})
</script>

<template>
  <div class="flex h-full items-center justify-center">
    <p>Loading chats...</p>
  </div>
</template>
