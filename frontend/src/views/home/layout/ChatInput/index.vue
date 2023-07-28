<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router';
import { Icon } from '@iconify/vue';
import { useUserStore, useAuthStore } from '@/store'
import { useChatStore, useSocketStore } from '@/store'
import { useConversationStore } from '@/store';
import { createConversation , chatGroup } from '@/api'

const router = useRouter()

// ref

const contentLast = ref<string>('')

// store

const userStore = useUserStore()
const authStore = useAuthStore()
const chatStore = useChatStore()
const socketStore = useSocketStore()
const conversationStore = useConversationStore()
// method

function logout(): void {
    userStore.resetUserInfo()
    authStore.removeAuth()
}

async function createConversationUser(): Promise<void> {
    console.log('chatStore.group_id',chatStore.group_id , 'chatStore.is_group' , chatStore.is_group)
    if(chatStore.group_id != undefined && chatStore.is_group == true){
        socketStore.sendMessageGroup(
            chatStore.group_id,
            chatStore.conversation_id,
            contentLast.value,
            userStore.userInfo.email
        )
        conversationStore.updateNewMessage(contentLast.value , chatStore.group_id)
        await chatGroup(chatStore.conversation_id, contentLast.value)
    }
    if (chatStore.chatSelect != undefined  && chatStore.is_group == false) {
        if (chatStore.list_chat.length == 0 ) {
            const res = await createConversation(chatStore.chatSelect, contentLast.value);

            // Establish the WebSocket connection
            await new Promise<void>((resolve, reject) => {
                socketStore.initSocket(
                    res.conversation.id,
                    userStore.userInfo.email,
                    chatStore.chatSelect
                );
            });

            // Send the message once the WebSocket is fully established
            socketStore.sendMessage(
                chatStore.user_to,
                chatStore.conversation_id,
                contentLast.value,
                userStore.userInfo.email
            );

            // Set up the onmessage event handler after sending the message
        } else {
            await createConversation(chatStore.chatSelect, contentLast.value)
            if(chatStore.is_group == false){
                socketStore.sendMessage(
                    chatStore.user_to,
                    chatStore.conversation_id,
                    contentLast.value,
                    userStore.userInfo.email
                )
                conversationStore.updateNewMessage(contentLast.value , chatStore.user_to)
            }

        }
    }
}


// computed

const userToChat = computed((): string | undefined => {
    return chatStore.chatSelect
})


const isUserChatOnline = computed((): boolean | undefined => {
    return chatStore.isOnline
})
</script>
<template>
    <div class="align-items-center bg-white p-3 position-relative">
        <Icon icon="material-symbols:image-sharp"
            class="text-dark icon-size-1 m-0 p-2 cursor border border-dark border-2" />
        <div class="p-3 w-100">
            <input v-model="contentLast" type="text" id="input-chat-send" class="p-2 m-1 mx-2 w-100"
                placeholder="Enter content chat" v-on:keyup.enter="createConversationUser">
        </div>
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