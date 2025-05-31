import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import '@/assets/global.css'
import '@/assets/css/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import DataVVue3 from '@kjgl77/datav-vue3'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// 解决浏览器中缺少 global 的问题
if (typeof window.global === 'undefined') {
    window.global = window;
}

const app = createApp(App)


app.use(router)
app.use(store)
app.use(DataVVue3)
app.use(ElementPlus,{
    locale: zhCn,
})
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.mount('#app')
