from django.shortcuts import render
from requests.api import request
from apps.pipeline_app.models import StudentsInfo
from django.http import JsonResponse
import os
import json
import uuid
import hashlib
import pandas as pd
from django.conf import settings
from django.db.models import Q    # 导入Q查询
from django.views.generic.base import View
from django.core import serializers
from rest_framework import status
from apps.pipeline_app.serializers import StudentsSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response


class StudentsPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    page_query_param = "page_num"
    max_page_size = 100

class StudentsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
        获取所有学生数据和查询信息接口
        分页、搜索、排序
    '''
    queryset = StudentsInfo.objects.all()
    serializer_class = StudentsSerializer                
    pagination_class = StudentsPagination
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['sno', 'name', "gender","birthday","mobile","email","address"]
    ordering_fields = ['birthday', 'sno']
    permission_classes = [IsAuthenticated,IsAdminUser]

class StudentOperationViewSet(viewsets.ModelViewSet):
    queryset = StudentsInfo.objects.all()
    serializer_class = StudentsSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get_random_str(self,request):
        uuid_val = uuid.uuid4()  # 获取uuid的随机数
        uuid_str = str(uuid_val).encode('utf8') # 获取uuid的随机数字字符串
        md5 = hashlib.md5() # 获取md5实例
        md5.update(uuid_str) # 拿到uuid的md5摘要
        return md5.hexdigest() # 返回固定长度的字符串

    def excel_to_dict(self,path):
        '''读取excel的数据,存储为字典'''
        keys = ['sno','name','gender','birthday','mobile','email','address']
        data = pd.read_excel(path,sheet_name=['student'],header = None,index_col=None, names = keys )
        df = data['student']
        result = []
        for row in df.iterrows():
            result.append(row[1].to_dict())
        return result


    def write_to_excel(self,data,path):
        df = pd.DataFrame(data)
        # print(df)
        df.to_excel(path,header=None,index=None)



    # def get_queryset(self):
    #     queryset = Student.objects.all()
    #     inputStr = self.request.query_params.get("inputStr","")
    #     if inputStr:
    #         queryset =queryset.filter(
    #             Q(sno__icontains=inputStr)|
    #             Q(name__icontains=inputStr)|
    #             Q(gender__icontains=inputStr)|
    #             Q(birthday__icontains=inputStr)|
    #             Q(mobile__icontains=inputStr)|
    #             Q(email__icontains=inputStr)|
    #             Q(address__icontains=inputStr)|
    #             Q(image__icontains=inputStr)
    #         )
    #     return queryset


# class StudentsListView(APIView):
#     """
#     List all students.
#     """
#     def get(self, request, format=None):
#         obj_students = Student.objects.all()
#         stu_serializer = StudentsSerializer(obj_students, many=True)
#         return Response(stu_serializer.data)


#     def post(self, request, format=None):
#         serializer = StudentsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class StudentViews(View):
    
#     def get_random_str(self):
#         uuid_val = uuid.uuid4()  # 获取uuid的随机数
#         uuid_str = str(uuid_val).encode('utf8') # 获取uuid的随机数字字符串
#         md5 = hashlib.md5() # 获取md5实例
#         md5.update(uuid_str) # 拿到uuid的md5摘要
#         return md5.hexdigest() # 返回固定长度的字符串

#     def excel_to_dict(self,path):
#         '''读取excel的数据,存储为字典'''
#         keys = ['sno','name','gender','birthday','mobile','email','address']
#         data = pd.read_excel(path,sheet_name=['student'],header = None,index_col=None, names = keys )
#         df = data['student']
#         result = []
#         for row in df.iterrows():
#             result.append(row[1].to_dict())
#         return result


#     def write_to_excel(self,data,path):
#         df = pd.DataFrame(data)
#         # print(df)
#         df.to_excel(path,header=None,index=None)


#     def get_students(self):
#         '''获取所有学生的信息'''
#         try:
#             # 使用ORM获取所有学生的信息
#             obj_students = Student.objects.all().only()
#             # 把结果转为list
#             students = serializers.serialize('json',obj_students)
#             json_data = json.loads(students)
#             print(json_data)
#             return JsonResponse(json_data,safe=False)
#             # return JsonResponse({"code":0,"data":json_data})
#         except Exception as e:
#             return JsonResponse({"code":-1,"msg":"获取学生信息异常："+str(e)})


# def query_students(request):
#     '''查询学生的信息'''   
#     # 接受传递过来的查询条件，axios默认是json格式
#     data = json.loads(request.body.decode("utf8"))
#     try:
#         # 使用ORM获取所有满足条件的学生信息
#         obj_students = Student.objects.filter(
#             Q(sno__icontains=data["inputStr"])|
#             Q(name__icontains=data["inputStr"])|
#             Q(gender__icontains=data["inputStr"])|
#             Q(birthday__icontains=data["inputStr"])|
#             Q(mobile__icontains=data["inputStr"])|
#             Q(email__icontains=data["inputStr"])|
#             Q(address__icontains=data["inputStr"])|
#             Q(image__icontains=data["inputStr"])
#         ).values()
#         # 把结果转为list
#         students = list(obj_students)

#         return JsonResponse({"code":0,"data":students})
#     except Exception as e:
#         return JsonResponse({"code":-1,"msg":"查询学生信息异常："+str(e)})
  
# def is_exsits_sno(request):
#     '''判断学号是否存在'''
#     data = json.loads(request.body.decode("utf8"))
#     try:
#         obj_students = Student.objects.filter(sno=data['sno'])
#         if obj_students.count() == 0:
#             return JsonResponse({"code":0,"exists":False})
#         else:
#             return JsonResponse({"code":0,"exists":True})
#     except Exception as e:
#         return JsonResponse({"code":-1,"msg":"校验学号失败："+str(e)})
  
# def add_student(request):
#     '''添加学生'''
#     data = json.loads(request.body.decode("utf8"))
#     try:
#         obj_students = Student(
#             sno=data['sno'],
#             name=data['name'],
#             gender=data['gender'],
#             birthday=data['birthday'],
#             mobile=data['mobile'],
#             email=data['email'],    
#             address=data['address'],
#             image = data['image'],     
#             )
#         obj_students.save()
#         obj_students = Student.objects.all().values()
#         students = list(obj_students)
#         return JsonResponse({"code":0,"data":students})
#     except Exception as e:
#         return JsonResponse({"code":-1,"msg":"添加数据库异常："+str(e)})

# def update_student(request):
#     '''修改学生'''
#     data = json.loads(request.body.decode("utf8"))
#     try:
#         # 查找要修改的学生的信息
#         obj_students = Student.objects.get(sno=data['sno'])
#         obj_students.name = data['name']
#         obj_students.gender = data['gender']
#         obj_students.birthday = data['birthday']
#         obj_students.mobile = data['mobile']
#         obj_students.email = data['email']
#         obj_students.address = data['address']
#         obj_students.image = data["image"]
#         obj_students.save()
#         obj_students = Student.objects.all().values()
#         students = list(obj_students)
#         return JsonResponse({"code":0,"data":students})
#     except Exception as e:
#         return JsonResponse({"code":-1,"msg":"修改数据库异常："+str(e)})

# def delete_student(request):
#     '''删除学生'''
#     data = json.loads(request.body.decode("utf8"))
#     try:
#         # 查找要修改的学生的信息
#         obj_students = Student.objects.get(sno=data['sno'])
#         obj_students.delete()
#         obj_students = Student.objects.all().values()
#         students = list(obj_students)
#         return JsonResponse({"code":0,"data":students})
#     except Exception as e:
#         return JsonResponse({"code":-1,"msg":"删除数据库异常："+str(e)})

# def delete_students(request):
#     '''批量删除学生'''
#     data = json.loads(request.body.decode("utf8"))
#     try:
#         # 遍历传递的集合
#         for studentSno in data['studentsSno']:
#             # 查询当前记录
#             obj_student = Student.objects.get(sno=studentSno)
#             # 删除
#             obj_student.delete()
#         obj_students = Student.objects.all().values()
#         students = list(obj_students)
#         return JsonResponse({"code":0,"data":students})
#     except Exception as e:
#         return JsonResponse({"code":-1,"msg":"批量删除数据库异常："+str(e)})

# def upload_pic(request):
#     '''接收上传的文件--存在缓存中'''
#     rev_file = request.FILES.get('avatar')
#     # 判断是否有文件
#     if not rev_file:
#         return JsonResponse({'code':-1,'mag':'图片不存在!'})
#     else:
#         # 获取一个唯一的名字(uuid+hash)
#         new_name = get_random_str()
#         # 写入url
#         file_path = os.path.join(settings.MEDIA_ROOT,new_name + os.path.splitext(rev_file.name)[1])
#         # 写入本地磁盘
#         try:
#             with open(file_path,"wb") as f:
#                 for i in rev_file.chunks():
#                     f.write(i)
#             return JsonResponse({"code":0,"name":new_name + os.path.splitext(rev_file.name)[1]})
#         except Exception as e:
#             return JsonResponse({"code":-1,"msg":str(e)})

# def import_students_excel(request):
#     '''从excel批量导入学生信息'''
#     # 1.接收excel文件存储到media文件夹
#     rev_file = request.FILES.get('Excel')
#     # 判断是否有文件
#     if not rev_file:
#         return JsonResponse({'code':-1,'mag':'Excel文件不存在!'})
#     else:
#         # 获取一个唯一的名字(uuid+hash)
#         new_name = get_random_str()
#         # 写入url
#         file_path = os.path.join(settings.MEDIA_ROOT,new_name + os.path.splitext(rev_file.name)[1])
#         # 写入本地磁盘
#         try:
#             with open(file_path,"wb") as f:
#                 for i in rev_file.chunks():
#                     f.write(i)
#         except Exception as e:
#             return JsonResponse({"code":-1,"msg":str(e)})
#     # 2.读取存储在media文件夹的数据
#     ex_students = excel_to_dict(file_path)
#     # 3.把读取的数据存储到数据库
#     success = 0
#     error = 0
#     error_snos = []
#     for one_student in ex_students:
#         try:
#             Student.objects.create(
#                 sno=one_student['sno'],
#                 name=one_student['name'],
#                 gender=one_student['gender'],
#                 birthday=one_student['birthday'],
#                 mobile=one_student['mobile'],
#                 email=one_student['email'],    
#                 address=one_student['address'],
#             )
#             success += 1
#         except:
#             error += 1
#             error_snos.append(one_student['sno'])

#     # 4.返回导入信息
#     obj_students = Student.objects.all().values()
#     students = list(obj_students)
#     return JsonResponse({
#         'code':0,
#         'success':success,
#         'error':error,
#         'errors':error_snos,
#         'data': students
#         })


# def export_students_excel(request):
#     '''导出数据到excel'''
#     obj_students = Student.objects.all().values()
#     students = list(obj_students)
#     excel_name = get_random_str()+'.xlsx'
#     path = os.path.join(settings.MEDIA_ROOT,excel_name)
#     write_to_excel(students,path)
#     return JsonResponse({'code':0,'name':excel_name})
