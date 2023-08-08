<script lang="ts" setup>
import { ref, onMounted ,computed} from 'vue'
import { useRouter } from 'vue-router';
import { Icon } from '@iconify/vue';
import {
    useUserStore , useAuthStore,
    useSettingStore , useSelectLayoutStore ,
    useNotificationStore
} from '@/store'

// component

import NotificationComponent from './../../component/notification/index.vue'

// ref
const router = useRouter()

// store
const userStore = useUserStore()
const authStore = useAuthStore()
const settingStore = useSettingStore()
const selectLayout = useSelectLayoutStore()
const notificationStore = useNotificationStore()
//computed

const listDataNotification = computed ( () : any => {
    return notificationStore.list_notification
})

const showLayout = computed ( () : any => {
  return selectLayout.show
} )
const emailUser = computed(() : string => userStore.userInfo.email )

// method


</script>
<template>
    <div class="layout-notification ">
        <div  v-for="item in listDataNotification" class="d-flex align-items-center mb-2 chat-item " >
            <NotificationComponent   v-if="item.type == 'NTFCT'"
                :email_user_chat="item.email_user_chat"
                :content="item.content"
                :type="item.type"
                :conversation_id="''"
                :is_seem="item.is_seem"
            />
            <NotificationComponent   v-if="item.type == 'NTFCG'"
                :email_user_chat="item.email_user_chat"
                :content="item.content"
                :type="item.type"
                :conversation_id="item.conversation_id"
                :is_seem="item.is_seem"
            />
        </div>
    </div>
</template>
<style>
.layout-notification {
    overflow-y: scroll;
    height: 650px;
}
/* Hide scrollbar for Chrome, Safari and Opera */
.layout-notification::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.layout-notification {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
</style>