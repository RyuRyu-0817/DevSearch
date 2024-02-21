<template>
    <div class="h-screen flex items-center">
        <!-- <HeaderComponent></HeaderComponent> -->
        <!-- Right Pane -->
        <div class="w-full lg:w-1/2 m-auto">
            <div class="max-w-md w-full m-auto">
                <h1 class="text-3xl font-semibold mb-6 text-black text-center">新規登録</h1>
                <div class="mt-4 flex flex-col lg:flex-row items-center justify-between">
                    <!-- <div class="w-full lg:w-1/2 mb-2 lg:mb-0">
                    <button type="button" class="w-full flex justify-center items-center gap-2 bg-white text-sm text-gray-600 p-2 rounded-md hover:bg-gray-50 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-200 transition-colors duration-300">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="w-4" id="google">
                        <path fill="#fbbb00" d="M113.47 309.408 95.648 375.94l-65.139 1.378C11.042 341.211 0 299.9 0 256c0-42.451 10.324-82.483 28.624-117.732h.014L86.63 148.9l25.404 57.644c-5.317 15.501-8.215 32.141-8.215 49.456.002 18.792 3.406 36.797 9.651 53.408z"></path>
                        <path fill="#518ef8" d="M507.527 208.176C510.467 223.662 512 239.655 512 256c0 18.328-1.927 36.206-5.598 53.451-12.462 58.683-45.025 109.925-90.134 146.187l-.014-.014-73.044-3.727-10.338-64.535c29.932-17.554 53.324-45.025 65.646-77.911h-136.89V208.176h245.899z"></path>
                        <path fill="#28b446" d="m416.253 455.624.014.014C372.396 490.901 316.666 512 256 512c-97.491 0-182.252-54.491-225.491-134.681l82.961-67.91c21.619 57.698 77.278 98.771 142.53 98.771 28.047 0 54.323-7.582 76.87-20.818l83.383 68.262z"></path>
                        <path fill="#f14336" d="m419.404 58.936-82.933 67.896C313.136 112.246 285.552 103.82 256 103.82c-66.729 0-123.429 42.957-143.965 102.724l-83.397-68.276h-.014C71.23 56.123 157.06 0 256 0c62.115 0 119.068 22.126 163.404 58.936z"></path>
                        </svg> Googleでログイン </button>
                    </div> -->
                    <!-- <div class="w-full lg:w-1/2 ml-0 lg:ml-2">
                    <button type="button" class="w-full flex justify-center items-center gap-2 bg-white text-sm text-gray-600 p-2 rounded-md hover:bg-gray-50 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-200 transition-colors duration-300">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" id="github" class="w-4">
                        <path d="M7.999 0C3.582 0 0 3.596 0 8.032a8.031 8.031 0 0 0 5.472 7.621c.4.074.546-.174.546-.387 0-.191-.007-.696-.011-1.366-2.225.485-2.695-1.077-2.695-1.077-.363-.928-.888-1.175-.888-1.175-.727-.498.054-.488.054-.488.803.057 1.225.828 1.225.828.714 1.227 1.873.873 2.329.667.072-.519.279-.873.508-1.074-1.776-.203-3.644-.892-3.644-3.969 0-.877.312-1.594.824-2.156-.083-.203-.357-1.02.078-2.125 0 0 .672-.216 2.2.823a7.633 7.633 0 0 1 2.003-.27 7.65 7.65 0 0 1 2.003.271c1.527-1.039 2.198-.823 2.198-.823.436 1.106.162 1.922.08 2.125.513.562.822 1.279.822 2.156 0 3.085-1.87 3.764-3.652 3.963.287.248.543.738.543 1.487 0 1.074-.01 1.94-.01 2.203 0 .215.144.465.55.386A8.032 8.032 0 0 0 16 8.032C16 3.596 12.418 0 7.999 0z"></path>
                        </svg> Githubでログイン </button>
                    </div> -->
                </div>
                <!-- <div class="mt-4 text-sm text-gray-600 text-center">
                    <p>もしくは</p>
                </div> -->
                <div v-if="mail_message" class="text-center mb-3">
                    <p class="mb-2" v-html="mail_message"></p>
                    <form @submit.prevent="resendMail">
                        <input type="text" id="resendemail" :value="userData.email" required name="resendemail" class="mb-1 p-2 border rounded-md focus:border-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-300 transition-colors duration-300" placeholder="再度受け取るメールアドレス">
                        <button type="submit" class="bg-black text-white p-2 rounded-md hover:bg-gray-800 focus:outline-none focus:bg-black focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900 transition-colors duration-300">再度受け取る</button>
                    </form>
                    <p class="text-xs">※迷惑メールフォルダも確認した上でご利用ください</p>
                </div>
 
                <form @submit.prevent="signUp" class="space-y-4">
                    <!-- Your form elements go here -->
                    <div>
                        <label for="username" class="block text-sm font-medium text-gray-700">ユーザ名</label>
                        <input type="text" id="username" v-model="userData.username" required name="username" class="mt-1 p-2 w-full border rounded-md focus:border-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-300 transition-colors duration-300">
                        <div v-if="error_messages.username">
                            <p v-for="error_message in error_messages.username" :key="error_message" class="text-red-500">{{ error_message }}</p>
                        </div>
                    </div>
                    <div>
                        <label for="email" class="block text-sm font-medium text-gray-700">メールアドレス</label>
                        <input type="text" id="email" v-model="userData.email" required name="email" class="mt-1 p-2 w-full border rounded-md focus:border-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-300 transition-colors duration-300">
                        <div v-if="error_messages.email">
                            <p v-for="error_message in error_messages.email" :key="error_message" class="text-red-500">{{ error_message }}</p>
                        </div>
                    </div>
                    <div>
                        <label for="password" class="block text-sm font-medium text-gray-700">パスワード</label>
                        <input type="password" id="password1" v-model="userData.password1" required name="password" class="mt-1 p-2 w-full border rounded-md focus:border-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-300 transition-colors duration-300">
                        <div v-if="error_messages.password1">
                            <p v-for="error_message in error_messages.password1" :key="error_message" class="text-red-500">{{ error_message }}</p>
                        </div>
                    </div>
                    <div>
                        <label for="password" class="block text-sm font-medium text-gray-700">パスワード(再)</label>
                        <input type="password" id="password2" v-model="userData.password2" required name="password" class="mt-1 p-2 w-full border rounded-md focus:border-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-300 transition-colors duration-300">
                        <div v-if="error_messages.password2">
                            <p v-for="error_message in error_messages.password2" :key="error_message" class="text-red-500">{{ error_message }}</p>
                            
                        </div>
                    </div>
                    <div>
                        <button type="submit" class="w-full bg-black text-white p-2 rounded-md hover:bg-gray-800 focus:outline-none focus:bg-black focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900 transition-colors duration-300">新規登録</button>
                    </div>
                </form>
                <div class="mt-4 text-sm text-gray-600 text-center">
                    <p>すでにアカウントをお持ちですか？ <router-link to="/login" class="text-black hover:underline">ログインはこちら</router-link>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue';
    import axios from 'axios';


    const error_messages = ref({})
    const userData = ref({
        username: "",
        email: "",
        password1: "",
        password2: "",

    })
    const mail_message = ref("")
    const apiUrl = process.env.VUE_APP_API_DOMAIN;


    const signUp = async () => {
        await axios.post(`${apiUrl}/auth/signup/`, userData.value)
        .then(() => {
            mail_message.value = "-登録されたメールアドレスに確認メールを送信しました-<br>(再度受け取る場合は3分空けてご利用ください)"
        })
        .catch((error) => {
            error_messages.value = error.response.data
        })
    };

    const resendMail = async () => {
        await axios.post(`${apiUrl}/auth/resend-email/`, {email: userData.value.email})
        .then(() => {
            mail_message.value = "-メールアドレスに再度確認メールを送信しました-"
        })
        .catch(() => {
            mail_message.value = "-再送信に失敗しました-"
        })
    }
</script>
