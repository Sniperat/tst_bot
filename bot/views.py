from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views import View
from itertools import chain
from operator import attrgetter
from .models import *
from .forms import MForm
from .vlidators import phonevalidate, emailvalidate
import telebot
from telebot import types
import requests
import json
from telegram import ReplyKeyboardMarkup,KeyboardButton
webhook_url = f'https://api.telegram.org/bot{settings.BOT_TOKEN}/'
print(webhook_url)
bot = telebot.TeleBot(settings.BOT_TOKEN, parse_mode=None)

from django.core.files.storage import FileSystemStorage

@csrf_exempt
def event(request):
    json_list = json.loads(request.body)
    # chat_id = json_list['message']['chat']['id']
    print(json_list)

    user = get_user(json_list)
    data = acceptMessage(user, json_list)
    if data:
        response = requests.post(webhook_url+'sendMessage', data=data)
    return HttpResponse('hello')


def acceptMessage(user: TgUserModel, data):
    if saveMessage(user, data):
        msg = data['message']['text']
        if msg == '/start':
            text_me = 'Iltmos To\'liq ismingizni kiriting!'
        elif user.steps ==  FULL_NAME:
            user.full_name = msg
            user.steps = PHONE
            user.save()
            text_me = 'Iltmos telefon raqamingizni kiriting!'
        elif user.steps == PHONE:
            check = phonevalidate(msg)
            if check:
                user.phone_number = msg
                user.steps = EMAIL
                user.save()
                text_me = 'Iltmos email kiriting!\nPochtangiz bolmasa skip tugmasini bosing'
                catalogKBoard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
                skip = types.KeyboardButton(text="skip")
                catalogKBoard.add(skip)

                bot.send_message(chat_id=user.chat_id, text=text_me, reply_markup=catalogKBoard)
                return False
            else:text_me = 'Raqam noto\'g\'ri kiritildi'
        elif user.steps == EMAIL:
            if msg == 'skip':
                user.steps = ADDRESS
                user.save()
                text_me = 'Iltmos To\'liq manzilingizni kiriting!'
            else:
                check = emailvalidate(msg)
                if check:
                    user.email = msg
                    user.steps = ADDRESS
                    user.save()
                    text_me = 'Iltmos To\'liq manzilingizni kiriting!'
                else:text_me = 'email noto\'g\'ri kiritildi!'
        elif user.steps == ADDRESS:
            user.address = msg
            user.steps = READY_TO_CHAT
            user.save()
            text_me = """
                Ma`lumotlaringizni biz bilan ulashganingiz uchun rahmat\n
                Bemalol murojatlaringizni yuboravering, ma`lum muddatdan kein sizga 
                habar qaytarishadi
                    """
        elif user.steps == READY_TO_CHAT:

            # bot.send_message(chat_id=user.chat_id, text='asdasd')
            return False
        
        return {
                'chat_id':user.chat_id,
                'text': text_me
            }
    return False




def saveMessage(user: TgUserModel, data):
    if 'document' in data['message']:
        file_info = bot.get_file(data['message']['document']['file_id'])
        downloaded_file = bot.download_file(file_info.file_path)
        f_name = data['message']['document']['file_name']
        new_file = open(f"{f_name}", 'wb')
        new_file.write(downloaded_file)
        existing_file = open(f'{f_name}', 'rb')
        django_file = File(file=existing_file, name=f'{f_name}')
        MessageModel.objects.create(
            msg_type=2,
            file=django_file,
            tg_user=user
        )
        new_file.close()
        existing_file.close()

        print('tugadi')
        return False
    elif 'photo' in data['message']:
        print(data)
        print('boshlandi')

        file_info = bot.get_file(data['message']['photo'][-1]['file_id'])
        downloaded_file = bot.download_file(file_info.file_path)
        new_file = open(f"image.jpg", 'wb')
        new_file.write(downloaded_file)
        existing_file = open('image.jpg', 'rb')
        django_image_file = File(file=existing_file, name='filename.jpg')
        MessageModel.objects.create(
            msg_type=IMAGE,
            file=django_image_file,
            tg_user=user
        )
        new_file.close()
        existing_file.close()
        print('tugadi')
        return False
    elif 'text' in data['message']:
        MessageModel.objects.create(
            text=data['message']['text'],
            tg_user=user
        )
        return True


def get_user(data):
    try:
        user = TgUserModel.objects.get(chat_id=data['message']['chat']['id'])
    except Exception as e:
        dict_me = data['message']['chat']
        username = None
        first_name = None
        last_name = None
        if 'username' in dict_me:
            username = dict_me['username']
        if 'first_name' in dict_me:
            first_name = dict_me['first_name']
        if 'last_name' in dict_me:
            last_name = dict_me['last_name']
        user = TgUserModel(
            chat_id=data['message']['chat']['id'],
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
    return user



class SendView(View):

    def post(self, request):

        users = request.POST.get('tgUsers')
        msg = request.POST.get('text')
        res = list(map(int,users.translate({ ord(c): None for c in "[] " }).split(',')))
        users = TgUserModel.objects.filter(chat_id__in=res)
        for i in users:
            MessageModel.objects.filter(m_status=NEW).update(m_status=READ)
            try:
                bot.send_message(chat_id=i.chat_id, text=msg)
                ServerMessageModel.objects.create(text=msg, tg_user=i, send_type=BROAD, m_status=READ)
            except Exception as e:
                ServerMessageModel.objects.create(text=msg, tg_user=i, send_type=BROAD, m_status=READ, is_recive=False)
                i.is_active = False
                i.save()

        return redirect('http://127.0.0.1:8000/admin/bot/tgusermodel/')

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
        except:
            myfile = ""
        server_msg = ServerMessageModel(tg_user=usr, send_type=PRIVATE, m_status=READ)
        
        if myfile != "":
            server_msg.file = filename
            server_msg.save()
            img = True
        else:
            server_msg.text = msg
            server_msg.save()
            img = False
        print(server_msg)
        try:
            if img:
                print('file sending')
                print(server_msg.file.url)
                document = open(f'.{server_msg.file.url}', 'rb')
                print('problem')
                bot.send_document(id, document)
                print('file  sended')
                document.close()
            else:
                bot.send_message(chat_id=id, text=msg)
        except Exception as e:
            server_msg.is_recive=False
            server_msg.save()
            usr.is_active = False
            usr.save()
        return redirect('bot:chat', id)