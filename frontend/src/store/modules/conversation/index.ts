import { defineStore } from 'pinia'
import { type ConversationState , type Conversation , getConversationState } from './helper'
import { store } from '@/store'
import { getAllConversation } from '@/api'

export interface ChatResponse {
  chats : Array<any>
}
export const useConversationStore = defineStore('conversation-store', {
  state: (): ConversationState => getConversationState(),

  getters: {
    getConversation(state): Array<Conversation> {
      return state.list_conversation
    },
  },

  actions: {
    fetchData() : void {
      getAllConversation().then( (res : any) => {
        this.list_conversation = res.conversation
      })
    },
    updateNewMessage(message_new : string , email_user_chat : string) : void {
      this.list_conversation = this.list_conversation.filter( ( conversation : any ) => {
        if (
          conversation.email_user_from  == email_user_chat
          || conversation.email_user_to == email_user_chat
        ) {
          conversation.content_last = message_new
        }
        return conversation
      })
    }, 
    getConversationFind( email_user_chat : string) : any{
      var conversationFind
      this.list_conversation.filter( ( conversation : any ) => {
        if (
          conversation.email_user_from  == email_user_chat
          || conversation.email_user_to == email_user_chat
        ) conversationFind = conversation
      })
      return conversationFind
    }

  },
})

