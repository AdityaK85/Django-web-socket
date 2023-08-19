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
        print("Websocket Sync Connected....", event)
        # print('channal layers ', self.channel_layer)
        # print('channal name ', self.channel_name)

        self.group_name =  self.scope['url_route']['kwargs']['group_name']
        # print(self.scope['user'])
        # add new member in group
        async_to_sync(self.channel_layer.group_add)
        (self.group_name, self.channel_name)

        self.send({
            'type':'websocket.accept'
        })
        

    def websocket_receive(self, event):
        # print("Websocket Received....", event['text'])
        # print("Websocket Received....", type(event['text']))
        
        data = json.loads(event['text'])
        group = GroupMaster.objects.get(name = self.group_name)

        if self.scope['user'].is_authenticated:
            # print('..........data',json.dumps(data))
            chat =  ChatMaster(
                content = data['msg'],
                group = group,  
            )
            chat.save()
            data['user'] = self.scope['user'].username
            # print("............user", type(data))
            # ChatMaster.objects.create(content=data['msg'], group=group)
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'chat.message',
                    'message':json.dumps(data)
                }
            )
        else :
            self.send({
                'type':'websocket.send',
                'text': json.dumps({"msg":"Please login first", "user":"Unknown"})
            })

    def chat_message(self, event):
        print('EVENT--> ', event)
        print('EVENT--> ', event['message'])
        print('EVENT--> ', type(event['message']))
        self.send({
            'type' : 'websocket.send',
            'text' : event['message']
        })

    def websocket_disconnect(self , event):
        print("Websocket Disconnected....", event)
        raise StopConsumer()


# AsynConsumer
class AsycConsumer_Connect(AsyncConsumer):
    async def websocket_connect(self , event):
        print("Websocket Asyc Connected....", event)
        self.group_name =  self.scope['url_route']['kwargs']['group_name']
        await self.channel_layer.group_add( self.group_name , self.channel_name )
        await self.send({
                'type':'websocket.accept'
            })

    async def websocket_receive(self , event):
        # print("Websocket Recived....", event['text'])
        # print("Websocket Recived type....", type(event['text']))
        data = json.loads(event['text'])
        # print('................jsone',type(data))
        # print('................jsone',data)
        group = await database_sync_to_async(GroupMaster.objects.get)(name = self.group_name)
        data['user'] = self.scope['user'].username
        if self.scope['user'].is_authenticated:

            print('..........data',json.dumps(data))

            await database_sync_to_async(ChatMaster.objects.create)(content=data['msg'], group=group)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type':'chat.message',
                    'message':json.dumps(data),
                },
            )
        else:
            await self.send({
                'type':'websocket.send',
                'text': json.dumps({"msg":"Please login first  "})
            })

    async def chat_message(self, event):
        # print('EVENT--> ', event['message'])
        await self.send({
            'type':'websocket.send',
            'text': event['message']
        })

    async def websocket_disconnect(self , event):
        # print("Websocket Disconnected....", event)

        # Remove Group & Discard  
        await self.channel_layer.group_discard (
            'Programmers_Groups', self.channel_name)
        StopConsumer()


# Genric Cosumers
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

class New_WebSocket_Consumer(WebsocketConsumer):
    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        print("Server Connected")
        async_to_sync(self.channel_layer.group_add)( self.group_name , self.channel_name  )
        self.accept()
        # self.close()   Use for Force fully disconnect
    
    def receive(self, text_data=None,bytes_data=None):
        data = json.loads(text_data)

        if self.scope['user'].is_authenticated:
            data['user'] = self.scope['user'].username
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'chat.message',
                    'message': data['msg']
                }
            )
        else:
            self.send(
                text_data=json.dumps({
                    'msg':'Please login first'
                })
            )
        print("Recived MSG", data)
        
    def chat_message(self, event):
        print('...........,', event)
        self.send( text_data= json.dumps({
            'msg':event['message']
            })
        )


    def disconnect(self, code):
        self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        return print("Server Disconnected")


# AsyncWebsocketConsumer
class New_Async_WebSocket_Consumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.group_name = self.scope['url_route']['kwargs']['group_name']
        await self.channel_layer.group_add( self.group_name ,self.channel_name,)
        await self.accept()
        print("Server Connected")
        # await self.close()   Use for Force fully disconnect
    
    async def receive(self, text_data=None, bytes_data=None):

        data = json.loads(text_data)
        print('.........,', data)
        if self.scope['user'].is_authenticated:
            data['user'] = self.scope['user'].username
            # print("..............user", data['user'])
            await self.channel_layer.group_send( self.group_name , { 'type':'chat.message', 'message': data['msg'] })
        else:
            self.send(
                text_data = json.dumps({
                    'msg':'Please login first'
                })
            )
        print("Recived MSG", text_data)

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({

                'msg': event['message'] 
            })
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(

            self.group_name, 
            self.channel_name
        )
        return print("Server Disconnected")



#  Sync & Async Json Websocket consumers
from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer

class my_Json_Websockete_Consumer(JsonWebsocketConsumer):
    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()
        return "Json Websocket connected"
    
    def receive_json(self, content, **kwargs):
        # print("Json Websocket Recived", content)
        if self.scope['user'].is_authenticated:
            content['user'] = self.scope['user'].username
            print("..............., ", content)
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type':'chat.message',
                    'message':content
                }
            )
        else:
            self.send_json({
                'msg':'Please login first'
            })

    def chat_message(self, event):
        self.send_json({'msg':event['message']})

    def disconnect(self, code):
        return f"Json Websocket disconnected{code}"

class my_Async_Json_Websockete_Consumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        await self.channel_layer.group_add (
            self.group_name,
            self.channel_name
        )
        await self.accept()
        return "Json Websocket connected"
    
    async def receive_json(self, content, **kwargs):
        print("Json Websocket Recived", content)
        # for i in range(50):
        #     await self.send_json({"msg":str(i)})
        #     await asyncio.sleep(1)
        if self.scope['user'].is_authenticated:
            content['user'] = self.scope['user'].username
            print("..............., ", content)
            await self.channel_layer.group_send(self.group_name, {
                'type':'chat.message',
                'message':content
            })

        else : 
            self.send_json({'msg':'Please login first'})
    
    async def chat_message(self, event):
        await self.send_json({'msg':event['message']})

    async def disconnect(self, code):
         return f"Json Websocket disconnected{code}"
