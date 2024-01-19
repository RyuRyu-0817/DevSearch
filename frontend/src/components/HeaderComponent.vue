<template>
    <header class="z-50 flex items-center justify-between py-8 md:py-8 mx-auto max-w-screen-2xl px-4 lg:px-28 bg-white sticky top-0" >
        <!-- logo - start -->
        <router-link to="/home" class="inline-flex items-center gap-2.5 text-2xl font-bold text-black md:text-3xl" aria-label="logo">
            <svg width="95" height="94" viewBox="0 0 95 94" class="h-auto w-6 text-indigo-500" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <path d="M96 0V47L48 94H0V47L48 0H96Z" />
            </svg>
            DevSearch
        </router-link>
        <!-- logo - end -->

        <!-- nav - start -->
        <nav class="hidden gap-12 lg:flex">
            <router-link to="/tag" active-class="border-b-4 border-purple-500" class="text-lg font-semibold text-gray-600 transition duration-100 hover:text-indigo-500">タグ検索</router-link>
            <router-link to="/post" active-class="border-b-4 border-purple-500" class="text-lg font-semibold text-gray-600 transition duration-100 hover:text-indigo-500">記事検索</router-link>
        </nav>
        <!-- nav - end -->

        <!-- buttons - start -->
        <div v-if="store.state.login_user">
            <div class="-ml-8 hidden flex-col gap-2.5 sm:flex-row sm:justify-center lg:flex lg:justify-start">
                <router-link to="/profile"><img src="../assets/logo.png" alt="" class="rounded-full border border-indigo-500 w-12 h-12"></router-link>
            </div>
        </div>
        <div v-else>
            <div class="-ml-8 hidden flex-col gap-2.5 sm:flex-row sm:justify-center lg:flex lg:justify-start">
                <router-link to="login" class="inline-block rounded-lg px-4 py-3 text-center text-sm font-semibold text-gray-500 outline-none ring-indigo-300 transition duration-100 hover:text-indigo-500 focus-visible:ring active:text-indigo-600 md:text-base">ログイン</router-link>

                <router-link to="signup" class="inline-block rounded-lg bg-indigo-500 px-8 py-3 text-center text-sm font-semibold text-white outline-none ring-indigo-300 transition duration-100 hover:bg-indigo-600 focus-visible:ring active:bg-indigo-700 md:text-base">新規登録</router-link>
            </div>
        </div>

        <!-- <button type="button" @click="open=!open" class="inline-flex items-center gap-2 rounded-lg bg-gray-200 px-2.5 py-2 text-sm font-semibold text-gray-500 ring-indigo-300 hover:bg-gray-300 focus-visible:ring active:text-gray-700 md:text-base lg:hidden">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd" />
            </svg>
            Menu
        </button>  -->
        <div @click="open = !open" :class="{'is-open': open}" class="cursor-pointer inline-block md:text-base lg:hidden">
            <span class="bar top-bar"></span>
            <span class="bar middle-bar"></span>
            <span class="bar bottom-bar"></span>
        </div>

        <div v-if=open class="absolute top-full left-0 border-t-2 border-gray-200 lg:hidden">
            <div class="bg-white w-screen p-4 text-center">
                <router-link to="/tag" class="block text-lg font-semibold text-gray-600 transition duration-100 hover:text-indigo-500 py-2">タグ検索</router-link>
                <router-link to="/post" class="block text-lg font-semibold text-gray-600 transition duration-100 hover:text-indigo-500 py-2">記事検索</router-link>

                <div v-if="store.state.login_user">
                    <router-link to="/profile" class="block text-lg font-semibold text-gray-600 transition duration-100 hover:text-indigo-500 py-2">{{ store.state.login_user.username }}さんのマイページ</router-link>
                </div>
                <div v-else>
                    <router-link to="login" class="block text-lg font-semibold text-gray-600 transition duration-100 hover:text-indigo-500 py-2">ログイン</router-link>
                    <router-link to="signup" class="block text-lg font-semibold text-gray-600 transition duration-100 hover:text-indigo-500 py-2">新規登録</router-link>
                </div>
            </div>
        </div>
    </header>
</template>

<script setup>
    import store from "../store"
    import { ref } from "vue"

    const open = ref(false)
    
 

</script>

<style scoped>
.bar {
  display: block;
  width: 30px;
  height: 3px;
  margin: 5px auto;
  transition: all 0.3s ease-in-out;
  background-color: #333;
}

/* メニューが開いた時のアニメーション */
.is-open .top-bar {
  transform: rotate(45deg) translate(5px, 5px);
}

.is-open .middle-bar {
  opacity: 0;
}

.is-open .bottom-bar {
  transform: rotate(-45deg) translate(7px, -6px);
}

</style>
