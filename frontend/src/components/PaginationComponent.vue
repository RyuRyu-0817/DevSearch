<template>
    <div class="max-w-2xl pt-16 pb-16">
        <nav aria-label="Page navigation example">  
            <ul class="inline-flex -space-x-px items-center">
                <li v-if="currentPage !== 1 && totalpage !== 0"> 
                    <button @click="to_previous(keywords)" class="bg-white border border-gray-300 text-gray-500 hover:bg-gray-100 hover:text-gray-700 leading-tight py-2 px-3 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">前へ</button>
                </li>
                <li v-for="page in pages(currentPage, totalpage)" :key="page">
                    <div v-if="currentPage == page" @click="to_page(page, keywords)" class="bg-indigo-500 border border-gray-300 text-white hover:bg-gray-100 hover:text-gray-700 leading-tight py-2 px-3 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">{{ page }}</div>
                    <div v-else-if="page == 0" class="text-gray-500 leading-tight py-2 px-3 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400">・・・</div>
                    <button v-else  @click="to_page(page, keywords)" class="bg-white border border-gray-300 text-gray-500 hover:bg-gray-100 hover:text-gray-700 leading-tight py-2 px-3 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">{{ page }}</button>
                </li>
                <li v-if="currentPage !== totalpage && totalpage !== 0"> 
                    <button  @click="to_next" class="bg-white border border-gray-300 text-gray-500 hover:bg-gray-100 hover:text-gray-700 leading-tight py-2 px-3 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">次へ</button>
                </li>
            </ul>
        </nav>
    </div>
</template>

<script setup>
    import { defineProps, defineEmits } from "vue"

    /*
        ページネーションコンポーネントを使うときに与える引数
        pagename:  ページネーションを使いたいページの名前
        keywords:  検索ワードがあればクエリに一緒にのせる  (任意)
        currentPage:  現在のページはどこか
        totalpage:  全体で何ページあるか
        to_previous (page) => 指定関数: 前へが押されたときに指定する関数
        to_page (page) => 指定関数:  ページ番号を押されたときに指定する関数
        to_next (page) => 指定関数: 次へが押されたときに指定する関数
    */

    const props = defineProps({ // eslint-disable-line
        pagename: String,
        keywords: {type: String, required: false},
        currentPage: Number,
        totalpage: Number
    })

    const emit = defineEmits(["to_previous", "to_page", "to_next"])

    const to_previous = (keywords) => {
        emit('to_previous', keywords);
    };
    
    const to_page = (page, keywords) => {
        emit("to_page", page, keywords)
    }

    const to_next = (keywords) => {
        emit('to_next', keywords);
    };

    const pages = (currentpage, totalpage) => {
        /* 
        input: currentpage(現在のページ), totalpage(全部で何ページか)
        ouput: 表示されるページネーション（省略部分は0）
        */

        let current = currentpage,
        last = totalpage,
        delta = 1,
        left = current - delta,
        right = current + delta + 1,
        range = [],
        rangeWithDots = [],
        l;

        // ページネーションで表示する部分
        for (let i = 1; i <= last; i++) {
            if (i == 1 || i == last || i >= left && i < right) {
                range.push(i);
            }
        
        }

        // 省略部分を配列に追加
        for (let i of range) {
            if (l) {
                if (i - l === 2) {
                    rangeWithDots.push(l + 1);
                } 
                else if (i - l !== 1) {
                    rangeWithDots.push(0);
                }
            }
            rangeWithDots.push(i);
            l = i;
        }

        return rangeWithDots;

    }
</script>
