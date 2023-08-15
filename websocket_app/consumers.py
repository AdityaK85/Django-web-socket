import asyncio
from time import sleep
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
import json
from asgiref.sync import async_to_sync
from .models import *
import datetime
from channels.db import database_sync_to_async

# SyncConsumer
class MySyncConsumer_Connect(SyncConsumer):
    def websocket_connect(self , event):
        # print('channal layers ', self.channel_layer)
        # print('channal name ', self.channel_name)

        self.group_name =  self.scope['url_route']['kwargs']['group_name']
        # add new member in group
        async_to_sync(self.channel_layer.group_add)
        (self.group_name, self.channel_name)

        self.send({
            'type':'websocket.accept'
        })
        print("Websocket Connected....", event)
        

def websocket_receive(self, event):
    print("Websocket Received....", event['text'])
    print("Websocket Received....", type(event['text']))

    data = type(json.loads(event['text']))
    # print("..........json", data)
    group = GroupMaster.objects.get(name = self.group_name)
    ChatMaster.objects.create(content=data['msg'], group=group)

    async_to_sync(self.channel_layer.group_send)(
        self.group_name,
        {
            'type': 'chat.message',
            'message': event['text'],
        }
    )

    def chat_message(self, event):
        print('EVENT--> ', event['message'])
        self.send({
            'type' : 'websocket.send',
            'text' : event['message']
        })

    def websocket_disconnect(self , event):
        print("Websocket Disconnected....", event)
        StopConsumer()


# AsynConsumer
class AsycConsumer_Connect(AsyncConsumer):
    async def websocket_connect(self , event):
        print("Websocket Connected....", event)
        self.group_name =  self.scope['url_route']['kwargs']['group_name']
        await self.channel_layer.group_add( self.group_name , self.channel_name )
        await self.send({
                'type':'websocket.accept'
            })

    async def websocket_receive(self , event):
        print("Websocket Recived....", event['text'])
        print("Websocket Recived type....", type(event['text']))
        data = json.loads(event['text'])
        # print('................jsone',type(data))
        # print('................jsone',data)
        group = await database_sync_to_async(GroupMaster.objects.get)(name = self.group_name)
        await database_sync_to_async(ChatMaster.objects.create)(content=data['msg'], group=group)
        
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'chat.message',
                'message':event['text'],
            }
        )

    async def chat_message(self, event):
        print('EVENT--> ', event['message'])
        await self.send({
            'type':'websocket.send',
            'text': event['message']
        })

    async def websocket_disconnect(self , event):
        print("Websocket Disconnected....", event)

        # Remove Group & Discard  
        await self.channel_layer.group_discard (
            'Programmers_Groups', self.channel_name)
        StopConsumer()