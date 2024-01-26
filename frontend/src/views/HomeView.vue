<template>
  <div class="home">
    <HeaderComponent></HeaderComponent>
    <div class="mx-auto max-w-screen-2xl px-4 lg:px-28 mt-14">
      <div class="flex">
        <!-- タグ一覧 -->
        <div class="custom-flex-ratio-left mr-12 hidden md:block">
          <div class="flex items-center pl-2 mb-2">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 18.75h-9m9 0a3 3 0 013 3h-15a3 3 0 013-3m9 0v-3.375c0-.621-.503-1.125-1.125-1.125h-.871M7.5 18.75v-3.375c0-.621.504-1.125 1.125-1.125h.872m5.007 0H9.497m5.007 0a7.454 7.454 0 01-.982-3.172M9.497 14.25a7.454 7.454 0 00.981-3.172M5.25 4.236c-.982.143-1.954.317-2.916.52A6.003 6.003 0 007.73 9.728M5.25 4.236V4.5c0 2.108.966 3.99 2.48 5.228M5.25 4.236V2.721C7.456 2.41 9.71 2.25 12 2.25c2.291 0 4.545.16 6.75.47v1.516M7.73 9.728a6.726 6.726 0 002.748 1.35m8.272-6.842V4.5c0 2.108-.966 3.99-2.48 5.228m2.48-5.492a46.32 46.32 0 012.916.52 6.003 6.003 0 01-5.395 4.972m0 0a6.726 6.726 0 01-2.749 1.35m0 0a6.772 6.772 0 01-3.044 0" />
            </svg>
            <p class="text-2xl font-extrabold">上位タグ</p>
          </div>
          <ul>
            <TagLink :tagname="tag.tagname" :tagid="tag.id" v-for="tag in popular_tags" :key="tag"></TagLink>
          </ul>
        </div>

        <!-- 投稿部分 -->
        <div class="custom-flex-ratio-right">
          <div class="flex items-center pl-2 mb-2">
            <p class="text-2xl font-extrabold">各サイトでいいね数の多い記事</p>
          </div>
          <ul class="grid sm:grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 mb-3">
            <PostDetail v-for="post in likesort_posts" :key="post" :post="post"></PostDetail>
          </ul>
          <PaginationComponent :pagename="router.path" :currentPage="currentPage" :totalpage="totalpage" @to_page="(page) => likesort_Search(page)" @to_previous="likesort_Search(currentPage - 1)" @to_next="likesort_Search(currentPage + 1)"></PaginationComponent>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import HeaderComponent from "../components/HeaderComponent.vue";
  import PaginationComponent from "../components/PaginationComponent.vue"
  import PostDetail from "../components/atoms/PostDetail.vue"
  import TagLink from "../components/atoms/TagLink.vue"
  import { ref, onMounted } from "vue"
  import axios from "axios";
  import { useRouter, useRoute } from 'vue-router';
  
  // apiコールの取得件数
  const page_size = 30

  const router = useRouter()
  const route = useRoute()
  const likesort_posts = ref([]) //いいね順にソートされた投稿
  const popular_tags = ref([]) //人気タグ
  const params = ref(null) 
  const allpost_count = ref(null)
  const totalpage = ref(null)
  const currentPage = ref(null)
  const apiUrl = process.env.VUE_APP_API_DOMAIN;

  onMounted(() => {
    likesort_Search()
    popularTag_search()
  })


  const popularTag_search = async () => {
    await axios.get(`${apiUrl}/api/tags/`)
    .then((response) => {
      // 上位50タグに絞って表示
        popular_tags.value = response.data.slice(0, 50)

    })
    .catch((error) => {
        console.log(error)
    })
  }

  const likesort_Search = async (page) => {
    currentPage.value = page
    params.value = {
      page: page,
      page_size: page_size
    }

    await axios.get(`${apiUrl}/api/posts/`, {params: params.value})
    .then((response) => {
      if(currentPage.value === undefined) currentPage.value = 1
      likesort_posts.value = response.data.results
      allpost_count.value = response.data.count
      totalpage.value = Math.ceil(allpost_count.value / page_size)
      router.push({ path: route.path, query: { page: page } })

        
    })
    .catch((error) => {
        console.log(error)
    })
  };

</script>

<style scoped>
.custom-flex-ratio-left{
  flex: 1;
}

.custom-flex-ratio-right{
  flex: 6;
}
</style>