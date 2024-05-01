import telebot
from speechkit import (text_to_speech,speech_to_text)
from yandex_gpt import *
from config import TOKEN
from bd import *
import math


# создаём бота, используя сгенерированный токен
bot = telebot.TeleBot(TOKEN)
create_table()

def tts(text, user):
        den, out = text_to_speech(text)
        seve_in_bd_TTS(user, len(text))
        return out
def stt(file, user, lenght):
        # Получаем статус и содержимое ответа от SpeechKit
        status, text = speech_to_text(file)
        seve_in_bd_STT(user, lenght)
        return text
def gpt(text, user):
    out = ask_gpt(text)
    print(out[1])
    seve_in_bd_GPT(user,count_tokens_in_dialog(out[1],"assistant") + count_tokens_in_dialog(text,"user"))
    return out[1]

def com_tts(message):
    if message.text:
        user = message.from_user.id
        voice = tts(message.text, user)
        bot.send_voice(user, voice)
    else:
        bot.send_message(message.from_user.id, "у вас закончились токены")

def com_stt(message):
    if message.voice:
        if message.voice.duration < 15:
            user = message.from_user.id
            if not check_user(user):
                create_user(user)
            if user_check_all(user):
                file_id = message.voice.file_id  # получаем id голосового сообщения
                file_info = bot.get_file(file_id)  # получаем информацию о голосовом сообщении
                file = bot.download_file(file_info.file_path)  # скачиваем голосовое сообщение
                lenght = math.ceil(message.voice.duration / 15)
                bot.send_message(user, stt(file, user, lenght))
            else:
                bot.send_message(message.from_user.id, "Похоже вы исчерпали лимиты или пользователей слишком много")
        else:
            bot.send_message(message.from_user.id, "Сообщение слишком длинное")
    else:
        bot.send_message(message.from_user.id, "Голосовое сообщение")
# обрабатываем команду /start
@bot.message_handler(commands=['start'])
def start(message):
    if not check_user(message.from_user.id):
        create_user(message.from_user.id)
    print(message.from_user.id)
    bot.send_message(message.from_user.id, "Привет! Я бот использующий GPT для общения с тобой.")

@bot.message_handler(commands= ['tts'])
def txt_to_sp(message: telebot.types.Message):
    user = message.from_user.id
    # Три проверки
    if not check_user(user):
        create_user(user)
    if user_check_TTS(user):
        bot.send_message(user, "жду сообщения")
        bot.register_next_step_handler(message, com_tts)
    else:
        bot.send_message(message.from_user.id, "Похоже вы исчерпали лимиты")

@bot.message_handler(commands= ['stt'])
def sp_to_txt(message: telebot.types.Message):
    user = message.from_user.id
    # Три проверки
    if not check_user(user):
        create_user(user)
    if user_check_STT(user):
        bot.send_message(user, "жду сообщения")
        bot.register_next_step_handler(message, com_stt)
    else:
        bot.send_message(message.from_user.id, "Похоже вы исчерпали лимиты")

# обрабатываем голосовые сообщения
@bot.message_handler(content_types=['voice'])
def handle_voice(message: telebot.types.Message):
    pass
    # Три проверки
    if message.voice.duration < 15:
        user = message.from_user.id
        if not check_user(user):
            create_user(user)
        if user_check_all(user):
            file_id = message.voice.file_id  # получаем id голосового сообщения
            file_info = bot.get_file(file_id)  # получаем информацию о голосовом сообщении
            file = bot.download_file(file_info.file_path)  # скачиваем голосовое сообщение
            lenght = math.ceil(message.voice.duration / 15)
            bot.send_voice(user, tts(gpt(stt(file, user, lenght), user), user))
        else:
            bot.send_message(message.from_user.id, "Похоже вы исчерпали лимиты")
    else:
        bot.send_message(message.from_user.id, "Сообщение слишком длинное")
    # Речь в текст
    # Сгенерировать пост

@bot.message_handler(content_types=['text'])
def txt_gpt(message: telebot.types.Message):
    user = message.from_user.id
    text = message.text
    # Три проверки
    if not check_user(user):
        create_user(user)
    if user_check_GPT(user):
        bot.send_message(user, gpt(text, user))
    else:
        bot.send_message(message.from_user.id, "Похоже вы исчерпали лимиты")
    # Речь в текст
    # Сгенерировать пост
bot.polling()  # запускаем бота
