<script lang="ts" setup>
import { ref, onMounted, computed, watch, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router';
import MenuLayour from './layout/menu/index.vue'
import {
  useUserStore, useBGStore,
  useSettingStore, useChatStore,
  useSelectLayoutStore, useSocketStore,
  useConversationStore, useNotificationStore,
  useMemberShipStore, useGroupStore
} from '@/store'
import {
  getAllMemberShip, getAllNotification,
  createNotification, getAllGroup
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

if (userStore.userInfo.email == "") {
  router.push({ name: 'login' })
}

getAllMemberShip().then((res: any) => {
  membershipStore.uploadData(res.memberships)
})

getAllNotification().then((res: any) => {
  notificationStore.fetchData(res.notifications)
})

getAllGroup().then((res: any) => {
  groupStore.uploadData(res.groups)
})

// computed
const selectLayouReponse = computed((): any => {
  return selectLayout.view_reponsice.isSelectLayouMenu
})
const userEmailComputed = computed((): string => userStore.userInfo.email)
const bgSelect = computed((): any => userBG.imgSelect)
const conversationChat = computed((): any => {
  return chatStore.conversation_id
})
const divStyle = computed(() => {
  return {
    backgroundImage: `url(${bgSelect.value})`,
    backgroundSize: 'cover',
  };
});

const isShowSetting = computed((): boolean => {
  return settingStore.isShowState
})


const notification = computed((): any => {
  return socketStore.notification
})

const isShowLayout = computed((): any => {
  return selectLayout.view_layout
})

const isShowLayouFeature = computed((): any => {
  adjustChatLayoutMenu()
  return selectLayout.show
})

const isShowMenuReponsive = computed((): boolean => {
  return selectLayout.view_show_menu_reponsive.isShowMenu
})
// watch
watch(isShowLayouFeature, (newuserEmailComputed, olduserEmailComputed): void => {
  adjustChatLayoutMenu()
})
watch(userEmailComputed, (newuserEmailComputed, olduserEmailComputed): void => {
  if (newuserEmailComputed == '') {
    router.push({ name: 'login' })
  }
})
watch(notification, (newnotification, oldnotification): void => {
  // console.log('change notify', newnotification )
  if (newnotification.type == "GUO") {
    membershipStore.uploadOnline(newnotification.list_user_online)
  }
  if (newnotification.type == "NTFUO") {
    membershipStore.uploadUserOnline(newnotification.email_user_online)
  }
  if (chatStore.user_to != newnotification.email_user_chat) {
    if (selectLayout.show.isShowNotification == true) {
      notificationStore.uploadData(newnotification, true)
    } else {
      notificationStore.uploadData(newnotification, false)
    }
    if (newnotification.type == 'NTFCT') {
      conversationStore.updateNewMessage(newnotification.content, newnotification.email_user_chat)
      conversationStore.uploadSentMessageConversation(newnotification.email_user_chat, userStore.userInfo.email)
    }
    if (newnotification.type == 'NTFOU') {

    }
  }
  if (newnotification.type == 'NTFCG') {
    let conversationGroup = groupStore.getGroupById(newnotification.group_id)
    if (
      conversationGroup != false
      && conversationGroup.conversation_id != chatStore.conversation_id
    ) {
      groupStore.updateNewMessage(
        newnotification.content, newnotification.group_id,
        newnotification.email_user_chat, userStore.userInfo.email)
      if (
        userStore.userInfo.email != newnotification.email_user_chat
        && chatStore.group_id != newnotification.group_id
      ) {
        groupStore.uploadSentMessageConversation(newnotification.group_id, userStore.userInfo.email)
      }
    }
  }
  if(newnotification.type == 'NTFCREATE'){
    if(newnotification.is_chat == true){
      conversationStore.fetchData()
      console.log('conversationStore.fetchData()')
    }
    if(newnotification.is_chat == false){
      groupStore.fetchDataGroup()
    }
  }
})

// ref

const isShowMenuReponse = ref<boolean>(false)
const chatLayoutHeight = ref<any>('100%');

const widthLayoutSetting = ref<any>('100%')

async function adjustChatLayoutHeight() {
  const [ListChatLayoutHeight, InputChatLayoutHeight]: any = await Promise.all([
    document.querySelector('#list-chat-layout'),
    document.querySelector('#chat-input-layout'),
  ])
  const chatLayoutHeightValue = {
    height: `calc(100% - ${InputChatLayoutHeight.offsetHeight}px)`
  }
  chatLayoutHeight.value = chatLayoutHeightValue;
}

async function adjustChatLayoutMenu() {
  try {
    if (window.innerWidth < 1024) {
      const chatLayoutWidthValue = {
        width: '250px'
      }
      widthLayoutSetting.value = chatLayoutWidthValue;
      if (window.innerWidth > 1024) {
        widthLayoutSetting.value = {
          width: '300px'
        }
      }
      if (window.innerWidth <= 720) {
        const [LayoutMenuSetting, LayoutMenu]: any = await Promise.all([
          document.querySelector('#layout-menu-setting'),
          document.querySelector('#layout-menu'),
        ])
        const chatLayoutWidthValue = {
          width: `calc(100% - ${LayoutMenuSetting.offsetWidth}px)`
        }
        widthLayoutSetting.value = chatLayoutWidthValue;
      }
    }
  }
  catch (e) {

  }

}


async function changeWidthContentLast() {
  const [contentConversation, overflowText, chatImage]: any = await Promise.all([
    document.querySelector('.conversion-content'),
    document.querySelectorAll('.overflow-text'),
    document.querySelector('.chat-no-image'),
  ])
  overflowText.forEach((element: any) => {
    element.style.width = contentConversation.offsetWidth - chatImage.offsetWidth + "px"
  });

}
async function changShowMenuResponsive() {
  if (window.innerWidth <= 720) {
    isShowMenuReponse.value = true
  } else {
    isShowMenuReponse.value = false
  }
}
// Lifecycle hook mounted
onMounted(() => {
  adjustChatLayoutHeight();
  adjustChatLayoutMenu();
  changeWidthContentLast();
  changShowMenuResponsive()
  window.addEventListener('resize', adjustChatLayoutHeight);
  window.addEventListener('resize', adjustChatLayoutMenu);
  window.addEventListener('resize', changeWidthContentLast);
  window.addEventListener('resize', changShowMenuResponsive);
});

// Lifecycle hook beforeUnmount
onBeforeUnmount(() => {
  window.removeEventListener('resize', adjustChatLayoutHeight);

});

</script>
<template>
  <main class="bg-login d-flex w-100 position-relative" :style="divStyle">
    <div id="layout-menu-setting" class="col-feature ">
      <MenuSettingLayout />
    </div>
    <div :style="widthLayoutSetting" id="layout-menu" :class="{ 'col-feature-2-hide': selectLayouReponse }"
      class="col-feature-2 d-flex flex-column position-relative layout-menu h-100 justify-content-between border p-0 m-0 border-2 border-dark border-start-0 border-top-0 border-bottom-0">
      <MenuLayour />
    </div>
    <div class="col layout-chat d-flex flex-column position-relative layout-chat h-100 p-0">
      <ChatLayout v-if="conversationChat && isShowLayout.isShowConversation" :style="chatLayoutHeight"
        class="d-flex flex-column bg-white" />
      <IntroductLayout v-if="!conversationChat && !isShowLayout.isShowCreateGroup" :style="chatLayoutHeight"
        class="d-flex flex-column bg-white" />
      <CreateGroupLayout v-if="isShowLayout.isShowCreateGroup" />
      <ChatInputLayout v-if="!isShowLayout.isShowCreateGroup" :id="'chat-input-layout'" />
    </div>
    <SettingLayout v-if="isShowSetting" class="position-fixed setting-layout" />
  </main>
</template>
<style>
html,
body {
  height: 100%;
  margin: 0;
}

.bg-login {
  height: 100%;

  background: url('./../../../src/assets/images/display/bg-4.jpg');
}

#app {
  height: 100%;
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
.layout-chat>* {
  margin: 0;
  padding: 0;
}

.col-feature {
  max-width: 80px;
  background-color: #0091ff;
}

.col-feature-2 {
  width: 400px;
}

@media screen and (max-width: 1024px) {
  p {
    font-size: 14px;
  }
}

@media screen and (max-width: 720px) {
  .col-feature-2 {
    width: 100%;
    position: fixed !important;
    right: 0%;
    z-index: 99;
  }

  .col-feature-2-hide {
    right: 100%;
  }
}</style>