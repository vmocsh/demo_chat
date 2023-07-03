from django.contrib import admin

from chat.models import Message, Task, Files


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'thread_name', 'get_username', 'message', 'timestamp', 'file', 'filename']
    list_per_page: int = 20

    def get_username(self, obj):
        return obj.sender.username if obj.sender else ''
    
admin.site.register(Task)
admin.site.register(Files)