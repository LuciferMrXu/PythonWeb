<template>
  <div class="profile-container">
    <el-form ref="ruleForm" :model="ruleForm" :rules="rules" label-width="100px" class="demo-ruleForm" label-position="left">
      <el-form-item label="用户名">
        <el-input v-model="ruleForm.username" :disabled="true" suffix-icon="el-icon-loading" />
      </el-form-item>
      <el-form-item label="创建时间">
        <el-date-picker v-model="ruleForm.date_joined" type="datetime" readonly style="width:100%" />
      </el-form-item>
      <el-form-item label="姓名">
        <el-input v-model="ruleForm.name" clearable suffix-icon="el-icon-edit" />
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="ruleForm.password" show-password clearable />
      </el-form-item>
      <el-form-item label="手机号" prop="mobile">
        <el-input v-model="ruleForm.mobile" clearable suffix-icon="el-icon-edit"><template slot="prepend">+86</template></el-input>
      </el-form-item>
      <el-form-item label="邮箱地址" prop="email">
        <el-input v-model="ruleForm.email" clearable suffix-icon="el-icon-edit" />
      </el-form-item>
      <el-form-item label="超管">
        <el-input v-model="ruleForm.is_superuser" :disabled="true" suffix-icon="el-icon-loading" />
      </el-form-item>
      <el-form-item label="管理员">
        <el-input v-model="ruleForm.is_staff" :disabled="true" suffix-icon="el-icon-loading" />
      </el-form-item>
    </el-form>
    <el-divider />
    <el-button type="primary" style="float:right" @click="submitForm">更新信息</el-button>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import http from '@/api/profile'
export default {
  name: 'Profile',
  data() {
    return {
      ruleForm: {
        date_joined: '',
        email: '',
        is_staff: '',
        is_superuser: '',
        mobile: '',
        name: '',
        username: '',
        password: ''
      },
      rules: {
        mobile: [
          { pattern: /^[1][35789]\d{9}$/, message: '手机号码必须符合规范！', trigger: 'blur' }
        ],
        email: [
          { pattern: /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/, message: '邮箱地址必须要符合规范', trigger: 'blur' }
        ],
        password: [
          { pattern: /(?=.*\d)(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9]).{6,16}/, message: '密码必须由数字、字母、特殊字符组合,请输入6-16位', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    ...mapGetters([
      'id'
    ])
  },
  created() {
    this.queryUser()
  },
  methods: {
    queryUser() {
      http.getUserInfo(
        this.id
      ).then(res => {
        this.ruleForm = res.data
        console.log(this.ruleForm)
      }).catch(err => {
        console.log(err)
      })
    },
    submitForm() {
      this.$refs.ruleForm
        .validate()
        // 校验成功后执行添加或修改
        .then(() => {
          const data = JSON.parse(JSON.stringify(this.ruleForm))
          data.is_staff = this.ruleForm.is_staff === '是'
          data.is_superuser = this.ruleForm.is_superuser === '是'
          http.updateUser(this.id, data).then(res => {
            this.queryUser()
            this.$message.success('数据上传成功！')
          }).catch(err => {
            console.log(err)
            this.$message.error(err)
          })
        })
        .catch(error => {
          console.log('error', error)
        })
    }
  }
}
</script>
<style lang="scss">
.profile-container{
   background: #fff;
   padding:20px;
   .block{
     margin-bottom: 20px;
     display: flex;
     .upload-demo{
       margin-left: 30px;
       padding-top: 44px;
     }
   }
   .el-form{
     overflow: hidden;
   }
   .el-form-item{
     width:43%;
     float: left;
     &:nth-child(even){
       float: right;
     }
     >label{
       display: block;
       float: unset;
     }
     >.el-form-item__content{
       margin-left: 0!important;
     }
   }
}
</style>
