import { ref, onMounted, watch } from 'vue'
import type { Chat } from '~/types/chat'

const chats = ref<Chat[]>([])
const storageKey = 'chats'

function _saveChats() {
  if (typeof window === 'undefined')
    return
  localStorage.setItem(storageKey, JSON.stringify(chats.value))
}

export function useChats() {
  onMounted(() => {
    if (typeof window !== 'undefined') {
      const storedChats = localStorage.getItem(storageKey)
      if (storedChats) {
        chats.value = JSON.parse(storedChats)
      }
    }
  })

  watch(chats, _saveChats, { deep: true })

  const getChatById = (id: number) => {
    return chats.value.find((chat: Chat) => chat.id === id)
  }

  const createNewChat = () => {
    const newId = chats.value.length > 0 ? Math.max(...chats.value.map(c => c.id)) + 1 : 1
    const newChat: Chat = {
      id: newId,
      title: `New Chat ${newId}`,
      messages: [
        {
          content: 'Hello! I am an AI expert in international business and consulting. How can I help you today?',
          role: "assistant",
        },
      ],
    }
    chats.value.push(newChat)
    return newChat
  }

  const deleteChat = (chatId: number) => {
    const index = chats.value.findIndex(c => c.id === chatId)
    if (index !== -1)
      chats.value.splice(index, 1)
  }

  return {
    chats,
    getChatById,
    createNewChat,
    deleteChat,
  }
}
