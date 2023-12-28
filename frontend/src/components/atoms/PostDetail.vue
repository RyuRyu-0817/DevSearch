<template>
    <li class="bg-white rounded-md p-4 shadow">
        <a :href="post.url" target="_blank">
            <img :src="post.image" alt="" class="mb-4">
        </a>
        <div class="relative group block">
            <div class="bg-gray-300 font-semibold py-2 px-4 rounded text-center">
                <span class="text-xs text-gray-500">タグを見る</span>
            </div>
            <div class="absolute group-hover:block hidden">
                <ul class="rounded bg-gray-200 p-2">
                    <li v-for="tag in post.tags" :key="tag" class="p-1 z-50">
                        <router-link :to="{ name: 'tagpost', params: { tagname: tag.tagname, tagid: tag.id } }" class="block border-b border-gray-200 hover:bg-gray-300"># {{ tag.tagname }}</router-link>
                    </li>
                </ul>
            </div>
        </div>
        <div class="p-3 border-t border-gray-300 mb-4">
            <p class="font-extrabold">{{ post.title }}</p>
        </div>
        <div class="flex gap-3 bottom-1 left-4"> 
            <div>
                <div class="flex items-center justify-center gap-1">
                    <button v-if="is_liked" @click="do_like()">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart-fill" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
                        </svg>
                    </button>
                    <button v-else @click="do_like()"> 
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                            <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
                        </svg>
                    </button>
                    <span>{{ post.like_count }}</span>
                </div>
            </div>
            <div>
                <button v-if="is_bookmarked" @click="do_bookmark()">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bookmark-plus-fill" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M2 15.5V2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.74.439L8 13.069l-5.26 2.87A.5.5 0 0 1 2 15.5zm6.5-11a.5.5 0 0 0-1 0V6H6a.5.5 0 0 0 0 1h1.5v1.5a.5.5 0 0 0 1 0V7H10a.5.5 0 0 0 0-1H8.5V4.5z"/>
                    </svg>
                </button>
                <button v-else @click="do_bookmark()">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bookmark-plus" viewBox="0 0 16 16">
                        <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5V2zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1H4z"/>
                        <path d="M8 4a.5.5 0 0 1 .5.5V6H10a.5.5 0 0 1 0 1H8.5v1.5a.5.5 0 0 1-1 0V7H6a.5.5 0 0 1 0-1h1.5V4.5A.5.5 0 0 1 8 4z"/>
                    </svg>
                </button>
            </div>   
        </div>
    </li>
</template>

<script setup>
    import { ref, defineProps } from "vue"
    // import axios from "axios";
    import ax from "../../main";
    import store from "../../store"


    const props = defineProps({
        post: Object
    })



    const post = ref(props.post)
    const is_liked = ref(null)
    const is_bookmarked = ref(null)
    if (store.state.login_user){
        // 初回ロードでログインユーザが投稿にいいねorブックマークをしたか
        is_liked.value = post.value.who_like.some(user => { return user.id == store.state.login_user.pk })
        is_bookmarked.value = post.value.who_bookmark.some(user => { return user.id == store.state.login_user.pk })
    }
    
    const do_like = async () => {
        await ax.post("http://127.0.0.1:8000/api/like/", { user: store.state.login_user, post: post.value })
        .then((response) => {
            is_liked.value = response.data.is_liked
            post.value = response.data.post
        })
        .catch((error) => {
            console.log("error" + error)
        })
    };

    const do_bookmark = async () => {
        await ax.post("http://127.0.0.1:8000/api/bookmark/", { user: store.state.login_user, post: post.value })
        .then((response) => {
            is_bookmarked.value = response.data.is_bookmarked
            post.value = response.data.post
        })
        .catch((error) => {
            console.log("error" + error)
        })
    }

</script>
