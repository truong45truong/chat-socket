import { defineStore } from 'pinia'
import { type NotificationState , type Notification , getNotificationState } from './helper'
import { store } from '@/store'
import {seemNotification} from '@/api'

export const useNotificationStore = defineStore('notification-store', {
  state: (): NotificationState => getNotificationState(),

  getters: {
    getListNotification(state): Array<Notification> {
      return state.list_notification
    },
  },

  actions: {
    fetchData( data : Array<Notification> ){
      this.list_notification = data
      for( let notification of data ){
        if(notification.is_seem == false){
          this.number_notification += 1
        }
      }
    },
    uploadData(notification : Notification , is_activate : boolean ) {
      this.list_notification = [notification,...this.list_notification]
      if ( is_activate == false) this.number_notification += 1
    },
    seem(){
      for(let notification of this.list_notification){
        if(notification.is_seem == false){
          seemNotification(notification.id)
        }
      }
      this.number_notification = 0
    }
  },
})

