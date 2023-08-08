<script lang="ts" setup>
import { ref , computed , onMounted } from 'vue'
import { useRouter } from 'vue-router';
import { searchUser , checkConversation } from '@/api';
import { Icon, _api } from '@iconify/vue';
import { 
    useChatStore , useUserStore , 
    useSocketStore , useSelectLayoutStore ,
    useConversationStore , useMemberShipStore , 
} from '@/store'

import {getAllGroup , seemConversation} from '@/api'

const router = useRouter()

// component

import ConversationComponent from './../../component/conversation/index.vue'
import NotificationLayout from './../notification/index.vue'
import GroupLayout from './../group/index.vue'
//ref

const keySearch = ref<string>('')
const listUserSearch = ref<any>([])
const isOnline = ref<boolean>(true)
    const dataConversation = ref<any>([])

// store

const chatStore = useChatStore()
const userStore = useUserStore()
const socketStore = useSocketStore()
const selectLayout = useSelectLayoutStore()
const conversationStore = useConversationStore()
const membershipStore = useMemberShipStore()

// fetch data

conversationStore.fetchData()

//computed

const listDataConversation = computed( () : any => {
    return conversationStore.list_conversation
})

const showLayout = computed ( () : any => {
  return selectLayout.show
} )
const user = computed( () : string => {
    return userStore.userInfo.email
})

const listMemberShip = computed( () : any => {
    return membershipStore.list_membership
})

const selectLayouReponse = computed( (): any => {
    return selectLayout.view_reponsice.isSelectLayouMenu
})
// method


function search(): void {
    searchUser(keySearch.value).then((res : any ) => {
        listUserSearch.value = res.users 
    })

}

function selectChat(email : string): void {
    keySearch.value = ''
    var conversationCheck = conversationStore.getConversationByEmail(email)
    if ( conversationCheck == undefined){
        checkConversation(email).then( (res : any) => {
            if(res.empty == false){
                chatStore.uploadDataChat(email,res.chats , res.conversation_id)
                socketStore.initSocket(res.conversation_id , userStore.userInfo.email , email )
            } else {
                chatStore.uploadDataChat(email,[] , true)
            }
        })
        selectLayout.selectLayoutView(1)
    } else {
        selectChatReply(
            conversationCheck.email_user_to ,
            conversationCheck.email_user_from ,
            conversationCheck.id
        )
    }
    // chatStore.setSelectChat( email , conversation_id)
    // chatStore.fetchChats()
    if(window.innerWidth <= 720){
        selectLayout.selectLayoutReponsive(1)
    }
}

function selectChatReply(user_to : string , user_from : string , conversation_id : string): void {
    keySearch.value = ''
    if (userStore.userInfo.email == user_to){
        chatStore.setSelectChat( user_from , conversation_id)
        socketStore.initSocket(conversation_id , user_to , user_from )
    } else{
        chatStore.setSelectChat( user_to , conversation_id)
        socketStore.initSocket(conversation_id , user_from , user_to )
    }
    seemConversation(conversation_id)
    conversationStore.seemConversation(conversation_id , userStore.userInfo.email)
    chatStore.fetchChats()
    selectLayout.selectLayoutView(1)
    if(window.innerWidth <= 720){
        selectLayout.selectLayoutReponsive(1)
    }
    
}
function ramdomBG() : any {
    var predefinedColors = ['#7B68EE', '#E9967A', '#20B2AA', '#33FFFF', '#B0C4DE']; 
    var max = 5
    var min = 1
    var randomInteger = Math.floor(Math.random() * (max - min + 1)) + min
    return {
        backgroundColor : predefinedColors[randomInteger]
    }
}

</script>
<template>
    <div class="p-3 w-100">
        <div class="d-flex align-items-center mb-2">
            <div class="ms-1 ">
                <p class="text-dark m-0 ms-1"><b>{{ user }}</b></p>
                <div class="d-flex align-items-center">
                    <Icon icon="carbon:circle-filled" class="ms-1" :class="[ isOnline ? 'color-online' : 'color-offline']" />
                    <p v-if="isOnline" class="m-0 ms-1 color-online"> Online</p>
                    <p v-if="!isOnline" class="m-0 ms-1 color-offline"> Hide online</p>
                </div>
                <div title=".slideThree" class="ms-1 mt-1">
                    <!-- .slideThree -->
                    <div class="slideThree">
                        <input v-model="isOnline" type="checkbox" value="None" id="slideThree" name="check" checked />
                        <label for="slideThree"></label>
                    </div>
                    <!-- end .slideThree -->
                </div>
            </div>

        </div>
        <div class="m-1  position-relative">
            <div class="d-flex">    
                <input v-model="keySearch" type="text" class="p-2 w-100" placeholder="Search" v-on:keyup.enter="search">
            </div>
            <div v-if="keySearch != ''" class="p-2 list-user-search position-absolute shadow bg-white border w-100">
                <p v-if="listUserSearch.length == 0" class="m-0 text-center text-dark">
                    No have user searched
                </p>
                <div v-for="item in listUserSearch" class="d-flex align-items-center mb-2 chat-item" @click="selectChat(item.email)">
                    <div :style="ramdomBG()" class="chat-no-image-search text-center p-3 text-white"> Chat </div>
                    <div class="ms-3 d-flex flex-column align-item-center justify-content-around">
                        <p class="m-0 text-dark"> <b>{{ item.email }}</b></p>

                    </div>
                </div>
            </div>
        </div>

        <div v-if="showLayout.isShowChat" class="p-1 my-3">
            <div v-for="item in listDataConversation" class="d-flex align-items-center mb-2 w-100 chat-item" @click="selectChatReply(item.email_user_to, item.email_user_from , item.id)" >
                <ConversationComponent   
                    :email_user_from="item.email_user_from" 
                    :email_user_to="item.email_user_to"
                    :content_last="item.content_last"
                    :list_message_sent="item.list_message_sent"
                    :list_user_seen="item.list_user_seen"
                    :user_chat="item.user_chat"
                />
            </div>
        </div>
        <div v-if="showLayout.isShowNotification" class="p-1 my-3">
            <p class="py-3">
                <b>Notification : </b>
            </p>
            <hr class="my-1">
            <NotificationLayout />
        </div>
        <div v-if="showLayout.isShowFriend" class="p-1 my-3">
            <p class="py-3">
                <b>Friends : </b>
            </p>
            <hr class="my-1">
            <div v-for="item in listMemberShip" class=" my-2  ">
                <div class="d-flex align-items-center justify-content-between">
                    <p class="m-0"> <b class=""> {{ item.email }}</b></p>

                    <div class="d-flex align-items-center justify-content-end">
                        <p  v-if="item.is_online" class="m-0 me-1 icon-online-friend"> Active </p>
                        <p  v-if="item.is_online == false" class="m-0 me-1 icon-off-friend"> Inactive </p>
                        <Icon v-if="item.is_online" class="icon-online-friend" icon="prime:circle-fill" />
                        <Icon v-if="item.is_online == false" class="icon-off-friend" icon="prime:circle-fill" />
                    </div>
                </div>
            </div>
        </div>
        <div v-if="showLayout.isShowGroup" class="p-1 my-3">
            <GroupLayout />
        </div>
    </div>
</template>
<style lang="scss">
.icon-online-friend {
    color: rgb(14, 160, 50);
    font-size: 12px;
}
.icon-off-friend {
    color: rgb(73, 73, 73);
    font-size: 12px;
}
.list-user-search {
    z-index: 99;
}
html,
body {
    height: 100%;
    margin: 0;
}
.color-offline {
    color:#4d4d4d
}
.bg-login {
    height: 100%;

    background: url('./../../../public/15835.jpg');
}

#app {
    height: 100%;
}

.chat-no-image {
    background-color: rgb(1, 35, 85);
    border-radius: 50%;
}

.chat-no-image-search {
    background-color: rgb(134, 30, 160);
    border-radius: 50%;
}
.chat-item {
    cursor : pointer;
}
.slideThree {
  width: 80px;
  height: 26px;
  background: #333;
  position: relative;
  border-radius: 50px;
  box-shadow: inset 0px 1px 1px rgba(0,0,0,0.5), 0px 1px 0px rgba(255,255,255,0.2);
  &:after {
    content: 'OFF';
    color: white;
    position: absolute;
    right: 10px;
    z-index: 0;
    font: 12px/26px Arial, sans-serif;
    font-weight: bold;
    text-shadow: 1px 1px 0px rgba(255,255,255,.15);
  }
  &:before {
    content: 'ON';
    color: rgb(14, 160, 50);
    position: absolute;
    left: 10px;
    z-index: 0;
    font: 12px/26px Arial, sans-serif;
    font-weight: bold;
  }
  label {
    display: block;
    width: 34px;
    height: 20px;
    cursor: pointer;
    position: absolute;
    top: 3px;
    left: 3px;
    z-index: 1;
    background: #fcfff4;
    background: linear-gradient(top, #fcfff4 0%, #dfe5d7 40%, #b3bead 100%);
    border-radius: 50px;
    transition: all 0.4s ease;
    box-shadow: 0px 2px 5px 0px rgba(0,0,0,0.3);
  }
  input[type=checkbox] {
    visibility: hidden;
    &:checked + label {
      left: 43px;
    }
  }    
}
@media screen and (max-width: 720px) {
  p {
    font-size: 14px;
  }
  .chat-no-image{
    width:47px;
    height:47px;
    padding: 10px 7px !important;
  }

}
</style>