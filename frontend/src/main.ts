import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { setupStore } from './store'
/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

export const app = createApp(App).component('font-awesome-icon', FontAwesomeIcon)

app.use(router)
setupStore(app)
app.mount('#app')
