<template>
  <div class="app-container">
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
            >添加用户</el-button>
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
      width="50%"
      :show-close="false"
      :close-on-click-modal="false"
    >
      <el-form
        ref="userForm"
        :model="userForm"
        :rules="rules"
        :inline="true"
        label-width="100px"
        label-position="right"
        size="mini"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" suffix-icon="el-icon-edit" clearable />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="userForm.name" suffix-icon="el-icon-edit" clearable />
        </el-form-item>
        <el-form-item label="手机号码" prop="mobile">
          <el-input v-model="userForm.mobile" suffix-icon="el-icon-edit" clearable />
        </el-form-item>
        <el-form-item label="邮箱地址" prop="email">
          <el-input v-model="userForm.email" suffix-icon="el-icon-edit" clearable />
        </el-form-item>
        <el-form-item label="管理员">
          <el-select v-model="userForm.is_staff">
            <el-option lable="是" value="true" />
            <el-option lable="否" value="false" />
          </el-select>
        </el-form-item>
        <el-form-item label="激活账号">
          <el-select v-model="userForm.is_active">
            <el-option lable="是" value="true" />
            <el-option lable="否" value="false" />
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
import http from '@/api/users'
export default {
  name: 'Users',
  components: { Pagination },
  data() {
    return {
      dialogVisible: false,
      dialogTitle: '',
      isEdit: false,
      rules: {
        username: [
          { required: true, message: '登录账号不能为空', trigger: 'blur' }
        ],
        mobile: [
          { pattern: /^[1][35789]\d{9}$/, message: '手机号码必须符合规范！', trigger: 'blur' }
        ],
        email: [
          { pattern: /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/, message: '邮箱地址必须要符合规范', trigger: 'blur' }
        ]
      },
      tableParam: {
        tableLabel: [
          { width: 70, code: 'username', label: '用户名' },
          { width: 70, code: 'name', label: '姓名' },
          { width: 120, code: 'mobile', label: '电话' },
          { width: 160, code: 'email', label: '邮箱' },
          { width: 50, code: 'is_staff', label: '管理员' },
          { width: 80, code: 'is_active', label: '激活状态' }
        ],
        tableData: []
      },
      listQuery: {
        total: 0,
        pageNum: 1,
        pageSize: 5,
        search: ''
      },
      userForm: {
        id: '',
        username: '',
        name: '',
        mobile: '',
        email: '',
        is_staff: 'false',
        is_active: 'false',
        password: ''
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    closeDialogForm() {
      this.$refs.userForm.resetFields()
      this.userForm = {
        id: '',
        username: '',
        name: '',
        mobile: '',
        email: '',
        is_staff: 'false',
        is_active: 'false',
        password: ''
      }
      this.dialogVisible = false
      this.isEdit = false
    },
    getList() {
      http.getUsers(this.listQuery.pageNum, this.listQuery.pageSize, this.listQuery.search)
        .then(res => {
          // console.log(res)
          this.tableParam.tableData = res.data.results
          this.listQuery.total = res.data.count
        }).catch((err) => {
          console.log(err)
          this.$message.error('获取后端查询结果异常！')
        })
    },
    addHandler() {
      this.dialogTitle = '新增用户'
      this.dialogVisible = true
    },
    submitForm() {
      Boolean(this.userForm.is_active)
      Boolean(this.userForm.is_staff)
      this.$refs.userForm
        .validate()
        // 校验成功后执行添加或修改
        .then(() => {
          if (this.isEdit) {
            http.editUser(this.userForm.id, this.userForm).then(res => {
              this.$message.success('修改用户成功！')
              this.getList()
              this.closeDialogForm()
            }).catch((err) => {
              console.log(err)
              this.$message.error('获取后端查询结果异常！')
            })
          } else {
            this.userForm.password = 'password'
            http.createUser(this.userForm).then(res => {
              this.$message.success('创建用户成功！')
              this.getList()
              this.closeDialogForm()
            }).catch((err) => {
              console.log(err)
              this.$message.error('获取后端查询结果异常！')
            })
          }
        })
        .catch(error => {
          console.log('error', error)
        })
    },
    editHandler(row) {
      this.dialogTitle = '编辑用户'
      this.dialogVisible = true
      this.userForm = {
        id: row.id,
        username: row.username,
        name: row.name,
        mobile: row.mobile,
        email: row.email,
        is_staff: String(row.is_staff),
        is_active: String(row.is_active)
      }
      this.isEdit = true
    },
    deleteHandler(row) {
      this.$confirm('是否确认删除账号：' + row.username,
        '提示', {
          confirmButtonText: '确定删除',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
        http.delUser(row.id).then(res => {
          this.$message.success('删除用户成功！')
          console.log(res)
          this.getList()
        }).catch((err) => {
          console.log(err)
          this.$message.error('获取后端查询结果异常！')
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

</style>
