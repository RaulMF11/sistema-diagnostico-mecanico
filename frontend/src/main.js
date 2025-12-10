import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
console.log('API URL usada por Vue:', import.meta.env.VUE_APP_API_URL);
console.log('Todas las variables de entorno:', import.meta.env);
