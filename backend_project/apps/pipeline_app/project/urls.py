from django.urls import path, include
from apps.pipeline_app.project.views import ProjectsViewSet,ProjectsAPIViewSet,NodesViewSet,TasksViewSet,FileViewSet,GroupsAPIViewSet,RelationViewSet,JiraAPIViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'projectAPI', ProjectsAPIViewSet, basename='projectAPI')
router.register(r'groupAPI', GroupsAPIViewSet, basename='groupAPI')
router.register(r'jiraAPI', JiraAPIViewSet, basename='jiraAPI')
router.register(r'nodeAPI', NodesViewSet, basename='nodeAPI')
router.register(r'taskAPI', TasksViewSet, basename='taskAPI')
router.register(r'projects', ProjectsViewSet, basename='projects')
# router.register(r'nodes', NodesViewSet, basename='nodes')
# router.register(r'tasks', TasksViewSet, basename='tasks')
router.register(r'upload', FileViewSet, basename='upload')
router.register(r'relation', RelationViewSet, basename='relation')

urlpatterns = [
    path('', include(router.urls))
]