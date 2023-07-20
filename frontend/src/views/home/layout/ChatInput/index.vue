<script lang="ts" setup>
import { ref, onMounted ,computed} from 'vue'
import { useRouter } from 'vue-router';
import { Icon } from '@iconify/vue';
import {useUserStore , useAuthStore} from '@/store'
import { useChatStore} from '@/store'
import { createConversation } from '@/api'

const router = useRouter()

// ref

const contentLast = ref<string>('')

// store

const userStore = useUserStore()
const authStore = useAuthStore()
const chatStore = useChatStore()

// method

function logout(): void {
    userStore.resetUserInfo()
    authStore.removeAuth()
}

function createConversationUser() : void {
    console.log('userToChat' , userToChat)
    if(chatStore.chatSelect != undefined) {
        createConversation( chatStore.chatSelect , contentLast.value )
    }
}


// computed

const userToChat = computed(  () : string | undefined=> {
    return chatStore.chatSelect
})


const isUserChatOnline = computed( () : boolean | undefined => {
    return chatStore.isOnline
})
</script>
<template>
    <div class="d-flex align-items-center bg-white p-3">
        <Icon icon="material-symbols:image-sharp" class="text-dark icon-size-1 m-0 p-2 cursor border border-dark border-2" />
        <div class="p-3 w-100">
            <input v-model="contentLast" type="text" class="p-2 m-1 mx-2 rounded boder w-100" placeholder="Enter content chat"
            v-on:keyup.enter="createConversationUser" >
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

    background: url('./../../../public/15835.jpg');
}
#app {
    height:100%;
}
.cursor {
    cursor : pointer;
}
.cursor:hover {
    text-decoration-line: underline;
}
.icon-size-1 {
    font-size: 44px;
}
</style>