<template>
    <div class="like">
        <ul class="grid sm:grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-3">
            <PostDetail v-for="post in bookmarkedPosts" :key="post" :post="post"></PostDetail>
        </ul>
        <PaginationComponent :pagename="router.path" :currentPage="currentPage" :totalpage="totalpage" @to_page="(page) => bookmarkPost_search(page)" @to_previous="bookmarkPost_search(currentPage - 1)" @to_next="bookmarkPost_search(currentPage + 1)"></PaginationComponent>

        
    </div>
</template>

<script setup>
    import PostDetail from "../components/atoms/PostDetail.vue"
    import PaginationComponent from "../components/PaginationComponent.vue"
    import axios from "axios"
    import { ref, onMounted } from "vue"
    import { useRouter, useRoute } from 'vue-router';
    import store from "../store"

    // apiコールの取得件数
    const page_size = 10
    const login_user = store.state.login_user


    const router = useRouter()
    const route = useRoute()
    const params = ref(null)
    const currentPage = ref(null)
    const bookmarkedPosts = ref([])
    const allpost_count = ref(null)
    const totalpage = ref(null)
    const apiUrl = process.env.VUE_APP_API_DOMAIN;

    onMounted(() => {
        bookmarkPost_search()
    })


    const bookmarkPost_search = async (page) => {
        currentPage.value = page
        params.value = {
            page: page,
            page_size: page_size
        }
        axios.get(`${apiUrl}/api/users/${login_user.pk}/bookmark/`, {params: params.value})
        .then((response) => {
            if(currentPage.value === undefined) currentPage.value = 1
            bookmarkedPosts.value = response.data.results
            allpost_count.value = response.data.count
            totalpage.value = Math.ceil(allpost_count.value / page_size)
            router.push({ path: route.path, query: { page: page } })

        })
        .catch((error) => {
            console.log(error)
        })
    };

</script>

