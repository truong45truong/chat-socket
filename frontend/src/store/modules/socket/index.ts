import { defineStore } from 'pinia'
import type { SocketSate } from './helper'
import { intialSocketState } from './helper'
import soundNoticy from './../../../assets/sound/mixkit-elevator-tone-2863.wav'
import { URL_SOCKET } from './helper'


export const useSocketStore = defineStore('socket-store', {
  state: (): SocketSate => intialSocketState(),
  actions: {
    async initSocketNotification(user_from : string){
      const chatSocket = new WebSocket(
        'ws://'
        + URL_SOCKET
        + '/ws/notification/'
        + this.id_socket
        + '/'
      );
      await new Promise<void>((resolve) => {
        chatSocket.addEventListener('open', () => {
          resolve();
        });
      });
        chatSocket.send(JSON.stringify({
          'user_from' : user_from ,
          'init_socket' : 0,
          'client_id' : this.id_socket ,
        }));
        chatSocket.send(JSON.stringify({
          'email_user_chat' : user_from ,
          'init_socket' : 5,
          'client_id' : this.id_socket ,
        }));
      chatSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        if( data.is_chat == false){
          this.notification =  data
          if(data.type != "GUO" && data.type != "NTFUO"){
            var audio = new Audio(soundNoticy);
            const promise = audio.play();
            if(promise !== undefined){
                promise.then(() => {
              }).catch(error => {
                  audio.muted = true;
                  audio.play();
              });
            }
          }
        }else {

        }
        
       };
    } ,
    async initSocket(conversation : string ,  user_from : string , user_to : string) : Promise<any> {
      this.is_group = false
      this.list_chat_receiver = []
      if (this.socket !== undefined) {
        this.socket.close();
        this.socket = undefined;
      }
      const chatSocket = new WebSocket(
        'ws://'
        + URL_SOCKET
        + '/ws/chat/'
        + conversation
        + '/'
        + this.id_socket
        + '/'
      );
      this.socket = chatSocket
      await new Promise<void>((resolve) => {
        chatSocket.addEventListener('open', () => {
          resolve();
        });
      });
      this.socket.send(JSON.stringify({
        'conversation': conversation ,
        'user_to' : user_to ,
        'user_from' : user_from ,
        'init_socket' : 1,
        'client_id' : this.id_socket ,
      }));
      chatSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        if (data.is_chat == true){
          this.list_chat_receiver = [...this.list_chat_receiver , data]
        } 
       };
       
    },
    async initSocketChatGroup(conversation : string ,  user_from : string , group_id : string ) : Promise<any>{
      this.is_group = true
      this.list_chat_receiver = []
      if (this.socket !== undefined) {
        this.socket.close();
        this.socket = undefined;
      }
      const chatSocket = new WebSocket(
        'ws://'
        + URL_SOCKET
        + '/ws/chat/'
        + conversation
        + '/'
        + this.id_socket
        + '/'
      );
      this.socket = chatSocket
      await new Promise<void>((resolve) => {
        chatSocket.addEventListener('open', () => {
          resolve();
        });
      });
      this.socket.send(JSON.stringify({
        'conversation': conversation ,
        'user_from' : user_from ,
        'init_socket' : 3,
        'client_id' : this.id_socket ,
        'group_id' : group_id,
      }));
      chatSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        if (data.is_chat == true){
          this.list_chat_receiver = [...this.list_chat_receiver , data]
        } 
        
       };
    },
    updateListChatSocket(data : string) : void {
      this.list_chat_receiver = [...this.list_chat_receiver , data]
    },
    sendMessage(
        user_to : string | undefined, conversation : string , 
        content : string , email_user_chat : string
    ) : void {
        this.user_to = user_to
        this.conversation = conversation
        if(this.is_group == false){
          this.socket.send(JSON.stringify({
            'message': content,
            'conversation': conversation ,
            'user_to' : user_to ,
            'init_socket' : 2,
            'client_id' : this.id_socket ,
            'email_user_chat' : email_user_chat
          }));
        }
    },
    sendMessageGroup(
      group_id : string | undefined , conversation : string | undefined , 
      content : string | undefined, email_user_chat : string | undefined
    ) : void {
      this.conversation = conversation
      if(this.is_group == true){
        this.socket.send(JSON.stringify({
          'message': content,
          'conversation': conversation ,
          'init_socket' : 4,
          'client_id' : this.id_socket ,
          'email_user_chat' : email_user_chat ,
          'group_id' : group_id
        }))
      }
    },
    sendNotifiCreateGroup(
      email_user_chat : string | undefined ,
      group_id : string | undefined
    ){
      this.socket.send(JSON.stringify({
        'init_socket' : 6,
        'client_id' : this.id_socket ,
        'email_user_chat' : email_user_chat ,
        'group_id' : group_id
      }))
    },
    sendNotifiCreateChat(
      email_user_chat : string | undefined ,
      user_to : string | undefined
    ){
      this.socket.send(JSON.stringify({
        'init_socket' : 7,
        'client_id' : this.id_socket ,
        'email_user_chat' : email_user_chat ,
        'user_to' : user_to
      }))
    }
  },
})
