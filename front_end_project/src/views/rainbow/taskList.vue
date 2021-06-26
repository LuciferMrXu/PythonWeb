<template>
  <div class="scoreList-contanier">
    <el-form :inline="true" style="height: 60px">
      <el-row>
        <el-col :span="7">
          <el-input v-model="listQuery.search" placeholder="请输入搜索内容" class="input-with-select" clearable>
            <el-button slot="append" icon="el-icon-search" @click="getList" />
          </el-input>
        </el-col>
        <el-col :span="17" style="text-align: right">
          <el-button-group>
            <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              @click="addHandler"
            >添加模板</el-button>
          </el-button-group>
        </el-col>
      </el-row>
    </el-form>
    <div class="table">
      <el-table :data="tableParam.tableData" header-row-class-name="headbg">
        <el-table-column type="index" label="序号" width="50" align="center" />
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
        <el-table-column label="操作" min-width="100" align="center">
          <template slot-scope="scope">
            <el-button type="primary" icon="el-icon-edit" size="small" circle @click="editHandler(scope.row)" />
            <el-button type="danger" icon="el-icon-delete" size="small" circle @click="deleteHandler(scope.row)" />
          </template>
        </el-table-column>
      </el-table>
      <pagination v-show="listQuery.total>0" class="pagination-container" :total="listQuery.total" :page.sync="listQuery.pageNum" :limit.sync="listQuery.pageSize" @pagination="getList" />
    </div>
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="36%"
      :show-close="false"
      :close-on-click-modal="false"
    >
      <el-form
        ref="taskForm"
        :model="taskForm"
        :rules="rules"
        label-width="100px"
        label-position="right"
        size="mini"
      >
        <el-form-item label="模板名称" prop="describe">
          <el-input v-model="taskForm.describe" :disabled="isEdit" suffix-icon="el-icon-edit" clearable style="width: 90%" />
        </el-form-item>
        <el-form-item v-show="isEdit==false" label="模板ID">
          <el-input-number v-model="taskForm.name" :min="0" />
        </el-form-item>
        <el-form-item label="任务流程" prop="pipeline">
          <el-input v-model="taskForm.pipeline" suffix-icon="el-icon-edit" clearable style="width: 90%" />
        </el-form-item>
        <el-form-item label="所属项目" prop="project">
          <el-select v-model="taskForm.project" placeholder="请选择所属项目" style="width: 90%">
            <el-option
              v-for="item in projectOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button
          type="primary"
          size="mini"
          @click="submitForm"
        >确 定</el-button>
        <el-button type="info" size="mini" @click="closeDialogForm">取 消
        </el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import Pagination from '@/components/Pagination'
import http from '@/api/rainbow'
export default {
  name: 'TaskList',
  components: { Pagination },
  data() {
    return {
      dialogVisible: false,
      dialogTitle: '',
      isEdit: false,
      rules: {
        describe: [
          { required: true, message: '任务名称不能为空', trigger: 'blur' }
        ],
        pipeline: [
          { required: true, message: '任务流程不能为空', trigger: 'blur' }
        ],
        project: [
          { required: true, message: '所属项目不能为空', trigger: 'change' }
        ]
      },
      tableParam: {
        tableLabel: [
          { width: 120, code: 'describe', label: '模板名称' },
          { width: 50, code: 'name', label: '模板ID' },
          { width: 150, code: 'pipeline', label: '任务流程' },
          { width: 100, code: 'pro_name', label: '所属项目' },
          { width: 100, code: 'add_time', label: '创建时间' }
        ],
        tableData: [],
        relationShip: []
      },
      listQuery: {
        total: 0,
        pageNum: 1,
        pageSize: 5,
        search: ''
      },
      taskOptions: [
        { value: 0, label: '模型更新' },
        { value: 1, label: '引擎更新' },
        { value: 2, label: '模型&引擎更新' },
        { value: 3, label: '新方案产品化' },
        { value: 4, label: '引擎支持' },
        { value: 5, label: '标准IPD流程' }
      ],
      projectOptions: [],
      taskForm: {
        id: '',
        describe: '',
        name: '',
        pro_name: '',
        pipeline: '',
        project: ''
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    closeDialogForm() {
      this.$refs.taskForm.resetFields()
      this.taskForm = {
        id: '',
        describe: '',
        pro_name: '',
        name: '',
        pipeline: '',
        project: ''
      }
      this.dialogVisible = false
      this.isEdit = false
    },
    getList() {
      http.getProject().then(res => {
        // console.log(res)
        this.tableParam.relationShip = res.data
        this.projectOptions = []
        for (const id in this.tableParam.relationShip) {
          const obj = {
            'value': Number(id),
            'label': this.tableParam.relationShip[id]
          }
          this.projectOptions.push(obj)
        }
        // console.log(this.projectOptions)
        http.getTask(this.listQuery.pageNum, this.listQuery.pageSize, this.listQuery.search)
          .then(res => {
            // console.log(res)
            this.tableParam.tableData = res.data.results
            this.tableParam.tableData.forEach(val => {
              val.add_time = this.$moment(val.add_time).format('YYYY-MM-DD')
              // val['project'] = this.tableParam.relationShip[val['project']]
            })
            this.listQuery.total = res.data.count
          }).catch((err) => {
            console.log(err)
            this.$message.error(err)
          })
      }).catch((err) => {
        console.log(err)
        this.$message.error(err)
      })
    },
    addHandler() {
      this.dialogTitle = '新增模板'
      this.dialogVisible = true
    },
    submitForm() {
      this.$refs.taskForm
        .validate()
        // 校验成功后执行添加或修改
        .then(() => {
          if (this.isEdit) {
            http.updateTask(this.taskForm.id, this.taskForm).then(res => {
              this.$message.success('修改模板成功！')
              this.getList()
              this.closeDialogForm()
            }).catch((err) => {
              console.log(err)
              this.$message.error(err)
            })
          } else {
            this.taskForm.name = Number(this.taskForm.name)
            this.taskForm.pro_name = this.tableParam.relationShip[this.taskForm.project]
            console.log(this.taskForm)
            http.createTask(this.taskForm).then(res => {
              this.$message.success('创建模板成功！')
              this.getList()
              this.closeDialogForm()
            }).catch((err) => {
              console.log(err)
              this.$message.error(err)
            })
          }
        })
        .catch(error => {
          console.log('error', error)
        })
    },
    editHandler(row) {
      http.readTask(row.id).then(res => {
        this.dialogTitle = '编辑模板'
        this.dialogVisible = true
        this.taskForm = res.data
        // console.log(this.taskForm)
        // console.log(this.projectOptions)
        this.isEdit = true
      }).catch((err) => {
        console.log(err)
        this.$message.error(err)
      })
    },
    deleteHandler(row) {
      this.$confirm('是否确认删除【' + row.name + '】模板？',
        '提示', {
          confirmButtonText: '确定删除',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
        http.delTask(row.id).then(res => {
          this.$message.success('删除模板成功！')
          http.delInfo({ 'taskId': row.id })
          this.getList()
        }).catch((err) => {
          console.log(err)
          this.$message.error(err)
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    }
  }
}
</script>
<style lang="scss">
.scoreList-contanier{
 .el-table th{
   .cell {
     padding-left: 0;
   }
 }
}
</style>
