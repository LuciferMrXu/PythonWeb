<template>
  <div class="project-contanier">
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="项目配置" name="project"><projectList v-if="activeName=='project'" /></el-tab-pane>
      <el-tab-pane label="节点配置" name="node"><nodeList v-if="activeName=='node'" /></el-tab-pane>
      <el-tab-pane label="模板配置" name="task"><taskList v-if="activeName=='task'" /></el-tab-pane>
    </el-tabs>
  </div>
</template>
<script>
import projectList from './projectList'
import nodeList from './nodeList'
import taskList from './taskList'
export default {
  name: 'Rainbow',
  components: {
    projectList,
    nodeList,
    taskList
  },
  data() {
    return {
      activeName: 'project'
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
