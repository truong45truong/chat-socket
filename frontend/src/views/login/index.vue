<script lang="ts" setup>
import {  ref, onMounted } from 'vue'
import { useRouter } from 'vue-router';
import LayoutLogin from './layout/index.vue'
import {useUserStore} from '@/store'
const router = useRouter()

const userStore = useUserStore()
onMounted(() => {

    if( userStore.userInfo.email){
        router.push({name : 'home'})
    }

})
</script>
<template>
    <main class="bg-login">
        <LayoutLogin />
    </main>
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

</style>