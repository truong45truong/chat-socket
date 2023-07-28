<script lang="ts" setup>
import { ref, onMounted ,computed , defineProps } from 'vue'
import { useRouter } from 'vue-router';
import { Icon } from '@iconify/vue';
import {useUserStore , useAuthStore, useSettingStore} from '@/store'

// interface

interface IProps {
    email_user_from : string,
    email_user_to : string , 
    is_seen : boolean ,
    is_sent : boolean ,
    content_last : string 
}

// props

const props = defineProps<IProps>()

// ref

const router = useRouter()

// store

const userStore = useUserStore()

// computed

const emailUser = computed(() : string => userStore.userInfo.email )

// method

function ramdomBG() : any {
    var predefinedColors = ['#7B68EE', '#E9967A', '#20B2AA', '#BC8F8F', '#B0C4DE']; 
    var max = 5
    var min = 1
    var randomInteger = Math.floor(Math.random() * (max - min + 1)) + min
    return {
        backgroundColor : predefinedColors[randomInteger]
    }
}

</script>
<template>
    <div class="d-flex w-100">
        <div :style="ramdomBG()" class="chat-no-image text-center p-3 text-white"> Chat </div>
        <div class="ms-3 d-flex flex-column align-item-center justify-content-around">
            <p v-if="emailUser == props.email_user_from" class="m-0 text-dark"> <b>{{props.email_user_to}}</b></p>
            <p  v-else="emailUser == props.email_user_to" class="m-0 text-dark"> <b>{{props.email_user_from}}</b></p>

            <p  v-if="!props.is_seen" class="m-0"> 
                <b > 
                    <span>{{props.content_last}}</span>
                </b>
            </p>
            <p  v-if="props.is_seen" class="m-0"> 
                    <span v-if="!props.is_sent" >{{props.content_last}}</span>
                    <span v-if="props.is_sent" > You : {{props.content_last}}</span>
            </p>
    
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