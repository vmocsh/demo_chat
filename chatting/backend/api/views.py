import json

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST

from api.utils import CustomSerializer
from chat.models import Message, Files
from chat.consumers import ChatConsumer
from channels.layers import get_channel_layer
from rest_framework.views import APIView
from asgiref.sync import async_to_sync
from multiprocessing import Process
from .bar import send_file_message
import asyncio
from django.contrib.auth.models import User

def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response


@csrf_exempt
@require_POST
def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    PASSWORD = "client123"

    URL = "http://vmocsh.cse.iitb.ac.in/demo_chat/management/getClientTasks/?phno=" + username
    
    PARAMS = {'phno':username}
    r = requests.get(url = URL, params = PARAMS)
    tasks = r
    data = json.loads(tasks.content)
    # for x in range(len(data['accepted'])):
    #     data['accepted'][x] = json.loads(data['accepted'][x])
    print(data)
    if 'detail' in data:
        return JsonResponse({'detail': 'You have no tasks.'}, status=400)
    if username is None or password is None:
        return JsonResponse({'detail': 'Please provide username and password.'}, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        if password != PASSWORD:
            return JsonResponse({'detail': 'Invalid credentials.'}, status=400)
        else:
            user = User.objects.create_user(username=username,
                                 password=PASSWORD)

    # login(request, user)
    return JsonResponse(
        {
            'detail': 'Successfully logged in.',
            'user': json.loads(
                serializers.serialize(
                    'json',
                    [user],
                    fields=(
                        'last_login',
                        'is_superuser',
                        'username',
                        'first_name',
                        'last_name',
                        'email',
                        'is_staff',
                        'is_active',
                        'date_joined',
                    ),
                )
            ),
        }
    )


def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'You\'re not logged in.'}, status=400)

    logout(request)
    return JsonResponse({'detail': 'Successfully logged out.'})


@ensure_csrf_cookie
def session_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False})

    return JsonResponse({'isAuthenticated': True})


def whoami_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False})

    return JsonResponse({'username': request.user.username})


def list_contacts(request):
    # users = get_user_model().objects.exclude(username=request.GET.get('username'))
    # print("hi")
    username =request.GET.get('username')
    URL = "http://vmocsh.cse.iitb.ac.in/demo_chat/management/getClientTasks/?phno=" + username
    
    PARAMS = {'phno':username}
    r = requests.get(url = URL, params = PARAMS)
    tasks = r
    # print(users)
    # print(tasks.content)
    # print(users)
    data = json.loads(tasks.content)
    for x in range(len(data['accepted'])):
        data['accepted'][x] = json.loads(data['accepted'][x])
    print(data)
    # data = serializers.serialize(
    #     'json',
    #     users,
    #     fields=(
    #         'last_login',
    #         'is_superuser',
    #         'username',
    #         'first_name',
    #         'last_name',
    #         'email',
    #         'is_staff',
    #         'is_active',
    #         'date_joined',
    #     ),
    # )
    # print(data)
    return JsonResponse(data, safe=False)

import requests


class ChatPage(APIView): 
    def get(self, request, taskId):
        # print(request, taskId)
        username = request.GET.get('username')
        # print(username)
        PARAMS = {'taskId':taskId}
        URL = "http://vmocsh.cse.iitb.ac.in/demo_chat/management/getTask/?taskId=" + taskId
        r = requests.get(url = URL, params = PARAMS)
        task = json.loads(r.content)
        task = json.loads(task['task'][0])
        # print(task)
        # username = "9881246601"
        URL = "http://vmocsh.cse.iitb.ac.in/demo_chat/management/getClientTasks/?phno=" + username
        
        PARAMS = {'phno':username}
        r = requests.get(url = URL, params = PARAMS)
        tasks = json.loads(r.content)
        for x in range(len(tasks['accepted'])):
            tasks['accepted'][x] = json.loads(tasks['accepted'][x])
        thread_name = (
            f'chat_{taskId}'
        )
        custom_serializers = CustomSerializer()
        messages = custom_serializers.serialize(
            Message.objects.select_related().filter(thread_name=thread_name),
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
                'filename'
            ),
        )
        # print(messages)
        context = {
            'tasks': tasks,
            'task_object': task,
            'messages': messages,
        }
        return JsonResponse(json.loads(json.dumps(context)), safe=False)
    
    def post(self, request):
        print(request)


def getMessages(request):
    taskId = request.GET.get('taskId')
    
    thread_name = (
        f'chat_{taskId}'
    )
    custom_serializers = CustomSerializer()
    messages = Message.objects.filter(thread_name=thread_name)
    msg_list = []
    for msg in messages:
        data = {"id" : msg.id, "message": msg.message, "senderUsername": msg.sender.get_username(), "thread_name": msg.thread_name, "timestamp": str(msg.timestamp), "filename": msg.filename}
        msg_list.append(data)
    context = {
        'messages': msg_list,
    }
    
    return JsonResponse(json.loads(json.dumps(context)), safe=False)

# def uploadFile(request):
#     file = request.get()
    # consumer = ChatConsumer()
    # consumer.room_group_name = "chat_82"
    # messages = consumer.get_messages()
    # consumer.channel_layer.group_send(
    #         consumer.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': "Hello",
    #             'senderUsername': "9881246601",
    #             'messages': messages,
    #         },
    #     )

class uploadFile(APIView): 
    # def send_file_msg(filename, )
    

    def post(self, request):
        # print(request.GET, "kkkk", request.POST, "=====", request.data)
        # file = request.FILES
        file = None
        for file_it in request.FILES:
            file = request.FILES[file_it]
            # file = request.FILES[filename]
        if not file:
            return JsonResponse({'status': 500})

        task_id = request.GET.get("taskId", "")
        # print("taskId ======" + task_id)
        channel = get_channel_layer()
        message = ""
        # task_id = "82"
        room_name = (
            f'{task_id}'
        )
        sender_username = request.GET.get("senderUsername", "")
        room_group_name = f'chat_{room_name}'

        filename = file.name
        username = sender_username.replace('"', '')
        sender = get_user_model().objects.filter(username=username).first()
        messageobj = Message(sender=sender, message="", thread_name=room_group_name, file=None, filename=filename)
        messageobj.save()
        Files.objects.create(message=messageobj, file=file)
        
        custom_serializers = CustomSerializer()
        messages = custom_serializers.serialize(
            Message.objects.select_related().filter(thread_name=room_group_name),
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
        async_to_sync(channel.group_send)(
            room_group_name,
                {
                    "type": "chat.message",
                    "message": message,
                    "senderUsername": sender_username,
                    "messages": messages,
                },
        )
        return JsonResponse({'status': 200})


def downloadFile(request):
    # task_id = request.GET.get("taskId")
    message_id = request.GET.get("msg_id")
    # timestamp = request.GET.get("timestamp")
    # thread_name = f'{task_id}'
    # sender = request.GET.get("senderUsername")
    # username = sender.replace('"', '')
    # sender = get_user_model().objects.filter(username=username).first()
    # print(timestamp, thread_name, sender)
    msg = Message.objects.all().get(id=message_id)
    # print(type(msg))
    file = Files.objects.filter(message=msg).first()
    # print(file)
    file_path = file.file.path

    if file_path:
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/file")
            response['Content-Disposition'] = 'attachment;filename=' + file.file.name
            return response