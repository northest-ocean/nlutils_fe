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
          width="120"
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
          width="120"
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
        "induc_epoch",
        "user_degree_threshold",
        "item_degree_threshold",
        "learning_rate",
        "temp",
        "network",
      ],
    };
  },
  computed: {
    ...mapState({
      visible_paramters: (state) => state.params.visible_paramters,
    }),
  },
  mounted() {
    // this.getDeviceTypes();
    let url = "http://api.nlutils.org:8000/params";
    // let url = "http://127.0.0.1:8000/params";
    let request = new XMLHttpRequest();
    let _this = this;
    request.onreadystatechange = function () {
      if (request.readyState == 4) {
        // console.log(request.responseText.substring(40850, 40870));
        let pobj = JSON.parse(request.responseText);
        let parameters = Object.keys(pobj.data[0]["parameters"]);
        parameters = parameters.filter((val) => {
          // console.log(val);
          // console.log(_this.visible_paramters);
          if (this.visible_paramters !== undefined)
            return _this.visible_paramters.indexOf(val) !== -1;
          else return _this.default_params.indexOf(val) !== -1;
        });
        let results = Object.keys(pobj.data[0]["results"]);
        results = ["name", "time_consumed", "end_time_stamp", ...parameters, ...results];
        _this.columns = results.map((val) => {
          return { prop: val, label: val };
        });
        let tmpTableData = [];

        for (let i = 0; i < pobj.data.length; i++) {
          let tmp = pobj.data[i]["results"];
          tmp = Object.assign(tmp, pobj.data[i]["parameters"]);
          tmp = Object.assign(tmp, pobj.data[i]);
          tmp = Object.assign(tmp, pobj.data[i]["basic_parameters"]);
          // compatible with 0.0.12 before
          // tmp["time_consumed"] = Math.abs(pobj.data[i]["time_consumed"]) ? Math.abs(pobj.data[i]["time_consumed"]) : Math.abs(pobj.data[i]["basic_parameters"]["time_consumed"]);
          // tmp["end_time_stamp"] = parseInt(pobj.data[i]["end_time_stamp"]) ? parseInt(pobj.data[i]["end_time_stamp"]) : parseInt(pobj.data[i]["basic_parameters"]["end_time_stamp"]);
          // tmp["name"] = pobj.data[i]["name"] ? pobj.data[i]["name"] : pobj.data[i]["basic_parameters"]["name"];
          // tmp["time"] = pobj.data[i]["time"] ? pobj.data[i]["time"] : pobj.data[i]["basic_parameters"]["time"];
          // tmp["start_time_stamp"] = parseInt(pobj.data[i]["start_time_stamp"]) ? parseInt(pobj.data[i]["start_time_stamp"]) : parseInt(pobj.data[i]["basic_parameters"]["start_time_stamp"]);
          // tmp["description"] = pobj.data[i]["description"] ? pobj.data[i]["description"] : pobj.data[i]["basic_parameters"]["description"];

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
      const property = column['property'];
      return row[property] === value;
    },
    tableCellClassName(cell) {
      let column = cell['column'];
      let row = cell['row'];
      let columnIndex = cell['columnIndex'];
      let rowIndex = cell['rowIndex'];
      if(Date.now() / 1000 - parseInt(row['end_time_stamp']) < 24 * 3600) {
        if(columnIndex >= 2)
          return 'newest-row-body';
        else
          return 'newest-row-head'
      }
      return '';
    },
    handleSelectionChange(val) {
      console.log(val);
    },
    changeTableSort(column) {
      console.log(column);
      //获取字段名称和排序类型
      var fieldName = column.prop;
      var sortingType = column.order;
      //如果字段名称为“创建时间”，将“创建时间”转换为时间戳，才能进行大小比较
      if (fieldName == "createTime") {
        this.tableData.map((item) => {
          item.createTime = this.$moment(item.createTime).valueOf();
        });
      }

      //按照降序排序
      if (sortingType == "descending") {
        this.tableData = this.tableData.sort((a, b) =>
          typeof b[fieldName] !== "string"
            ? b[fieldName] - a[fieldName]
            : a[fieldName].localeCompare(b[fieldName])
        );
      }
      //按照升序排序
      else {
        this.tableData = this.tableData.sort((a, b) =>
          typeof b[fieldName] !== "string"
            ? b[fieldName] - a[fieldName]
            : b[fieldName].localeCompare(a[fieldName])
        );
      }
    },
  },
};
</script>

<style>
.el-table .newest-row-body {
  background:rgb(70, 43, 68, 0.2);
  color: rgb(8, 8, 8);
}

.el-table .newest-row-head {
  background:rgb(80, 103, 180);
  color: rgb(255, 255, 255);
}

.el-table__body .el-table__row.hover-row td {
    background: rgba(255, 181, 71, 0.7);
    font-size: 15px;
    font-weight: bold;
    color: rgb(78, 72, 72);
}

</style>
