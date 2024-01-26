import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import TagView from '../views/TagView.vue'
import PostView from '../views/PostView.vue'
import TagpostView from '../views/TagpostView.vue'
import ProfileView from '../views/ProfileView.vue'
import LikeView from '../views/LikeView.vue'
import BookmarkView from '../views/BookmarkView.vue'

const SERVICE_NAME = "DevSearch"

const routes = [
  {
    path: '/',
    redirect: 'home',
    meta: {
      title: 'ホーム - ' + SERVICE_NAME
    }
  },
  {
    path: '/home',
    name: 'home',
    component: HomeView,
    meta: {
      title: 'ホーム - ' + SERVICE_NAME
    }
  },
  {
    path: '/tag',
    name: 'tag',
    component: TagView,
    meta: {
      title: 'タグ検索 - ' + SERVICE_NAME
    }

  },
  {
    path: '/tag/:tagid/:tagname/',
    name: 'tagpost',
    component: TagpostView,
    props: true,
    meta: {
      title: 'タグ詳細 - ' + SERVICE_NAME
    }
  },
  {
    path: '/post',
    name: 'post',
    component: PostView,
    meta: {
      title: '記事一覧 - ' + SERVICE_NAME
    }
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: {
      title: 'プロフィール - ' + SERVICE_NAME
    },
    children: [
      {
        path: "like",
        component: LikeView
      },
      {
        path: "bookmark",
        component: BookmarkView
      }
    ]
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupView,
    meta: {
      title: '新規登録 - ' + SERVICE_NAME
    }
  },
  {
    path: '/login',
    name: 'Article',
    component: LoginView,
    meta: {
      title: 'ログイン - ' + SERVICE_NAME
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? to.meta.title : "DevSearch"
 
  next() 
})

export default router
