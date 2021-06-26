<template>
  <el-container class="pipeLine-contanier">
    <el-header class="pipeLine-header" style="height: 54px">
      <el-form :inline="true">
        <el-row>
          <el-col :span="18">
            <el-button
              type="primary"
              icon="el-icon-folder-add"
              @click="versionFormVisible=true"
            >新建版本</el-button>
          </el-col>
          <el-col :span="6">
            <el-input v-model="listQuery.search" placeholder="请输入版本名称或版本号" clearable class="input-with-select" style="text-align: right">
              <el-button slot="append" icon="el-icon-search" />
            </el-input>
          </el-col>
        </el-row>
      </el-form>
    </el-header>
    <el-main class="pipeLine-main">
      <el-table
        :data="tableParam.tableData"
        header-row-class-name="headbg"
        fit
        style="width: 100%;"
      >
        <!-- <el-table-column type="index" label="序号" width="50" align="center" /> -->
        <el-table-column
          v-for="item in tableParam.tableLabel"
          :key="item.index"
          :prop="item.code"
          :label="item.label"
          align="center"
          :min-width="item.width"
        >
          <template slot-scope="scope">
            <el-col align="center">
              {{ scope.row[item.code] || scope.row[item.code] === 0 ? scope.row[item.code] : '--' }}
            </el-col>
          </template>
        </el-table-column>
        <el-table-column label="模板" min-width="250" align="center">
          <template slot-scope="{row}">
            <strong class="template-title">{{ row.templateName }}</strong>
            <Pipeline :data="row.templates" />
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="160" align="center">
          <template>
            <el-button type="text" @click="excuteFormVisible=true">执行</el-button>
            <el-button type="text" @click="templateVisible=true">模板</el-button>
            <el-button type="text" @click="versionFormVisible=true">编辑</el-button>
            <el-button type="text">复制</el-button>
            <el-button type="text">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-main>
    <el-footer>
      <pagination v-show="listQuery.total>0" class="pagination-container" :total="listQuery.total" :page.sync="listQuery.pageNum" :limit.sync="listQuery.pageSize" @pagination="getList" />
    </el-footer>
    <el-dialog title="执行选项" :visible.sync="excuteFormVisible" width="45%">
      <el-form :model="excuteForm">
        <el-form-item label="执行方式：" label-width="90px">
          <el-radio-group v-model="excute" size="small">
            <el-radio-button label="立即执行" />
            <el-radio-button label="预约执行" />
          </el-radio-group>
        </el-form-item>
        <el-form-item v-show="excute==='预约执行'" label="预约方式：" label-width="90px">
          <el-radio-group v-model="order" size="small">
            <el-radio :label="0">定时执行</el-radio>
            <el-radio :label="1">周期执行</el-radio>
            <el-radio :label="2">变更触发</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-show="excute==='预约执行' && order===0" label="执行时间：" label-width="90px">
          <el-date-picker
            v-model="excuteForm.onceTime"
            type="datetime"
            placeholder="选择日期时间"
            size="small"
          />
        </el-form-item>
        <el-form-item v-show="excute==='预约执行' && order===1" label="执行周期：" label-width="90px">
          <el-row>
            <el-col :span="12">
              <el-select v-model="excuteForm.cycle" placeholder="请选择周期" size="small">
                <el-option
                  v-for="item in excuteOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-col>
            <el-col :span="12">
              <el-time-picker
                v-model="excuteForm.time"
                placeholder="任意时间点"
                size="small"
              />
            </el-col>
          </el-row>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button
          type="primary"
          size="small"
          @click="excuteFormVisible=false"
        >确 定</el-button>
        <el-button type="info" size="small" @click="excuteFormVisible=false">取 消
        </el-button>
      </span>
    </el-dialog>
    <el-dialog
      :title="dialogTitle"
      :visible.sync="versionFormVisible"
      width="85vh"
    >
      <el-form :model="versionForm">
        <el-form-item label="制品来源：" label-width="90px">
          <el-radio-group v-model="product" size="small">
            <el-radio-button label="构建" />
            <el-radio-button label="制品库" />
          </el-radio-group>
        </el-form-item>
        <el-form-item v-show="product==='构建'" label="分支：" label-width="90px">
          <el-select v-model="versionForm.branch" placeholder="请选择分支" size="small" style="width: 60vh">
            <el-option
              v-for="item in branchOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item v-show="product==='构建'" label="提交号：" label-width="90px">
          <el-input v-model="versionForm.submit" placeholder="请输入提交号" suffix-icon="el-icon-edit" clearable size="small" style="width: 60vh" />
        </el-form-item>
        <el-form-item v-show="product==='制品库'" label="制品：" label-width="90px" />
        <el-form-item label="测试场景：" label-width="90px">
          <el-radio-group v-model="scan" size="small">
            <el-radio-button label="研发自测" />
            <el-radio-button label="正式构建" />
          </el-radio-group>
        </el-form-item>
        <el-form-item v-show="scan==='正式构建'" label="版本号：" label-width="90px">
          <el-row style="width: 60vh">
            <el-col :span="20">
              <el-input v-model="versionForm.structure" placeholder="请输入版本号" clearable size="small" />
            </el-col>
            <el-col :span="4" style="display: flex;padding: 1vh 0 0 3vh">
              <el-tooltip content="构建时打tag！" placement="top" effect="light">
                <svg-icon v-show="versionForm.isTag===true" icon-class="tag" style="font-size: 5vh;" @click="versionForm.isTag=false" />
              </el-tooltip>
              <el-tooltip content="构建时不打tag！" placement="top" effect="light">
                <svg-icon v-show="versionForm.isTag===false" icon-class="tag_b" style="font-size: 5vh;" @click="versionForm.isTag=true" />
              </el-tooltip>
            </el-col>
          </el-row>
        </el-form-item>
        <el-form-item label="描述：" label-width="90px">
          <el-input
            v-model="versionForm.describe"
            type="textarea"
            :autosize="{ minRows: 3, maxRows: 5}"
            placeholder="请输入描述"
            style="width: 60vh"
          />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button
          type="primary"
          size="small"
          @click="versionFormVisible=false"
        >确 定</el-button>
        <el-button type="info" size="small" @click="versionFormVisible=false">取 消
        </el-button>
      </span>
    </el-dialog>
    <el-dialog class="model_dialog" title="选择模板" :visible.sync="templateVisible" width="60%">
      <el-scrollbar
        style="height: 55vh"
        wrap-class="scrollbar-wrapper"
      >
        <el-row :gutter="16">
          <el-col v-for="(item, key) in templateList" :key="key" :span="12">
            <el-card class="box-card">
              <div slot="header" class="clearfix">
                <el-row style="line-height:30px;">
                  <el-col :span="2">
                    <el-radio v-model="radio" :label="item.id">{{ }}</el-radio>
                  </el-col>
                  <el-col :span="20"><strong>{{ item.name }}</strong></el-col>
                  <el-col :span="2">
                    <svg-icon icon-class="edit_b" @click="jumpTemplate(item.id)" />
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
      </el-scrollbar>
      <span slot="footer" class="dialog-footer">
        <el-button
          type="primary"
          size="small"
          @click="templateVisible=false"
        >确 定</el-button>
        <el-button type="info" size="small" @click="templateVisible=false">取 消
        </el-button>
      </span>
    </el-dialog>
  </el-container>
</template>

<script>
import Pagination from '@/components/Pagination'
import Pipeline from '@/components/Pipeline'
// import http from '@/api/xtest'
export default {
  name: 'Version',
  components: { Pagination, Pipeline },
  data() {
    return {
      tableParam: {
        tableLabel: [
          { width: 100, code: 'versionName', label: '版本名称' },
          { width: 50, code: 'versionId', label: '版本号' },
          { width: 50, code: 'creater', label: '创建人' },
          { width: 70, code: 'createTime', label: '创建时间' }
        ],
        tableData: [
          { 'versionName': 'test', 'versionId': '11111', 'creater': 'wtxu3', 'templateName': '自定义模板1', 'templates': [{ name: '静态扫描', status: '' }, { name: '构建', status: '' }] }
        ]
      },
      listQuery: {
        total: 10,
        pageNum: 1,
        pageSize: 5,
        search: ''
      },
      excuteOptions: [
        { value: 0, label: '每天' },
        { value: 1, label: '隔天' },
        { value: 2, label: '每周' }
      ],
      excute: '立即执行',
      order: '',
      excuteForm: {
        cycle: '',
        time: '',
        onceTime: ''
      },
      excuteFormVisible: false,
      versionFormVisible: false,
      product: '构建',
      scan: '研发自测',
      dialogTitle: '新建版本',
      branchOptions: [],
      versionForm: {
        isTag: true,
        branch: '',
        submit: '',
        structure: '',
        describe: ''
      },
      templateVisible: false,
      radio: '',
      templateList: [
        { id: '1', name: '自定义模板1', creater: 'wtxu3', createTime: '2021-04-01', changer: 'yfyang12', changeTime: '2021-04-12' },
        { id: '2', name: 'hahaha', creater: 'wtxu3', createTime: '2021-04-01', changer: '', changeTime: '' },
        { id: '3', name: '懵逼', creater: 'wtxu3', createTime: '2021-04-01', changer: 'yfwang50', changeTime: '2021-04-12' },
        { id: '4', name: '烦躁烦躁烦躁烦躁烦躁烦', creater: 'dstian', createTime: '2021-04-01', changer: 'xingchen7', changeTime: '2021-04-12' },
        { id: '5', name: '自定义模板1', creater: 'wtxu3', createTime: '2021-04-01', changer: 'yfyang12', changeTime: '2021-04-12' },
        { id: '6', name: 'hahaha', creater: 'wtxu3', createTime: '2021-04-01', changer: '', changeTime: '' },
        { id: '7', name: '懵逼', creater: 'wtxu3', createTime: '2021-04-01', changer: 'yfwang50', changeTime: '2021-04-12' },
        { id: '8', name: '烦躁烦躁烦躁烦躁烦躁烦', creater: 'dstian', createTime: '2021-04-01', changer: 'xingchen7', changeTime: '2021-04-12' }
      ]
    }
  },
  created() {
  },
  methods: {
    getList() {

    },
    jumpTemplate(id) {
      this.$router.push({ path: '/template/templateEdit', query: { Id: id }})
    }
  }
}
</script>
<style lang="scss">
.scrollbar-wrapper {
  overflow-x: hidden !important;
}
.model_dialog {
  .el-scrollbar__bar.is-horizontal {
    right: inherit;
    bottom: inherit;
  }
  .el-row {
    margin-left: 0 !important;
    margin-right: 0 !important;
  }
}
.el-form-item {
  margin-bottom: 7px;
}
.pipeLine-contanier{
 .el-table th{
   .cell {
     padding-left: 0;
   }
 }
}
.template-title{
  display: block;
  text-align: left;
  font-size: 10px;
  margin: 0 40px;
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
}
.el-table__header tr,
  .el-table__header th {
    padding: 0;
    height: 50px;
}
.el-table__body tr,
  .el-table__body td {
    padding: 0;
    height: 40px;
}
</style>
