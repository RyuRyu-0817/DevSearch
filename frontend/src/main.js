import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store';
import './style.css'
import axios from 'axios';

// 認証が必要なviewはaxでリクエスト
const ax = axios.create()
const apiUrl = process.env.VUE_APP_API_DOMAIN;

export default ax

async function verifyAccessToken(token){
    try {
        await axios.post(`${apiUrl}/auth/token/verify/`, { token: token });
        return true; // トークンが有効な場合
    } catch (error) {
        return false; // トークンが無効な場合
    }
}
async function TokenRefresh(refreshToken){
    try {
        const response = await axios.post(`${apiUrl}/auth/token/refresh/`, { refresh: refreshToken });
        store.dispatch("setAccessToken", response.data.access);
        store.dispatch("setRefreshToken", response.data.refresh);
        return response.data.access; 
    } catch (error) {
        return null
    }
}

ax.interceptors.request.use(
    async config => {
        const accessToken = store.getters.getAccessToken;
        const refreshToken = store.getters.getRefreshToken;

        if (await verifyAccessToken(accessToken)) {
            config.headers.Authorization = `Bearer ${accessToken}`;
        } 
        else {
            const newAccessToken = await TokenRefresh(refreshToken);
            if (newAccessToken) {
                config.headers.Authorization = `Bearer ${newAccessToken}`;
            } 
            else {
                alert("ログインしてください")
                store.dispatch("clearAccessToken")
                store.dispatch("clearRefreshToken")
                store.dispatch("clearLoginUser")
                router.push("/login");
                return Promise.reject(new Error("Failed to refresh token"));

            }
        }

        return config;
    },
    error => Promise.reject(error)
);



createApp(App).use(router).use(store).mount('#app')
