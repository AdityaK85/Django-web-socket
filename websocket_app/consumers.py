import asyncio
from time import sleep
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
import json
from asgiref.sync import async_to_sync

# SyncConsumer
class MySyncConsumer_Connect(SyncConsumer):
    def websocket_connect(self , event):
        print('channal layers ', self.channel_layer)
        print('channal name ', self.channel_name)
         
        # add new member in group
        async_to_sync(self.channel_layer.group_add)('Programmers_Groups', self.channel_name)

        self.send({
            'type':'websocket.accept'
        })
        print("Websocket Connected....", event)
        

    def websocket_receive(self , event):
        print("Websocket Recived....", event['text'])
        async_to_sync(self.channel_layer.group_send)(
            'Programmers_Groups', 
            {
            'type': 'chat.message',
            'message': event['text'],
            }
        )
        # for i in range(50):
        #     self.send({
        #         'type':'websocket.send',
        #         'text':json.dumps(str(i)) ,
        #     })
        #     sleep(1)

    def chat_message(self, event):
        print('EVENT--> ', event['message'])
        self.send({
            'type' : 'websocket.send',
            'text' : event['message']
        })

    def websocket_disconnect(self , event):
        print("Websocket Disconnected....", event)


# AsynConsumer
class AsycConsumer_Connect(AsyncConsumer):
    async def websocket_connect(self , event):
        print("Websocket Connected....", event)

        await self.channel_layer.group_add( 'Programmers_Groups', self.channel_name )
        await self.send({
                'type':'websocket.accept'
            })

    async def websocket_receive(self , event):
        print("Websocket Recived....", event)
        await self.channel_layer.group_send(
            'Programmers_Groups',
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