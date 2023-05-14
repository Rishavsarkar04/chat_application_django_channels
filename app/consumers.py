from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from channels.db import database_sync_to_async 
import json
from app.models import MyUser,Chat
from datetime import datetime
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer




class PersonalChat(AsyncWebsocketConsumer):
    async def connect(self):
        print('connect personal chat')
        user_to_id = self.scope["url_route"]["kwargs"]["id"]
        user_from_id = self.scope['user'].id
        
        if int(user_from_id) > int(user_to_id):
            self.room_name = f'{user_to_id}-{user_from_id}'
        else:
            self.room_name = f'{user_from_id}-{user_to_id}'

        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        msg = data['msg']
        user_to = data['user_to']
        user_from = data['user_from']

        now = datetime.now()
        current_time = now.strftime("%I:%M %p")

        await self.channel_layer.group_send(self.room_group_name,{
                        'type':'chat_message',
                        'message':msg,
                        'user_to':user_to,
                        'user_from':user_from
                                 })
        

        
        ch_group_list = self.channel_layer.groups.get(self.room_group_name) # only can be used in InMemoryChannelLayer
        if len(ch_group_list) == 2:
            seen = True
            await self.save_chat(msg, user_to, user_from, self.room_group_name ,current_time,seen)
        else:
            await self.save_chat(msg, user_to, user_from, self.room_group_name ,current_time)
    
    async def chat_message(self,event):
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        message = event['message']
        user_to = event['user_to']
        user_from = event['user_from']
        await self.send(json.dumps({
            'message':message,
            'user_to':user_to,
            'user_from':user_from,
            'time':current_time
        }))
      
    @database_sync_to_async
    def save_chat(self, message ,user_to ,user_from ,group_name,time,seen=False):
        a = Chat(sender=user_from, receiver=user_to, message=message,group_name=group_name,date_time=time,is_seen =seen)
        a.save()
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)
        print('server disconect personal chat',close_code)


class OnlineNotification(AsyncWebsocketConsumer):
    async def connect(self):
        print('connect online notification')
        self.room_group_name = 'online'
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()
    

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        status = data['status']
        self.username = self.scope['user'].username
        await self.change_online_status(self.username,status)

    
    async def chat_online(self,event):
        data = event['data']
        username = data['username']
        status = data['status']

        dict = {
            'username': username,
            'status':status
        }
        await self.send(json.dumps(dict))
        

        
    async def disconnect(self, close_code):
        await self.change_online_status(self.username,status=None)
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)

    @database_sync_to_async
    def change_online_status(self , username , status):
        user = MyUser.objects.get(username=username)
        if status == 'online':
            user.is_online = True
            user.save()
        else:
            user.is_online = False
            user.save()

class Chat_notification(AsyncWebsocketConsumer):
    async def connect(self):
        print("chat notification connect")
        self.room_group_name = 'noti'
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()


    async def chat_noti(self,event): 
        data = event['data']
        form_user = data['from']
        number = data['num']
        current_user = data['current_user']
        status = data['status']
            
        await self.send(json.dumps({
                'form_user':form_user,
                'num':number,
                'current_user':current_user,
                'status':status
            }))
        
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)
        print('chat notifiacation disconnect')
