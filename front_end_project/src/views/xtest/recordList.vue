<template>
  <el-container class="pipeLine-contanier">
    <el-header class="pipeLine-header" style="height: 54px">
      <el-form :inline="true">
        <el-row>
          <el-col :span="18">
            <el-radio-group v-model="record">
              <el-radio-button label="执行记录" />
              <el-radio-button label="预约记录" />
            </el-radio-group>
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
        <el-table-column label="状态" width="70" align="center">
          <template slot-scope="{row}">
            <el-tag :type="row.status | statusFilter">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="160" align="center">
          <template>
            <el-button type="text">执行</el-button>
            <el-button type="text">模板</el-button>
            <el-button type="text">编辑</el-button>
            <el-button type="text">复制</el-button>
            <el-button type="text">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-main>
    <el-footer>
      <pagination v-show="listQuery.total>0" class="pagination-container" :total="listQuery.total" :page.sync="listQuery.pageNum" :limit.sync="listQuery.pageSize" @pagination="getList" />
    </el-footer>
  </el-container>
</template>

<script>
import Pagination from '@/components/Pagination'
import Pipeline from '@/components/Pipeline'
// import http from '@/api/xtest'
export default {
  name: 'Record',
  components: { Pagination, Pipeline },
  filters: {
    statusFilter(status) {
      const statusMap = {
        成功: 'success',
        启动中: 'info',
        失败: 'danger',
        运行中: 'primary'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      record: '执行记录',
      tableParam: {
        tableLabel: [
          { width: 100, code: 'versionName', label: '版本名称' },
          { width: 60, code: 'versionId', label: '版本/构建号' },
          { width: 50, code: 'creater', label: '执行人' },
          { width: 70, code: 'createTime', label: '执行时间' }
        ],
        tableData: [
          { 'versionName': 'test', 'versionId': '11111', 'creater': 'wtxu3', 'status': '启动中', 'templateName': '自定义模板1', 'templates': [{ name: '静态扫描', status: 'sucess' }, { name: '构建', status: 'active' }] },
          { 'versionName': 'test2', 'versionId': '10086', 'creater': 'wtxu3', 'createTime': '2021-04-01', 'status': '运行中', 'templateName': '自定义模板2048', 'templates': [{ name: '静态扫描', status: 'sucess' }, { name: '构建', status: 'sucess' }, { name: '测试', status: 'active' }, { name: '报告', status: '' }, { name: '发布', status: '' }] },
          { 'versionName': 'test2', 'versionId': '10086', 'creater': 'wtxu3', 'createTime': '2021-04-01', 'status': '失败', 'templateName': '自定义模板12138', 'templates': [{ name: '静态扫描', status: 'sucess' }, { name: '构建', status: 'fail' }, { name: '测试', status: '' }, { name: '报告', status: '' }, { name: '发布', status: '' }] }
        ]
      },
      listQuery: {
        total: 10,
        pageNum: 1,
        pageSize: 5,
        search: ''
      }
    }
  },
  created() {

  },
  methods: {
    getList() {

    }
  }
}
</script>
<style lang="scss">
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
