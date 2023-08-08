<script lang="ts" setup>
import { onMounted ,computed  } from 'vue'
import { useRouter } from 'vue-router';
import {useUserStore , useConversationStore} from '@/store'

// interface

interface IProps {
    email_user_from : string,
    email_user_to : string , 
    content_last : string ,
    list_message_sent : Array<any> ,
    list_user_seen : Array<any>,
    user_chat : string
}

// props

const props = defineProps<IProps>()

// ref

const router = useRouter()

// store

const userStore = useUserStore()
const conversationStore = useConversationStore()
// computed

const emailUser = computed(() : string => userStore.userInfo.email )
// method
function numberMessage (list_message_sent : Array<any> ) : number {
    try {
        for( let item of list_message_sent ){
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
        for( let item of list_user_seen ){
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

async function changeWidthContentLast(){
      const [contentConversation  , overflowText , chatImage ]: any = await Promise.all([
        document.querySelector('.conversion-content'),
        document.querySelectorAll('.overflow-text'),
        document.querySelector('.chat-no-image'),
      ])
      overflowText.forEach((element: any) => {
        element.style.width = contentConversation.offsetWidth - chatImage.offsetWidth + "px"
      });

}

onMounted(() => {
  changeWidthContentLast();
  window.addEventListener('resize', changeWidthContentLast);
});

</script>
<template>
    <div class="d-flex conversion-content position-relative">
        <div :style="ramdomBG()" class="chat-no-image text-center p-3 text-white"> <p class="m-0">Chat</p> </div>
        <div class="ms-3 content-info d-flex flex-column align-item-center justify-content-around">
            <p v-if="emailUser == props.email_user_from" class="m-0 text-dark"> <b>{{props.email_user_to}}</b></p>
            <p  v-else="emailUser == props.email_user_to" class="m-0 text-dark"> <b>{{props.email_user_from}}</b></p>

            <p v-if="numberMessage(props.list_message_sent) > 0" class="m-0 overflow-text"> 
                <b > 
                    <span v-if="user_chat == emailUser" class="me-1">
                        You: 
                    </span> 
                    <span class="w-100">{{props.content_last}}</span>
                </b>
            </p>
            <p  v-else="numberMessage(props.list_message_sent) > 0" class="m-0 overflow-text"> 
                <span v-if="user_chat == emailUser" class="me-1">
                        You: 
                    </span> 
                   {{props.content_last}}
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
    padding: 3px 0;
}
.text-content-last {
  white-space: nowrap; 
  text-overflow: ellipsis; 
  max-width: 300px; 
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
  text-overflow: ellipsis; 
}
.text-email-setting {
    max-width: 200px;
}
.conversion-content {
    max-width: 100%;
}

@media screen and (max-width: 720px) {
    .message-sent-notification {
        top:60% !important;
        left:3% !important;
        padding: 0 !important;
    }
    .number-notification {
        font-size: 11px !important;
    }
}
</style>