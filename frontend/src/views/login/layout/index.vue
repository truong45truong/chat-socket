<script lang="ts" setup>
import { defineEmits, ref, onMounted , computed , watch } from 'vue';
import { useRouter } from 'vue-router';
import  { loginUser , registerUser}  from '@/api';
import {useUserStore , useAuthStore} from '@/store'

/* -------------------------------------------------------------------------- */
/*                                     REF                                    */
/* -------------------------------------------------------------------------- */

const router = useRouter();
/* ---------------------------------- show ---------------------------------- */
const isSignUp = ref<boolean>(true);
const isSignIn = ref<boolean>(false);
/* ---------------------------------- login --------------------------------- */
const usernameLogin = ref<string>('');
const passwordLogin = ref<string>('');
/* -------------------------------- register -------------------------------- */
const usernameRegister = ref<string>('');
const emailRegister = ref<string>('');
const nameRegister = ref<string>('');
const passwordRegister1 = ref<string>('');
const passwordRegister2 = ref<string>('');
/* ---------------------------------- store --------------------------------- */

const userStore = useUserStore();
const authStore = useAuthStore();

const userData = computed(() => userStore.userInfo)

/* -------------------------------------------------------------------------- */
/*                                   METHOD                                   */
/* -------------------------------------------------------------------------- */
function isShowSigUp() : void {
    isSignUp.value = true;
    isSignIn.value = false
}
function isShowSigIn() : void {
    isSignIn.value = true
    isSignUp.value = false;
}
async function login() : Promise<boolean> {
    loginUser( usernameLogin.value , passwordLogin.value ).then( (res : any) => {
        userStore.updateUserInfo(res.user)
        authStore.setAuth(res.access_token)
    })
    return true
}
async function register() : Promise<boolean> {
    registerUser( 
        usernameRegister.value , emailRegister.value 
        , passwordRegister1.value , nameRegister.value
    ).then( (res : any) => {
        userStore.updateUserInfo(res.user)
        authStore.setAuth(res.access_token)
    })
    return true
}
/* -------------------------------------------------------------------------- */
/*                                    WATCH                                   */
/* -------------------------------------------------------------------------- */

watch(userData, (newUserData, oldUserData) => {
    if (newUserData.email){
        router.push({name : 'home'})
    }
});

</script>
<template>
    <div class="container px-4 p-5 px-md-5 text-center text-lg-start">
        <div class="row gx-lg-5 mb-5">
            <div  v-if="isSignUp"  class="col-sm-6 mb-5 mb-lg-0">
                <form class="border border-5 border-white p-5">
                    <!-- Email input -->
                    <div class="form-outline mb-4">
                        <input v-model="usernameLogin" type="text" id="form3Example3" class="form-control input-chat" placeholder="Username" />
                    </div>

                    <!-- Password input -->
                    <div class="form-outline ">
                        <input v-model="passwordLogin" type="password" id="form3Example4" class="form-control input-chat" placeholder="Password"  />
                    </div>
                    
                </form>
            </div>
            <div  v-if="isSignIn"  class="col-sm-6 mb-5 mb-lg-0">
                <form class="border border-5 border-white p-5">
                    <!-- Email input -->
                    <div class="form-outline mb-4">
                        <input v-model="usernameRegister" type="text" id="form3Example3" class="form-control input-chat" placeholder="Enter Username" />
                    </div>
                    <div class="form-outline mb-4">
                        <input v-model="emailRegister" type="email" id="form3Example3" class="form-control input-chat" placeholder="Enter Email" />
                    </div>
                    <div class="form-outline mb-4">
                        <input v-model="nameRegister" type="text" id="form3Example3" class="form-control input-chat" placeholder="Enter Name" />
                    </div>
                    <!-- Password input -->
                    <div class="form-outline mb-4 ">
                        <input v-model="passwordRegister1" type="password" id="form3Example4" class="form-control input-chat" placeholder="Enter Password"  />
                    </div>
                    <div class="form-outline ">
                        <input v-model="passwordRegister2" type="password" id="form3Example4" class="form-control input-chat" placeholder="Re-enter Password"  />
                    </div>
                </form>
            </div>
            <div class="col-sm-6">
                <!-- Submit button -->
                <div class="p-4 d-flex flex-column justify-content-start">
                    <button v-if="isSignIn" type="submit" class="btn btn-primary p-3 mb-4" @click="register">
                            Sign In
                    </button>
                    <button v-if="isSignUp" type="submit" class="btn btn-primary p-3 mb-4" @click="login">
                            Sign Up
                    </button>
                    <p v-if="isSignIn" class="text-white cursor" @click="isShowSigUp">
                        Click to Sign up
                    </p>
                    <p v-if="isSignUp" class="text-white cursor" @click="isShowSigIn">
                        If you don't have an account, please Sign in
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>
<style scoped>
.icon-dashboard {
    font-size: 24px;
    color: rgb(34, 197, 94);
}
.input-chat {
    border-color: rgb(74, 147, 207);
}
.cursor {
    cursor:pointer
}
.cursor:hover  {
    text-decoration: underline;
}
</style>