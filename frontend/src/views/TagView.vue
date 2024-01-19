<template>
    <div>
        <HeaderComponent></HeaderComponent>
        <h1 class="sm:text-3xl text-2xl font-medium title-font mb-8 text-gray-900 text-center mt-14">タグ検索</h1>
        <SearchAtom v-model:keyword="keyword" :placeholder="placeholder" @search="(word) => keyword = word"></SearchAtom>
        <div class="mx-auto max-w-screen-2xl px-4 lg:px-28 mt-14">
            <ul v-if="tags" class="grid sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-6 mt-8 gap-4">
                <TagLink :tagname="tag.tagname" :tagid=tag.id v-for="tag in filtered_tags" :key="tag"></TagLink>
            </ul>
        </div>
    </div>
</template>

<script setup>
    import HeaderComponent from '../components/HeaderComponent.vue';
    import SearchAtom from "../components/atoms/SearchAtom.vue"
    import TagLink from "../components/atoms/TagLink.vue"
    import axios from "axios";
    import { onMounted, ref, watch } from "vue"

    const keyword = ref("")
    const tags = ref([])
    const filtered_tags = ref([])
    const placeholder = "タグ名で検索できます"
    const apiUrl = process.env.VUE_APP_API_DOMAIN;


    onMounted(() => {
        tagSearch()
    })

    watch(keyword, (newkeyword) => {
        // 検索文字が変わる度にフィルタリングする
        filtered_tags.value = []
        tags.value.forEach(tag => {
            if(tag.tagname.toLowerCase().indexOf(newkeyword.toLowerCase()) !== -1){
                filtered_tags.value.push(tag);
            }
        });

    })

    const tagSearch = async () => {
       await  axios.get(`${apiUrl}/api/tags/`)
        .then((response) => {
            tags.value = response.data
            filtered_tags.value = tags.value            

        })
        .catch((error) => {
            console.log(error)
        })
    };


</script>
