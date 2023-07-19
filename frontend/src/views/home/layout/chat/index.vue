<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router';
import { Icon } from '@iconify/vue';
import { getAllConversation } from '@/api'

const router = useRouter()

// ref

const dataConversation = ref<any>([])
onMounted(() => {
    getAllConversation().then( (res) : any => {
        dataConversation.value = res.conversations
    })

})
</script>
<template>
    <div class="d-flex flex-column bg-white">
        <div class="d-flex align-items-center p-2 border border-2 border-dark
        border-top-0 border-start-0 border-end-0 ">
            <div class="chat-no-image text-center p-3 text-white border border-dark border-2"> Chat </div>
            <div class="ms-3 d-flex flex-column align-item-center justify-content-around">
                <p class="m-0 text-dark"> <b>User 1</b></p>
            </div>
            <Icon icon="carbon:circle-filled" class="ms-3 color-online" />
            <p class="m-0 ms-1 color-online"> Online</p>
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
</style>