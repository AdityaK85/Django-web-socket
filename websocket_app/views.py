from django.shortcuts import render
from .models import *
import json
# Create your views here.
def index(request, group_name):
    group = GroupMaster.objects.filter(name = group_name).first()
    chats= []
    if group:
        chats = ChatMaster.objects.filter(group=group)
    else:
        GroupMaster.objects.create(name=group_name)
    return render(request, 'index.html',  {'group_name':group_name, 'chats':chats})