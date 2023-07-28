<script lang="ts" setup>
import { ref , computed , onMounted , onUpdated , watch  } from 'vue'
import { useRouter } from 'vue-router';
import { Icon } from '@iconify/vue';
import {
    useChatStore , useUserStore , 
    useBGStore , useSocketStore ,
    useConversationStore ,
    useNotificationStore ,
    useMemberShipStore ,
} from '@/store'
import { addMemberShip } from '@/api';
const router = useRouter()
const chatLayout = ref(null);

// store

const chatStore = useChatStore()
const userStore = useUserStore()
const userBG = useBGStore()
const socketStore = useSocketStore()
const membershipStore = useMemberShipStore()

// computed

const userChatSelect = computed( () : string | undefined => {
    return chatStore.chatSelect
})

const isGroupChat = computed( () : boolean | undefined => {
    return chatStore.is_group
} )

const nameGroup = computed ( () : string | undefined => {
    return chatStore.group_name
})
const isUserChatOnline = computed( () : boolean | undefined => {
    return chatStore.isOnline
})
const listChatSelected = computed(() : any | undefined => {
    return chatStore.list_chat
})
const userCurrent = computed(() : string | undefined => {
    return userStore.userInfo.email
})

const listChatReceiver = computed( () : any => {
    return socketStore.list_chat_receiver
} )

const bgSelect = computed( () : string => userBG.imgSelect)


const divStyle = computed(() => {
  return {
    backgroundImage: `url(${bgSelect.value})`,
    backgroundSize: 'cover',
  };
});

onUpdated(() => {
  if (chatLayout.value) {
    chatLayout.value.scrollTo(0, chatLayout.value.scrollHeight);
  }
});

// method 
function checkIsFriend() : boolean {
    if (membershipStore.checkMemberShip(chatStore.user_to) == true){
        return true
    }
    return false
}
const isFriend = ref<boolean>(checkIsFriend())

async function addFriend(user_to : string) : Promise<void> {
    await addMemberShip(user_to).then( (res : any) => {
        if(res.success == true){
            membershipStore.addFriend(user_to)
        }
    })
    isFriend.value = checkIsFriend()
}   
async function removeFriend(user_to : string) : Promise<void> {
    await addMemberShip(user_to).then( (res : any) => {
        if(res.success == true){
            membershipStore.removeFriend(user_to)
        }
    })
    isFriend.value = checkIsFriend()
}

// watch 

watch( userChatSelect , (newuserChatSelect , olduserChatSelect) : void => {
        isFriend.value = checkIsFriend()
} )

</script>
<template>
    <div :style="divStyle" :id="'list-chat-layout'">
        <div v-if="!isGroupChat"  class="d-flex align-items-center p-2 border border-2 border-dark
        border-top-0 border-start-0 border-end-0 bg-white justify-content-between ">
            <div class="d-flex align-items-center ">
                <div class="ms-3 d-flex flex-column align-item-center justify-content-around">
                    <p  class="m-0 text-dark"> <b>{{userChatSelect}}</b></p>
                </div>
                <Icon icon="carbon:circle-filled" class="ms-3 color-online" />
                <p v-if="isUserChatOnline == true" class="m-0 ms-1 color-online"> Online</p>
                <p v-if="isUserChatOnline == false" class="m-0 ms-1 color-online"> Offline</p>
            </div>
            <div  v-if="isFriend == false" class="d-flex align-items-center cursor" @click="addFriend(userChatSelect)">
                <p  class="m-0 text-primary"> Add</p>
                <Icon icon="fluent-mdl2:add-friend" class="mx-3 text-primary fs-4" />
            </div>
            <div v-if="isFriend == true"  class="d-flex align-items-center cursor"  @click="removeFriend(userChatSelect)">
                <p class="m-0 text-primary mx-3">Cancel Friend</p>
            </div>
        </div>
        <div v-if="isGroupChat == true"  class="d-flex align-items-center p-2 border border-2 border-dark
        border-top-0 border-start-0 border-end-0 bg-white justify-content-between ">
            <div class="d-flex align-items-center ">
                <div class="ms-3 d-flex flex-column align-item-center justify-content-around">
                    <p  class="m-0 text-dark"> <b>{{nameGroup}}</b></p>
                </div>     
            </div>
        </div>
        <div class="layout-chat" id="conversation-chat-layout" ref="chatLayout" >
            <div v-for="item in listChatSelected " class="row mt-2">
                <div class="col-6 d-flex justify-content-start ps-3">
                    <div v-if="userCurrent != item.email_user_chat " class="chat-no-image text-center p-3 text-white border border-dark border-2"> Chat </div>
                    <div v-if="userCurrent != item.email_user_chat " class="chat-no-current ms-2 p-3 mb-3">
                        <p class="m-0 text-start text-dark">{{item.content}}</p>
                    </div>
                </div>
                <div class="col-6 d-flex justify-content-end pe-4">
                    <div v-if="userCurrent == item.email_user_chat " class="chat-current p-3 mb-3">
                        <p class="m-0 text-end text-white">{{item.content}}</p>
                    </div>
                </div>
            </div>
            <div v-for="item in listChatReceiver " class="row mt-2">
                <div class="col-6 d-flex justify-content-start ps-3">
                    <div v-if="userCurrent != item.email_user_chat " class="chat-no-image text-center p-3 text-white border border-dark border-2"> Chat </div>
                    <div v-if="userCurrent != item.email_user_chat " class="chat-no-current ms-2 p-3 mb-3">
                        <p class="m-0 text-start text-dark">{{item.content}}</p>
                    </div>
                </div>
                <div class="col-6 d-flex justify-content-end pe-4">
                    <div v-if="userCurrent == item.email_user_chat " class="chat-current p-3 mb-3">
                        <p class="m-0 text-end text-white">{{item.content}}</p>
                    </div>
                </div>
            </div>
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

    background: url('./../../../../assets/images/display/bg-1.jpg');
}
#app {
    height:100%;
}
.color-online {
    color :rgb(14, 160, 50)
}
.layout-chat {
    overflow-y: scroll;
}
/* Hide scrollbar for Chrome, Safari and Opera */
.layout-chat::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.layout-chat {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
.chat-current {
    width:fit-content;
    background-color: black;
    justify-content: end;
    border-radius: 15px;
}
.chat-no-current {
    background-color: aliceblue;
    width:fit-content;
    border-radius: 15px;
}
.chat-no-image {
    width:67px;
    height:67px;
}
</style>