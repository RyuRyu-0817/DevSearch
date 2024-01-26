<template>
    <div class="profile">
        <HeaderComponent></HeaderComponent>
        <div class="mx-auto max-w-screen-2xl px-4 lg:px-28 mt-14">
            <div class="bg-white shadow rounded-lg p-12 mb-6 xl:w-5/12 mx-auto">
                <div class="text-center">
                    <!-- <img src="../assets/logo.png" alt="" class="w-32 h-32 rounded-full inline-block m-auto"> -->
                    <svg xmlns="http://www.w3.org/2000/svg" width="52" height="52" fill="currentColor" class="bi bi-person-circle inline-block m-auto mb-4" viewBox="0 0 16 16">
                        <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
                        <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"/>
                    </svg>
                    <p class="text-lg font-semibold text-center mb-4">@{{ login_user.username }}</p>
                    <button class="bg-indigo-500 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded" @click="logout()">ログアウト</button>
                </div>
            </div>
            <div class="bg-white shadow rounded-lg p-4 mb-6">
                <div class="flex border-b">
                    <router-link to="/profile/like" active-class="border-b-4 border-purple-500" class="py-2 px-4 text-gray-500 hover:text-gray-700">
                        いいねした記事
                    </router-link>
                    <router-link to="/profile/bookmark" active-class="border-b-4 border-purple-500" class="py-2 px-4 text-gray-500 hover:text-gray-700">
                        ブックマークした記事
                    </router-link>
                </div>
            </div>
            <router-view></router-view>
        </div>
    </div>
</template>

<script setup>
    import HeaderComponent from "../components/HeaderComponent.vue"
    import store from "../store"
    import { useRouter } from 'vue-router';


    const router = useRouter()
    const login_user = store.state.login_user

    const logout = () => {
        store.dispatch('clearAccessToken');
        store.dispatch('clearRefreshToken');
        store.dispatch('clearLoginUser')
        router.push('/home')
    }


</script>
