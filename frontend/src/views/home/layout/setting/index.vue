<script lang="ts" setup>
import { ref, onMounted ,computed} from 'vue'
import { useRouter } from 'vue-router';
import { Icon } from '@iconify/vue';
import {
    useUserStore , useAuthStore , 
    useBGStore , useSettingStore ,
    useConversationStore
} from '@/store'

// ref
const router = useRouter()

// store

const userStore = useUserStore()
const authStore = useAuthStore()
const BgStore = useBGStore()
const settingStore = useSettingStore()

// computed

const dataBG = computed( (): any => {
    return BgStore.listDisplay
})
// method
function logout(): void {
    userStore.resetUserInfo()
    authStore.removeAuth()
}
function selectBG(url){
    BgStore.setBG(url)
}
function hideSetting(){
    settingStore.hideSetting()
}
onMounted(() => {


})
</script>
<template>

    <div class="d-flex flex-column bg-white p-3 shadow">
        <button class="d-flex align-items-center border border-dark btn-cancel-setting" @click="hideSetting">
            <Icon icon="entypo:back" class="fs-2 me-2" />
            <p class="m-0"> CANCEL</p>
        </button>
        <hr class="mt-2">
        <p class="text-dark mt-2"><b> Background:  </b></p>
       <div class="row">
        <div v-for="item,index in dataBG" class="col-6 mt-2 img-col d-flex flex-column align-items-center justify-content-center">
            <img :src="item.url" :alt="index" class=" img-display">
            <button class="btn-select-bg px-3 py-2 cursor mt-2" @click="selectBG(item.url)">
                Select
            </button>
        </div>
       </div>
    </div>
</template>
<style scoped>
.btn-select-bg {
    background-color: white;
    border-radius: 15px;
    
}
.img-display {
    max-width: 200px;
    height : 150px;

}
.btn-cancel-setting {
    width :fit-content;
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