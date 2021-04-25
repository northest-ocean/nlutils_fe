const params = {
  state: {
    visible_paramters: ["name", "time", "epoch"],
  },
  getters: {},

  mutations: {
    SET_VISIBLE_PARAMETERS: (state, params) =>
      (state.visible_paramters = params),
  },

  actions: {},
};

export default params;
