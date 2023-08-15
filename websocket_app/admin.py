from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(ChatMaster)
class ChatMasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'group', 'created_dt']

@admin.register(GroupMaster)
class GroupMasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']