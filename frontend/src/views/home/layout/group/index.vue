<script lang="ts" setup>
import { computed , onMounted } from 'vue'
import { Icon } from '@iconify/vue';
import {
    useGroupStore ,
    useSelectLayoutStore ,
    useChatStore ,
    useSocketStore,
    useUserStore ,
} from '@/store'
import {getAllGroup , seemConversation} from '@/api'

// store 

const selectLayoutStore = useSelectLayoutStore()
const chatStore = useChatStore()
const socketStore = useSocketStore()
const userStore = useUserStore()
const groupStore = useGroupStore()
const selectLayout = useSelectLayoutStore()


//computed

const listGroup = computed( () : any => {
    return groupStore.list_group
} )

const emailUser = computed( () : string => {
    return userStore.userInfo.email
})

// method

function showCreateGroup() : void {
    selectLayoutStore.selectLayoutView(2)
    if(window.innerWidth <= 720){
        selectLayout.selectLayoutReponsive(1)
    }
}

function selectChatGroup(conversation_id : string , group_name : string  , group_id : string , list_message_sent : any ){
    socketStore.initSocketChatGroup(conversation_id ,userStore.userInfo.email , group_id)
    chatStore.selectGroupChat(conversation_id , group_name , group_id , list_message_sent)
    seemConversation(conversation_id)
    groupStore.seemConversation(conversation_id , userStore.userInfo.email)
    chatStore.fetchChats()
    selectLayoutStore.selectLayoutView(1)
    if(window.innerWidth <= 720){
        selectLayout.selectLayoutReponsive(1)
    }
}
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
    var predefinedColors = ['#7B68EE', '#E9967A', '#20B2AA', '#33FFFF', '#B0C4DE']; 
    var max = 5
    var min = 1
    var randomInteger = Math.floor(Math.random() * (max - min + 1)) + min
    return {
        backgroundColor : predefinedColors[randomInteger]
    }
}
async function changeWidthContentLast(){
      const [contentConversation  , overflowText , chatImage ]: any = await Promise.all([
        document.querySelector('.group-content'),
        document.querySelectorAll('.text-content-last'),
        document.querySelector('.group-img'),
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
    <div class="d-flex align-items-center p-2 cursor" @click="showCreateGroup">
        <Icon icon="mdi:plus-outline" class="fs-4" />
        <p class="m-0"> Create new group </p>
    </div>
    <p class="py-3">
        <b>Group : </b>
    </p>
    <hr class="my-1">
    <div v-for="item in listGroup" class="d-flex group-content  align-items-center mb-2 chat-item position-relative" >
        <div class="d-flex align-items-center " @click="selectChatGroup(item.id,item.group_name,item.group_id,item.list_message_sent)">
            <div :style="ramdomBG()" 
                class="group-img d-flex justify-content-center align-items-center m-0 me-2  text-white"> 
                <img src="./../../../../assets/images/media/group.png" class="icon-group-items" alt="">
            </div>
            <div class="d-flex flex-column">
                <p class="my-2"> <b class=""> {{ item.group_name }}</b></p>
                <p  v-if="checkSeem(item.list_user_seen) == false" class="m-0 text-content-last text-dark"> 
                    <b > 
                        <span v-if="item.user_chat == emailUser" class="me-1 text-dark">
                            You: 
                        </span> 
                        <span v-else="item.user_chat == emailUser" class="me-1 text-dark">
                            {{ item.user_chat  }}: 
                        </span>
                        <span>{{item.content_last}}</span>
                    </b>
                </p>
                <p  v-if="checkSeem(item.list_user_seen)" class="m-0 text-content-last text-dark"> 
                        <span v-if="item.user_chat == emailUser" class="me-1 text-dark">
                            You: 
                        </span> 
                        <span v-else="item.user_chat == emailUser" class="me-1 text-dark">
                            {{ item.user_chat  }}: 
                        </span>
                        <span>{{item.content_last}}</span>
                </p>
            </div>
        </div>
        <div v-if="checkSeem(item.list_user_seen) == false" class="message-sent-notification text-center">
            <p class="number-notification m-0 text-white"><b>{{ numberMessage(item.list_message_sent) }}</b></p>
        </div>
    </div>
</template>
<style>
.group-img {
    border-radius: 50%;
    background-color: rgb(127, 127, 206);
    width: 67px;
    height: 67px;
    text-align: center;
}
.icon-group-items {
    max-width: 100%;
}
.group-content {
    overflow:  hidden;
    padding: 15px;
}
.message-sent-notification {
    position: absolute;
    top:60%;
    left:0%;
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
@media screen and (max-width: 1024px) {
  p {
    font-size: 14px;
  }
  .group-img{
    width:57px;
    height:57px;
  }
}
@media screen and (max-width: 720px) {
  p {
    font-size: 14px;
  }
  .group-img{
    width:47px;
    height:47px;
  }
}
@media screen and (max-width: 420px) {
  p {
    font-size: 11px;
  }
  .group-img {
    font-size: 11px;
  }
  .group-img{
    width:42px;
    height:42px;
  }
}
</style>