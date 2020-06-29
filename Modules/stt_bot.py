import telebot
import urllib.request
import subprocess
import speech_recognition as sr
import os
import configparser as cfg

config = cfg.ConfigParser()
config.read("config")

token = config["TELEGRAM_BOT"]["Token"]
bot = telebot.TeleBot(token)
filename = "1.wav"


@bot.message_handler(func=lambda x: True)
def welcom(message):
    bot.send_message(message.chat.id, f"И тебе {message.text}")


@bot.message_handler(content_types=["voice"])
def receive_audio(message):
    id_voice = message.voice.file_id
    file_info = bot.get_file(id_voice)
    urllib.request.urlretrieve(f"http://api.telegram.org/file/bot{token}/{file_info.file_path}", "1.ogg")
    convert_ogg_to_wav()
    bot.send_message(message.chat.id, recognition())
    clear()


def convert_ogg_to_wav():
    process = subprocess.run(["ffmpeg", "-i", "1.ogg", "1.wav"])


def recognition():
    r = sr.Recognizer()
    text = ""
    with sr.AudioFile(filename) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language="ru-RU")
    return text


def clear():
    os.remove("1.ogg")
    os.remove("1.wav")


bot.polling()
