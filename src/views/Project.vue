<template>
  <div>
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
import TableTop from "../components/TableTop";
export default {
  name: "Project",
  components: {
    TableTop,
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
      console.log(param_list);
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
  },
};
</script>

<style></style>
