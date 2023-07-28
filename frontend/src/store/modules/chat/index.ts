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
    selectGroupChat( 
      conversation_id : string | boolean , 
      group_name : string | undefined ,
      group_id : string | undefined
    ){
      this.conversation_id = conversation_id
      this.is_group = true
      this.group_name = group_name 
      this.group_id = group_id
    },
    setSelectChat(userTo: string , conversation_id : string | boolean) : void {
      this.user_to = userTo
      this.conversation_id = conversation_id
      this.is_group = false
      this.group_id = undefined
    },
    setIsOnline(isOnline : boolean) : void {
      this.is_online = isOnline
    },
    fetchChats() : void {
      getConversation( this.conversation_id ).then( (res) : any => {
        this.list_chat = res.chats
      })
    },
    uploadDataChat(userTo : string , chats : any , conversation_id : string | boolean ) {
      this.user_to = userTo
      this.conversation_id = conversation_id
      this.list_chat = chats
    }
  },
})

export function useChatStoreWithout() {
  return useChatStore(store)
}
