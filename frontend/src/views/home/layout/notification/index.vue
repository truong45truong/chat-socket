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
    <div v-for="item in listDataNotification" class="d-flex align-items-center mb-2 chat-item" >
        <NotificationComponent   v-if="item.type == 'NTFCT'"
            :email_user_chat="item.email_user_chat" 
            :content="item.content"
            :type="item.type" 
            :group_id="''"
        />
        <NotificationComponent   v-if="item.type == 'NTFCG'"
            :email_user_chat="item.email_user_chat" 
            :content="item.content"
            :type="item.type"
            :group_id="item.group_id"
        />
    </div>
</template>
<style>

</style>