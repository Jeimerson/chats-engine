from django.contrib import admin

from chats.apps.projects.models import Project, ProjectPermission, TemplateType

# Register your models here.

admin.site.register(Project)
admin.site.register(ProjectPermission)
admin.site.register(TemplateType)
