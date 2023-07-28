<script lang="ts" setup>
import {computed} from 'vue'
import { useUserStore } from '@/store';

const userStore = useUserStore()

const user = computed(()=> {
    return userStore.userInfo.name
})
</script>
<template>
    <div class="d-flex flex-column align-items-center w-100 h-100 bg-introduce">
        <h1 class="mt-5"> WelCome</h1>
        <h3> {{ user }} </h3>
        <p class="p-5 w-75">
            We are delighted to welcome you into our amazing chat experience. This online chat site will help you connect and communicate with new people and old friends in an easy and fun way.

            With a simple and friendly interface, you can start chatting right away. Enter your name and start a fun chat with us.

            We respect your privacy and are committed to keeping your personal information secure. Rest assured and enjoy a safe and enjoyable chat experience on our website.

            If you have any questions or encounter any problems during use, please contact us through the support or contact section. We will always be happy to help you.
        </p>
        <div class="row w-75">
            <div class="col-6 d-flex justify-content-center">
                <img src="./../../../../assets/images/media/pexels-ketut-subiyanto-4353617.jpg" alt="" class="img-introduce">
            </div>
            <div class="col-6 d-flex justify-content-center">
                <img src="./../../../../assets/images/media/pexels-ketut-subiyanto-4353618.jpg" alt="" class="img-introduce">
            </div>
        </div>
    </div>
</template>
<style scoped>
.img-introduce {
    max-width: 300px;
    height: auto;
}
.bg-introduce{
    background-image: linear-gradient(45deg,#efefef 25%,rgba(239,239,239,0) 25%,rgba(239,239,239,0) 75%,#efefef 75%,#efefef),linear-gradient(45deg,#efefef 25%,rgba(239,239,239,0) 25%,rgba(239,239,239,0) 75%,#efefef 75%,#efefef) !important;
}
</style>