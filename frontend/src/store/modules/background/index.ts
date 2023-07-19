import { defineStore } from 'pinia'
import { type BgState , getBG, removeBG, setBG } from './helper'
import { store } from '@/store'


export const useBGStore = defineStore('auth-store', {
  state: (): BgState => getBG(),

  getters: {
    listDisplay(state): any {
      return state.image
    },
    imgSelect(state) : string | undefined {
      return state.isSelect
    }
  },

  actions: {
    setBG(isSelect: string) {
      this.isSelect = isSelect
      setBG(isSelect)
    },

    removeBG() {
			this.isSelect = undefined
      removeBG()
    },
  },
})

export function useBGStoreWithout() {
  return useBGStore(store)
}
