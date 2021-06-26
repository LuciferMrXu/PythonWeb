from django.db import models
from datetime import datetime
# Create your models here.


class Projects(models.Model):
    # id = models.AutoField(primary_key=True,verbose_name="项目ID")
    name = models.CharField(max_length=30,null=False, verbose_name="项目名称")
    principal = models.CharField(max_length=50,null=False, verbose_name="负责人")
    account = models.CharField(max_length=30,null=True,blank=True, verbose_name="Jira账号")
    password = models.CharField(max_length=100,null=True,blank=True,verbose_name="Jira密码")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    strategy = models.TextField(max_length=4096,null=True,blank=True,verbose_name="打分策略")
    change_times = models.IntegerField(default=1,null=False, verbose_name="变更次数")
    json = models.FileField(null=True, blank=True,upload_to='json',verbose_name="策略文件")
    excel = models.FileField(null=True, blank=True,upload_to='excel',verbose_name="导入ROM")
    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name
        unique_together = ['id', 'name']
        ordering = ['add_time']

    def __str__(self):
        return self.name


class Groups(models.Model):
    GROUP_ROLES = (
        (0, "研究"),
        (1, "开发"),
        (2, "测试"),
        (3, "运营"),
        (4, "产品")
        )
    # id = models.AutoField(primary_key=True,verbose_name="分组ID")
    project = models.ForeignKey(Projects,null=True,verbose_name="项目ID",related_name="groups", on_delete=models.CASCADE)
    name = models.CharField(max_length=30,null=False, verbose_name="分组名称")
    role = models.IntegerField(choices=GROUP_ROLES,null=False, verbose_name="分组角色")

    class Meta:
        verbose_name = '分组'
        verbose_name_plural = verbose_name
        # unique_together = ['project', 'name']

    def __str__(self):
        return self.name

class Nodes(models.Model):
    # NODE_TYPES = (
    #     (0, "概念"),
    #     (1, "计划"),
    #     (2, "研究"),
    #     (3, "开发"),
    #     (4, "验证"),
    #     (5, "发布"),
    #     (6, "自定义节点1"),
    #     (7, "自定义节点2"),
    #     (8, "自定义节点3"),
    #     (9, "自定义节点4"),
    # )
    # id = models.AutoField(primary_key=True,verbose_name="节点ID")
    project = models.ForeignKey(Projects,null=True,verbose_name="项目ID",related_name="nodes", on_delete=models.CASCADE)
    name = models.IntegerField(blank=False, null=False, verbose_name="节点名称")
    describe = models.CharField(max_length=50,null=True, verbose_name="节点描述")
    child_node = models.CharField(max_length=50,null=True, verbose_name="子节点")
    principal = models.CharField(max_length=50,null=True,blank=True,verbose_name="负责人")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    class Meta:
        verbose_name = '节点'
        verbose_name_plural = verbose_name
        unique_together = [['project', 'name'],['project','describe']]
        ordering = ['add_time']

    def __str__(self):
        return "项目:{0}==>节点:{1}".format(self.project.name,self.describe)


class Tasks(models.Model):
    # TASK_TYPES = (
    #     (0, "模型更新"),
    #     (1, "引擎更新"),
    #     (2, "模型&引擎更新"),
    #     (3, "新方案产品化"),
    #     (4, "引擎支持"),       
    #     (5, "标准IPD流程"),
    #     (6, "自定义模板1"),
    #     (7, "自定义模板2"),
    #     (8, "自定义模板3"),
    #     (9, "自定义模板4"),
    # )
    # id = models.AutoField(primary_key=True,blank=True,verbose_name="任务ID")
    project = models.ForeignKey(Projects,null=True,verbose_name="项目ID",related_name="tasks", on_delete=models.CASCADE)
    name = models.IntegerField(blank=False,null=False, verbose_name="任务名称")
    describe = models.CharField(max_length=50,null=True, verbose_name="任务描述")
    pipeline = models.CharField(max_length=50,null=True, verbose_name="任务流程")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    class Meta:
        verbose_name = '任务'
        verbose_name_plural = verbose_name
        unique_together = [['project', 'name'],['project','describe']]
        ordering = ['add_time']

    def __str__(self):
        return "项目:{0}==>模板:{1}".format(self.project.name,self.describe)

class ROM(models.Model):
    name = models.CharField(max_length=50,null=False, verbose_name="归属项目")
    project = models.ForeignKey(Projects,null=True,verbose_name="项目ID",related_name="rom", on_delete=models.CASCADE)
    class Meta:
        verbose_name = '归属'
        verbose_name_plural = verbose_name
        unique_together = ['project', 'name']

    def __str__(self):
        return self.name

class Jira(models.Model):
    ISSUE_TYPES = (
        (0, "线上缺陷"),
        (1, "提测缺陷"),
        (2, "线上问题")
    )
    component = models.CharField(max_length=50,null=False, verbose_name="模块")
    jira_pro = models.CharField(max_length=30,null=False, verbose_name="Jira项目")
    issue = models.IntegerField(choices=ISSUE_TYPES,null=False, verbose_name="错误类型")
    principal = models.CharField(max_length=30,null=False, verbose_name="负责人")
    project = models.ForeignKey(Projects,null=True,verbose_name="项目ID",related_name="jira", on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'JIRA'
        verbose_name_plural = verbose_name
        # unique_together = ['project', 'component']

    def __str__(self):
        return "Jira项目:{0}==>模块:{1}".format(self.jira_pro,self.component)

class StudentsInfo(models.Model):
    GENDER_CHOICES=(
        ("male", "男"), 
        ("female", "女")
    )
    sno = models.IntegerField(null=False,verbose_name="学号", help_text="学号") 
    name = models.CharField(max_length=30,null=False, verbose_name="姓名", help_text="姓名")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="female", verbose_name="性别", help_text="性别")
    birthday = models.DateField(null=False,verbose_name="出生年月",help_text="出生日期")
    mobile = models.CharField(max_length=11,null=True, verbose_name="电话", help_text="手机号码")
    email = models.EmailField(max_length=100, null=True, verbose_name="邮箱", help_text="邮箱地址")
    address = models.CharField(max_length=200,null=True,verbose_name="地址", help_text="家庭住址")
    image = models.ImageField(max_length=200,upload_to="test/avatar/", null=True, blank=True, verbose_name="头像", help_text="照片")
    class Meta:
        verbose_name = "学生信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

