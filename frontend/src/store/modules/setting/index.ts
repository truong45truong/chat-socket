import { defineStore } from 'pinia'
import { type SettingState , getSettingState } from './helper'
import { store } from '@/store'


export const useSettingStore = defineStore('setting-store', {
  state: (): SettingState => getSettingState(),

  getters: {
    isShowState(state): boolean {
      return state.isShow
    },
   
  },

  actions: {
    showSetting() {
      this.isShow = true
    },

    hideSetting() {
      this.isShow = false
    },
  },
})

export function useSettingStoreWithout() {
  return useSettingStore(store)
}
