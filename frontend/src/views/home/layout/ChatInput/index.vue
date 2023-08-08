<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router';
import { Icon } from '@iconify/vue';
import { useUserStore, useAuthStore, useSelectLayoutStore } from '@/store'
import { useChatStore, useSocketStore } from '@/store'
import { useConversationStore } from '@/store';
import { createConversation , chatGroup , createNotification ,
    chatConversation
} from '@/api'

const router = useRouter()

// ref

const contentLast = ref<string>('')

// store

const userStore = useUserStore()
const authStore = useAuthStore()
const chatStore = useChatStore()
const socketStore = useSocketStore()
const conversationStore = useConversationStore()
const selectLayout = useSelectLayoutStore()
// method

function logout(): void {
    userStore.resetUserInfo()
    authStore.removeAuth()
}
async function selectChatReply(user_to : string , user_from : string , conversation_id : string): Promise<void> {
    if (userStore.userInfo.email == user_to){
        chatStore.setSelectChat( user_from , conversation_id)
        await socketStore.initSocket(conversation_id , user_to , user_from )
    } else{
        chatStore.setSelectChat( user_to , conversation_id)
        await socketStore.initSocket(conversation_id , user_from , user_to )
    }
    await conversationStore.seemConversation(conversation_id , userStore.userInfo.email)
    await chatStore.fetchChats()
    
}

async function createConversationUser(): Promise<void> {
    if(chatStore.group_id != undefined && chatStore.is_group == true){
        socketStore.sendMessageGroup(
            chatStore.group_id,
            chatStore.conversation_id + "",
            contentLast.value,
            userStore.userInfo.email
        )
        conversationStore.updateNewMessage(contentLast.value , chatStore.group_id)
        await chatGroup(chatStore.conversation_id + "", contentLast.value)
        createNotification(
            contentLast.value,
            'NTFCG',
            userStore.userInfo.email ,
            chatStore.conversation_id + "" ,
        )
    }
    if (chatStore.chatSelect != undefined  && chatStore.is_group == false) {
        if (chatStore.list_chat.length == 0 ) {
            const res: any = await createConversation(chatStore.chatSelect, contentLast.value);
            await conversationStore.updateNewConversation(res.conversation)
                
            await selectChatReply(chatStore.chatSelect , userStore.userInfo.email, res.conversation.id )

            socketStore.sendNotifiCreateChat( userStore.userInfo.email , chatStore.chatSelect )
                        
        } else {
            await chatConversation(chatStore.conversation_id + "" , chatStore.chatSelect, contentLast.value)
            if(chatStore.is_group == false){
                socketStore.sendMessage(
                    chatStore.user_to,
                    chatStore.conversation_id + "",
                    contentLast.value,
                    userStore.userInfo.email
                )
                conversationStore.updateNewMessage(contentLast.value , chatStore.user_to + "")
            }
            createNotification(
                contentLast.value,
                'NTFCT',
                userStore.userInfo.email ,
                chatStore.conversation_id + "" ,
            )
        }
    }
    contentLast.value =""

}


// computed

const userToChat = computed((): string | undefined => {
    return chatStore.chatSelect
})


const isUserChatOnline = computed((): boolean | undefined => {
    return chatStore.isOnline
})

const isShowMenuReponsive = computed ( () : boolean => {
    return selectLayout.view_show_menu_reponsive.isShowMenu
})
</script>
<template>
    <div class="d-flex align-items-center bg-white p-3 position-relative">
        <div class="p-3 w-100">
            <input v-model="contentLast" type="text" id="input-chat-send" class="p-2 m-1 mx-2 w-100"
                placeholder="Enter content chat" v-on:keyup.enter="createConversationUser">
        </div>
        <Icon icon="carbon:send-filled" @click="createConversationUser" class="text-dark icon-size-1 m-0 p-2 cursor"  />
    </div>
</template>
<style>
html,
body {
    height: 100%;
    margin: 0;
}

.bg-login {
    height: 100%;

    background: url('./../../../public/15835.jpg');
}

#app {
    height: 100%;
}

.cursor {
    cursor: pointer;
}

.cursor:hover {
    text-decoration-line: underline;
}

.icon-size-1 {
    font-size: 44px;
}

#input-chat-send {
    border: none;
    border-bottom: 1px solid black;
    background-color: transparent;
}

#input-chat-send:focus {
    outline: none;
    border-bottom: 1px solid black;
}</style>