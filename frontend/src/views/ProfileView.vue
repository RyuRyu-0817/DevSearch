<template>
    <div class="profile">
        <HeaderComponent></HeaderComponent>
        <div class="mx-auto max-w-screen-2xl px-4 lg:px-28 mt-14">
            <div class="bg-white shadow rounded-lg p-12 mb-6 xl:w-5/12 mx-auto">
                <div class="text-center">
                    <img src="../assets/logo.png" alt="" class="w-32 h-32 rounded-full inline-block m-auto">
                    <p class="text-lg font-semibold text-center mb-4">@{{ login_user.username }}</p>
                    <button class="bg-indigo-500 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded">画像を選択</button>
                </div>
            </div>
            <div class="bg-white shadow rounded-lg p-4 mb-6">
                <!-- タブセクション -->
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


    const login_user = store.state.login_user



</script>
