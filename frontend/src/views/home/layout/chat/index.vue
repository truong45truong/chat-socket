<script lang="ts" setup>
import { ref , computed } from 'vue'
import { useRouter } from 'vue-router';
import { Icon } from '@iconify/vue';
import {useChatStore , useUserStore , useBGStore} from '@/store'

const router = useRouter()

// store

const chatStore = useChatStore()
const userStore = useUserStore()
const userBG = useBGStore()
// computed

const userChatSelect = computed( () : string | undefined => {
    return chatStore.chatSelect
} )

const isUserChatOnline = computed( () : boolean | undefined => {
    return chatStore.isOnline
})
const listChatSelected = computed(() : any | undefined => {
    return chatStore.list_chat
})
const userCurrent = computed(() : string | undefined => {
    return userStore.userInfo.email
})

const bgSelect = computed( () : string => userBG.imgSelect)

const divStyle = computed(() => {
  return {
    backgroundImage: `url(${bgSelect.value})`,
    backgroundSize: 'cover',
  };
});
</script>
<template>
    <div class="d-flex flex-column bg-white h-100">
        <div class="d-flex align-items-center p-2 border border-2 border-dark
        border-top-0 border-start-0 border-end-0 ">
            <div class="chat-no-image text-center p-3 text-white border border-dark border-2"> Chat </div>
            <div class="ms-3 d-flex flex-column align-item-center justify-content-around">
                <p class="m-0 text-dark"> <b>{{userChatSelect}}</b></p>
            </div>
            <Icon icon="carbon:circle-filled" class="ms-3 color-online" />
            <p v-if="isUserChatOnline == true" class="m-0 ms-1 color-online"> Online</p>
            <p v-if="isUserChatOnline == false" class="m-0 ms-1 color-online"> Offline</p>
        </div>
        <div class="layout-chat" :style="divStyle">
            <div v-for="item in listChatSelected " class="row mt-2">
                <div class="col-6 d-flex justify-content-start ps-3">
                    <div v-if="userCurrent != item.email_user_chat " class="chat-no-image text-center p-3 text-white border border-dark border-2"> Chat </div>
                    <div v-if="userCurrent != item.email_user_chat " class="chat-no-current ms-2 p-3 mb-3">
                        <p class="m-0 text-start text-dark">{{item.content}}</p>
                    </div>
                </div>
                <div class="col-6 d-flex justify-content-end pe-4">
                    <div v-if="userCurrent == item.email_user_chat " class="chat-current p-3 mb-3">
                        <p class="m-0 text-end text-white">{{item.content}}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<style>
html, body {
  height: 100%;
  margin :0;
}
.bg-login {
    height:100%;

    background: url('./../../../../assets/images/display/bg-1.jpg');
}
#app {
    height:100%;
}
.color-online {
    color :rgb(14, 160, 50)
}
.layout-chat {
    height:100%;
}
.chat-current {
    width:fit-content;
    background-color: black;
    justify-content: end;
    border-radius: 15px;
}
.chat-no-current {
    background-color: aliceblue;
    width:fit-content;
    border-radius: 15px;
}
.chat-no-image {
    width:67px;
    height:67px;
}
</style>