// src/store/index.js
import { createStore } from 'vuex';
import createPersistedState from 'vuex-persistedstate'

export default createStore({
  state: {
    accessToken: null,
    refreshToken: null,
    login_user: null
  },

  mutations: {
    setAccessToken(state, token) {
      state.accessToken = token;
    },
    setRefreshToken(state, token) {
      state.refreshToken = token;
    },
    setLoginUser(state, user) {
      state.login_user = user
    },
    clearAccessToken(state) {
      state.accessToken = null;
    },
    clearRefreshToken(state) {
      state.refreshToken = null;
    },
    clearLoginUser(state){
      state.login_user = null
    }
  },

  actions: {
    setAccessToken({ commit }, token) {
      commit('setAccessToken', token);
    },
    setRefreshToken({ commit }, token) {
      commit('setRefreshToken', token);
    },
    setLoginUser({ commit }, user) {
      commit('setLoginUser', user);
    },
    clearAccessToken({ commit }) {
      commit('clearAccessToken');
    },
    clearRefreshToken({ commit }) {
      commit('clearRefreshToken');
    },
    clearLoginUser({ commit }){
      commit('clearLoginUser');
    }
  },
  getters: {
    getAccessToken: state => {
      return state.accessToken
    },

    getRefreshToken: state => {
      return state.refreshToken
    },


    isAuthenticated: state => {
      return state.accessToken !== null;
    },
  },

  // `createPersistedState()`でインスタンス作成。引数に設定を書く
  plugins: [createPersistedState(
    { // ストレージのキーを指定。デフォルトではvuex
      key: 'authuser_info',

      // 管理対象のステートを指定。pathsを書かない時は`modules`に書いたモジュールに含まれるステート全て。`[]`の時はどれも保存されない
      // paths: ["auth"],

      // ストレージの種類を指定する。デフォルトではローカルストレージ
      // storage: window.sessionStorage
    }
  )]
});
