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

export function searchUserAddGroup<T = any>(key_search: string, group_id : string | undefined) {
  return get<T>({
    url: '/search-user/add-group/',
    data: { key_search , group_id },
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

export function getConversation<T = any>( conversation_id : string | undefined) {
  return get<T>({
    url: '/conversation/' + conversation_id + "/",
  })
}

export function createConversation<T = any>(user_to: string | undefined , content_last : string) {
  return post<T>({
    url: '/conversation/create/',
    data: { user_to , content_last },
  })
}
export function chatConversation<T = any>(conversation_id: string | undefined , user_to : string , content_last : string) {
  return post<T>({
    url: '/conversation/chat/',
    data: { conversation_id, user_to , content_last },
  })
}
export function checkConversation<T = any>(user_to: string | undefined ) {
  return post<T>({
    url: '/conversation/check/',
    data: { user_to },
  })
}
export function seemConversation<T = any>(conversation_id: string | undefined ) {
  return post<T>({
    url: '/conversation/seem/',
    data: { conversation_id },
  })
}

/* -------------------------------------------------------------------------- */
/*                                 MEMBER SHIP                                */
/* -------------------------------------------------------------------------- */

export function addMemberShip<T = any>(user_to: string ) {
  return post<T>({
    url: '/add-friends/',
    data: { user_to },
  })
}

export function getAllMemberShip<T = any>() {
  return get<T>({
    url: '/get-membership/',
  })
}

/* -------------------------------------------------------------------------- */
/*                                 GROUP CHAT                                 */
/* -------------------------------------------------------------------------- */

export function createGroup<T = any>(name: string , list_member : Array<string> , description : string ) {
  return post<T>({
    url: '/group/create/',
    data: { name ,list_member , description},
  })
}

export function updateGroup<T = any>(name: string , list_member_add : Array<string> ,
  list_member_remove : Array<string>   , description : string ) {
  return post<T>({
    url: '/group/update/',
    data: { name ,list_member_add , list_member_remove , description},
  })
}

export function chatGroup<T = any>(conversation_id: string , content_last : string ) {
  return post<T>({
    url: '/group/chat/',
    data: { conversation_id ,content_last},
  })
}

export function getAllGroup <T = any>(){
  return get<T>({
    url : '/group/'
  })
}

export function getListMember <T = any>(group_id : string | undefined){
  return get<T>({
    url : '/group/' + 'member/' + group_id + "/"
  })
}
/* -------------------------------------------------------------------------- */
/*                                NOTIFICATION                                */
/* -------------------------------------------------------------------------- */

export function getAllNotification <T = any>(){
  return get<T>({
    url : '/notification/'
  })
}

export function createNotification<T = any>(
    content: string ,  type : string ,
    email_user_chat : string , 
    conversation_id : string
  ){
    return post<T>({
      url: '/notification/create/',
      data: { content , email_user_chat , type ,conversation_id },
  })
}

export function seemNotification<T = any>(
  notification_id : string
){
  return post<T>({
    url: '/notification/seem/',
    data: { notification_id },
})
}