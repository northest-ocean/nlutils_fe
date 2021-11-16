<template>
  <div>
    <el-table
      :data="tableData"
      style="width: 100%"
      fit
      border
      height="750"
      @sort-change="changeTableSort"
      @selection-change="handleSelectionChange"
      ref="multipleTable"
      :cell-class-name="tableCellClassName"
    >
      <template v-for="(col, idx) in columns">
        <el-table-column
          v-if="idx === 0"
          :key="idx + 'f'"
          type="selection"
          align="center"
          width="180"
        >
        </el-table-column>
        <el-table-column
          :fixed="idx === 0"
          :key="idx"
          :prop="col.prop"
          :label="col.label"
          header-align="center"
          align="center"
          :show-overflow-tooltip="true"
          width="180"
          :sortable="'custom'"
        >
        </el-table-column>
      </template>
    </el-table>
  </div>
</template>

<script>
// import { parserParamJSONFile } from '../plugin/parameter-json-parser';
import { mapState } from "vuex";
/* eslint-disable */
import store from "../store/index";
export default {
  name: "TableTop",
  props: {
    parameters: {},
  },
  data() {
    return {
      columns: [],
      tableData: [],
      default_params: [
        "epoch",
        "learning_rate",
        "data"
      ],
    };
  },
  computed: {
    ...mapState({
      visible_paramters: (state) => state.params.visible_paramters,
    }),
  },
  mounted() {
    this.request_from_local();
  },
  watch: {
    visible_paramters(val) {
      // TODO set level-wised sort, name, time, id should go first
      this.columns = val.map((v) => {
        return { prop: v, label: v };
      });
      this.$nextTick(() => {
        this.$refs.multipleTable.doLayout();
        // el-table加ref="multipleTable"
      });
    },
  },

  methods: {
    filterHandler(value, row, column) {
      const property = column["property"];
      return row[property] === value;
    },
    tableCellClassName(cell) {
      let column = cell["column"];
      let row = cell["row"];
      let columnIndex = cell["columnIndex"];
      let rowIndex = cell["rowIndex"];
      if (Date.now() / 1000 - parseInt(row["end_time_stamp"]) < 24 * 3600) {
        if (columnIndex >= 2) return "newest-row-body";
        else return "newest-row-head";
      }
      return "";
    },
    handleSelectionChange(val) {
      console.log(val);
    },
    changeTableSort(column) {
      console.log(column);
      var fieldName = column.prop;
      var sortingType = column.order;
      if (fieldName == "createTime") {
        this.tableData.map((item) => {
          item.createTime = this.$moment(item.createTime).valueOf();
        });
      }

      if (sortingType == "descending") {
        this.tableData = this.tableData.sort((a, b) =>
          typeof b[fieldName] !== "string"
            ? b[fieldName] - a[fieldName]
            : a[fieldName].localeCompare(b[fieldName])
        );
      } else {
        this.tableData = this.tableData.sort((a, b) =>
          typeof b[fieldName] !== "string"
            ? b[fieldName] - a[fieldName]
            : b[fieldName].localeCompare(a[fieldName])
        );
      }
    },
    request_from_local() {
      let request = new XMLHttpRequest();
      request.open("GET", "params/parameters.json");
      request.send(null);
      let _this = this;
      request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
          let response = JSON.parse(request.responseText);
          let data = response;
          let parameters = Object.keys(data[0]["parameters"]);
          parameters = parameters.filter((val) => {
            if (this.visible_paramters !== undefined)
              return _this.visible_paramters.indexOf(val) !== -1;
            else return _this.default_params.indexOf(val) !== -1;
          });
          let results = Object.keys(data[0]["results"]);
          results = [
            "name",
            ...results,
            "time_consumed",
            ...parameters,
          ];
          _this.columns = results.map((val) => {
            return { prop: val, label: val };
          });
          let tmpTableData = [];

          for (let i = 0; i < data.length; i++) {
            let tmp = data[i]["results"];
            tmp = Object.assign(tmp, data[i]["parameters"]);
            tmp = Object.assign(tmp, data[i]);
            tmp = Object.assign(tmp, data[i]["basic_parameters"]);

            console.error(tmp);

            for (let i = 0; i < Object.keys(tmp).length; i++) {
              let key = Object.keys(tmp)[i];
              if (typeof tmp[key] === "number") {
                if (key === "learning_rate") tmp[key] = tmp[key].toFixed(4);
                else if (
                  key.includes("epoch") ||
                  key.includes("degree") ||
                  key.includes("num")
                )
                  tmp[key] = tmp[key].toFixed(0);
                else if (key.includes("temp")) tmp[key] = tmp[key].toFixed(1);
                else tmp[key] = tmp[key].toFixed(3);
              }
            }
            tmpTableData.push(tmp);
          }
          _this.$emit("func", Object.keys(tmpTableData[3]));
          _this.tableData = tmpTableData;
          console.log(tmpTableData)
        }
      };
    },
    request_from_webserver() {
      let url = "http://api.nlutils.org:8000/params";
      // let url = "http://127.0.0.1:8000/params";
      let request = new XMLHttpRequest();
      let _this = this;
      request.onreadystatechange = function () {
        if (request.readyState == 4) {
          let pobj = JSON.parse(request.responseText);
          let parameters = Object.keys(pobj.data[0]["parameters"]);
          parameters = parameters.filter((val) => {
            if (this.visible_paramters !== undefined)
              return _this.visible_paramters.indexOf(val) !== -1;
            else return _this.default_params.indexOf(val) !== -1;
          });
          let results = Object.keys(pobj.data[0]["results"]);
          results = [
            "name",
            "time_consumed",
            "end_time_stamp",
            ...parameters,
            ...results,
          ];
          _this.columns = results.map((val) => {
            return { prop: val, label: val };
          });
          let tmpTableData = [];

          for (let i = 0; i < pobj.data.length; i++) {
            let tmp = pobj.data[i]["results"];
            tmp = Object.assign(tmp, pobj.data[i]["parameters"]);
            tmp = Object.assign(tmp, pobj.data[i]);
            tmp = Object.assign(tmp, pobj.data[i]["basic_parameters"]);

            console.log(tmp);
            for (let i = 0; i < Object.keys(tmp).length; i++) {
              let key = Object.keys(tmp)[i];
              if (typeof tmp[key] === "number") {
                if (key === "learning_rate") tmp[key] = tmp[key].toFixed(4);
                else if (
                  key.includes("epoch") ||
                  key.includes("degree") ||
                  key.includes("num")
                )
                  tmp[key] = tmp[key].toFixed(0);
                else if (key.includes("temp")) tmp[key] = tmp[key].toFixed(1);
                else tmp[key] = tmp[key].toFixed(3);
              }
            }
            tmpTableData.push(tmp);
          }
          _this.$emit("func", Object.keys(tmpTableData[0]));
          _this.tableData = tmpTableData;
        }
      };
      request.open("POST", url, true);
      let data = {
        name: "",
        server: "heat",
      };
      request.send(JSON.stringify(data));
    },
  },
};
</script>

<style>
.el-table .newest-row-body {
  background: rgb(70, 43, 68, 0.2);
  color: rgb(8, 8, 8);
}

.el-table .newest-row-head {
  background: rgb(80, 103, 180);
  color: rgb(255, 255, 255);
}

.el-table__body .el-table__row.hover-row td {
  background: rgba(255, 181, 71, 0.7);
  font-size: 15px;
  font-weight: bold;
  color: rgb(78, 72, 72);
}
</style>
