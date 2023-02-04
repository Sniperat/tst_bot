from .models import *
from .validators import *
from django.conf import settings
from telebot import types
from django.core.files import File
import telebot
bot = telebot.TeleBot(settings.BOT_TOKEN, parse_mode=None)


def acceptMessage(user: TgUserModel, data):
    if saveMessage(user, data):
        msg = data['message']['text']
        if msg == '/start':
            text_me = 'Iltmos To\'liq ismingizni kiriting!'
        elif user.steps == FULL_NAME:
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
            else:
                text_me = 'Raqam noto\'g\'ri kiritildi'
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
                else:
                    text_me = 'email noto\'g\'ri kiritildi!'
        elif user.steps == ADDRESS:
            user.address = msg
            user.steps = READY_TO_CHAT
            user.save()
            text_me = 'Ma`lumotlaringizni biz bilan ulashganingiz uchun rahmat\n \
                Bemalol murojatlaringizni yuboravering, ma`lum muddatdan kein sizga \
                habar qaytarishadi'

        elif user.steps == READY_TO_CHAT:

            # bot.send_message(chat_id=user.chat_id, text='asdasd')
            return False

        return {
            'chat_id': user.chat_id,
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

        return False
    elif 'photo' in data['message']:

        file_info = bot.get_file(data['message']['photo'][-1]['file_id'])
        downloaded_file = bot.download_file(file_info.file_path)
        new_file = open(f"image.jpg", 'wb')
        new_file.write(downloaded_file)
        existing_file = open('image.jpg', 'rb')
        django_image_file = File(file=existing_file, name='filename.jpg')
        MessageModel.objects.create(
            msg_type=FILE,
            file=django_image_file,
            tg_user=user
        )
        new_file.close()
        existing_file.close()
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
