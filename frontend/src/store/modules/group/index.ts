import { defineStore } from 'pinia'
import { type GroupState , type Group , getGroupState } from './helper'
import { store } from '@/store'
import {getAllGroup} from '@/api'

export const useGroupStore = defineStore('group-store', {
  state: (): GroupState => getGroupState(),

  getters: {
    getListGRoup(state): Array<Group> {
      return state.list_group
    },
  },

  actions: {
    async fetchDataGroup(){
      await getAllGroup().then((res: any) => {
        this.list_group = res.groups
      })
    },
    uploadData(list_group : Array<Group> ) {
      this.list_group = list_group
    },
    getGroupById(group_id : string) : any {
      for( let group of this.list_group){
        if(group_id == group.group_id){
          return group
        }
      }
      return false
    },
    getNameGroup(conversation_id : string) : boolean | string {
      for( let group of this.list_group){
        if(conversation_id == group.id){
          return group.group_name
        }
      }
      return false
    },
    getNumberNotification(user_email : string) : number {
      let countMessageSented = 0
      for( let conversation of this.list_group){
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
    updateNewMessage( 
      message_new: string, group_id: string , 
      email_user_chat : string , user_email : string
    ): void {
      this.list_group = this.list_group.filter((conversation: any) => {
        if (
          conversation.group_id == group_id
        ) {
          conversation.content_last = message_new
          conversation.user_chat = email_user_chat
          conversation.list_user_seen = []
          conversation.list_message_sent =  conversation.list_message_sent.filter(
            (item: any) =>{
              const convertedDict = JSON.parse(item.replace(/'/g, '"'));
              var keys = Object.keys(convertedDict)
              if(keys[0] == user_email){
                item = "{'" + user_email + "' : " +  (convertedDict[keys[0]] + 1) +"}"
              }
              return item
            }
          )
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
      this.list_group = this.list_group.filter((conversation: any) => {
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
    uploadSentMessageConversation(group_id: string , user_email : string) : void {
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
      this.list_group = this.list_group.filter((conversation: any) => {
        if (
          conversation.group_id == group_id
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

  },
})

