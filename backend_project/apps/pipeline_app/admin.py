from django.contrib import admin
# from apps.pipeline_app.models import pipeline_projects,pipeline_groups,pipeline_modules,pipeline_templates

# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    pass
    '''
    #fields指定某些字段需要显示
    #fields = ("name","number","address")

    #exculde指定某些字段不显示
    #exclude = ("birthday","address")

    #fieldsets设置分栏显示
    fieldsets = (
            ["base",{'fields':("name","number")}],
            ["personal",{'fields':("birthday","address")}]
        )

    #list_display属性显示更多列栏目
    list_display = ("name","number","address")

    #list_filter过滤条
    list_filter = ("address",)

    #search_fields增加搜索栏
    search_fields = ("name",)
    '''


# #注册models中的表到admin中管理
# admin.site.register([pipeline_projects,pipeline_groups,pipeline_modules,pipeline_templates],ContactAdmin)
