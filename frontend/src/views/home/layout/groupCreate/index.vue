<script lang="ts" setup>
import { computed , ref } from 'vue'
import { Icon } from '@iconify/vue';
import {
    useGroupStore , useChatStore ,
    useUserStore , useSocketStore ,
    useSelectLayoutStore , 
} from '@/store'
import {createGroup, getAllGroup , searchUser} from '@/api'

// ref

const nameGroupCreate = ref<string>('')
const descriptionGroupCreate = ref<string>('')
const listUserSearch = ref<any>([])
const listUserAddGroup = ref<any>([])
const showErrorNameGroup = ref<boolean>(false)
const showErrorUserSelect = ref<boolean>(false)
const keySearch = ref<string>('')

// store 

const groupStore = useGroupStore()
const chatStore = useChatStore()
const userStore = useUserStore()
const socketStore = useSocketStore()
const selectLayout = useSelectLayoutStore()

// fetch data
getAllGroup().then( (res : any) => {
    groupStore.uploadData(res.groups)
} )


//computed

const listGroup = computed( () : any => {
    return groupStore.list_group
} )


// method

function search(): void {
    searchUser(keySearch.value).then((res : any ) => {
        listUserSearch.value = res.users 
    })
}
function addUserGroup (email: string) : void {
    var check = false
    listUserAddGroup.value.filter( (item: any) => {
        if (item == email) {
            check = true
        }
    } )
    if( check == false) listUserAddGroup.value.push(email)
}
function removeUserGroup( email : string ) : void {
    listUserAddGroup.value=listUserAddGroup.value.filter( (item : any) => {
        return item != email
    } )
}
function isNullOrWhitespace(input: string): boolean {
  return !input || /^\s*$/.test(input);
}
function createNewGroup() : void {
    if ( isNullOrWhitespace(nameGroupCreate.value) == true ){ 
        showErrorNameGroup.value = true
    }
    else showErrorNameGroup.value = false;
    if ( listUserAddGroup.value.length == 0) showErrorUserSelect.value = true;
    else showErrorUserSelect.value = false;
    if ( showErrorUserSelect.value == false && showErrorNameGroup.value == false ){
        createGroup(  nameGroupCreate.value , listUserAddGroup.value ,  descriptionGroupCreate.value  ).then( async (res: any) => {
            let conversation_id = res.conversation.id
            groupStore.fetchDataGroup()
            await socketStore.initSocketChatGroup(
                conversation_id ,userStore.userInfo.email , 
                res.conversation.group_id
            )
            chatStore.selectGroupChat(
                conversation_id , res.conversation.group_name , 
                res.conversation.group_id , res.conversation.list_message_sent
            )
            groupStore.seemConversation(conversation_id , userStore.userInfo.email)
            chatStore.fetchChats()
            selectLayout.selectLayoutView(1)
            if(window.innerWidth <= 720){
                selectLayout.selectLayoutReponsive(1)
            }
            socketStore.sendNotifiCreateGroup(res.conversation.group_id , userStore.userInfo.email )
        })
    }
}
</script>
<template>
    <div class="p-2 h-100 bg-white bg-introduce ">
        <div class="p-5 w-100">
            <input type="text" v-model="nameGroupCreate" class="input-name-group p-2 w-100" placeholder="Enter name group" />
            <p v-if="showErrorNameGroup" class="text-danger m-0"> Name group is empty </p>
        </div>
        <div class="px-5 pb-5 position-relative">
            <input v-model="descriptionGroupCreate" type="text" class=" p-2 w-100" placeholder="Enter description">
        </div>
        <div class="p-1 px-5 position-relative">
            <input v-model="keySearch" type="text" class=" p-2 w-100" placeholder="Add member into group" v-on:keyup.enter="search">
        </div>
        <div class="position-relative list-user-search">
            <div v-if="keySearch != ''" class="p-2 shadow position-absolute bg-white border w-100 px-3"
            >
                <p v-if="listUserSearch.length == 0" class="m-0 text-center text-dark">
                    No have user searched
                </p>
            
                    <div v-for="item in listUserSearch" class="d-flex align-items-center mb-2 chat-item" @click="addUserGroup(item.email)">
                        <div class="chat-no-image-search text-center p-3 text-white"> Chat </div>
                        <div class="ms-3 d-flex flex-column align-item-center justify-content-around">
                            <p class="m-0 text-dark"> <b>{{ item.email }}</b></p>
                        </div>
                    </div>
                
            </div>
        </div>
        <div class="position-relative p-5">
             <p class="text-dark"> <b> User Select : </b> </p>
            <div class="p-2 bg-white border w-100 px-3" :class="{'border-danger' : showErrorUserSelect}" >
                <p v-if="listUserAddGroup.length == 0" class="m-0 text-center text-dark">
                    User select empty
                </p>
                <div v-for="item in listUserAddGroup" class="d-flex align-items-center justify-content-between mb-2" >
                    <div class="d-flex">
                        <div class="chat-no-image-search text-center p-3 text-white"> Chat </div>
                        <div class="ms-3 d-flex flex-column align-item-center justify-content-around">
                            <p class="m-0 text-dark"> <b>{{ item }}</b></p>
                        </div>
                    </div>
                    <Icon icon="mdi:remove-box-outline" class="fs-1" @click="removeUserGroup(item)" />
                </div>     
            </div>
        </div>
        <div class="d-flex flex-column align-items-center">
            <button class="btn btn-dark px-3" @click="createNewGroup" >
                <p class="m-0" > Create  </p>
            </button>
        </div>
    </div>
</template>
<style>
.input-add-member {
    border: 1px solid black;
    border-radius: 15px;
}
.bg-introduce{
    background-image: linear-gradient(45deg,#efefef 25%,rgba(239,239,239,0) 25%,rgba(239,239,239,0) 75%,#efefef 75%,#efefef),linear-gradient(45deg,#efefef 25%,rgba(239,239,239,0) 25%,rgba(239,239,239,0) 75%,#efefef 75%,#efefef) !important;
}
.list-user-search {
    z-index:99;
}
</style>