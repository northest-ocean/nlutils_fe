<template>
  <div>
    <Selector
      :title="current_server === null ? 'Server' : current_server"
      :items="display_server_list"
    />
    <Selector
      :title="current_project === null ? 'Project' : current_project"
      :items="project_list"
    />
    <el-button type="text" @click="dialogTableVisible = true"
      >Select Visible Paramter</el-button
    >
    <el-dialog title="Paramter Selection" :visible.sync="dialogTableVisible">
      <el-table
        :data="parameter_list"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" label="CheckStatus"></el-table-column>
        <el-table-column
          property="name"
          label="Parameter Name"
        ></el-table-column>
        <el-table-column
          property="description"
          label="Parameter Description"
        ></el-table-column>
      </el-table>
    </el-dialog>
    <TableTop @func="get_params" />
  </div>
</template>

<script>
import { mapState } from "vuex";

import TableTop from "../components/TableTop";
import Selector from "../components/Selector";

export default {
  name: "Project",
  components: {
    TableTop,
    Selector,
  },
  data() {
    return {
      dialogTableVisible: false,
      multipleSelection: [],
      parameters: [],
    };
  },
  methods: {
    handleSelectionChange(val) {
      this.multipleSelection = val;
      let param_list = this.multipleSelection.map((selection) => {
        return selection["name"];
      });
      this.$store.commit("SET_VISIBLE_PARAMETERS", param_list);
    },
    get_params(data) {
      this.parameters = data;
    },
  },
  computed: {
    parameter_list() {
      let params_list = [];
      for (let i = 0; i < this.parameters.length; i++) {
        params_list.push({
          name: this.parameters[i],
          description: this.parameters[i],
        });
      }
      return params_list;
    },
    project_list() {
      if(!this.data) return ['Null'];
      let project_list = new Set();
      for(let i=0;i<this.data.length;i++){
        project_list.add(this.data[i].basic_parameters["name"])
      }
      return [...project_list];
    },
    display_server_list() {
      return this.server_list ? this.server_list : ["Demo"];
    },
    ...mapState({
      current_server: (state) => state.params.current_server,
      server_list: (state) => state.params.server_list,
      current_project: (state) => state.params.current_project,
      server_project_map: (state) => state.params.server_project_map,
      data: (state) => state.params.data,
    }),
  },
};
</script>

<style></style>
