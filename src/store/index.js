import Vue from "vue";
import Vuex from "vuex";

import params from "./params";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    params
  },
});
export default store;