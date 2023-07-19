import { defineStore } from 'pinia'
import { type AuthState , getAuth, removeAuth, setAuth } from './helper'
import { store } from '@/store'


export const useAuthStore = defineStore('auth-store', {
  state: (): AuthState => getAuth(),

  getters: {
    isTokenExists(state): boolean {
      return state.access_token !== undefined
    },
  },

  actions: {
    setAuth(access_token: string) {
      this.access_token = access_token
      setAuth(access_token)
    },

    removeAuth() {
			this.access_token = undefined
      removeAuth()
    },
  },
})

export function useAuthStoreWithout() {
  return useAuthStore(store)
}
