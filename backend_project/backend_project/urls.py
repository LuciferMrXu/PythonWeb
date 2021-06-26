"""backend_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from rest_framework.documentation import include_docs_urls
# from rest_framework.authtoken import views


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('docs/',include_docs_urls(title="测试平台接口API",
                                   description="平台接口调试工具"
                                   )), 
    path('api/',include('apps.users.urls')),
    path('api/',include('apps.pipeline_app.test.urls')),
    path('api/',include('apps.pipeline_app.project.urls')),
    # drf自带的token认证
    # path('api-token-auth/', views.obtain_auth_token),

]

# 允许所有的media文件被访问
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)