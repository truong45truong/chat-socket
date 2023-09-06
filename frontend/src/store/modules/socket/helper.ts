

export const URL_SOCKET = '0.0.0.0'

function generateUUID() {
  // Generate a random hexadecimal string of length 32 (representing 16 bytes)
  const getRandomHex = (size: any) => [...Array(size)].map(() => Math.floor(Math.random() * 16).toString(16)).join('');

  // Generate four different segments of the UUID
  const segment1 = getRandomHex(8);
  const segment2 = getRandomHex(4);
  const segment3 = '4' + getRandomHex(3); // UUID version 4
  const segment4 = (8 + Math.floor(Math.random() * 4)).toString(16) + getRandomHex(3); // Set the most significant bits (MSBs) of clock_seq_hi_and_reserved

  // Join the segments with dashes to form the final UUID
  return `${segment1}-${segment2}-${segment3}-${segment4}`;
}

export interface SocketSate {
  id_socket : any
  socket : any | undefined ,
  conversation: string |undefined
  user_from: string | undefined
  user_to: string | undefined 
  list_chat_receiver : any | undefined
  notification : any | undefined 
  is_group : boolean
}

export function intialSocketState(): SocketSate {
  return {
    id_socket : generateUUID() , 
    socket : undefined ,
    conversation: undefined ,
    user_from : undefined ,
    user_to : undefined , 
    list_chat_receiver : [] ,
    notification : undefined ,
    is_group : false
  }
}
