import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from api.utils import CustomSerializer
from chat.models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("This is the main game", self.scope)
        # current_user_id = self.scope['user'].id if self.scope['user'].id else int(self.scope['query_string'])
        other_user_id = self.scope['url_route']['kwargs']['id']
        self.room_name = (
            f'{other_user_id}'
        )
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        # await self.send(text_data=self.room_group_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_layer)
        await self.disconnect(close_code)

    async def receive(self, text_data=None, bytes_data=None):
        print("This is the main game2", text_data)
        print("This is the main game3", bytes_data)

        data = json.loads(text_data)
        message = ""
        try :
            file = data['file']
            filename = data['filename']
            print(file.name + "hu hu")
        except:
            file = None
            filename = ""
            try:
                message = data['message']
            except:
                return
        
        sender_username = data['senderUsername'].replace('"', '')
        sender = await self.get_user(sender_username.replace('"', ''))

        await self.save_message(sender=sender, message=message, thread_name=self.room_group_name, file=file, filename=filename)

        messages = await self.get_messages()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'senderUsername': sender_username,
                'messages': messages,
            },
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['senderUsername']
        messages = event['messages']
        # print("Inside chat maessage")
        # print(message + username + messages)
        await self.send(
            text_data=json.dumps(
                {
                    'message': message,
                    'senderUsername': username,
                    'messages': messages,
                }
            )
        )

    async def temp(self, event):
        message = event['message']
        # Send the build progress update to the WebSocket connection
        print("called this")
        await self.send(text_data=json.dumps({'message': message}))

    @database_sync_to_async
    def get_user(self, username):
        return get_user_model().objects.filter(username=username).first()

    @database_sync_to_async
    def get_messages(self):
        custom_serializers = CustomSerializer()
        messages = custom_serializers.serialize(
            Message.objects.select_related().filter(thread_name=self.room_group_name),
            fields=(
                'id',
                'sender__pk',
                'sender__username',
                'sender__last_name',
                'sender__first_name',
                'sender__email',
                'sender__last_login',
                'sender__is_staff',
                'sender__is_active',
                'sender__date_joined',
                'sender__is_superuser',
                'message',
                'thread_name',
                'timestamp',
                'file',
                'filename',
            ),
        )
        
        
        return messages

    @database_sync_to_async
    def save_message(self, sender, message, thread_name, file, filename):
        Message.objects.create(sender=sender, message=message, thread_name=thread_name, file=file, filename=filename)
