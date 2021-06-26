<template>
  <div class="project-contanier">
    <el-tabs v-model="activeName" type="border-card" @tab-click="handleClick">
      <el-tab-pane label="版本列表" name="version"><versionList v-if="activeName=='version'" /></el-tab-pane>
      <el-tab-pane label="模板列表" name="template"><templateList v-if="activeName=='template'" /></el-tab-pane>
      <el-tab-pane label="历史记录" name="record"><recordList v-if="activeName=='record'" /></el-tab-pane>
    </el-tabs>
  </div>
</template>
<script>
import versionList from './versionList'
import templateList from './templateList'
import recordList from './recordList'
export default {
  name: 'Student',
  components: {
    versionList,
    templateList,
    recordList
  },
  data() {
    return {
      activeName: 'version'
    }
  },
  created() {

  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event)
    }
  }
}
</script>
<style lang="scss">
.project-contanier{
  background:#fff;
  padding:5px 20px 20px;
}
</style>
