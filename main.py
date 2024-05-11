import subprocess
import wolframalpha
import pyttsx3
import tkinter
import json
import random
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import feedparser
import smtplib
import ctypes
import time
import requests
import pyautogui
import pygame
import shutil
from twilio.rest import Client
from clint.textui import progress
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from newsapi import NewsApiClient
from gtts import gTTS
from pyvi import ViTokenizer

wikipedia.set_lang('vi')
language = 'vi'
path = ChromeDriverManager().install()

engine = pyttsx3.init()

# Lấy danh sách các giọng đọc có sẵn
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[2].id)

# Lặp qua danh sách giọng đọc để tìm giọng tiếng Việt
for voice in voices:
    if "vi" in voice.languages:
        engine.setProperty('voice', voice.id)
        break
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Chào buổi sáng !")

    elif 12 <= hour <= 18:
        speak("Chào buổi chiều !")

    else:
        speak("Chào buổi tối !")

    assname = ("Siêu đẹp trai")
    speak("Tôi là trợ lí ảo của bạn")
    speak(assname)

def username():
    speak("Bạn tên là gì nhỉ...")
    uname = takeCommand()
    if uname is None:
        print("Tôi không biết tên của bạn...")
        return
    print("Hello", uname)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Đang nghe...")
        try:
            audio = r.listen(source)
            print("Đang nhận dạng...")
            query = r.recognize_google(audio, language='vi-VN')
            print("Bạn nói:", query)
            return query.lower()
        except sr.UnknownValueError:
            print("Xin lỗi, tôi không nghe rõ.")
            return None
        except sr.RequestError as e:
            print("Không thể kết nối với dịch vụ nhận dạng giọng nói; {0}".format(e))
            return None
        except KeyboardInterrupt:
            print("User interrupted the program.")
            return None

def sendEmail(to, content):
    server = smtplib.SMTP('anhq2303.gmail.com', 587)
    server.ehlo()
    server.starttls()

    # Enable low security in gmail
    server.login('your email id', 'your email password')
    server.sendmail('your email id', to, content)
    server.close()
def search_google(query):
    speak('Đang tìm kiếm trên Google...')
    webbrowser.open(f"https://www.google.com/search?q={query}")

#Biến để theo dõi trạng thái của việc phát nhạc
is_playing_music = False

def play_random_music():
    global is_playing_music
    if not is_playing_music:
        speak("Chọn bài hát để phát")
        music_dir = "C:\\QuangAnh\\Music"
        songs = os.listdir(music_dir)
        if len(songs) > 0:
            random_song = random.choice(songs)
            speak(f"Đang phát bài hát {random_song}")
            pygame.mixer.init()
            pygame.mixer.music.load(os.path.join(music_dir, random_song))
            pygame.mixer.music.play()
            is_playing_music = True
        else:
            speak("Thư mục nhạc của bạn đang trống. Vui lòng thêm bài hát vào thư mục và thử lại sau.")
    else:
        speak("Nhạc đang được phát.")

def stop_music():
    global is_playing_music
    if is_playing_music:
        pygame.mixer.music.stop()
        is_playing_music = False
        speak("Đã dừng phát nhạc.")
    else:
        speak("Không có nhạc đang phát.")

def calculate_query(query):
    speak("Đang tính toán.")
    app_id = "A7UUW6-X77KGQJPJ7"
    client = wolframalpha.Client(app_id)
    query = query.replace("tính toán", "").strip()
    res = client.query(query)
    try:
        answer = next(res.results).text
        print("Kết quả là " + answer)
        speak("Kết quả là " + answer)
    except StopIteration:
        print("Không có kết quả từ Wolfram Alpha.")
        speak("Không có kết quả từ Wolfram Alpha.")

def get_weather(city):
    api_key = "0fc0671b48c24abb97bb73a22c07e60c"
    url = f"https://api.weatherbit.io/v2.0/current?key={api_key}&city={city}&country=VN"

    try:
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            return "Không tìm thấy thông tin thời tiết cho thành phố này."

        weather_description = data["data"][0]["weather"]["description"]
        temperature = data["data"][0]["temp"]
        humidity = data["data"][0]["rh"]

        return f"Thời tiết ở {city} hiện tại là {weather_description}. Nhiệt độ là {temperature} độ C, độ ẩm là {humidity}%."

    except Exception as e:
        print("Đã xảy ra lỗi:", e)
        return "Đã xảy ra lỗi khi lấy thông tin thời tiết."

def open_notes():
    # Mở tập tin ghi chú bằng trình soạn thảo văn bản mặc định trên hệ thống
    try:
        os.system('start ghichu.txt')
    except Exception as e:
        print("Không thể mở tập tin ghi chú.")
        print(e)

def get_vietnamese_news():
    try:
        url = "https://newsdata.io/api/1/news?country=vi&apikey=pub_439129b0ee4fe1a61d747e187eb5aca122bbc"

        response = urlopen(url)
        data = json.load(response)

        speak('Đây là một số tin tức mới trong ngày')
        print('=============== Tin tức nổi bật ============' + '\n')

        article_count = 0  # Biến đếm số lượng bài báo đã hiển thị

        for article in data['results']:
            if article_count >= 3:  # Nếu đã hiển thị đủ 3 bài báo, thoát vòng lặp
                break

            title = article['title']
            link = article['link']
            description = article['description']

            # Kiểm tra nếu title hoặc description là None, bỏ qua bài báo này
            if title is None or description is None:
                continue

            # Phân tích từng từ trong tiêu đề và mô tả
            title_tokens = ViTokenizer.tokenize(title).split()
            description_tokens = ViTokenizer.tokenize(description).split()

            # Tạo ra câu mới từ các từ đã phân tích
            title = ' '.join(title_tokens)
            description = ' '.join(description_tokens)

            print(f"Tiêu đề: {title}")
            print(f"Liên kết: {link}")
            print(f"Mô tả: {description}")
            print("\n")
            speak(f"{title}")

            article_count += 1

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == '__main__':
    clear = lambda: os.system('cls')

    # This Function will clean any
    # command before execution of this python file
    clear()
    wishMe()
    username()

    while True:

        query = takeCommand().lower()

        # All the commands said by user will be
        # stored here in 'query' and will be
        # converted to lower case for easily
        # recognition of command

        if 'wikipedia' in query:
            speak('Đang tìm kiếm Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            speak("Theo Wikipedia")
            print(results)
            speak(results)

        elif 'tìm kiếm' in query:
            search_query = query.replace("tìm kiếm", "").strip()
            search_google(search_query)

        elif 'mở youtube' in query:
            speak("Đang mở Youtube")
            webbrowser.open("youtube.com")

        elif 'mở facebook' in query:
            speak("Đang mở Facebook")
            webbrowser.open("facebook.com")

        elif 'mở google' in query:
            speak("Đang mở Google")
            webbrowser.open("google.com")

        elif 'mở spotify' in query:
            speak("Đang mở Spotify")
            webbrowser.open("https://open.spotify.com/")

        elif "mở wikipedia" in query:
            webbrowser.open("wikipedia.com")

        elif 'phát nhạc' in query or "bật bài hát" in query:
                play_random_music()

        elif 'dừng nhạc' in query or "dừng phát nhạc" in query:
            stop_music()

        elif 'mấy giờ' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Bây giờ là {strTime}")

        if 'thời tiết' in query:
            speak("Bạn muốn biết thời tiết ở thành phố nào?")
            city_name = takeCommand().lower()  # Lấy tên thành phố từ người dùng
            weather_info = get_weather(city_name)
            speak(weather_info)

        elif "camera" in query or "chụp ảnh" in query:
            time.sleep(10)
            ec.capture(0, "Ame Camera ", "img.jpg")

        elif 'email cho Quang Anh' in query:
            try:
                speak("Nội dung email là gì?")
                content = takeCommand()
                to = "Địa chỉ email người nhận?"
                sendEmail(to, content)
                speak("Email đã được gửi !")
            except Exception as e:
                print(e)
                speak("Không thể gửi email")

        elif 'gửi email' in query:
            try:
                speak("Nội dung email là gì?")
                content = takeCommand()
                speak("gửi cho ai?")
                to = input()
                sendEmail(to, content)
                speak("Email đã được gửi !")
            except Exception as e:
                print(e)
                speak("Không thể gửi email")

        elif "tính toán" in query:
            calculate_query(query)

        elif "viết ghi chú" in query:
            speak("Bạn muốn ghi chú gì?")
            note_content = takeCommand()
            if note_content:
                try:
                    with open('ghichu.txt', 'a', encoding='utf-8') as file:
                        current_time = datetime.datetime.now().strftime("%H:%M:%S")
                        file.write(f"{current_time} - {note_content}\n")
                    speak("Ghi chú đã được lưu.")
                    open_notes()
                except Exception as e:
                    speak("Xin lỗi, có lỗi xảy ra khi ghi chú.")
                    print(e)
            else:
                speak("Xin lỗi, tôi không nhận được nội dung ghi chú từ bạn.")

        elif "xem ghi chú" in query:
            speak("Ghi chú của bạn đây")
            file = open("ghichu.txt", "r")
            print(file.read())
            speak(file.read(6))


        elif 'tin tức' in query:
            get_vietnamese_news()

        elif 'chụp màn hình' in query:
            try:
                # Chụp ảnh màn hình và lưu vào tệp 'screenshot.png'
                pyautogui.screenshot('screenshot.png')
                print("Đã chụp ảnh màn hình ")
            except Exception as e:
                print(f"Lỗi: {e}")

        elif "ở đâu" in query:
            query = query.replace("", "ở đâu")
            location = query
            speak("Tôi đang tìm địa điểm đó cho bạn")
            webbrowser.open("https://www.google.com/maps/place/" + location + "")





            # most asked question from google Assistant
        elif 'bạn thế nào' in query:
            speak("Hôm nay tôi rất vui!")
            speak("Thế còn bạn thì sao")

        elif 'vui' in query or "ổn" in query:
            speak("Tôi cũng vui khi thấy bạn thế")

        elif 'buồn' in query or "chán" in query:
            speak("Không có chuyện gì phải buồn đâu")

        elif "đổi tên của tôi thành" in query:
            query = query.replace("đổi tên của tôi thành", "")
            assname = query

        elif "đổi tên" in query:
            speak("Giờ tôi có thể được gọi bằng gì ")
            assname = takeCommand()
            speak("Cảm ơn đã đặt tên cho tôi")

        elif "Tên của bạn là gì" in query or "Bạn tên là gì" in query:
            speak("Bạn của tôi gọi tôi")
            speak(assname)
            print("Bạn của tôi gọi tôi", assname)

        elif "Ai đã tạo ra bạn" in query or "Bạn được ai tạo ra" in query:
            speak("Tôi được tạo bởi Quang Anh.")

        elif 'đùa' in query:
            speak(pyjokes.get_joke())

        elif "will you be my gf" in query or "will you be my bf" in query:
            speak("I'm not sure about, may be you should give me some time")

        elif "bao nhiêu tuổi" in query or "tuổi" in query:
            speak("Tôi mới được gần 1 tháng tuổi")

        elif "i love you" in query:
            speak("Tôi cũng yêu bạn")

        elif "tôi là ai" in query:
            speak("Bạn là người đã tạo ra tôi.")

        elif "con gà có trước hay quả trứng có trước" in query:
            speak("ha ha bạn thật vui tính. Tôi nghĩ đây là một câu nói đùa.")

        elif 'tình yêu là gì' in query:
            speak("Ý bạn là bài hát 'tình yêu có nghĩa là gì' của Tlinh")

        elif "Ai lười nhất" in query:
            speak("Tôi nghĩ đó là Hoàng Trung Hiếu")

        elif 'reason for you' in query:
            speak("I was created as a Minor project by Mister Gaurav ")

        elif 'thoát' in query:
            speak("Chúc bạn một ngày tốt lành")
            exit()

        elif 'đóng màn hình' in query or "khóa màn  hình" in query:
            speak("Đang khóa màn hình")
            ctypes.windll.user32.LockWorkStation()

        elif 'tắt máy' in query:
            speak("Máy sẽ được tắt")
            subprocess.call('shutdown / p /f')

        elif "khởi động lại máy" in query:
            subprocess.call(["shutdown", "/r"])

        elif "nghỉ ngơi thôi" in query or "đi ngủ thôi" in query:
            speak("Chúc bạn ngủ ngon")
            subprocess.call("shutdown / h")




    # elif "" in query:
    # Command go here
    # For adding more commands

