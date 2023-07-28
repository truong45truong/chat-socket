
export interface Conversation {
  id : string ,
  email_user_to : string ,
  email_user_from : string ,
  content_last : string ,
  is_seen : boolean ,
  is_sent : boolean ,
}

export interface ConversationState {
  list_conversation : Array<Conversation>
}

export function getConversationState() : ConversationState {
  return {
    list_conversation : []
  }
}


