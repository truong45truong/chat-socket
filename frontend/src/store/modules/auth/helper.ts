import { ss } from '@/utils/storage'

const LOCAL_NAME = 'SECRET_TOKEN'

export interface AuthState {
  access_token: string | undefined
}

export function getAuth() : string {
  if (ss.get(LOCAL_NAME)) {
    console.log(ss.get(LOCAL_NAME))
    return ss.get(LOCAL_NAME)
  }
  return ''
}

export function setAuth(access_token : string) {
  return ss.set(LOCAL_NAME, access_token) 
}

export function removeAuth() {
  return ss.remove(LOCAL_NAME)
}

