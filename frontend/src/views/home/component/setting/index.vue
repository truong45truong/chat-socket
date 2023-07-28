<script lang="ts" setup>
import { ref, onMounted ,computed} from 'vue'
import { useRouter } from 'vue-router';
import { Icon } from '@iconify/vue';
import {useUserStore , useAuthStore, useSettingStore} from '@/store'

// ref
const router = useRouter()

// store
const userStore = useUserStore()
const authStore = useAuthStore()
const settingStore = useSettingStore()

// computed

const emailUser = computed(() : string => userStore.userInfo.email )

// method

function logout(): void {
    userStore.resetUserInfo()
    authStore.removeAuth()
}

function showSetting() : void {
    settingStore.showSetting()
}
onMounted(() => {


})
</script>
<template>
    <div class="d-flex justify-content-between w-100">
        <div class="d-flex bg-dark w-100 p-3 align-items-center cursor" @click="logout">
            <Icon icon="material-symbols:logout" class="text-white" />
            <p class="m-0 ms-2 text-white"> Logout</p>
        </div>
        <div class="d-flex bg-dark p-3 align-items-center cursor" @click="showSetting">
            <Icon icon="uiw:setting" class="text-white  " />
            <p class="m-0 ms-2 text-white"> Setting</p>
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
.overflow-text {
  white-space: nowrap; 
  overflow: hidden;
  text-overflow: ellipsis; 
}
.text-email-setting {
    max-width: 200px;
}
</style>