from django.views.generic.base import View
from numpy.core.numeric import True_
from apps.pipeline_app.models import Jira, Projects,Groups,Tasks,Nodes
from apps.pipeline_app.serializers import ProjectsSerializer,GroupsSerializer, ProjectsViewSerializer,FileSerializer,NodesViewSerializer,TasksViewSerializer,RelationSerializer,JiraSerializer
from apps.users.models import UserProfile
from apps.pipeline_app.models import Projects,Nodes,Groups,Tasks,ROM
from django.conf import settings
from django.db.models import Q    # 导入Q查询
import os,json
from django.views.decorators.cache import cache_page
from rest_framework import mixins
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser,MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser,BasePermission, IsAuthenticated, SAFE_METHODS
from django.core.mail import send_mail
import pandas as pd
class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class ProjectsPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    page_query_param = "page_num"
    max_page_size = 100

class RelationViewSet(mixins.ListModelMixin, 
                            viewsets.GenericViewSet):
    queryset = Projects.objects.all()
    serializer_class = RelationSerializer   
    permission_classes = [IsAuthenticated,ReadOnly]  

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        relationShip = {}
        for val in serializer.data:
            relationShip[val["id"]] = val["name"]
        return Response(relationShip)


class ProjectsViewSet(mixins.ListModelMixin, 
                        viewsets.GenericViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsViewSerializer
    pagination_class = ProjectsPagination
    throttle_classes = [UserRateThrottle]
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,ReadOnly]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['name', 'principal',"account"]
    ordering_fields = ['add_time']


class ProjectsAPIViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer              
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['$id']


    def perform_destroy(self, instance):
        receiver=[]
        users = UserProfile.objects.all().values()
        for user in users:
            receiver.append(user["email"])

        subject = 'RDG综合管理平台配置变更'
        message = '您好，彩虹平台【'+str(instance) +'项目】已被删除，请及时确认！'    

        send_mail(subject, message, settings.EMAIL_FROM, receiver,html_message=None)

        instance.delete()

class FileViewSet(mixins.UpdateModelMixin,viewsets.GenericViewSet):
    queryset = Projects.objects.all()
    serializer_class = FileSerializer              
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        file_type = list(request.data.keys())[0]
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        if file_type == "json":
            json_path = list(Projects.objects.filter(id=serializer.instance.id).values())[0]["json"]
            final_path = os.path.join(settings.MEDIA_ROOT,json_path)
            try:
                with open(final_path,'r',encoding='utf8') as f:
                    # json_data = json.loads(f.read())
                    json_data = f.read()
                    Projects.objects.filter(id=serializer.instance.id).update(strategy=json_data)
            except Exception as e:
                return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif file_type == "excel":
            romList = []
            excel_path = list(Projects.objects.filter(id=serializer.instance.id).values())[0]["excel"]
            final_path = os.path.join(settings.MEDIA_ROOT,excel_path)
            try:
                data = pd.read_excel(final_path)
                ROM.objects.filter(project=instance).delete()
                for i in list(data["项目名称"]):
                    rom = ROM(project=instance,name=i)
                    romList.append(rom)
                ROM.objects.bulk_create(romList)
            except Exception as e:
                return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # data = pd.read_excel(final_path)
            # ROM.objects.filter(project=instance).delete()
            # for i in list(data["项目名称"]):
            #     rom = ROM(project=instance,name=i)
            #     romList.append(rom)
            # ROM.objects.bulk_create(romList)

        return Response(serializer.data)
 
    
class GroupsAPIViewSet(mixins.DestroyModelMixin, 
                    viewsets.GenericViewSet):
    queryset = Groups.objects.all()
    serializer_class = GroupsSerializer
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    def perform_destroy(self, instance):
        receiver=[]
        users = UserProfile.objects.all().values()
        for user in users:
            receiver.append(user["email"])

        subject = 'RDG综合管理平台配置变更'
        message = '您好，彩虹平台【'+str(instance) +'分组】已被删除，请及时确认！'    

        send_mail(subject, message, settings.EMAIL_FROM, receiver,html_message=None)

        instance.delete()

class JiraAPIViewSet(mixins.DestroyModelMixin, 
                    viewsets.GenericViewSet):
    queryset = Jira.objects.all()
    serializer_class = JiraSerializer
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    def perform_destroy(self, instance):
        receiver=[]
        users = UserProfile.objects.all().values()
        for user in users:
            receiver.append(user["email"])

        subject = 'RDG综合管理平台配置变更'
        message = '您好，彩虹平台【'+str(instance) +'】已被删除，请及时确认！'    

        send_mail(subject, message, settings.EMAIL_FROM, receiver,html_message=None)

        instance.delete()

class NodesViewSet(viewsets.ModelViewSet):
    queryset = Nodes.objects.all()
    serializer_class = NodesViewSerializer
    pagination_class = ProjectsPagination
    throttle_classes = [UserRateThrottle]
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['child_node', 'principal','project__name','describe']
    ordering_fields = ['add_time']

    def perform_destroy(self, instance):
        receiver=[]
        users = UserProfile.objects.all().values()
        for user in users:
            receiver.append(user["email"])

        subject = 'RDG综合管理平台配置变更'
        message = '您好，彩虹平台【'+str(instance) +'】已被删除，请及时确认！'    

        send_mail(subject, message, settings.EMAIL_FROM, receiver,html_message=None)

        instance.delete()


# class NodesAPIViewSet(viewsets.ModelViewSet):
#     queryset = Nodes.objects.all()
#     serializer_class = NodesSerializer
#     permission_classes = [IsAuthenticated,IsAdminUser]
#     # authentication_classes = [TokenAuthentication]

#     def perform_destroy(self, instance):
#         receiver=[]
#         users = UserProfile.objects.all().values()
#         for user in users:
#             receiver.append(user["email"])

#         subject = 'RDG综合管理平台配置变更'
#         message = '您好，彩虹平台【'+str(instance) +'】已被删除，请及时确认！'    

#         send_mail(subject, message, settings.EMAIL_FROM, receiver,html_message=None)

#         instance.delete()


class TasksViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksViewSerializer
    pagination_class = ProjectsPagination
    throttle_classes = [UserRateThrottle]
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['pipeline','project__name','describe']
    ordering_fields = ['add_time']

    def perform_destroy(self, instance):
        receiver=[]
        users = UserProfile.objects.all().values()
        for user in users:
            receiver.append(user["email"])

        subject = 'RDG综合管理平台配置变更'
        message = '您好，彩虹平台【'+str(instance) +'】已被删除，请及时确认！'    

        send_mail(subject, message, settings.EMAIL_FROM, receiver,html_message=None)

        instance.delete()


# class TasksAPIViewSet(viewsets.ModelViewSet):
#     queryset = Tasks.objects.all()
#     serializer_class = TasksSerializer
#     permission_classes = [IsAuthenticated,IsAdminUser]
#     # authentication_classes = [TokenAuthentication]

#     def perform_destroy(self, instance):
#         receiver=[]
#         users = UserProfile.objects.all().values()
#         for user in users:
#             receiver.append(user["email"])

#         subject = 'RDG综合管理平台配置变更'
#         message = '您好，彩虹平台【'+str(instance) +'】已被删除，请及时确认！'    

#         send_mail(subject, message, settings.EMAIL_FROM, receiver,html_message=None)

#         instance.delete()
