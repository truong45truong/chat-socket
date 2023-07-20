import { defineStore } from 'pinia'
import { type ChatState , getChatState } from './helper'
import { store } from '@/store'
import { getConversation } from '@/api'

export interface ChatResponse {
  chats : Array<any>
}
export const useChatStore = defineStore('chat-store', {
  state: (): ChatState => getChatState(),

  getters: {
    chatSelect(state): string | undefined {
      return state.user_to
    },
    isOnline(state) : boolean | undefined {
      return state.is_online
    }
  },

  actions: {
    setSelectChat(userTo: string , conversation_id : string | undefined) : void {
      this.user_to = userTo
      this.conversation_id = conversation_id
    },
    setIsOnline(isOnline : boolean) : void {
      this.is_online = isOnline
    },
    fetchChats() : void {
      getConversation(this.conversation_id).then( (res) : any => {
        this.list_chat = res.chats
      })
    },
  },
})

export function useChatStoreWithout() {
  return useChatStore(store)
}
