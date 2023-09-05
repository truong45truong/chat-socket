import { defineStore } from 'pinia'
import { type ConversationState, type Conversation, getConversationState } from './helper'
import { getAllConversation } from '@/api'


export const useConversationStore = defineStore('conversation-store', {
  state: (): ConversationState => getConversationState(),

  getters: {
    getConversation(state): Array<Conversation> {
      return state.list_conversation
    },
  },

  actions: {
    getNumberNotification(user_email : string) : number {
      let countMessageSented = 0
      for( let conversation of this.list_conversation){
          for (let item of conversation.list_message_sent) {
            const convertedDict = JSON.parse(item.replace(/'/g, '"'));
            var keys = Object.keys(convertedDict)
            if (keys[0] == user_email) {
              countMessageSented += convertedDict[keys[0]]
            }
          }
      }
      return countMessageSented
    },
    fetchData(): void {
      getAllConversation().then((res: any) => {
        this.list_conversation = res.conversation
      })
    },
    getConversationByEmail(email : string ) : Conversation | undefined {
      for ( let conversation of this.list_conversation){
        if ( 
            conversation.email_user_from == email 
            || conversation.email_user_to == email
          ){
            return conversation
          }
      }
      return undefined
    },
    updateNewMessage(message_new: string, email_user_chat: string): void {
      this.list_conversation = this.list_conversation.filter((conversation: any) => {
        if (
          conversation.email_user_from == email_user_chat
          || conversation.email_user_to == email_user_chat
        ) {
          conversation.content_last = message_new
        }
        return conversation
      })
    },
    seemConversation( conversation_id : string , user_email : string): void {
      function checkSeem(email: string, list_user_seen: Array<any>): boolean {
        try {
          for (let item of list_user_seen) {
            if (item == email) {
              return true
            }
          }

          // Now `convertedDict` is an actual dictionary (object)
          return false
        } catch (error) {
          return false
        }
      }
      this.list_conversation = this.list_conversation.filter((conversation: any) => {
        if ( conversation_id = conversation.id ) {
            if (checkSeem(user_email , conversation.list_user_seen ) == false){
              conversation.list_user_seen = [... conversation.list_user_seen , user_email ]
            }
            var listMessageSent: string[] = [];
            for (let item of conversation.list_message_sent) {
              const convertedDict = JSON.parse(item.replace(/'/g, '"'));
              var keys = Object.keys(convertedDict)
              if (keys[0] == user_email) {
                listMessageSent = [...listMessageSent , JSON.stringify({ [keys[0]] : 0 })]
              } else {
                listMessageSent = [...listMessageSent , item]
              }
            }
            conversation.list_message_sent = listMessageSent
        }
        return conversation
      })
    },
    uploadSentMessageConversation(email_user_chat: string , user_email : string) : void {
      function removeSeem(email: string, list_user_seen: Array<any>): boolean | Array<string> {
        try {
          var listUserSeem: string[] = []
          for (let item of list_user_seen) {
            if (item != email) {
              listUserSeem = [...listUserSeem , item]
            }
          }
          return listUserSeem
          // Now `convertedDict` is an actual dictionary (object)
          return false
        } catch (error) {
          return false
        }
      }
      this.list_conversation = this.list_conversation.filter((conversation: any) => {
        if (
          conversation.email_user_from == email_user_chat
          || conversation.email_user_to == email_user_chat
        ) {
            if (removeSeem(user_email , conversation.list_user_seen ) != false){
              conversation.list_user_seen = removeSeem(user_email , conversation.list_user_seen )
            }
            var listMessageSent: string[] = [];
            for (let item of conversation.list_message_sent) {
              const convertedDict = JSON.parse(item.replace(/'/g, '"'));
              var keys = Object.keys(convertedDict)
              if (keys[0] == user_email) {
                let newUser = {
                  [keys[0]] : convertedDict[keys[0]] + 1
                }
                listMessageSent = [...listMessageSent , JSON.stringify(newUser)]
              } else {
                listMessageSent = [...listMessageSent , item]
              }
            }
            conversation.list_message_sent = listMessageSent
        }
        return conversation
      })
    },
    getConversationFind(email_user_chat: string): any {
      var conversationFind
      this.list_conversation.filter((conversation: any) => {
        if (
          conversation.email_user_from == email_user_chat
          || conversation.email_user_to == email_user_chat
        ) conversationFind = conversation
      })
      return conversationFind
    },
    updateNewConversation(conversation : Conversation) : void {
      this.list_conversation = [conversation , ... this.list_conversation]
    }

  },
})

