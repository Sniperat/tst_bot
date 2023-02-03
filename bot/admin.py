from django.contrib import admin
from .models import TgUserModel, MessageModel, ServerMessageModel
from django.shortcuts import render


class TgUserAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'username', 'first_name','full_name', 'phone_number', 'go_chat']
    actions = ['send_all_msg']
    
    def send_all_msg(self, request, queryset):

        return render(request, 'send_msg.html',
            {'title': u'Send Message',
             'objects': list(queryset.values_list('chat_id', flat=True))
             })

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'msg_type', 'text', 'datetime', 'tg_user', 'm_status']


admin.site.register(TgUserModel, TgUserAdmin)
admin.site.register(MessageModel, MessageAdmin)
admin.site.register(ServerMessageModel, MessageAdmin)