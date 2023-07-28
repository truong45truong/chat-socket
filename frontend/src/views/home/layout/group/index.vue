<script lang="ts" setup>
import { computed } from 'vue'
import { Icon } from '@iconify/vue';
import {
    useGroupStore ,
    useSelectLayoutStore ,
    useChatStore ,
    useSocketStore,
    useUserStore ,
} from '@/store'
import {getAllGroup} from '@/api'

// store 

const selectLayoutStore = useSelectLayoutStore()
const chatStore = useChatStore()
const socketStore = useSocketStore()
const userStore = useUserStore()
const groupStore = useGroupStore()

//computed

const listGroup = computed( () : any => {
    return groupStore.list_group
} )


// method

function showCreateGroup() : void {
    selectLayoutStore.selectLayoutView(2)
}

function selectChatGroup(conversation_id : string , group_name : string  , group_id : string ){
    socketStore.initSocketChatGroup(conversation_id ,userStore.userInfo.email , group_id)
    chatStore.selectGroupChat(conversation_id , group_name , group_id)
    chatStore.fetchChats()
    selectLayoutStore.selectLayoutView(1)
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
    <div v-for="item in listGroup" class="d-flex align-items-center mb-2 chat-item" >
        <div class="d-flex align-items-center " @click="selectChatGroup(item.id,item.group_name,item.group_id)">
            <p :style="ramdomBG()" class="group-img  m-0 me-2 text-white"> Group </p>
            <p class="my-2"> <b class=""> {{ item.group_name }}</b></p>
        </div>
    </div>
</template>
<style>
.group-img {
    border-radius: 50%;
    background-color: rgb(127, 127, 206);
    padding : 20px 10px;
}
</style>