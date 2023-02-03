from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


FULL_NAME = 0
PHONE = 1
EMAIL = 2
ADDRESS = 3
READY_TO_CHAT = 4

STEPS = (
    (FULL_NAME, 'add fullname'),
    (PHONE, 'add phone number'),
    (EMAIL, 'add email'),
    (ADDRESS, 'add address'),
    (READY_TO_CHAT, 'ready to chat')
)


class TgUserModel(models.Model):
    chat_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    steps = models.SmallIntegerField(choices=STEPS, default=FULL_NAME)

    def __str__(self) -> str:
        return f'{self.username}'
    
    def go_chat(self):
        return mark_safe(f'<a href="/chat/{self.chat_id}" height="150">go chat<a/>')

    def image_tag(self):
        return mark_safe('<img src="/media/%s" height="200" />' % (self.image))


TEXT = 0
IMAGE = 1
FILE = 2
MSG_TYPE = (
    (TEXT, 'Text'),
    (IMAGE, 'Image'),
    (FILE, 'File')
)

NEW = 0
READ = 1
M_STATUS = (
    (NEW, 'New message'),
    (READ, 'read')
)


class MessageModel(models.Model):
    msg_type = models.SmallIntegerField(choices=MSG_TYPE, default=TEXT)
    text = models.TextField()
    file = models.FileField(upload_to='files/', null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    tg_user = models.ForeignKey(TgUserModel, on_delete=models.RESTRICT)
    m_status = models.SmallIntegerField(choices=M_STATUS, default=NEW)

    def __str__(self) -> str:
        return str(self.msg_type)


PRIVATE = 0
BROAD = 1
SEND_STATUS = (
    (PRIVATE, 'Private'),
    (BROAD, 'Broad')
)
class ServerMessageModel(models.Model):
    msg_type = models.SmallIntegerField(choices=MSG_TYPE, default=TEXT)
    text = models.TextField()
    file = models.FileField(null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    tg_user = models.ForeignKey(TgUserModel, on_delete=models.RESTRICT)
    m_status = models.SmallIntegerField(choices=M_STATUS, default=NEW)
    is_admin = models.BooleanField(default=True)
    send_type = models.SmallIntegerField(choices=SEND_STATUS, default=PRIVATE)
    is_recive = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.id)



# aaa = MessageModel.objects.raw('Select bot_messagemodel.text as text, bot_ from bot_tgusermodel')
# for i in aaa:
#     print(i.chat_id)