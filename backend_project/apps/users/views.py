from django.http import JsonResponse
from django.db.models import Q    # 导入Q查询
from django.contrib.auth.backends import ModelBackend
from rest_framework import mixins
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework import viewsets
from apps.users.serializers import UserSerializer
from apps.users.models import UserProfile
from apps.utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.utils import jwt_decode_handler
from django.views.generic.base import View
from django.contrib import auth
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(name=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):

    def userInfo(request):
        if request.method=='GET':
            token = request.GET.get('token')
            toke_user = jwt_decode_handler(token)
            user_id = toke_user['user_id']
            user = UserProfile.objects.get(id=user_id)
            if user.is_staff:
                roles = ['admin']
            else:
                roles = ['editor']
            return JsonResponse({
                'id': user.id,
                "roles": roles,
                'name': user.name,
                'email': user.email,
            })
    
    def userLogout(request):
        auth.logout(request)
        return JsonResponse({"msg":"success"}, safe=False)

class UserControlViewSet(
                    mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):

    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        if data["is_staff"]:
            data["is_staff"] = "是"
        else:
            data["is_staff"] = "否"
        if data["is_superuser"]:
            data["is_superuser"] = "是"
        else:
            data["is_superuser"] = "否"
        return Response(data)


class UsersPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    page_query_param = "page_num"
    max_page_size = 100

class UserViewSet(viewsets.ModelViewSet):

    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    pagination_class = UsersPagination
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    permission_classes = [IsAuthenticated,IsAdminUser]
    search_fields = ['username', 'name', "mobile","email"]
    ordering_fields = ['date_joined']
    