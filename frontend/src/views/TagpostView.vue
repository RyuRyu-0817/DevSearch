<template>
    <div>
        <HeaderComponent></HeaderComponent>
        <h1 class="text-center text-2xl mt-14"><span class="text-5xl font-bold">{{ tagname }}</span>({{ allpost_count }}件)</h1>
        <div class="mx-auto max-w-screen-2xl px-4 lg:px-28 mt-14">
            <ul v-if="tagposts" class="grid sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 mt-8 gap-4">
                <PostDetail v-for="tagpost in tagposts" :post="tagpost" :key="tagpost" >
                </PostDetail>
            </ul>
            <PaginationComponent v-if="allpost_count !== 0" :pagename="route.path" :currentPage="currentPage" :totalpage="totalpage" @to_page="(page) => tagpostSearch(tagid, page, true)" @to_previous="tagpostSearch(tagid, currentPage - 1, true)" @to_next="tagpostSearch(tagid, currentPage + 1, true)"></PaginationComponent>
        </div>
    </div>
</template>

<script setup>
    import HeaderComponent from '../components/HeaderComponent.vue';
    import PaginationComponent from "../components/PaginationComponent.vue"
    import PostDetail from "../components/atoms/PostDetail.vue"
    import axios from "axios";
    import { ref, onMounted, watch  } from 'vue';
    import { useRoute, useRouter } from 'vue-router';

    // apiコールの取得件数
    const page_size = 30

    // 現在のルート
    const route = useRoute();
    const router = useRouter();
    const tagposts = ref(null)
    const tagname = ref(route.params.tagname)
    const tagid = ref(route.params.tagid)
    const params = ref(null)
    const currentPage = ref(null)
    const totalpage = ref(null)
    const allpost_count = ref(null)
    const isPaginationClicked = ref(false); 


    onMounted(() => {
        tagpostSearch(tagid.value)
    })

    watch(route, (newRoute) => {
        // urlが変わったら、そのタグの投稿情報に切り替える
        if (!isPaginationClicked.value) {
            // ページネーションのクリックによる変更でない場合のみ反応
            tagname.value = newRoute.params.tagname;
            tagid.value = newRoute.params.tagid;
            tagpostSearch(tagid.value)
        }
        isPaginationClicked.value = false
    });

    // ページネーションクリック時にwatchが動いてしまうので、ページネーションをクリックしたかのフラグ入れる
    const tagpostSearch = async (tagid, page, isPagination=false) => {
        currentPage.value = page
        isPaginationClicked.value = isPagination
        params.value = {
            page: page,
            page_size: page_size,
        }
        console.log(tagid.value)
        await axios.get(`http://127.0.0.1:8000/api/tags/${tagid}/posts/`, {params: params.value})
        .then((response) => {
            if(currentPage.value === undefined) currentPage.value = 1
            tagposts.value = response.data.results
            allpost_count.value = response.data.count
            totalpage.value = Math.ceil(allpost_count.value / page_size)
            router.push({ path: route.path, query: { page: page } })
        })
        .catch((error) => {
            console.log(error)
        })
    };


</script>
