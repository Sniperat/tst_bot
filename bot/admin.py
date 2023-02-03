from django.contrib import admin
from .models import TgUserModel, MessageModel, ServerMessageModel
from .forms import MForm
from django.shortcuts import render, HttpResponseRedirect


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'username', 'first_name','full_name', 'phone_number', 'go_chat']
    # ordering = ['title']
    actions = ['send_all_msg']

    def send_all_msg(self, request, queryset):

        # form = MForm()

        return render(request, 'send_msg.html',
            {'title': u'Send Message',
             'objects': list(queryset.values_list('chat_id', flat=True))
             })

admin.site.register(TgUserModel, ArticleAdmin)
admin.site.register(MessageModel)
admin.site.register(ServerMessageModel)