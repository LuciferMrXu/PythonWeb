<template>
  <el-container class="pipeLine-contanier">
    <el-header class="pipeLine-header" style="height: 54px">
      <el-form :inline="true">
        <el-row>
          <el-col :span="18">
            <el-button
              type="primary"
              icon="el-icon-document-add"
              @click="outerVisible = true"
            >新建模板</el-button>
          </el-col>
          <el-col :span="6">
            <el-input v-model="search" placeholder="请输入模板名称" clearable class="input-with-select" style="text-align: right">
              <el-button slot="append" icon="el-icon-search" />
            </el-input>
          </el-col>
        </el-row>
      </el-form>
    </el-header>
    <el-main class="pipeLine-main">
      <el-row :gutter="16">
        <el-col v-for="(item, key) in templateList" :key="key" :span="8">
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <el-row style="line-height:30px;" type="flex">
                <el-col :span="22"><strong>{{ item.name }}</strong></el-col>
                <el-col :span="2">
                  <el-dropdown size="small">
                    <span class="el-dropdown-link">
                      <i class="el-icon-more" />
                    </span>
                    <el-dropdown-menu slot="dropdown">
                      <el-dropdown-item @click.native="jumpTemplate(item.id)"><i class="el-icon-edit" />编辑</el-dropdown-item>
                      <el-dropdown-item><i class="el-icon-copy-document" />复制</el-dropdown-item>
                      <el-dropdown-item><i class="el-icon-delete" />删除</el-dropdown-item>
                    </el-dropdown-menu>
                  </el-dropdown>
                </el-col>
              </el-row>
            </div>
            <div class="text item">
              <el-row>
                <el-col :span="12">创建人：{{ item.creater }}</el-col>
                <el-col :span="12">创建时间：{{ item.createTime }}</el-col>
              </el-row>
              <el-row>
                <el-col :span="12">修改人：{{ item.changer }}</el-col>
                <el-col :span="12">修改时间：{{ item.changeTime }}</el-col>
              </el-row>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
<!--    <el-dialog :visible.sync="outerVisible" :show-close="false" :fullscreen="true">-->
<!--      <template slot="title">-->
<!--        <div class="title-body">-->
<!--          <el-row type="flex" class="dialog_title" justify="space-between">-->
<!--            <el-col :span="20">-->
<!--              <el-input v-model="templateName" prefix-icon="el-icon-info" placeholder="请输入模板名称" style="width: 90vh" />-->
<!--            </el-col>-->
<!--            <el-col :span="4">-->
<!--              <el-button-group>-->
<!--                <el-button type="success" icon="el-icon-s-claim" >保存</el-button>-->
<!--                <el-button icon="el-icon-s-release">退出</el-button>-->
<!--              </el-button-group>-->
<!--            </el-col>-->
<!--          </el-row>-->
<!--        </div>-->
<!--      </template>-->
<!--      <el-dialog-->
<!--        v-el-drag-dialog-->
<!--        width="40%"-->
<!--        title="选择功能"-->
<!--        :visible.sync="innerVisible"-->
<!--        append-to-body-->
<!--        @dragDialog="handleDrag"-->
<!--      >-->
<!--        <el-row>-->
<!--          <el-col :span="6" style="text-align: center"><svg-icon icon-class="scan_b" style="font-size: 10vh;" />-->
<!--            <br><strong style="line-height: 36px">静态扫描</strong></el-col>-->
<!--          <el-col :span="6" style="text-align: center"><svg-icon icon-class="build" style="font-size: 10vh;" />-->
<!--            <br><strong style="line-height: 36px">构建</strong></el-col>-->
<!--          <el-col :span="6" style="text-align: center"><svg-icon icon-class="test_b" style="font-size: 10vh;" />-->
<!--            <br><strong style="line-height: 36px">测试</strong></el-col>-->
<!--          <el-col :span="6" style="text-align: center"><svg-icon icon-class="report_b" style="font-size: 10vh;" />-->
<!--            <br><strong style="line-height: 36px">报告</strong></el-col>-->
<!--        </el-row>-->
<!--        <el-row>-->
<!--          <el-col :span="6" style="text-align: center"><svg-icon icon-class="release" style="font-size: 10vh;" />-->
<!--            <br><strong style="line-height: 36px">发布</strong></el-col>-->
<!--        </el-row>-->
<!--      </el-dialog>-->
<!--      <el-container>-->
<!--        <el-header>Header</el-header>-->
<!--        <el-main>Main</el-main>-->
<!--      </el-container>-->
<!--      <div slot="footer" class="dialog-footer">-->
<!--        <el-button @click="outerVisible = false">取 消</el-button>-->
<!--        <el-button type="primary" @click="innerVisible = true">打开内层 Dialog</el-button>-->
<!--      </div>-->
<!--    </el-dialog>-->
  </el-container>
</template>

<script>
import elDragDialog from '@/directive/el-drag-dialog'
export default {
  name: 'Template',
  directives: { elDragDialog },
  data() {
    return {
      templateName: '',
      search: '',
      templateList: [
        { id: '1', name: '自定义模板1', creater: 'wtxu3', createTime: '2021-04-01', changer: 'yfyang12', changeTime: '2021-04-12' },
        { id: '2', name: 'hahaha', creater: 'wtxu3', createTime: '2021-04-01', changer: '', changeTime: '' },
        { id: '3', name: '懵逼', creater: 'wtxu3', createTime: '2021-04-01', changer: 'yfwang50', changeTime: '2021-04-12' },
        { id: '4', name: '烦躁烦躁烦躁烦躁烦躁烦', creater: 'dstian', createTime: '2021-04-01', changer: 'xingchen7', changeTime: '2021-04-12' },
        { id: '5', name: '自定义模板1', creater: 'wtxu3', createTime: '2021-04-01', changer: 'yfyang12', changeTime: '2021-04-12' },
        { id: '6', name: 'hahaha', creater: 'wtxu3', createTime: '2021-04-01', changer: '', changeTime: '' },
        { id: '7', name: '懵逼', creater: 'wtxu3', createTime: '2021-04-01', changer: 'yfwang50', changeTime: '2021-04-12' },
        { id: '8', name: '烦躁烦躁烦躁烦躁烦躁烦', creater: 'dstian', createTime: '2021-04-01', changer: 'xingchen7', changeTime: '2021-04-12' }
      ],
      outerVisible: false,
      innerVisible: false
    }
  },
  methods: {
    handleDrag() {
      this.$refs.select.blur()
    },
    jumpTemplate(id) {
      console.log(id)
      this.$router.push({ path: '/template/templateEdit', query: { Id: id }})
    }
  }
}
</script>
<style lang="scss">
/*.title-body {*/
/*  font-size: 20px;*/
/*  font-weight: bolder;*/
/*  height: 60px;*/
/*}*/
/*.el-dialog .el-dialog__body {*/
/*  border-bottom: 0*/
/*}*/
/*.el-dialog .el-dialog__header {*/
/*  border-bottom: 0*/
/*}*/
/*.dialog_title{*/
/*  height: 100%;*/
/*  margin-top: 16px;*/
/*}*/
.el-card{
		margin-bottom:16px; //下边距
}
.el-row {
  margin-bottom: 30px;
  &:last-child {
    margin-bottom: 0px;
  }
}
.el-col {
  border-radius: 4px;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
.text {
  font-size: 13px;
  color: #999;
}
.item {
  margin-bottom: 18px;
}
.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.clearfix:after {
  clear: both
}
.box-card {
  height: 165px;
}
.el-card__header{
  padding: 12px 8px;
}
.pipeLine-contanier{
 .el-table th{
   .cell {
     padding-left: 0;
   }
 }
}
.pipeLine-header{
  height: 100%;
  line-height: 30px;
  margin:auto 0;
  padding: 0;
}
.pipeLine-main{
  height: 100%;
  margin:auto 0;
  padding: 0;
  overflow-x: hidden;
}
</style>
