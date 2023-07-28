import { defineStore } from 'pinia'
import type { SocketSate } from './helper'
import { intialSocketState } from './helper'
import soundNoticy from './../../../assets/sound/mixkit-elevator-tone-2863.wav'
// import {useConversationStore} from '@/store/modules/conversation/index'

// const conversationStore = useConversationStore()

export const useSocketStore = defineStore('socket-store', {
  state: (): SocketSate => intialSocketState(),
  actions: {
    async initSocketNotification(user_from : string){
      const chatSocket = new WebSocket(
        'ws://'
        + "0.0.0.0:8000"
        + '/ws/notification/'
        + this.id_socket
        + '/'
      );
      await new Promise((resolve) => {
        chatSocket.addEventListener('open', () => {
          resolve();
        });
      });
      chatSocket.send(JSON.stringify({
        'user_from' : user_from ,
        'init_socket' : 0,
        'client_id' : this.id_socket ,
      }));
      chatSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        if( data.is_chat == false){
          console.log("notify : ", data)
          this.notification =  data
          var audio = new Audio(soundNoticy);
          const promise = audio.play();
          if(promise !== undefined){
              promise.then(() => {
                // Autoplay started
            }).catch(error => {
                // Autoplay was prevented.
                audio.muted = true;
                audio.play();
            });
          }
        }else {

        }
        
       };
    } ,
    async initSocket(conversation : string ,  user_from : string , user_to : string) : Promise<any> {
      this.is_group = false
      if (this.socket !== undefined) {
        this.socket.close();
        this.socket = undefined;
      }
      const chatSocket = new WebSocket(
        'ws://'
        + "0.0.0.0:8000"
        + '/ws/chat/'
        + conversation
        + '/'
        + this.id_socket
        + '/'
      );
      this.socket = chatSocket
      await new Promise((resolve) => {
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
          console.log("clients : ", data)
          this.list_chat_receiver = [...this.list_chat_receiver , data]
          // conversationStore.updateNewMessage( data )
        } else {
          console.log("notify : ", data)
          this.notification =  data
          var audio = new Audio(soundNoticy);
          const promise = audio.play();
          if(promise !== undefined){
              promise.then(() => {
                // Autoplay started
            }).catch(error => {
                // Autoplay was prevented.
                audio.muted = true;
                audio.play();
            });
          }
        }
       };
       
    },
    async initSocketChatGroup(conversation : string ,  user_from : string , group_id : string ) : Promise<any>{
      this.is_group = true
      if (this.socket !== undefined) {
        this.socket.close();
        this.socket = undefined;
      }
      const chatSocket = new WebSocket(
        'ws://'
        + "0.0.0.0:8000"
        + '/ws/chat/'
        + conversation
        + '/'
        + this.id_socket
        + '/'
      );
      this.socket = chatSocket
      await new Promise((resolve) => {
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
          console.log("clients : ", data)
          this.list_chat_receiver = [...this.list_chat_receiver , data]
          // conversationStore.updateNewMessage( data )
        } else {
          console.log("notify : ", data)
          this.notification =  data
          var audio = new Audio(soundNoticy);
          const promise = audio.play();
          if(promise !== undefined){
              promise.then(() => {
                // Autoplay started
            }).catch(error => {
                // Autoplay was prevented.
                audio.muted = true;
                audio.play();
            });
          }
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
      group_id : string | undefined , conversation : string , 
      content : string , email_user_chat : string
  ) : void {
      this.conversation = conversation
      console.log("send mess group")
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
  },
})
