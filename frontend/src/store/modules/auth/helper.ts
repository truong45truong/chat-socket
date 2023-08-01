import { ss } from '@/utils/storage'

const LOCAL_NAME = 'SECRET_TOKEN'

export interface AuthState {
  access_token: string | undefined
}

export function getAuth() : AuthState {
  if (ss.get(LOCAL_NAME)) {
    return {
      access_token : ss.get(LOCAL_NAME)
    }
  }
  return {
    access_token : undefined
}
}

export function setAuth(access_token : string) {
  return ss.set(LOCAL_NAME, access_token) 
}

export function removeAuth() {
  return ss.remove(LOCAL_NAME)
}

