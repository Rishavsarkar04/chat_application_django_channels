from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import MyUser,Chat
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.db.models import Q

@receiver(post_save,sender = MyUser)
def online_status_send(sender,instance,created,**kwargs):
    if not created:
        channel_layer = get_channel_layer()
        user = instance.username
        user_status = instance.is_online
        dict = {
            'username':user,
            'status':user_status
        }

        async_to_sync(channel_layer.group_send)("online",
                                                 {"type": "chat_online",
                                                  'data':dict
                                                  })
        

@receiver(post_save,sender = Chat)
def chat_notific(sender,instance,created,**kwargs):
    if created:
        channel_layer = get_channel_layer()
        print(instance.sender , instance.receiver)
        num = Chat.objects.filter(Q(receiver=instance.receiver) & Q(is_seen = False) & Q(sender=instance.sender)).all().count()
        dict = {
            'from':instance.sender,
            'num':num,
            'current_user':instance.receiver,
            'status':'unseen'
        }

        async_to_sync(channel_layer.group_send)('noti',
                                                 {"type": "chat_noti",
                                                  'data':dict
                                                  })
