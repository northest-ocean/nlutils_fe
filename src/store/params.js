const params = {
  state: {
    visible_paramters: ["name", "time", "epoch"],
    server_list:null,
    current_server:null,
    project_list:null,
    current_project:null,
    server_project_map:null,
    data:null,
  },
  getters: {},

  mutations: {
    SET_VISIBLE_PARAMETERS: (state, val) => (state.visible_paramters = val),
    SET_SERVER_LIST: (state, val) => (state.server_list = val),
    SET_CURRENT_SERVER: (state, val) => (state.current_server = val),
    SET_PROJECT_LIST: (state, val) => (state.project_list = val),
    SET_CURRENT_PROJECT: (state, val) => (state.current_project = val),
    SET_SERVER_PROJECT_MAP: (state, val) => (state.server_project_map = val),
    SET_DATA: (state, val) => (state.data = val)
  },

  actions: {},
};

export default params;
