<template>
  <el-container>
    <el-header>
      <el-row>
        <el-col :span="6">
          <el-input v-model="templateName" placeholder="请输入模板名" suffix-icon="el-icon-edit" clearable />
        </el-col>
        <el-col :span="18" style="text-align: right"><el-button type="success">保存</el-button></el-col>
      </el-row>
    </el-header>
    <el-main>
      <el-row>
        <el-col :span="5">
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span>卡片名称</span>
              <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button>
            </div>
            <!--            <div v-for="o in 4" :key="o" class="text item">-->
            <!--              {{'列表内容 ' + o }}-->
            <!--            </div>-->
          </el-card>
        </el-col>
      </el-row>
    </el-main>
    <el-main>{{ templateId }}</el-main>
  </el-container>
</template>

<script>
export default {
  name: 'TemplateEdit',
  data() {
    return {
      templateName: '',
      templateId: this.$route.query.Id
    }
  }
}
</script>

<style scoped>
.el-header {
  padding: 20px;
}
</style>
