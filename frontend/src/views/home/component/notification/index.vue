<script lang="ts" setup>
import { defineProps } from 'vue'

import { Icon } from '@iconify/vue';
import { useGroupStore } from '@/store'
// interface

interface IProps {
    email_user_chat : string,
    content : string , 
    type : string ,
    group_id : string ,
}

// store

const groupStore = useGroupStore()

// props
const props = defineProps<IProps>()




</script>
<template>
    <div class="d-flex mt-2 align-items-center">
        <div class="d-flex">
            <Icon icon="humbleicons:chat" v-if="props.type == 'NTFCT'" class="fs-3" />
            <Icon icon="clarity:group-solid" v-if="props.type == 'NTFCG'" class="fs-3" />
        </div>
        <div class="ms-3 d-flex flex-column align-item-center justify-content-around">
           <p v-if="props.type == 'NTFCT'" class="m-0">
                <b>{{ props.email_user_chat }}</b> sent Message
           </p>
           <p v-if="props.type == 'NTFCG'" class="M-0"> 
            <b>{{ props.email_user_chat }}</b> sent Message into group 
            <b>{{ groupStore.getNameGroup(props.group_id) }}</b>
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