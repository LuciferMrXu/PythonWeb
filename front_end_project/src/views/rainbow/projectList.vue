<template>
  <div class="scoreList-contanier">
    <el-form :inline="true" style="height: 60px">
      <el-row>
        <el-col :span="7">
          <el-input v-model="listQuery.search" placeholder="请输入搜索内容" clearable class="input-with-select">
            <el-button slot="append" icon="el-icon-search" @click="getList" />
          </el-input>
        </el-col>
        <el-col :span="17" style="text-align: right">
          <el-button-group>
            <el-button
              type="primary"
              icon="el-icon-finished"
              @click="configurationAPI"
            >发布配置</el-button>
            <el-button
              type="primary"
              icon="el-icon-folder-add"
              @click="drawer = true"
            >新建项目</el-button>
          </el-button-group>
        </el-col>
      </el-row>
    </el-form>
    <div class="table">
      <el-table :data="tableParam.projects" header-row-class-name="headbg">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-row :gutter="5">
              <el-col :span="6">
                <el-table :data="props.row.rom" highlight-current-row border size="mini" style="width: 100%" height="154" header-row-class-name="headbg">
                  <el-table-column prop="name" label="归属项目" align="center" />
                </el-table>
              </el-col>
              <el-col :span="6">
                <el-table :data="props.row.groups" highlight-current-row border size="mini" style="width: 100%" height="154" header-row-class-name="headbg">
                  <el-table-column prop="name" label="分组名称" align="center" />
                  <el-table-column prop="role" label="分组角色" width="80" align="center" />
                  <el-table-column label="操作" align="center" width="60">
                    <template slot-scope="scope">
                      <span class="opreater delete" @click="deleteGroup(scope.row)">删除</span>
                    </template>
                  </el-table-column>
                </el-table>
              </el-col>
              <el-col :span="12">
                <el-table :data="props.row.jira" highlight-current-row border size="mini" style="width: 100%" height="154" header-row-class-name="headbg">
                  <el-table-column prop="jira_pro" label="Jira项目" width="130" align="center" />
                  <el-table-column prop="component" label="模块" width="130" align="center" />
                  <el-table-column prop="issue" label="错误类型" width="80" align="center" />
                  <el-table-column prop="principal" label="负责人" align="center" />
                  <el-table-column label="操作" align="center" width="60">
                    <template slot-scope="scope">
                      <span class="opreater delete" @click="deleteJira(scope.row)">删除</span>
                    </template>
                  </el-table-column>
                </el-table>
              </el-col>
            </el-row>
          </template>
        </el-table-column>
        <el-table-column
          v-for="item in tableParam.projectLabel"
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
            <el-button type="primary" icon="el-icon-edit" size="small" circle @click="editProject(scope.row)" />
            <el-button type="danger" icon="el-icon-delete" size="small" circle @click="deleteProject(scope.row)" />
          </template>
        </el-table-column>
      </el-table>
      <pagination v-show="listQuery.total>0" class="pagination-container" :total="listQuery.total" :page.sync="listQuery.pageNum" :limit.sync="listQuery.pageSize" @pagination="getList" />
    </div>
    <el-drawer
      :open="openedHandler"
      :visible.sync="drawer"
      :show-close="false"
      :before-close="beforeColseDrawer"
      size="30%"
    >
      <template slot="title">
        <div class="title-body">
          <span>项目配置</span>
          <el-divider />
        </div>
      </template>
      <div
        class="drawer-body"
      >
        <div class="content-body">
          <el-form ref="rulePro" label-position="top" label-width="80px" :model="projectForm" :rules="rules.project">
            <el-form-item label="项目名称：" prop="name">
              <el-input v-model="projectForm.name" placeholder="请输入项目名称！" autocomplete="off" clearable suffix-icon="el-icon-edit" />
            </el-form-item>
            <el-form-item label="项目负责人：" prop="principal">
              <el-input v-model="projectForm.principal" placeholder="请输入项目负责人的域账号！" autocomplete="off" clearable suffix-icon="el-icon-edit" />
            </el-form-item>
            <el-form-item label="Jira账号：">
              <el-input v-model="projectForm.account" placeholder="请输入Jira账号！" autocomplete="off" clearable suffix-icon="el-icon-edit" />
            </el-form-item>
            <el-form-item label="Jira密码：">
              <el-input v-model="projectForm.password" placeholder="请输入Jira密码！" autocomplete="off" show-password clearable />
            </el-form-item>
            <el-form-item label="打分策略：">
              <el-upload
                class="upload-demo"
                action="aaa"
                :before-upload="beforeUpload"
                :http-request="uploadFile"
                :limit="1"
                :disabled="!isEdit"
                :file-list="projectForm.file_name"
              >
                <el-button icon="el-icon-upload" type="primary" :disabled="!isEdit" @click="fileType='json'">导入打分策略</el-button>
                <div slot="tip" class="el-upload__tip">只能上传json文件，且不超过4Mb</div>
              </el-upload>
            </el-form-item>
            <el-form-item label="归属项目：">
              <el-upload
                class="upload-demo"
                action="aaa"
                :before-upload="beforeUpload"
                :http-request="uploadFile"
                :limit="1"
                :disabled="!isEdit"
                :file-list="projectForm.file_name"
              >
                <el-button icon="el-icon-upload" type="primary" :disabled="!isEdit" @click="fileType='excel'">导入ROM项目</el-button>
                <div slot="tip" class="el-upload__tip">只能上传excel文件，且不超过4Mb</div>
              </el-upload>
            </el-form-item>
            <el-form-item label="可变更次数：">
              <el-input-number v-model="projectForm.change_times" :min="0" label="请输入该项目的可变更次数！" />
            </el-form-item>
          </el-form>
        </div>
        <el-divider />
        <el-button style="marginRight: 8px" @click="onDrawerClose">
          取消
        </el-button>
        <el-button type="primary" @click="showChildrenDrawer">
          详细配置
        </el-button>
      </div>
      <el-drawer
        :open="openedHandler"
        :append-to-body="true"
        :show-close="false"
        :visible.sync="childrenDrawer"
        :before-close="beforeColseDrawer"
        size="40%"
      >
        <template slot="title">
          <div class="title-body">
            <span>详细配置</span>
            <el-divider />
          </div>
        </template>
        <div class="drawer-body">
          <div class="table">
            <el-button type="primary" size="mini" style="margin-bottom: 10px" @click="dialogAddGroup=true">新增分组</el-button>
            <el-table :data="projectForm.groups" header-row-class-name="headbg" size="mini">
              <el-table-column type="index" label="序号" width="50" align="center" />
              <el-table-column
                v-for="item in tableParam.groupLable"
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
              <el-table-column fixed="right" align="center" label="操作" width="70">
                <template slot-scope="scope">
                  <el-button
                    type="text"
                    size="small"
                    @click="editGroup(scope.$index,scope.row)"
                  >
                    编辑
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <el-button type="primary" size="mini" style="margin: 10px 0px" @click="dialogAddJira=true">新增Jira</el-button>
            <el-table :data="projectForm.jira" header-row-class-name="headbg" size="mini">
              <el-table-column
                v-for="item in tableParam.jiraLable"
                :key="item.index"
                :prop="item.code"
                :label="item.label"
                align="center"
                :min-width="item.width"
                :sortable="item.sortable"
              >
                <template slot-scope="scope">
                  <el-col align="center">
                    {{ scope.row[item.code] || scope.row[item.code] === 0 ? scope.row[item.code] : '--' }}
                  </el-col>
                </template>
              </el-table-column>
              <el-table-column fixed="right" align="center" label="操作" width="70">
                <template slot-scope="scope">
                  <el-button
                    type="text"
                    size="small"
                    @click="editJira(scope.$index,scope.row)"
                  >
                    编辑
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
          <el-divider />
          <el-button style="marginRight: 8px" @click="onChildrenDrawerClose">
            取消
          </el-button>
          <el-button type="primary" @click="submit">
            提交
          </el-button>
        </div>
      </el-drawer>
    </el-drawer>
    <el-dialog title="添加分组" :visible.sync="dialogAddGroup" width="40%" :show-close="false" :close-on-click-modal="false">
      <el-form ref="ruleGroup" :model="groupForm" style="margin-right:20px" label-width="120px" :rules="rules.group">
        <el-form-item label="分组名称：" prop="name">
          <el-input v-model="groupForm.name" autocomplete="off" placeholder="请输入分组名称！" clearable suffix-icon="el-icon-edit" style="width: 90%" />
        </el-form-item>
        <el-form-item label="分组类型：" prop="role">
          <el-select v-model="groupForm.role" placeholder="请选择分组类型！" style="width: 90%">
            <el-option
              v-for="item in groupOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button
          type="primary"
          size="mini"
          @click="addGroup"
        >确 定</el-button>
        <el-button type="info" size="mini" @click="closeGroup">取 消</el-button>
      </div>
    </el-dialog>
    <el-dialog title="添加节点" :visible.sync="dialogAddJira" width="40%" :show-close="false" :close-on-click-modal="false">
      <el-form ref="ruleJira" :model="jiraForm" style="margin-right:20px" label-width="120px" :rules="rules.jira">
        <el-form-item label="Jira模块：" prop="component">
          <el-input v-model="jiraForm.component" autocomplete="off" placeholder="请输入Jira模块！" clearable suffix-icon="el-icon-edit" style="width: 90%" />
        </el-form-item>
        <el-form-item label="Jira项目：" prop="jira_pro">
          <el-input v-model="jiraForm.jira_pro" autocomplete="off" placeholder="请输入Jira项目！" clearable suffix-icon="el-icon-edit" style="width: 90%" />
        </el-form-item>
        <el-form-item label="默认负责人：" prop="principal">
          <el-input v-model="jiraForm.principal" autocomplete="off" placeholder="请输入默认负责人！" clearable suffix-icon="el-icon-edit" style="width: 90%" />
        </el-form-item>
        <el-form-item label="错误类型：" prop="issue">
          <el-select v-model="jiraForm.issue" placeholder="请选择错误类型！" style="width: 90%">
            <el-option
              v-for="item in jiraOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button
          type="primary"
          size="mini"
          @click="addJira"
        >确 定</el-button>
        <el-button type="info" size="mini" @click="closeJira">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import Pagination from '@/components/Pagination'
import http from '@/api/rainbow'
import { Base64 } from 'js-base64'
export default {
  name: 'ProjectList',
  components: { Pagination },
  data() {
    return {
      drawer: false,
      childrenDrawer: false,
      dialogAddGroup: false,
      dialogAddJira: false,
      isEdit: false,
      isChildrenEdit: false,
      fileType: 'json',
      rowIndex: 0,
      projectId: '',
      conf: {},
      rules: {
        project: {
          name: [
            { required: true, message: '项目名称不能为空！', trigger: 'blur' }
          ],
          principal: [
            { required: true, message: '项目负责人不能为空！', trigger: 'blur' }
          ]
        },
        group: {
          name: [
            { required: true, message: '分组名称不能为空！', trigger: 'blur' }
          ],
          role: [
            { required: true, message: '分组角色不能为空！', trigger: 'change' }
          ]
        },
        jira: {
          issue: [
            { required: true, message: '错误类型不能为空！', trigger: 'change' }
          ],
          component: [
            { required: true, message: 'Jira模块不能为空！', trigger: 'blur' }
          ],
          jira_pro: [
            { required: true, message: 'Jira项目不能为空！', trigger: 'blur' }
          ],
          principal: [
            { required: true, message: '默认负责人不能为空！', trigger: 'blur' }
          ]
        }
      },
      groupOptions: [
        { value: 0, label: '研究' },
        { value: 1, label: '开发' },
        { value: 2, label: '测试' },
        { value: 3, label: '运营' },
        { value: 4, label: '产品' }
      ],
      jiraOptions: [
        { value: 0, label: '线上缺陷' },
        { value: 1, label: '提测缺陷' },
        { value: 2, label: '线上问题' }
      ],
      tableParam: {
        projectLabel: [
          { width: 120, code: 'name', label: '项目名称' },
          { width: 100, code: 'principal', label: '负责人' },
          { width: 100, code: 'account', label: 'Jira账号' },
          { width: 70, code: 'change_times', label: '变更' },
          { width: 100, code: 'json', label: '打分策略' },
          { width: 100, code: 'add_time', label: '创建时间' }
        ],
        projects: [],
        groupLable: [
          { width: 100, code: 'name', label: '分组名称' },
          { width: 100, code: 'role', label: '分组角色' }
        ],
        jiraLable: [
          { width: 120, code: 'component', label: '模块' },
          { width: 120, code: 'jira_pro', label: 'Jira项目' },
          { width: 80, code: 'issue', label: '错误类型' },
          { width: 70, code: 'principal', label: '负责人' }
        ]
      },
      listQuery: {
        total: 0,
        pageNum: 1,
        pageSize: 5,
        search: ''
      },
      submitForm: {},
      projectForm: {
        id: '',
        name: '',
        principal: '',
        account: '',
        password: '',
        strategy: '',
        change_times: '',
        file_name: [],
        groups: [],
        jira: [],
        rom: []
      },
      groupForm: {
        name: '',
        role: '',
        project: ''
      },
      jiraForm: {
        component: '',
        jira_pro: '',
        issue: '',
        principal: '',
        project: ''
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    beforeUpload(file) {
      const isLt4M = file.size / 1024 / 1024 < 4
      if (!isLt4M) {
        this.$message.error('上传文件大小不能超过 4MB!')
      }
      if (this.fileType === 'json') {
        const isJson = file.type === 'application/json'
        if (!isJson) {
          this.$message.error('上传策略文件格式只能是 Json 文件!')
          return isJson && isLt4M
        }
      } else if (this.fileType === 'excel') {
        const isExcel = file.type === ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || 'application/vnd.ms-excel')
        if (!isExcel) {
          this.$message.error('上传策略文件格式只能是 excel 文件!')
          return isExcel && isLt4M
        }
      }
    },
    uploadFile(file) {
      const fileReq = new FormData()
      if (this.fileType === 'json') {
        fileReq.append('json', file.file)
      } else if (this.fileType === 'excel') {
        fileReq.append('excel', file.file)
      }
      console.log(fileReq)
      const id = JSON.parse(JSON.stringify(this.projectForm.id))
      http.uploadJson(id, fileReq).then(res => {
        console.log(res)
        this.$message.success('上传文件成功！')
      }).catch(err => {
        this.$message.error(err)
      })
    },
    onDrawerClose() {
      this.$refs.rulePro.resetFields()
      this.projectForm = {
        id: '',
        name: '',
        principal: '',
        strategy: '',
        change_times: '',
        file_name: [],
        groups: [],
        jira: [],
        rom: []
      }
      this.childrenDrawer = false
      this.drawer = false
      this.isEdit = false
    },
    onChildrenDrawerClose() {
      this.projectForm.groups = []
      this.projectForm.jira = []
      this.childrenDrawer = false
    },
    submit() {
      console.log(this.submitForm)
      if (this.submitForm.password !== '') {
        this.submitForm.password = Base64.encode(this.submitForm.password)
      }
      // debugger
      if (this.isEdit) {
        this.submitForm.groups.forEach(val => {
          val.project = this.projectId
        })
        this.submitForm.jira.forEach(val => {
          val.project = this.projectId
        })
        http.updateProject(this.submitForm.id, this.submitForm).then((response) => {
          console.log(response)
          this.getList()
          this.$message.success('数据更新成功！')
        }).catch((err) => {
          console.log(err)
          this.$message.error(err)
        })
      } else {
        http.createProject(this.submitForm).then((response) => {
          console.log(response)
          this.getList()
          this.$message.success('数据添加成功！')
        }).catch((err) => {
          console.log(err)
          this.$message.error(err)
        })
      }
      this.onDrawerClose()
    },
    getList() {
      http.getInfo(this.listQuery.pageNum, this.listQuery.pageSize, this.listQuery.search)
        .then(res => {
          this.tableParam.projects = res.data.results
          this.tableParam.projects.forEach(val => {
            // console.log(val)
            val.add_time = this.$moment(val.add_time).format('YYYY-MM-DD')
            if (val.json !== null) {
              const pos = val.json.substring(val.json.lastIndexOf('/') + 1)
              val.json = decodeURI(pos)
            }
            if (val.password !== null) {
              val.password = Base64.decode(val.password)
            }
          })
          this.listQuery.total = res.data.count
          console.log(this.tableParam.projects)
        }).catch((err) => {
          console.log(err)
          this.$message.error(err)
        })
    },
    openedHandler() {
      document.getElementById('elDrawer').scrollIntoView()
    },
    changeEdit() {
      http.readInfo(this.projectForm.id).then((res) => {
        res.data.groups.forEach(val => {
          delete val.project
        })
        res.data.jira.forEach(val => {
          delete val.project
        })
        this.projectForm.groups = res.data.groups
        this.projectForm.jira = res.data.jira
        this.submitForm = JSON.parse(JSON.stringify(this.projectForm))
      }).catch((err) => {
        this.$message.error(err)
      })
    },
    showChildrenDrawer() {
      this.$refs.rulePro
        .validate()
        .then(() => {
          if (this.projectForm.id !== '') {
            this.changeEdit()
          }
          this.submitForm = JSON.parse(JSON.stringify(this.projectForm))
          this.childrenDrawer = true
        })
        .catch(err => {
          console.log(err)
        })
    },
    beforeColseDrawer(done) {
      this.$confirm('还有工作未保存，确定关闭吗？', { type: 'warning' })
        .then(_ => {
          this.onDrawerClose()
          done()
        }).catch((err) => {
          this.$message.error(err)
        })
    },
    editProject(row) {
      this.projectId = row.id
      this.projectForm = JSON.parse(JSON.stringify(row))
      this.isEdit = true
      this.drawer = true
    },
    deleteProject(row) {
      this.$confirm('是否确认删除【' + row.name + '】项目？', '提示', {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        http.delProject(row.id).then((response) => {
          this.$message.success('删除项目成功！')
          http.delInfo({ 'projectId': row.id })
          this.getList()
        }).catch((err) => {
          this.$message.error(err)
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    deleteGroup(row) {
      this.$confirm('是否确认删除【' + row.name + '】分组？', '提示', {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        http.delGroup(row.id).then((response) => {
          this.$message.success('删除分组成功！')
          http.delInfo({ 'groupId': row.id })
          this.getList()
        }).catch((err) => {
          this.$message.error(err)
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    deleteJira(row) {
      console.log(row)
      this.$confirm('是否确认删除【' + row.component + '】模块？', '提示', {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        http.delJira(row.id).then((response) => {
          this.$message.success('删除Jira成功！')
          http.delInfo({ 'jiraId': row.id })
          this.getList()
        }).catch((err) => {
          this.$message.error(err)
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    addGroup() {
      this.$refs.ruleGroup
        .validate()
        // 校验成功后执行添加或修改
        .then(() => {
          const group = JSON.parse(JSON.stringify(this.groupForm))
          const dataSource = [...this.projectForm.groups]
          if (this.isChildrenEdit) {
            const target = dataSource.filter((item, index) => this.rowIndex === index)[0]
            if (target) {
              delete target.editable
              Object.assign(target, group)
              this.projectForm.groups = [...dataSource]
            }
          } else {
            this.projectForm.groups.push(group)
          }
          this.closeGroup()
          this.submitForm = JSON.parse(JSON.stringify(this.projectForm))
          // console.log(this.submitForm)
        })
        .catch(error => {
          console.log('error', error)
        })
    },
    closeGroup() {
      this.$refs.ruleGroup.resetFields()
      this.groupForm = {
        name: '',
        role: '',
        project: ''
      }
      this.dialogAddGroup = false
      this.isChildrenEdit = false
      this.rowIndex = 0
    },
    editGroup(index, row) {
      this.groupForm = JSON.parse(JSON.stringify(row))
      this.dialogAddGroup = true
      this.rowIndex = index
      this.isChildrenEdit = true
    },
    addJira() {
      this.$refs.ruleJira
        .validate()
        // 校验成功后执行添加或修改
        .then(() => {
          const Jira = JSON.parse(JSON.stringify(this.jiraForm))
          const dataSource = [...this.projectForm.jira]
          if (this.isChildrenEdit) {
            const target = dataSource.filter((item, index) => this.rowIndex === index)[0]
            if (target) {
              delete target.editable
              Object.assign(target, Jira)
              this.projectForm.jira = [...dataSource]
            }
          } else {
            this.projectForm.jira.push(Jira)
          }
          this.closeJira()
          this.submitForm = JSON.parse(JSON.stringify(this.projectForm))
        })
        .catch(error => {
          console.log('error', error)
        })
    },
    closeJira() {
      this.$refs.ruleJira.resetFields()
      this.jiraForm = {
        component: '',
        jira_pro: '',
        issue: '',
        principal: '',
        project: ''
      }
      this.dialogAddJira = false
      this.isChildrenEdit = false
      this.rowIndex = 0
    },
    editJira(index, row) {
      this.jiraForm = JSON.parse(JSON.stringify(row))
      this.dialogAddJira = true
      this.rowIndex = index
      this.isChildrenEdit = true
    },
    configurationAPI() {
      http.releaseInfo().then(res => {
        this.conf = res
        console.log(this.conf)
        http.sendInfo(this.conf).then(res => {
          console.log(res)
        }).catch((err) => {
          console.log(err)
          this.$message.error(err)
        })
      }).catch((err) => {
        console.log(err)
        this.$message.error(err)
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
.drawer-body {
  bottom: 0;
  width: 100%;
  padding: 0px 16px 10px 16px;
  text-align: right;
  left: 0;
  background: #fff;
  border-radius: 0 0 4px 4px;
}
.el-drawer__body {
  height: 100%;
  overflow-y: auto;
}
.title-body {
  font-size: 20px;
  font-weight: bolder;
  height: 20px
}
.content-body {
  text-align: left;
}
.opreater{
  color:#3c6eff;
  cursor: pointer;
  padding:0;
  border:0;

  &:hover{
    background:none;
  }
  &.delete:hover{
    color: #ff8b95;
  }
  &+.opreater{
    margin-left: 5px;
  }
  &.is-disabled{
    color:#999;
    &:hover{
      color:#999
    }
  }
  span{
    font-size:14px;
  }
}
</style>
