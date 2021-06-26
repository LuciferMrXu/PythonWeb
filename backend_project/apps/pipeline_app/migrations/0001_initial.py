# Generated by Django 2.2.17 on 2021-03-29 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='项目名称')),
                ('principal', models.CharField(max_length=50, verbose_name='负责人')),
                ('account', models.CharField(blank=True, max_length=30, null=True, verbose_name='Jira账号')),
                ('password', models.CharField(blank=True, max_length=100, null=True, verbose_name='Jira密码')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('strategy', models.TextField(blank=True, max_length=4096, null=True, verbose_name='打分策略')),
                ('change_times', models.IntegerField(default=1, verbose_name='变更次数')),
                ('json', models.FileField(blank=True, null=True, upload_to='json', verbose_name='策略文件')),
                ('excel', models.FileField(blank=True, null=True, upload_to='excel', verbose_name='导入ROM')),
            ],
            options={
                'verbose_name': '项目',
                'verbose_name_plural': '项目',
                'ordering': ['add_time'],
                'unique_together': {('id', 'name')},
            },
        ),
        migrations.CreateModel(
            name='StudentsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sno', models.IntegerField(help_text='学号', verbose_name='学号')),
                ('name', models.CharField(help_text='姓名', max_length=30, verbose_name='姓名')),
                ('gender', models.CharField(choices=[('male', '男'), ('female', '女')], default='female', help_text='性别', max_length=6, verbose_name='性别')),
                ('birthday', models.DateField(help_text='出生日期', verbose_name='出生年月')),
                ('mobile', models.CharField(help_text='手机号码', max_length=11, null=True, verbose_name='电话')),
                ('email', models.EmailField(help_text='邮箱地址', max_length=100, null=True, verbose_name='邮箱')),
                ('address', models.CharField(help_text='家庭住址', max_length=200, null=True, verbose_name='地址')),
                ('image', models.ImageField(blank=True, help_text='照片', max_length=200, null=True, upload_to='test/avatar/', verbose_name='头像')),
            ],
            options={
                'verbose_name': '学生信息',
                'verbose_name_plural': '学生信息',
            },
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField(verbose_name='任务名称')),
                ('describe', models.CharField(max_length=50, null=True, verbose_name='任务描述')),
                ('pipeline', models.CharField(max_length=50, null=True, verbose_name='任务流程')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='pipeline_app.Projects', verbose_name='项目ID')),
            ],
            options={
                'verbose_name': '任务',
                'verbose_name_plural': '任务',
                'ordering': ['add_time'],
                'unique_together': {('project', 'describe'), ('project', 'name')},
            },
        ),
        migrations.CreateModel(
            name='ROM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='归属项目')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rom', to='pipeline_app.Projects', verbose_name='项目ID')),
            ],
            options={
                'verbose_name': '归属',
                'verbose_name_plural': '归属',
                'unique_together': {('project', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Nodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField(verbose_name='节点名称')),
                ('describe', models.CharField(max_length=50, null=True, verbose_name='节点描述')),
                ('child_node', models.CharField(max_length=50, null=True, verbose_name='子节点')),
                ('principal', models.CharField(blank=True, max_length=50, null=True, verbose_name='负责人')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nodes', to='pipeline_app.Projects', verbose_name='项目ID')),
            ],
            options={
                'verbose_name': '节点',
                'verbose_name_plural': '节点',
                'ordering': ['add_time'],
                'unique_together': {('project', 'describe'), ('project', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Jira',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component', models.CharField(max_length=50, verbose_name='模块')),
                ('jira_pro', models.CharField(max_length=30, verbose_name='Jira项目')),
                ('issue', models.IntegerField(choices=[(0, '线上缺陷'), (1, '提测缺陷'), (2, '线上问题')], verbose_name='错误类型')),
                ('principal', models.CharField(max_length=30, verbose_name='负责人')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jira', to='pipeline_app.Projects', verbose_name='项目ID')),
            ],
            options={
                'verbose_name': 'JIRA',
                'verbose_name_plural': 'JIRA'
            },
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='分组名称')),
                ('role', models.IntegerField(choices=[(0, '研究'), (1, '开发'), (2, '测试')], verbose_name='分组角色')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='pipeline_app.Projects', verbose_name='项目ID')),
            ],
            options={
                'verbose_name': '分组',
                'verbose_name_plural': '分组'
            },
        ),
    ]