<template>
  <div>
    <el-table
      class="tableTop"
      :data="tableData"
      style="width: 100%"
      @sort-change="changeTableSort"
      :default-sort="{ prop: 'date', order: 'ascending' }"
    >
      <!-- <el-table-column
        label="时间"
        type="index"
        header-align="left"
        align="left"
      >
      </el-table-column> -->
      <div  v-for="(col, index) in columns" :key="index">
        <el-table-column
          :prop="col.prop"
          :label="col.label"
          header-align="left"
          align="left"
          :show-overflow-tooltip="true"
          :sortable="'custom'"
        >
        </el-table-column>
      </div>
      <!-- <el-table-column
        prop="time"
        label="Time"
        header-align="left"
        align="left"
        :show-overflow-tooltip="true"
      >
      </el-table-column>
      <el-table-column
        prop="name"
        label="Name"
        header-align="left"
        align="left"
        sortable
        :show-overflow-tooltip="true"
      >
        <template slot-scope="scope">
          {{ scope.row.amount | formatNum }}
        </template>
      </el-table-column>
      <el-table-column
        prop="epoch"
        label="epoch"
        header-align="left"
        align="left"
        :sortable="'custom'"
        :show-overflow-tooltip="true"
      >
      </el-table-column>
      <el-table-column
        prop="m_num"
        label="购买人数"
        header-align="left"
        align="left"
        :sortable="'custom'"
        :show-overflow-tooltip="true"
      >
        <template slot-scope="scope">
          {{ scope.row.m_num | formatNum }}
        </template>
      </el-table-column>
      <el-table-column
        prop="o_num"
        label="订单数"
        header-align="left"
        align="left"
        :sortable="'custom'"
        :show-overflow-tooltip="true"
      > -->
        <!-- <template slot-scope="scope">
          {{ scope.row.o_num | formatNum }}
        </template>
      </el-table-column> -->
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
      var url = "./x.json";/*json文件url，本地的就写本地的位置，如果是服务器的就写服务器的路径*/
      fetch(url)
        .then(function(response) {
          console.log(response);
          return response.json();
        })
        .then(function(myJson) {
          console.log(myJson);
        });
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
