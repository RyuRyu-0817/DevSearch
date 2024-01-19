<template>
    <div>
        <HeaderComponent></HeaderComponent>
        <h1 class="sm:text-3xl text-2xl font-medium title-font mb-8 text-gray-900 text-center mt-14">記事検索</h1>
        <form @submit.prevent="postSearch(undefined, keywords)">
            <!-- <SearchAtom v-model:keyword="keyword" @search="(word) => keyword = word"></SearchAtom> -->
            <SearchAtom v-model:keywords="keywords" :placeholder="placeholder" @search="(word) => keywords = word"></SearchAtom>
        </form>
        <div class="mx-auto max-w-screen-2xl px-4 lg:px-28 mt-14">
            <ul v-if="posts" class="grid sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 mt-8 gap-8">
                <PostDetail v-for="post in posts" :key="post" :post="post" >
                    <a :href="post.url" target="_blank">
                        <div class="p-4 bg-indigo-50 rounded-md">
                            <img :src="post.image" alt="">
                            <div class="p-4">
                                <p class="font-extrabold">{{ post.title }}</p>
                            </div>
                        </div>
                    </a>
                </PostDetail>
            </ul>
            <PaginationComponent :pagename="router.path" :keywords="keywords" :currentPage="currentPage" :totalpage="totalpage" @to_page="(page) => postSearch(page, keywords)" @to_previous="postSearch(currentPage - 1, keywords)" @to_next="postSearch(currentPage + 1, keywords)"></PaginationComponent>
        </div>
    </div>
</template>

<script setup>
    import HeaderComponent from '../components/HeaderComponent.vue';
    import PaginationComponent from "../components/PaginationComponent.vue"
    import SearchAtom from "../components/atoms/SearchAtom.vue"
    import PostDetail from "../components/atoms/PostDetail.vue"
    import axios from "axios";
    import { onMounted, ref } from "vue"
    import { useRouter, useRoute } from 'vue-router';

    // apiコールの取得件数
    const page_size = 30

    const router = useRouter()
    const route = useRoute()
    const posts = ref([])
    const placeholder = "タイトルで検索できます"
    const keywords = ref(null)
    const params = ref(null)
    const currentPage = ref(null)
    const totalpage = ref(null)
    const allpost_count = ref(null)
    const apiUrl = process.env.VUE_APP_API_DOMAIN;


    onMounted(() => {
        postSearch()
    })



    const postSearch = async (page, keywords=null) => {
        currentPage.value = page
        params.value = {
            keywords: keywords,
            page: page,
            page_size: page_size,
        }
        
        await axios.get(`${apiUrl}/api/posts/`, {params: params.value})
        .then((response) => {
            if(currentPage.value === undefined) currentPage.value = 1
            posts.value = response.data.results
            allpost_count.value = response.data.count
            totalpage.value = Math.ceil(allpost_count.value / page_size)
            
            // キーワードが入力されていたら、クエリにキーワードも載せる
            if(keywords){
                router.push({ path: route.path, query: { q: keywords, page: page } })
            }
            else {
                router.push({ path: route.path, query: { page: page } })
            }

        })
        .catch((error) => {
            console.log(error)
        })
    };


</script>
