<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import SocketService from './socket';

</script>

<template>
  <RouterView />
</template>

<style scoped>
.cursor {
    cursor:pointer
}
.cursor:hover  {
    text-decoration: underline;
}
</style>
