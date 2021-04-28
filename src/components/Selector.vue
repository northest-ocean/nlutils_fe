<template>
  <el-dropdown class="el-dropdown-title">
  <span class="el-dropdown-link">
    {{title}}<i class="el-icon-arrow-down el-icon--right"></i>
  </span>
  <el-dropdown-menu slot="dropdown">
      <template v-for="(item, idx) in items">
            <el-dropdown-item class="el-dropdown-item-text" :key="idx">{{item}}</el-dropdown-item>
      </template>
  </el-dropdown-menu>
</el-dropdown>
</template>

<script>
export default {
    name: "Selector",
    props: {
        title: {
            type: String,
            required: true,
        },
        items: {
            type: Array,
            required: true,
        }
    }
}
</script>

<style lang="less" scoped>  
.el-dropdown-title {
    height: 20px; 
    width: 100px;
    font-size: 18px;
}
.el-dropdown-link {
    color: #e0e9e7;
}
.el-dropdown-item-text {
    font-size: 18;
    font-weight: bold;
}
</style>