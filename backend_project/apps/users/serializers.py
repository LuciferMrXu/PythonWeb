from django.db import models
from rest_framework import serializers
from apps.users.models import UserProfile
from django.db.models import Q
from rest_framework.validators import UniqueValidator
from rest_framework.utils import model_meta
from django.core.mail import send_mail
from django.conf import settings
from apps.users.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=UserProfile.objects.all(), message="用户已经存在")])

    password = serializers.CharField(
        style={'input_type': 'password'},help_text="密码", label="密码", write_only=True,
    )

    def create(self, validated_data):
        '''重写create方法实现，将密码加密后保存'''
        user = UserProfile.objects.create_user(**validated_data)
        return user


    def update(self, instance, validated_data):
        if "password" in validated_data.keys():
            user = super(UserSerializer, self).update(instance=instance,validated_data=validated_data)
            user.set_password(validated_data["password"])
            user.save()
            return user
        else:
            serializers.raise_errors_on_nested_writes('update', self, validated_data)
            info = model_meta.get_field_info(instance)
            for attr, value in validated_data.items():
                if attr in info.relations and info.relations[attr].to_many:
                    field = getattr(instance, attr)
                    field.set(value)
                else:
                    setattr(instance, attr, value)
            instance.save()

            return instance

    class Meta:
        model = UserProfile
        fields = ["id","username","password","is_staff","mobile","email","name","is_superuser","date_joined","is_active"]



class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id','email']

    def validate(self, attrs):
        return attrs
        
    def update(self, instance, validated_data):
        '''
        :param instance: 视图传递过来的对象,通过get_object获取的实例对象
        :param validated_data:
        :return:
        '''
        instance.email = validated_data['email']
        instance.save()

        # 生成激活连接
        ts_obj = ts(settings.SECRET_KEY)
        data ={
            'user_id':instance.id,
            'username':instance.username,
            'email':instance.email
        }
        #加密
        token =ts_obj.dumps(data).decode()
        url = 'http://127.0.0.1:8000/user/email/?token='+token
        
        # todo 发送邮件
        '''
        def send_mail(subject, message, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None, html_message=None):'''

        url_string = '<a href=' + url + '>点击链接</a>'
        # 邮件主题
        subject = '尚惠欢迎信息'
        # 邮件信息，正文部分
        message = '欢迎'
        # 发送者，直接从配置文件中导入上面配置的发送者
        sender = settings.EMAIL_FROM
        # 接收者的邮箱，是一个列表，这里是前端用户注册时传过来的 email
        receiver = ['1246081324@qq.com', ]
        # html结构的信息，其中包含了加密后的用户信息token
        html_message = url_string
        # 调用Django发送邮件的方法，这里传了5个参数
        send_mail(subject, message, sender, receiver,html_message=html_message)

     
        return instance