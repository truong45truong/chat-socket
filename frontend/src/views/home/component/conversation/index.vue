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
    content_last : string ,
    list_message_sent : Array<any> ,
    list_user_seen : Array<any>
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
function numberMessage (list_message_sent : Array<any> ) : number {
    try {
        console.log(list_message_sent, typeof list_message_sent)
        for( let item of list_message_sent ){
            console.log("item:", item , typeof item);
            const convertedDict = JSON.parse(item.replace(/'/g, '"'));   
            var keys =Object.keys(convertedDict)
            if( keys[0] ==  userStore.userInfo.email ){
                return convertedDict[keys[0]]
            }
        }

    // Now `convertedDict` is an actual dictionary (object)
    return 0
    } catch (error) {
        console.log("errror number message" , error)
       return  0
    }
} 
function checkSeem (list_user_seen : Array<any>) : boolean {
    try {
        console.log(list_user_seen, typeof list_user_seen)
        for( let item of list_user_seen ){
            console.log( item ,  userStore.userInfo.email )
            if( item ==  userStore.userInfo.email ){
                return true
            }
        }

    // Now `convertedDict` is an actual dictionary (object)
    return false
    } catch (error) {
       return  false
    }
}
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
    <div class="d-flex w-100 position-relative">
        <div :style="ramdomBG()" class="chat-no-image text-center p-3 text-white"> Chat </div>
        <div class="ms-3 d-flex flex-column align-item-center justify-content-around">
            <p v-if="emailUser == props.email_user_from" class="m-0 text-dark"> <b>{{props.email_user_to}}</b></p>
            <p  v-else="emailUser == props.email_user_to" class="m-0 text-dark"> <b>{{props.email_user_from}}</b></p>

            <p  v-if="!props.is_seen" class="m-0 text-content-last"> 
                <b > 
                    <span>{{props.content_last}}</span>
                </b>
            </p>
            <p  v-if="props.is_seen" class="m-0"> 
                    <span v-if="!props.is_sent" >{{props.content_last}}</span>
                    <span v-if="props.is_sent" > You : {{props.content_last}}</span>
            </p>
    
        </div>
        <div v-if="checkSeem(props.list_user_seen) == false" class="message-sent-notification text-center">
            <p class="number-notification m-0 text-white"><b>{{ numberMessage(props.list_message_sent) }}</b></p>
        </div>
    </div>
</template>
<style>
.message-sent-notification {
    position: absolute;
    top:60%;
    left:40px;
}
.number-notification {
    font-size: 14px;
}
.text-content-last {
  white-space: nowrap; /* Ngăn không cho chữ xuống dòng */
  overflow: hidden; /* Ẩn phần vượt quá khung của p */
  text-overflow: ellipsis; /* Thêm dấu "..." vào cuối văn bản bị cắt */
  max-width: 100%; /* Đảm bảo chiều rộng tối đa của p không vượt quá cha của nó */
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