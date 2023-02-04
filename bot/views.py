from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.views import View
from itertools import chain
from operator import attrgetter
from .functions import *
from .models import *

import json

from django.core.files.storage import FileSystemStorage


@csrf_exempt
def event(request):
    json_list = json.loads(request.body)

    user = get_user(json_list)
    data = acceptMessage(user, json_list)
    if data:
        bot.send_message(chat_id=data['chat_id'], text=data['text'])
        # bot.send_message(chat_id=5828707322, text='dfbdfg')
    return HttpResponse('hello')


# TODO Admin paneldan tanlangan userlar uchun habar jo'natish
class SendView(View):

    def post(self, request):

        users = request.POST.get('tgUsers')
        msg = request.POST.get('text')
        res = list(map(int, users.translate({ord(c): None for c in "[] "}).split(',')))
        users = TgUserModel.objects.filter(chat_id__in=res)
        for i in users:
            MessageModel.objects.filter(m_status=NEW).update(m_status=READ)
            try:
                bot.send_message(chat_id=i.chat_id, text=msg)
                ServerMessageModel.objects.create(text=msg, tg_user=i, send_type=BROAD, m_status=READ)
                i.is_active = True
                i.save()
            except Exception as e:
                ServerMessageModel.objects.create(text=msg, tg_user=i, send_type=BROAD, m_status=READ, is_recive=False)
                i.is_active = False
                i.save()

        return redirect('/admin')


# TODO chatdan habar jo'natish
class ChatView(View):

    def get(self, request, id):
        usr = TgUserModel.objects.get(chat_id=id)
        a_list = MessageModel.objects.filter(tg_user__chat_id=id).order_by('datetime')
        b_list = ServerMessageModel.objects.filter(tg_user__chat_id=id).order_by('datetime')
        result_list = sorted(
            chain(a_list, b_list), key=attrgetter('datetime'))
        return render(request, 'chat.html', {'result_list': result_list, 'chat_id': id, 'user': usr})

    def post(self, request, id):
        usr = TgUserModel.objects.get(chat_id=id)
        MessageModel.objects.filter(m_status=NEW, tg_user=usr).update(m_status=READ)
        msg = request.POST.get('text')

        try:
            myfile = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
        except Exception as e:
            myfile = ""

        server_msg = ServerMessageModel(tg_user=usr, send_type=PRIVATE, m_status=READ)
        
        try:
            if myfile != "":
                server_msg.file = filename
                server_msg.msg_type = FILE
                server_msg.save()
                document = open(f'.{server_msg.file.url}', 'rb')
                bot.send_document(id, document)
                document.close()
            else:
                server_msg.text = msg
                server_msg.save()
                bot.send_message(chat_id=id, text=msg)
            usr.is_active = True
            usr.save()
        except Exception as e:
            server_msg.is_recive = False
            server_msg.save()
            usr.is_active = False
            usr.save()
        return redirect('bot:chat', id)
