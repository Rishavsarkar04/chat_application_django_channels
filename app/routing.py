from django.urls import path
from app import consumers


websocket_urlpatterns =[
    path('ws/<int:id>/', consumers.PersonalChat.as_asgi()),
    path('ws/online/', consumers.OnlineNotification.as_asgi()),
    path('ws/noti/', consumers.Chat_notification.as_asgi()),
]