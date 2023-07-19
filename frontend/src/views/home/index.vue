<script lang="ts" setup>
import { ref, onMounted, computed , watch } from 'vue'
import { useRouter } from 'vue-router';
import MenuLayour from './layout/menu/index.vue'
import SettingComponent from './component/setting/index.vue'
import { useUserStore , useBGStore , useSettingStore} from '@/store'
import ChatLayout from './layout/chat/index.vue'
import ChatInputLayout from './layout/ChatInput/index.vue'
import SettingLayout from './layout/setting/index.vue'
const router = useRouter()
// store
const userStore = useUserStore()
const userBG = useBGStore()
const settingStore = useSettingStore()

//computed
const userEmailComputed = computed( () : string => userStore.userInfo.email)
const bgSelect = computed( () : string => userBG.imgSelect)

const divStyle = computed(() => {
  return {
    backgroundImage: `url(${bgSelect.value})`,
    backgroundSize: 'cover',
  };
});

const isShowSetting = computed( () : boolean => {
    return settingStore.isShowState
})


// watch
watch( userEmailComputed , (newuserEmailComputed , olduserEmailComputed) : void => {
    if (newuserEmailComputed == ''){
        router.push({name : 'login'})
    }
} )
</script>
<template>
    <main class="bg-login row w-100" :style="divStyle"> 
        <div class="col-sm-3 d-flex flex-column position-relative layout-menu h-100 justify-content-between 
                    border p-0 m-0 border-2 border-dark border-start-0 border-top-0 border-bottom-0">
            <MenuLayour />
            <SettingComponent />
        </div>
        <div class="col layout-chat d-flex flex-column position-relative layout-chat h-100 justify-content-between p-0">
            <ChatLayout />
            <ChatInputLayout />
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
</style>