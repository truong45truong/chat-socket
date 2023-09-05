<script lang="ts" setup>
import { computed , ref ,onMounted } from 'vue'
import { Icon } from '@iconify/vue';
import {
    useGroupStore , useChatStore ,
    useUserStore , useSocketStore ,
    useSelectLayoutStore , 
} from '@/store'
import {updateGroup, getAllGroup , searchUserAddGroup , getListMember} from '@/api'

// ref

const nameGroupCreate = ref<string>('')
const descriptionGroupCreate = ref<string>('')
const listUserSearch = ref<any>([])
const listUserAddGroup = ref<any>([])
const showErrorNameGroup = ref<boolean>(false)
const showErrorUserSelect = ref<boolean>(false)
const keySearch = ref<string>('')

const isChangeName = ref<boolean>(false)
const isChangeDescription = ref<boolean>(false)
const listMemberGroup = ref<any>([])
const listMemberRemove = ref<any>([])
const listMemberAdd = ref<any>([])
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
function changeName(){
    isChangeName.value = !isChangeName.value
}
function changeDescription(){
    isChangeDescription.value = !isChangeDescription.value
}
function search(): void {
    searchUserAddGroup(keySearch.value , chatStore.group_id).then((res : any ) => {
        listUserSearch.value = res.users 
    })
}
function addUserGroup (email: string) : void {
    var check = false
    listMemberGroup.value.filter( (item: any) => {
        if (item == email) {
            check = true
        }
    } )
    if( check == false){
        listMemberAdd.value.push(email)
        listMemberGroup.value.push({email : email , group_id : false})
    }
}
function removeMemberAdd(email : string) : void {
    listMemberGroup.value = listMemberGroup.value.filter( (item : any) => {
        if(item.group_id == false && item.email == email)
            return 
        return item
    })
    listMemberRemove.value = listMemberRemove.value.filter( (item : any) => {
        if(item == email){
            return 
        }
        return item
    } )
}
function removeUserGroup( email : string ) : void {
    var check = false
    listMemberRemove.value = listMemberRemove.value.filter( (item : any) => {
        if(item == email){
            check = true
            return 
        }
        return item
    } )
    if(check == false){
        listMemberRemove.value = [...listMemberRemove.value , email]
    } 
}
function checkUserRemove(email : string) : boolean {
    var check = false
    listMemberRemove.value.filter( (item : any) => {
        if(item.email == email){
            check = true
        }
    } )
    return check
}
function isNullOrWhitespace(input: string): boolean {
  return !input || /^\s*$/.test(input);
}
function updateGroupCurrent() : void {
    if ( isNullOrWhitespace(nameGroupCreate.value) == true ){ 
        showErrorNameGroup.value = true
    }
    else showErrorNameGroup.value = false;
    if ( listUserAddGroup.value.length == 0) showErrorUserSelect.value = true;
    else showErrorUserSelect.value = false;

    updateGroup(  nameGroupCreate.value , listMemberAdd.value, listMemberRemove.value ,  descriptionGroupCreate.value  ).then( async (res: any) => {
        // let conversation_id = res.conversation.id
        // groupStore.fetchDataGroup()
        // await socketStore.initSocketChatGroup(
        //     conversation_id ,userStore.userInfo.email , 
        //     res.conversation.group_id
        // )
        // chatStore.selectGroupChat(
        //     conversation_id , res.conversation.group_name , 
        //     res.conversation.group_id , res.conversation.list_message_sent
        // )
        // groupStore.seemConversation(conversation_id , userStore.userInfo.email)
        // chatStore.fetchChats()
        // selectLayout.selectLayoutView(1)
        // if(window.innerWidth <= 720){
        //     selectLayout.selectLayoutReponsive(1)
        // }
        // socketStore.sendNotifiCreateGroup(res.conversation.group_id , userStore.userInfo.email )
    })
    
}
onMounted( () => {
    var listMessageSent: string[] = [];
    if(chatStore.list_user_sent != undefined)
    for (let item of chatStore.list_user_sent) {
        const convertedDict = JSON.parse(item.replace(/'/g, '"'));
        var keys = Object.keys(convertedDict)
        listMessageSent = [...listMessageSent , keys[0]]
    }
    getListMember(chatStore.group_id).then( (res : any) => {
        listMemberGroup.value = res.members
    })
    // listMemberGroup.value =listMessageSent
})
</script>
<template>
    <div class="p-2 h-100 bg-white bg-introduce ">
        <div class="layout-form-group  w-100">
            <p class="text-dark"> <b> Group information : </b> </p>
            <div v-if="isChangeName" class="d-flex align-items-center">
                <input type="text" v-model="nameGroupCreate" class="form-input input-name-group  w-100" placeholder="Enter name group" />
                <Icon icon="uil:x" class="cursor ms-2 fs-5" @click="changeName" />
            </div>
            <p v-if="showErrorNameGroup && isChangeName" class="text-danger m-0"> Name group is empty </p>
            <div  v-if="!isChangeName"  class="d-flex align-items-center ">
                <p class="m-0"> Name :  <span> {{ chatStore.group_name }} </span>  </p>
                <Icon class="cursor ms-2 fs-5" icon="typcn:edit" @click="changeName" />
            </div>
        </div>
        <div class="layout-form-group  position-relative">
            <div v-if="isChangeDescription" class="d-flex  align-items-center">
                <input v-model="descriptionGroupCreate" type="text" class="form-input p-2 w-100" placeholder="Enter description">
                <Icon icon="uil:x" class="cursor ms-2 fs-5"  @click="changeDescription" />
            </div>
            <div v-if="!isChangeDescription" class="d-flex align-items-center ">
                <p class="m-0"> Name :  <span> {{ chatStore.group_name }} </span>  </p>
                <Icon class="cursor ms-2 fs-5"  icon="typcn:edit" @click="changeDescription" />
            </div>
        </div>
        <div class="layout-form-group  position-relative">
            <p class="text-dark"> <b> Search user select : </b> </p>
            <input v-model="keySearch" type="text" class="form-input p-2 w-100" placeholder="Add member into group" v-on:keyup.enter="search">
        </div>
        <div class="position-relative list-user-search">
            <div v-if="keySearch != ''" class="p-2 shadow position-absolute bg-white border w-100 px-3"
            >
                <p v-if="listUserSearch.length == 0" class="m-0 text-center text-dark">
                    No have user searched
                </p>
            
                    <div v-for="item in listUserSearch" class="d-flex align-items-center mb-2 chat-item" @click="addUserGroup(item.email)">
                        <div class="text-center p-3 text-white"> 
                            <img src="./../../../../assets/images/media/user.png" alt="" class="chat-image-search ">
                        </div>
                        <div class="ms-3 d-flex flex-column align-item-center justify-content-around">
                            <p class="m-0 text-dark"> <b>{{ item.email }}</b></p>
                        </div>
                    </div>
                
            </div>
        </div>
        <div class="position-relative layout-form-group">
             <p class="text-dark"> <b> Member: </b> </p>
            <div class="p-2 bg-white border w-100 layout-member-group" 
            :class="{'border-danger' : showErrorUserSelect , 'layout-user-select' : listMemberGroup.length > 0}" >
                <div v-for="item in listMemberGroup" class="d-flex align-items-center justify-content-between mb-2" >
                    <div v-if="item.group_id != false" class="row w-100 layout-form-group justify-content-between">
                        <div class="col-2 text-center text-white"> 
                            <img src="./../../../../assets/images/media/user.png" alt="" class="chat-image-search ">
                        </div>
                        <div class="col-6 d-flex flex-column align-item-center justify-content-around">
                            <p class="m-0 overflow-text w-100  text-dark"> <b>{{ item.email }}</b></p>
                        </div>
                        <div class="col-2 d-flex flex-column align-item-center justify-content-around">
                            <Icon icon="mdi:remove-box-outline" class="fs-1" 
                            :class="{ 'text-danger' : checkUserRemove(item.email)}"  @click="removeUserGroup(item.email)" />
                        </div>
                    </div>
                    <div v-if="item.group_id == false" class="row w-100 layout-form-group justify-content-between">
                        <div class="col-2 text-center text-white"> 
                            <img src="./../../../../assets/images/media/user.png" alt="" class="chat-image-search ">
                            <p class="m-0 text-dark">Member new</p>
                        </div>
                        <div class="col-6 d-flex flex-column align-item-center justify-content-around"> 
                            <p class="m-0 overflow-text w-100  text-dark"> <b>{{ item.email }}</b></p>
                        </div>
                        <div class="col-2 d-flex flex-column align-item-center justify-content-around">
                            <Icon icon="mdi:remove-box-outline" class="fs-1" 
                            :class="{ 'text-danger' : checkUserRemove(item.email)}"  @click="removeMemberAdd(item.email)" />
                        </div>
                    </div>
                </div>     
            </div>
        </div>
        <div class="d-flex justify-content-around align-items-center mt-2">
            <button class="btn btn-dark px-3" @click="updateGroupCurrent" >
                <p class="m-0" > Save  </p>
            </button>

            <button class="btn btn-dark px-3" >
                <p class="m-0" > Cancel  </p>
            </button>
        </div>
    </div>
</template>
<style>
.layout-form-group {
    padding: 10px;
}
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
.chat-image-search {
    max-width: 40px;
}
.layout-user-select{
    max-width: 100%;
    overflow-y: scroll;
    overflow-x: none;
    max-height: 15vh;
}
.layout-member-group {
    max-height: 25vh;
}
.overflow-text {
  white-space: nowrap; 
  text-overflow: ellipsis; 
}
@media screen and (max-width: 720px) {
    .layout-form-group {
        padding: 10px;
    }
    .form-input {
        padding: 5px !important;
        font-size: 14px;
    }
}

@media screen and (max-width: 420px) {
  p {
    font-size: 11px;
  }
  .chat-image-search{
    max-width: 25px;
  }
  .chat-no-image  p {
    font-size: 10px;
    }
}
</style>