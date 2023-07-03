from chat.consumers import ChatConsumer
from channels.layers import get_channel_layer
import asyncio
from multiprocessing import Process
from channels.db import database_sync_to_async
from chat.models import Message
from django.contrib.auth import get_user_model

# @database_sync_to_async
def save_message(sender, message, thread_name, file=None, filename=""):
    Message.objects.create(sender=sender, message=message, thread_name=thread_name, file=file, filename=filename)

def send_file_message(messages):
        print("Andar to aaya")
        consumer = ChatConsumer()
        sender = "babu"
        message = "hehe"
        # other_user_id = consumer.scope['url_route']['kwargs']['id']
        # consumer.room_name = "82"
        # consumer.room_group_name = f'chat_{consumer.room_name}'
        
        # await consumer.channel_layer.group_add(consumer.room_group_name, consumer.channel_name)
        # await consumer.accept()
        file = None
        filename = ""
        # await consumer.save_message(sender=sender, message=message, thread_name="chat_82", file=file, filename=filename)
        print("saved message")
        # messages = await consumer.get_messages()
        channel_layer = get_channel_layer()
        print(channel_layer)
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # future = asyncio.ensure_future(channel_layer.group_send(
        #     "chat_82",
        #     {
        #         'type': 'chat_message',
        #         'message': message,
        #         'senderUsername': "9881246601",
        #         'messages': messages,
        #     },
        # )) # tasks to do
        # loop.run_until_complete(future)
        # print(future.result())
        user = get_user_model()
        sender = user.objects.all().get(username="9881246601")
        save_message(sender=sender, message=message, thread_name="chat_82")
        p = Process(target=channel_layer.group_send, args=("chat_82",
            {
                'type': 'chat_message',
                'message': message,
                'senderUsername': "9881246601",
                'messages': messages,
            },))
        p.start()


        print("Loop completed")
        