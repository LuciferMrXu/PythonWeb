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
            >添加节点</el-button>
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
        ref="nodeForm"
        :model="nodeForm"
        :rules="rules"
        label-width="100px"
        label-position="right"
        size="mini"
      >
        <el-form-item label="节点名称" prop="describe">
          <el-input v-model="nodeForm.describe" :disabled="isEdit" suffix-icon="el-icon-edit" clearable style="width: 90%" />
        </el-form-item>
        <el-form-item v-show="isEdit==false" label="节点ID">
          <el-input-number v-model="nodeForm.name" :min="0" />
        </el-form-item>
        <el-form-item label="子节点" prop="child_node">
          <el-input v-model="nodeForm.child_node" suffix-icon="el-icon-edit" clearable style="width: 90%" />
        </el-form-item>
        <el-form-item label="默认负责人">
          <el-input v-model="nodeForm.principal" suffix-icon="el-icon-edit" clearable style="width: 90%" />
        </el-form-item>
        <el-form-item label="所属项目" prop="project">
          <el-select v-model="nodeForm.project" placeholder="请选择所属项目" style="width: 90%">
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
  name: 'NodeList',
  components: { Pagination },
  data() {
    return {
      dialogVisible: false,
      dialogTitle: '',
      isEdit: false,
      rules: {
        describe: [
          { required: true, message: '节点名称不能为空', trigger: 'blur' }
        ],
        child_node: [
          { required: true, message: '子节点不能为空', trigger: 'blur' }
        ],
        project: [
          { required: true, message: '所属项目不能为空', trigger: 'change' }
        ]
      },
      tableParam: {
        tableLabel: [
          { width: 100, code: 'describe', label: '节点名称' },
          { width: 50, code: 'name', label: '节点ID' },
          { width: 150, code: 'child_node', label: '子节点' },
          { width: 100, code: 'principal', label: '默认负责人' },
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
      // nodeOptions: [
      //   { value: 0, label: '概念' },
      //   { value: 1, label: '计划' },
      //   { value: 2, label: '研究' },
      //   { value: 3, label: '开发' },
      //   { value: 4, label: '验证' },
      //   { value: 5, label: '发布' }
      // ],
      projectOptions: [],
      nodeForm: {
        id: '',
        name: '',
        describe: '',
        pro_name: '',
        child_node: '',
        principal: '',
        project: ''
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    closeDialogForm() {
      this.$refs.nodeForm.resetFields()
      this.nodeForm = {
        id: '',
        describe: '',
        name: '',
        pro_name: '',
        child_node: '',
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
        http.getNode(this.listQuery.pageNum, this.listQuery.pageSize, this.listQuery.search)
          .then(res => {
            // console.log(res)
            this.tableParam.tableData = res.data.results
            this.tableParam.tableData.forEach(val => {
              val.add_time = this.$moment(val.add_time).format('YYYY-MM-DD')
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
      this.dialogTitle = '新增节点'
      this.dialogVisible = true
    },
    submitForm() {
      this.$refs.nodeForm
        .validate()
        // 校验成功后执行添加或修改
        .then(() => {
          if (this.isEdit) {
            http.updateNode(this.nodeForm.id, this.nodeForm).then(res => {
              this.$message.success('修改节点成功！')
              this.getList()
              this.closeDialogForm()
            }).catch((err) => {
              console.log(err)
              this.$message.error(err)
            })
          } else {
            this.nodeForm.name = Number(this.nodeForm.name)
            this.nodeForm.pro_name = this.tableParam.relationShip[Number(this.nodeForm.project)]
            console.log(this.tableParam.relationShip[this.nodeForm.name])
            console.log(this.nodeForm)
            http.createNode(this.nodeForm).then(res => {
              this.$message.success('创建节点成功！')
              this.getList()
              this.closeDialogForm()
              console.log(res)
            }).catch((err) => {
              console.log(err)
              this.$message.error(err)
            })
          }
        })
        .catch(error => {
          console.log('error', error)
          this.$message.error(error)
        })
    },
    editHandler(row) {
      http.readNode(row.id).then(res => {
        this.dialogTitle = '编辑节点'
        this.dialogVisible = true
        this.nodeForm = res.data
        this.isEdit = true
      }).catch((err) => {
        console.log(err)
        this.$message.error(err)
      })
    },
    deleteHandler(row) {
      this.$confirm('是否确认删除【' + row.name + '】节点？',
        '提示', {
          confirmButtonText: '确定删除',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
        http.delNode(row.id).then(res => {
          this.$message.success('删除节点成功！')
          http.delInfo({ 'nodeId': row.id })
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
