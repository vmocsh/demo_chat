from django.contrib.auth import get_user_model
from django.shortcuts import render

from chat.models import Message
import requests
import json
from api.utils import CustomSerializer
from django.http import JsonResponse
from rest_framework.views import APIView


def index(request):
    users = get_user_model().objects.exclude(username=request.user.username)
    URL = "http://vmocsh.cse.iitb.ac.in/demo2/management/getClientTasks/"
    username = "9881246601"
    PARAMS = {'phno':username}
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()
    print(data)
    context = {'users': users}
    return render(request, 'index.html', context)

class ChatPage(APIView):
    
    def get(self, request, taskId):
        print(request, taskId)
        PARAMS = {'taskId':taskId}
        URL = "http://vmocsh.cse.iitb.ac.in/demo_chat/management/getTask/?taskId=" + taskId
        r = requests.get(url = URL, params = PARAMS)
        task = json.loads(r.content)
        task = json.loads(task['task'][0])
        # user_object = get_user_model().objects.defer('password').get(username=username)
        # task_object_serialized = serializers.serialize(
        #     'json',
        #     [task],
        #     fields=(
        #         'task_id',
        #         'status',
        #         'created',
        #     ),
        # )
        print(task)
        username = "9881246601"
        URL = "http://vmocsh.cse.iitb.ac.in/demo_chat/management/getClientTasks/?phno=" + username
        
        PARAMS = {'phno':username}
        r = requests.get(url = URL, params = PARAMS)
        # print(users)
        # print(tasks.content)
        # print(users)
        tasks = json.loads(r.content)
        for x in range(len(tasks['accepted'])):
            tasks['accepted'][x] = json.loads(tasks['accepted'][x])
        # users = serializers.serialize(
        #     'json',
        #     get_user_model().objects.exclude(username=request.GET.get('username')),
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
        # request_user_id = request.GET["id"]
        thread_name = (
            f'chat_{taskId}'
        )
        custom_serializers = CustomSerializer()
        messages = custom_serializers.serialize(
            Message.objects.select_related().filter(thread_name=thread_name),
            fields=(
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

        context = {
            'tasks': tasks,
            'task_object': task,
            'messages': messages,
        }
        return JsonResponse(json.loads(json.dumps(context)), safe=False)
    
    def post(self, request):
        files = request
        print(request)
