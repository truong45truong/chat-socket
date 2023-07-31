
export interface Conversation {
  id: string,
  email_user_to: string,
  email_user_from: string,
  content_last: string,
  list_message_sent: Array<any>,
  list_user_seen: Array<any>,

}

export interface ConversationState {
  list_conversation: Array<Conversation>
}

export function getConversationState(): ConversationState {
  return {
    list_conversation: []
  }
}


