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
import store from '../store'; // Vuexストアをインポート


const routes = [
  {
    path: '/home',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/tag',
    name: 'tag',
    component: TagView,
    // meta: { requiresAuth: true },

  },
  {
    path: '/tag/:tagid/:tagname/',
    name: 'tagpost',
    component: TagpostView,
    props: true
  },
  {
    path: '/post',
    name: 'post',
    component: PostView
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
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
    component: SignupView
  },
  {
    path: '/login',
    name: 'Article',
    component: LoginView
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
  if (to.meta.requiresAuth && !store.getters.isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router
