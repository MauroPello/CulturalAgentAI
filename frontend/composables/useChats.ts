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
      else {
        const sampleChats: Chat[] = [
          {
            id: 1,
            title: 'Meeting Reschedule',
            messages: [
              { id: 1, text: 'Hi team, I need to reschedule our meeting.', isUser: true },
              { id: 2, text: 'No problem, what time works for you?', isUser: false },
            ],
          },
          {
            id: 2,
            title: 'Document Request',
            messages: [
              { id: 1, text: 'Can you send me the project proposal?', isUser: true },
              { id: 2, text: 'Sure, I will send it right away.', isUser: false },
            ],
          },
          {
            id: 3,
            title: 'Project Question',
            messages: [
              { id: 1, text: 'I have a question about the budget.', isUser: true },
              { id: 2, text: 'I can help with that, what is your question?', isUser: false },
            ],
          },
        ]
        chats.value = sampleChats
        _saveChats()
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
          id: 1,
          text: 'Hello! I am an AI expert in international business and consulting. How can I help you today?',
          isUser: false,
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
