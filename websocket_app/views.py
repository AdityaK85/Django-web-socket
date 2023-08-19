from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
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

 #  This is static group add dynamic group name with logic
def send_dynamic_msg_to_group(request):
    channal_layer = get_channel_layer()
    async_to_sync(channal_layer.group_send)(
        	'love', 
        {
            'type':'chat.message',
            'message':  "Alert Message for this group ! Warning !!"
        }
    )
    return HttpResponse("Warning message sent")


def msg_to_group(request):
    return HttpResponse("Warning message sent")