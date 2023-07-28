<script lang="ts" setup>
import { ref, onMounted, computed , watch , onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router';
import MenuLayour from './layout/menu/index.vue'
import {
        useUserStore , useBGStore , 
        useSettingStore , useChatStore ,
        useSelectLayoutStore , useSocketStore,
        useConversationStore , useNotificationStore ,
        useMemberShipStore , useGroupStore
} from '@/store'
import { 
        getAllMemberShip , getAllNotification ,
        createNotification , getAllGroup
} from '@/api';

// layout

import ChatLayout from './layout/chat/index.vue'
import ChatInputLayout from './layout/ChatInput/index.vue'
import SettingLayout from './layout/setting/index.vue'
import MenuSettingLayout from './layout/menuFeature/index.vue'
import IntroductLayout from './layout/introduce/index.vue'
import CreateGroupLayout from './layout/groupCreate/index.vue'

const router = useRouter()

// storeIntroductLayout

const userStore = useUserStore()
const userBG = useBGStore()
const settingStore = useSettingStore()
const chatStore = useChatStore()
const socketStore = useSocketStore()
socketStore.initSocketNotification(userStore.userInfo.email)
const conversationStore = useConversationStore()
const notificationStore = useNotificationStore()
const membershipStore = useMemberShipStore()
const selectLayout = useSelectLayoutStore()
const groupStore = useGroupStore()

// fetch data

getAllMemberShip().then((res : any) => {
  membershipStore.uploadData(res.memberships)
})

getAllNotification().then( (res : any) => {
  notificationStore.fetchData( res.notifications )
})

getAllGroup().then( (res : any) => {
    groupStore.uploadData(res.groups)
} )

// computed

const userEmailComputed = computed( () : string => userStore.userInfo.email)
const bgSelect = computed( () : string => userBG.imgSelect)
const conversationChat = computed ( () : string | undefined => {
  return chatStore.conversation_id
})
const divStyle = computed(() => {
  return {
    backgroundImage: `url(${bgSelect.value})`,
    backgroundSize: 'cover',
  };
});

const isShowSetting = computed( () : boolean => {
    return settingStore.isShowState
})


const notification = computed( (): any => {
    return socketStore.notification
})

const isShowLayout = computed( () : any => {
  return selectLayout.view_layout
})
// watch
watch( userEmailComputed , (newuserEmailComputed , olduserEmailComputed) : void => {
    if (newuserEmailComputed == ''){
        router.push({name : 'login'})
    }
} )
watch( notification , (newnotification , oldnotification) : void => {
    console.log("change notify" ,newnotification )
    notificationStore.uploadData(newnotification)
    if(newnotification.type == 'NTFCT'){
      conversationStore.updateNewMessage( newnotification.content , newnotification.email_user_chat )
    }
    createNotification(
      newnotification.content , 
      newnotification.group_id,
      newnotification.email_user_chat ,
      newnotification.type
    )

} )

//
const chatContainer = ref<HTMLElement | null>(null);
const ChatInput = ref<HTMLElement | null>(null);
const chatLayoutHeight = ref('100%');


async function  adjustChatLayoutHeight() {
    const [ListChatLayoutHeight, InputChatLayoutHeight] = await Promise.all([
    document.querySelector('#list-chat-layout'),
    document.querySelector('#chat-input-layout'),
    ])
    const chatLayoutHeightValue = {
        height : `calc(100% - ${InputChatLayoutHeight.offsetHeight}px)`
    }
    chatLayoutHeight.value = chatLayoutHeightValue;
}

// Lifecycle hook mounted
onMounted(() => {
  adjustChatLayoutHeight();
  window.addEventListener('resize', adjustChatLayoutHeight);
});

// Lifecycle hook beforeUnmount
onBeforeUnmount(() => {
  window.removeEventListener('resize', adjustChatLayoutHeight);
});

// const socket = io("http://0.0.0.0:8000/ws/notification/9e9fdbf5-6b66-49d9-b90e-23fff3dbfb9e/");

//   // Sự kiện khi kết nối thành công
//   socket.on('connect', () => {
//     console.log('Connected to server');
//   });

//   // Sự kiện khi nhận được dữ liệu từ server
//   socket.on('my_response', (data) => {
//     console.log('Received data from server:', data);
//   });

//   // Gửi dữ liệu tới server
//   socket.emit('my_event', { message: 'Hello from client' });


</script>
<template>
    <main class="bg-login d-flex w-100" :style="divStyle">
      <div class="col-feature ">
        <MenuSettingLayout />
      </div>
      <div class="col-feature-2 d-flex flex-column position-relative layout-menu h-100 justify-content-between border p-0 m-0 border-2 border-dark border-start-0 border-top-0 border-bottom-0">
        <MenuLayour />
      </div>
      <div  class="col layout-chat d-flex flex-column position-relative layout-chat h-100 p-0">
        <ChatLayout v-if="conversationChat && isShowLayout.isShowConversation" :style="chatLayoutHeight" class="d-flex flex-column bg-white" />
        <IntroductLayout v-if="!conversationChat && !isShowLayout.isShowCreateGroup" :style="chatLayoutHeight"  class="d-flex flex-column bg-white" />
        <CreateGroupLayout v-if="isShowLayout.isShowCreateGroup" />
        <ChatInputLayout v-if="!isShowLayout.isShowCreateGroup" :id="'chat-input-layout'"  />
      </div>
      <SettingLayout v-if="isShowSetting" class="position-fixed setting-layout" />
    </main>
  </template>
<style>
html, body {
  height: 100%;
  margin :0;
}
.bg-login {
    height:100%;

    background: url('./../../../src/assets/images/display/bg-4.jpg');
}
#app {
    height:100%;
}
.layout-menu {
    background-color: rgba(255, 255, 255, 1);
}
.setting-layout {
    width: 400px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}


.chat-layout {
  flex-grow: 1;
}

/* Loại bỏ padding và margin của các phần tử con trong layout-chat */
.layout-chat > * {
  margin: 0;
  padding: 0;
}
.col-feature {
  max-width: 80px;
  background-color: #0091ff;
}
.col-feature-2 {
  width: 300px;
}
</style>