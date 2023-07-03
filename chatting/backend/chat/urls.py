from django.urls import path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/<str:taskId>/', views.ChatPage.as_view(), name='chat_page'),
]
