<template>
  <div>
    <el-table
      class="tableTop"
      :data="tableData"
      style="width: 100%"
      @sort-change="changeTableSort"
      :default-sort="{ prop: 'date', order: 'ascending' }"
    >
      <template  v-for="(col, idx) in columns">
        <el-table-column
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

export default {
  name: "TableTop",
  props: {
    tableData2: {
      type: Array,
      default: function () {
        return [];
      },
    },
  },
  data() {
    return {
      columns: [
        {
          prop: "date",
          label: "Date"
        },
        {
          prop: "time",
          label: "Time"
        },
        {
          prop: "epoch",
          label: "Epoch"
        },
      ],
      tableData: [
        {
          "date": '2012-2-3',
          "time": "12312412",
          "epoch": 180
        },
        {
          "date": '2012-2-1',
          "time": "12312412",
          "epoch": 120
        },
        {
          "date": '2012-1-2',
          "time": "12312412",
          "epoch": 50
        }
      ]
    };
  },
    mounted() {
      // this.getDeviceTypes();
      let url = "http://localhost:8000/params";
      let request = new XMLHttpRequest();
      let _this = this;
      request.onreadystatechange = function() {
        if (request.readyState == 4) {
          let pobj = JSON.parse(request.responseText);
          let parameters = Object.keys(pobj.data[0]['parameters']);
          parameters = parameters.filter(val => {
            // console.log(val);
            return ['epoch', 'induc_epoch', 'user_degree_threshold', 'item_degree_threshold', 'learning_rate', 'temp', 'network'].indexOf(val) !== -1;
          });
          let results = Object.keys(pobj.data[0]['results']);
          results = [...parameters, ...results];
          _this.columns = results.map(val => {
            return {prop: val, label: val.substring(0, 11)};
          });
          let tmpTableData = [];
          for(let i=0;i<pobj.data.length;i++) {
            let tmp = pobj.data[i]['results'];
            tmp = Object.assign(tmp, pobj.data[i]['parameters']);
            for(let i=0;i<Object.keys(tmp).length;i++) {
              let key = Object.keys(tmp)[i];
              if (typeof tmp[key] === "number") {
                if(key === 'learning_rate')
                  tmp[key] = tmp[key].toFixed(4);
                else if(key.includes('epoch') || key.includes('degree') || key.includes('num'))
                  tmp[key] = tmp[key].toFixed(0);
                else if(key.includes('temp'))
                  tmp[key] = tmp[key].toFixed(1);
                else
                  tmp[key] = tmp[key].toFixed(3);
              }
            }
            tmpTableData.push(tmp);
          }
          // console.log(tmpTableData);
          _this.tableData = tmpTableData;
        }
      }
      request.open("POST", url, true);
      let data = {
        name:"HybrdModel-induc-user-item"
      }
      request.send(JSON.stringify(data));
  },

  methods: {
    //   //初始化加载列表
    //   getDeviceTypes() {
    //     this.loading = true;

    //     //将“创建时间”转换为所需的时间格式
    //     this.tableData.map(item => {
    //         item.createTime = this.$moment(item.createTime).format("YYYY-MM-DD HH:mm:ss");
    //     });

    //     this.loading = false;
    // },

    // 监听事件
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
        this.tableData = this.tableData.sort(
          (a, b) => b[fieldName] - a[fieldName]
        );
      }
      //按照升序排序
      else {
        this.tableData = this.tableData.sort(
          (a, b) => a[fieldName] - b[fieldName]
        );
      }
      //如果字段名称为“创建时间”，将时间戳格式的“创建时间”再转换为时间格式
      //   if(fieldName=="createTime"){
      //     this.tableData.map(item => {
      //         item.createTime = this.$moment(item.createTime).format(
      //              "YYYY-MM-DD HH:mm:ss"
      //         );
      //     });
      // }

      console.log(this.tableData);
    },
  },
};
</script>

<style lang="less" scoped></style>
