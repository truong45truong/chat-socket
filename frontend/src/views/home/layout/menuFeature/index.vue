<script lang="ts" setup>
import { ref, onMounted ,computed} from 'vue'
import { useRouter } from 'vue-router';
import { Icon } from '@iconify/vue';
import {
    useUserStore , useAuthStore,
    useSettingStore , useSelectLayoutStore,
    useNotificationStore , useConversationStore,
    useGroupStore
} from '@/store'

// ref
const router = useRouter()

// store
const userStore = useUserStore()
const authStore = useAuthStore()
const settingStore = useSettingStore()
const selectLayout = useSelectLayoutStore()
const notificationStore = useNotificationStore()
const conversationStore = useConversationStore()
const groupStore = useGroupStore()

//computed


const showLayout = computed ( () : any => {
  return selectLayout.show
} )

const emailUser = computed(() : string => userStore.userInfo.email )

const numberNotification = computed ( () : number => {
    return notificationStore.number_notification 
} )

// method

function logout(): void {
    userStore.resetUserInfo()
    authStore.removeAuth()
}

function showSetting() : void {
    settingStore.showSetting()
}
function selectLayoutContent( type : number) : void {
    if(window.innerWidth < 720){
        if(selectLayout.view_reponsice.isSelectLayouMenu == true){   
            selectLayout.selectLayoutReponsive(2)
        } else {
            
            switch(type){
                case 1:{
                    if( selectLayout.show.isShowChat ) {
                        selectLayout.selectLayoutReponsive(1)
                    } 
                    break;
                }
                case 2:{
                    if( selectLayout.show.isShowGroup ){
                        selectLayout.selectLayoutReponsive(1)
                    } 
                    break
                }
                case 3:
                    if( selectLayout.show.isShowFriend ){
                        selectLayout.selectLayoutReponsive(1)
                    }
                    break
                case 4:
                    if( selectLayout.show.isShowNotification ){
                        selectLayout.selectLayoutReponsive(1)
                    }
                    break
            }
        }
    }
    selectLayout.selectLayout(type)
    if(type == 4){
        notificationStore.seem()
    }
}
</script>
<template>
    <div class="d-flex flex-column align-items-center  justify-content-between w-100 h-100">
        <div class="d-flex flex-column w-100">
                <div class="cursor img-user border border-2 border-white text-center mt-4 mx-2">
                    <Icon icon="mingcute:user-2-line"  class="text-white icon-user-menu" />
                </div>
            <div class="text-center w-100 mt-5">
                <div :class="{ 'bg-feature-activate' : showLayout.isShowChat }" 
                class="feature-option position-relative"
                @click="selectLayoutContent(1)" >
                    <Icon icon="material-symbols:chat" class="text-white fs-3" />
                    <div v-if="conversationStore.getNumberNotification(emailUser) > 0" 
                        class="position-absolute number-notification">
                        <p class="text-white m-0"><b>{{ conversationStore.getNumberNotification(emailUser) }}</b></p>
                    </div>
                </div>
                <div :class="{ 'bg-feature-activate' : showLayout.isShowGroup }" 
                class="feature-option position-relative"
                @click="selectLayoutContent(2)" >
                    <Icon icon="clarity:group-line" class="text-white fs-3" />
                    <div v-if="groupStore.getNumberNotification(emailUser) > 0" 
                        class="position-absolute number-notification">
                        <p class="text-white m-0"><b>{{ groupStore.getNumberNotification(emailUser) }}</b></p>
                    </div>
                </div>
                <div :class="{ 'bg-feature-activate' : showLayout.isShowFriend }" 
                class="feature-option"
                @click="selectLayoutContent(3)" >
                    <Icon icon="system-uicons:contacts"  class="text-white fs-3" />
                </div>
                <div :class="{ 'bg-feature-activate' : showLayout.isShowNotification }" 
                class="feature-option position-relative"
                @click="selectLayoutContent(4)" >
                    <Icon icon="iconamoon:notification-fill"  class="text-white fs-3" />
                    <div v-if="numberNotification > 0" 
                        class="position-absolute number-notification">
                        <p class="text-white m-0"><b>{{ numberNotification }}</b></p>
                    </div>
                </div>
            </div>

        </div>
        <div class="    ">
            <div class="cursor mt-2 mb-3" @click="logout">
                <Icon icon="material-symbols:logout" class="text-white fs-3" />
            </div>
        </div>
    </div>
</template>
<style>
.number-notification {
    background-color: rgb(243, 70, 70);
    width: 27px;
    height: 27px;
    border-radius: 50%;
    top:10px;
}
.feature-option {
    cursor: pointer;
    padding: 20px 0px;
}
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
.img-user {
    width: 50px;
    height: 50px;
    padding: 10px 5px;
    border-radius: 50%;
}
.icon-user-menu {
    font-size: 24px;
}
.bg-feature-activate {
    background-color: #1577c2 ;
}
@media screen and (max-width: 720px) {
    .feature-option {
        padding: 10px 0px;
    }
    .img-user {
        width: 35px;
        height: 35px;
        padding : 0;
    }
    .icon-user-menu {
        font-size: 16px;
    }
    .number-notification {
        width: 20px;
        height: 20px;
        padding: 2px;
    }
    .number-notification p {
        font-size: 10px;
    }
}
</style>