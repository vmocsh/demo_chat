from django.contrib.auth import get_user_model
from django.db import models


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='chat', blank=True)
    filename = models.TextField(blank=True)

    def __str__(self) -> str:
        return f'{self.sender.username}-{self.thread_name}' if self.sender else f'{self.message}-{self.thread_name}'
    
class Files(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='chat', blank=True)

class HelpLine(models.Model):
    """
    Model for different helpline numbers
    Eg: General helping number, education specific etc.
    """
    name = models.CharField(max_length=64, default="General")
    helpline_number = models.CharField(max_length=16, unique=True)
    helpline_tollfree_number = models.CharField(max_length=16, unique=True, default=None)

    def __str__(self):
        return self.name


class HelperCategory(models.Model):
    """
    Model to map helpers to different categories, many-to-many from helpers side
    """
    helpline = models.ForeignKey(HelpLine, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
    

class ClientStatusOptions:
    """
    Status options available to Client
    """
    ACTIVE = 1
    BLOCKED = 2
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (BLOCKED, 'Blocked'),
    )

class CallRequestStatusOptions:
    """
    Status options available to Call Requests
    """
    CREATED = 1
    BLOCKED = 2
    MERGED = 3
    INVALID_HELPLINE = 0
    STATUS_CHOICES = (
        (CREATED, 'Created'),
        (BLOCKED, 'Blocked'),
        (MERGED, 'Merged'),
    )


class TaskStatusOptions:
    """
    Status options available to Tasks
    """
    PENDING = 1
    COMPLETED = 2
    REJECTED = 3
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (REJECTED, 'Rejected'),
    )


class TaskType:

    DIRECT = 1
    INDIRECT = 2
    TYPE_CHOICES = (
        (DIRECT, 'DIRECT'),
        (INDIRECT, 'INDIRECT'),
    )

    
class Client(models.Model):
    """
    Model for details of people who are seeking for help
    New client gets added every time a request from new number is incoming
    """
    name = models.CharField(max_length=128, null=True, default=None, blank=True)
    location = models.CharField(max_length=128, null=True, default=None, blank=True)
    client_number = models.CharField(max_length=16, unique=True)
    lastSMSSent = models.DateTimeField('Last SMS Timestamp', auto_now=True, null=True)

    status = models.IntegerField(
        default=ClientStatusOptions.ACTIVE,
        choices=ClientStatusOptions.STATUS_CHOICES,
    )

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.client_number

    def is_blocked(self):
        """
        To check if client is blocked
        """
        return self.status == ClientStatusOptions.BLOCKED

class CallRequest(models.Model):
    """
    Model for storing incoming call requests
        Calls for whom task is already pending is merged
        Calls for whom client is blocked is blocked
        If above two condition fails is when task is created

    Refers to helpline and client
    """

    helpline = models.ForeignKey(HelpLine, related_name='call_requests', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='call_requests', on_delete=models.CASCADE)

    created = models.DateTimeField('Created Timestamp', auto_now_add=True)

    status = models.IntegerField(
        default=CallRequestStatusOptions.CREATED,
        choices=CallRequestStatusOptions.STATUS_CHOICES,
    )

    def __str__(self):
        return str(self.pk)

class CategorySubcategory(models.Model):
    language_options = (
        ('english', 'en'),
        ('hindi', 'hi'),
        ('gujarati', 'gj'),
        ('marathi', 'mr')
    )
    helpline = models.ForeignKey(HelpLine, on_delete=models.CASCADE)
    category = models.CharField(max_length=512)
    subcategory = models.CharField(max_length=512)
    language = models.CharField(max_length=13, choices=language_options, default='english')

    def __str__(self):
        return self.category+":"+self.subcategory

class Language(models.Model):
    language = models.CharField(max_length=20)
    helpline = models.ForeignKey(HelpLine, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.language)
    
class Task(models.Model):
    """
    Model for the actual Tasks created
    Creates only when request is valid and task not already pending

    Refers to call request
    """
    # Each helper may belong to more than one category
    call_request = models.ForeignKey(CallRequest, related_name='tasks', on_delete=models.CASCADE)
    category = models.ForeignKey(
        HelperCategory,
        related_name='tasks',
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    taskcategory = models.ManyToManyField(CategorySubcategory, related_name='taskcategory', default=None, blank=True)

    tasksubcategory = models.ManyToManyField(CategorySubcategory, related_name='tasksubcategory', default=None,
                                             blank=True)

    language = models.ManyToManyField('Language', blank=True)
    created = models.DateTimeField('Created Timestamp', auto_now_add=True)
    modified = models.DateTimeField('Modified Timestamp', auto_now=True)
    tag_string = models.CharField(max_length=256, default="", null=True, blank=True)
    task_type = models.IntegerField(
        default=TaskType.INDIRECT,
        choices=TaskType.TYPE_CHOICES
    )
    status = models.IntegerField(
        default=TaskStatusOptions.PENDING,
        choices=TaskStatusOptions.STATUS_CHOICES,
    )
    call_attempt = models.IntegerField(default=0)
    client_calls = models.IntegerField(default=1)
    from_whatsapp = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return str(self.pk)