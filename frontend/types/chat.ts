export interface Message {
  id: number
  text: string
  isUser: boolean
}

export interface Chat {
  id: number
  title: string
  messages: Message[]
}
