
export interface ChatState {
  conversation_id : string | boolean,
  user_to: string | undefined ,
  is_online : boolean | undefined ,
  list_chat : any | undefined ,
  is_group : boolean ,
  group_name : string | undefined ,
  group_id : string | undefined
  list_user_sent : Array<any> | undefined
}

export function getChatState() : ChatState {
  return {
    conversation_id : false ,
    user_to : undefined ,
    is_online : undefined ,
    list_chat : undefined ,
    is_group : false ,
    group_name : undefined ,
    group_id : undefined ,
    list_user_sent : undefined
  }
}


