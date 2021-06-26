from django.urls import path, include
from apps.pipeline_app.test.views import StudentsListViewSet,StudentOperationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'students', StudentsListViewSet, basename='students')
# router.register(r'student', StudentOperationViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)), #获取所有学生信息的接口
    # path("students/query/",StudentViews.query_students), #查询学生信息的接口
    # path("sno/check/",StudentViews.is_exsits_sno), #校验学号是否存在
    # path("student/add/",StudentViews.add_student),
    # path("student/update/",StudentViews.update_student),
    # path("student/delete/",StudentViews.delete_student),
    # path("students/delete/",StudentViews.delete_students), #批量删除
    # path("student/upload/",StudentViews.upload_pic),
    # path("excel/import/",StudentViews.import_students_excel),
    # path("excel/export/",StudentViews.export_students_excel),   
]