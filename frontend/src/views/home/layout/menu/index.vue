<script lang="ts" setup>
import { ref , onMounted } from 'vue'
import { useRouter } from 'vue-router';
import { searchUser , getAllConversation } from '@/api';
import { Icon } from '@iconify/vue';

const router = useRouter()

//ref

const keySearch = ref<string>('')
const listUserSearch = ref<any>([])
const isOnline = ref<boolean>(true)
    const dataConversation = ref<any>([])

// method

onMounted(() => {
    getAllConversation().then( (res) : any => {
        dataConversation.value = res.conversations
    })

})

function search(): void {
    searchUser(keySearch.value).then((res): any => {
        listUserSearch.value = res.users
    })
}
</script>
<template>
    <div class="p-3">
        <div class="d-flex align-items-center mb-2">
            <div class="chat-no-image text-center p-3 text-white bg-dark">
                <Icon icon="ph:user-bold" class="text-white fs-1" />
            </div>
            <div class="ms-3 ">
                <div class="d-flex align-items-center">
                    <Icon icon="carbon:circle-filled" class="ms-3" :class="[ isOnline ? 'color-online' : 'color-offline']" />
                    <p v-if="isOnline" class="m-0 ms-1 color-online"> Online</p>
                    <p v-if="!isOnline" class="m-0 ms-1 color-offline"> Hide online</p>
                </div>
                <div title=".slideThree" class="ms-3 mt-1">
                    <!-- .slideThree -->
                    <div class="slideThree">
                        <input v-model="isOnline" type="checkbox" value="None" id="slideThree" name="check" checked />
                        <label for="slideThree"></label>
                    </div>
                    <!-- end .slideThree -->
                </div>
            </div>

        </div>
        <div class="m-3  position-relative">
            <div class="d-flex">
                <Icon icon="mdi:plus-outline" class="text-dark fs-1 me-2 " />
                <input v-model="keySearch" type="text" class="p-2 w-100" placeholder="Search" v-on:keyup.enter="search">
            </div>
            <div v-if="keySearch != ''" class="p-2 position-absolute shadow bg-white border w-100">
                <p v-if="listUserSearch.length == 0" class="m-0 text-center text-dark">
                    No have user searched
                </p>
                <div v-for="item in listUserSearch" class="d-flex align-items-center mb-2">
                    <div class="chat-no-image-search text-center p-3 text-white"> Chat </div>
                    <div class="ms-3 d-flex flex-column align-item-center justify-content-around">
                        <p class="m-0 text-dark"> <b>{{ item.email }}</b></p>
                    </div>
                </div>
            </div>
        </div>

        <div class="p-3">
            <div v-for="item in dataConversation" class="d-flex align-items-center mb-2">
                <div class="chat-no-image text-center p-3 text-white"> Chat </div>
                <div class="ms-3 d-flex flex-column align-item-center justify-content-around">
                    <p class="m-0 text-dark"> <b>User 1</b></p>
                    <p class="m-0"> You: Hello ! </p>
                </div>
            </div>
        </div>
    </div>
</template>
<style lang="scss">
html,
body {
    height: 100%;
    margin: 0;
}
.color-offline {
    color:#4d4d4d
}
.bg-login {
    height: 100%;

    background: url('./../../../public/15835.jpg');
}

#app {
    height: 100%;
}

.chat-no-image {
    background-color: rgb(1, 35, 85);
    border-radius: 50%;
}

.chat-no-image-search {
    background-color: rgb(134, 30, 160);
    border-radius: 50%;
}
.slideThree {
  width: 80px;
  height: 26px;
  background: #333;
  position: relative;
  border-radius: 50px;
  box-shadow: inset 0px 1px 1px rgba(0,0,0,0.5), 0px 1px 0px rgba(255,255,255,0.2);
  &:after {
    content: 'OFF';
    color: white;
    position: absolute;
    right: 10px;
    z-index: 0;
    font: 12px/26px Arial, sans-serif;
    font-weight: bold;
    text-shadow: 1px 1px 0px rgba(255,255,255,.15);
  }
  &:before {
    content: 'ON';
    color: rgb(14, 160, 50);
    position: absolute;
    left: 10px;
    z-index: 0;
    font: 12px/26px Arial, sans-serif;
    font-weight: bold;
  }
  label {
    display: block;
    width: 34px;
    height: 20px;
    cursor: pointer;
    position: absolute;
    top: 3px;
    left: 3px;
    z-index: 1;
    background: #fcfff4;
    background: linear-gradient(top, #fcfff4 0%, #dfe5d7 40%, #b3bead 100%);
    border-radius: 50px;
    transition: all 0.4s ease;
    box-shadow: 0px 2px 5px 0px rgba(0,0,0,0.3);
  }
  input[type=checkbox] {
    visibility: hidden;
    &:checked + label {
      left: 43px;
    }
  }    
}
</style>