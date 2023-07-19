import type { AxiosProgressEvent, GenericAbortSignal } from 'axios'
import { post, get, put, destroy } from '@/utils/request'


/* -------------------------------------------------------------------------- */
/*                                    USER                                    */
/* -------------------------------------------------------------------------- */
export function loginUser<T = any>(username: string , password: string) {
  return post<T>({
    url: '/login/',
    data: { username, password },
  })
}
export function registerUser<T = any>(
    username: string ,email : string , 
    password: string ,name : string
  ) {
  return post<T>({
    url: '/register-user/',
    data: { username, email , password , name },
  })
}

export function searchUser<T = any>(key_search: string,) {
  return get<T>({
    url: '/search-user/',
    data: { key_search },
  })
}

/* -------------------------------------------------------------------------- */
/*                                CONVERSATION                                */
/* -------------------------------------------------------------------------- */

export function getAllConversation<T = any>() {
  return get<T>({
    url: '/conversation/',
  })
}


export function createConversation<T = any>(user_to: string) {
  return post<T>({
    url: '/conversation/create/',
    data: { user_to },
  })
}