import { defineStore } from 'pinia'
import { type NotificationState , type Notification , getNotificationState } from './helper'
import { store } from '@/store'


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
    },
    uploadData(notification : Notification ) {
      this.list_notification = [...this.list_notification , notification]
    }
  },
})

