from django.db import models
from rest_framework import serializers
from apps.pipeline_app.models import StudentsInfo,Projects,Nodes,Groups,Tasks,Jira,ROM
# from rest_framework_extensions.cache.mixins import CacheResponseMixin
from apps.users.models import UserProfile   
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings

class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ["id","name"]

class GroupsSerializer(serializers.ModelSerializer):
    group_id = serializers.IntegerField(source="id",required=False)
    class Meta:
        model = Groups
        fields = "__all__"
        # exclude = ['project']

class JiraSerializer(serializers.ModelSerializer):
    jira_id = serializers.IntegerField(source="id",required=False)
    class Meta:
        model = Jira
        fields = "__all__"
        # exclude = ['project']


class RomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ROM
        fields = "__all__"

# class NodesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Nodes
#         exclude = ['add_time']

# class TasksSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tasks
#         exclude = ['add_time']


class NodesViewSerializer(serializers.ModelSerializer):
    # Choice字段
    # name = serializers.CharField(source='get_name_display')
    pro_name = serializers.CharField(source='project.name')
    class Meta:
        model = Nodes
        fields = "__all__"

class TasksViewSerializer(serializers.ModelSerializer):
    # Choice字段
    # name = serializers.CharField(source='get_name_display')
    pro_name = serializers.CharField(source='project.name')
    class Meta:
        model = Tasks
        fields = "__all__"



class ProjectsSerializer(serializers.ModelSerializer):
    groups = GroupsSerializer(many=True,required=False)
    jira = JiraSerializer(many=True,required=False)
    nodes = NodesViewSerializer(many=True,read_only = True)
    tasks = TasksViewSerializer(many=True,read_only = True)
    rom = RomSerializer(many=True,read_only = True)

    def create(self, validated_data):
        groups = validated_data.pop('groups')
        jira = validated_data.pop('jira')
        project = Projects.objects.create(**validated_data)
        for group in groups:
            group.pop('project', None)
            Groups.objects.create(project=project, **group)
        for val in jira:
            val.pop('project', None)
            Jira.objects.create(project=project, **val)             
        return project

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups')
        jira = validated_data.pop('jira')
        super().update(instance,validated_data)

        for group in groups:
            if group.get('id')!=None:
                Groups.objects.filter(project=instance,id=group.get('id')).update(**group)
            else:
                group.pop('project', None)
                Groups.objects.create(project=instance, **group)

        for val in jira:
            if val.get('id')!=None:
                Jira.objects.filter(project=instance,id=val.get('id')).update(**val)
            else:
                val.pop('project', None)
                Jira.objects.create(project=instance, **val)

        receiver=[]
        users = UserProfile.objects.all().values()
        for user in users:
            receiver.append(user["email"])
         # 邮件主题
        subject = 'RDG综合管理平台配置变更'
        # 邮件信息，正文部分
        message = '您好，彩虹平台【'+str(instance)+'项目】配置信息已发生变更，请及时确认！'    
        # html结构的信息，其中包含了加密后的用户信息token
        # url = "172.31.184.60:9528"
        # html_message = '<a href=' + url + '>RDG综合管理平台</a>'
        send_mail(subject, message, settings.EMAIL_FROM, receiver,html_message=None)

        return instance


    class Meta:
        model = Projects
        exclude = ['add_time', 'json', 'excel']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'json', 'excel']


class GroupsViewSerializer(serializers.ModelSerializer):
    # Choice字段
    role = serializers.CharField(source='get_role_display')

    class Meta:
        model = Groups
        fields = "__all__"


class JiraViewSerializer(serializers.ModelSerializer):
    issue = serializers.CharField(source='get_issue_display')
    class Meta:
        model = Jira
        fields = "__all__"

class ProjectsViewSerializer(serializers.ModelSerializer):
    groups = GroupsViewSerializer(many=True,read_only = True)
    jira = JiraViewSerializer(many=True,read_only = True)
    rom = RomSerializer(many=True,read_only = True)

    class Meta:
        model = Projects
        exclude = ['strategy','excel']


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentsInfo
        fields = "__all__"