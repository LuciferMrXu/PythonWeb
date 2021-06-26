FROM python:3.7

RUN mkdir -p /var/www/html/ai-conf-platform/backend_project
# 设置容器内工作目录
WORKDIR /var/www/html/ai-conf-platform/backend_project
# 将当前目录文件加入到容器工作目录中（. 表示当前宿主机目录）
ADD . /var/www/html/ai-conf-platform/backend_project
#下载第三方包
# RUN pip install https://github.com/darklow/django-suit/tarball/v2
RUN pip install -i https://pypi.doubanio.com/simple uwsgi
RUN pip install -i https://pypi.doubanio.com/simple/ -r requirements.txt
# Windows环境下编写的start.sh每行命令结尾有多余的\r字符，需移除。
RUN sed -i 's/\r//' ./start.sh
# 设置start.sh文件可执行权限
RUN chmod +x ./start.sh