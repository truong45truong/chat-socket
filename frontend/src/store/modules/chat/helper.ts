
export interface ChatState {
  conversation_id : string | undefined,
  user_to: string | undefined ,
  is_online : boolean | undefined ,
  list_chat : any | undefined ,
}

export function getChatState() : ChatState {
  return {
    conversation_id : undefined ,
    user_to : undefined ,
    is_online : undefined ,
    list_chat : undefined ,
  }
}


