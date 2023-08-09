import { defineStore } from 'pinia'
import { type selectLayoutState , getSelectLayoutState } from './helper'
import { store } from '@/store'

export interface ChatResponse {
  chats : Array<any>
}
export const useSelectLayoutStore = defineStore('select-layout-store', {
  state: (): selectLayoutState => getSelectLayoutState(),

  getters: {
    layoutSelected(state): any {
      return state.show
    }
  },

  actions: {
    selectLayoutView(type :number ) : void {
      switch(type) {
        case 1:
          this.view_layout.isShowConversation = true
          this.view_layout.isShowCreateGroup = false
          this.view_layout.isShowSettingGroup = false
          break;
        case 2:
          this.view_layout.isShowConversation = false
          this.view_layout.isShowCreateGroup = true
          this.view_layout.isShowSettingGroup = false
          break;
        case 3:
          this.view_layout.isShowConversation = false
          this.view_layout.isShowCreateGroup = false
          this.view_layout.isShowSettingGroup = true
          break;
      }
    },
    selectLayout( type : number ){
      switch (type) {
        case 1:
          this.show.isShowChat = true
          this.show.isShowGroup = false
          this.show.isShowFriend = false
          this.show.isShowNotification = false
          break;
        case 2:
          this.show.isShowChat = false
          this.show.isShowGroup = true
          this.show.isShowFriend = false
          this.show.isShowNotification = false
          break;
        case 3:
          this.show.isShowChat = false 
          this.show.isShowGroup = false
          this.show.isShowFriend = true
          this.show.isShowNotification = false
          break
        case 4:
          this.show.isShowChat = false 
          this.show.isShowGroup = false
          this.show.isShowFriend = false
          this.show.isShowNotification = true
          
          break;

      }
    },
    selectLayoutReponsive(type : number){
      switch(type) {
        case 1:
          this.view_reponsice.isSelectLayouMenu = true
          break;
        case 2:
          this.view_reponsice.isSelectLayouMenu = false
          break;
      }
    },
    showMenuReponse(){
      this.view_show_menu_reponsive.isShowMenu = ! this.view_show_menu_reponsive.isShowMenu
    }
  }
})

export function useSelectLayoutStoreWithout() {
  return useSelectLayoutStore(store)
}
