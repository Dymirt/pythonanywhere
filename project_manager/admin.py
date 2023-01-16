from django.contrib import admin
from .models import Project, Milestone, Organization, Member

# Register your models here.

admin.site.register(Project)
admin.site.register(Milestone)
admin.site.register(Member)
admin.site.register(Organization)
