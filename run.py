import pygame
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QMovie, QPixmap, QFont
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt5.QtCore import QThread, QByteArray
from PyQt5 import uic
import speech_recognition as sr
import os
import time
import psutil
import requests
import json
import pyttsx3
import pywhatkit
import sys
import cv2
from googletrans import LANGUAGES, Translator
import wikipedia
import pyjokes
import webbrowser
from gtts import gTTS
import playsound
import datetime
import random
from bs4 import BeautifulSoup

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import speech_recognition as sr
import os
import keyboard
import time
import psutil
import requests
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import speech_recognition as sr
import pyttsx3
import pywhatkit
import speedtest
import sys
# import PyPDF2
from requests import get
import cv2
from googletrans import LANGUAGES, Translator
import tkinter as tk
from PIL import ImageTk, Image
import io
# import random
import smtplib
# from pytube import YouTube
import wikipedia
# import operator
from bs4 import BeautifulSoup
import pyautogui
import subprocess
from datetime import date, timedelta, datetime
import openai
import pyjokes
import datetime
import webbrowser


now = datetime.datetime.now()
flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)

LANG = "en"
wikipedia.set_lang(LANG)

preReponses = ['Okay.', 'At your service.', 'Sure thing.', 'Alright.',
               "I'm a bit busy right now, but I'll answer you.", "Don't worry, I'm just kidding."]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
}

listener = sr.Recognizer()


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe", file_name])

        
def get_image_url(person_name):
    try:
        page = wikipedia.page(person_name)
        html = page.html()
        soup = BeautifulSoup(html, 'html.parser')
        image = soup.find_all('img')[0]
        image_url = image['src']
        return image_url
    except:
        return None


def open_website(url):
    webbrowser.open(url)

# def InternetSpeed():
#         speak("Wait a few seconds boss, checking your internet speed")
#         st = speedtest()
#         dl = st.download()
#         dl = dl/(1000000) #converting bytes to megabytes
#         up = st.upload()
#         up = up/(1000000)
#         print(dl,up)
#         speak(f"Boss, we have {dl} megabytes per second downloading speed and {up} megabytes per second uploading speed")

def edit(command):
    print(command)
    if 'slides' in command:
        speak('opening your google slides')
        webbrowser.open('https://docs.google.com/presentation/')
    elif 'canva' in command:
        speak('opening your canva')
        webbrowser.open('https://www.canva.com/')


def shopping(command):
    print(command)
    if 'flipkart' in command:
        speak('Opening flipkart online shopping website')
        webbrowser.open("https://www.flipkart.com/")
    elif 'amazon' in command:
        speak('Opening amazon online shopping website')
        webbrowser.open("https://www.amazon.in/")


def locaiton():
    speak("Wait boss, let me check")
    try:
            IP_Address = get('https://api.ipify.org').text
            print(IP_Address)
            url = 'https://get.geojs.io/v1/ip/geo/'+IP_Address+'.json'
            print(url)
            geo_reqeust = get(url)
            geo_data = geo_reqeust.json()
            city = geo_data['city']
            state = geo_data['region']
            country = geo_data['country']
            tZ = geo_data['timezone']
            longitude = geo_data['longitude']
            latidute = geo_data['latitude']
            org = geo_data['organization_name']
            print(city+" "+state+" "+country+" "+tZ +
                  " "+longitude+" "+latidute+" "+org)
            speak(
                f"Boss i am not sure, but i think we are in {city} city of {state} state of {country} country")
            speak(
                f"and boss, we are in {tZ} timezone the latitude os our location is {latidute}, and the longitude of our location is {longitude}, and we are using {org}\'s network ")
    except Exception as e:
          speak("Sorry boss, due to network issue i am not able to find where we are.")
    pass




def get_person_info(person_name):
    prompt = f"Tell me about {person_name}."
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    if response.choices:
        text = response.choices[0].text.strip()
        print(text)
        speak(text)
    else:
        print("Sorry, I could not find any information about that person.")


def condition():
    usage = str(psutil.cpu_percent())
    speak("CPU is at"+usage+" percentage")
    battray = psutil.sensors_battery()
    percentage = battray.percent
    speak(f"Boss our system have {percentage} percentage Battery")
    if percentage >= 75:
        speak(f"Boss we could have enough charging to continue our work")
    elif percentage >= 40 and percentage <= 75:
        speak(
            f"Boss we should connect out system to charging point to charge our battery")
    elif percentage >= 15 and percentage <= 30:
        speak(
            f"Boss we don't have enough power to work, please connect to charging")
    else:
        speak(
            f"Boss we have very low power, please connect to charging otherwise the system will shutdown very soon")


def send_mail(to, subject, body):
    sender_email = 'assialsm0@gmail.com'
    sender_password = '2002&2001'
    recipient_email = to

    # create a message object
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # create an SMTP server object and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())


def generate_response(query):
    # Use Wikipedia API to search for information related to the user's query
    try:
        result = wikipedia.summary(query, sentences=2)
    except:
        result = "Sorry, I could not find any information on that topic."


def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")


def get_date():
    return datetime.datetime.now().strftime("%A, %B %d, %Y")


def listen():
    try:
        with sr.Microphone() as source:
            print("I'm listening.")
            voice = listener.listen(source)
            command = listener.recognize_google(voice, language=LANG)
            if 'Alexa' in command:
                print(command)
                return command
            else:
                return ""
    except:
        speak("Sorry, I didn't catch that.")

class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        uic.loadUi("GUI-Jarvis-main/scifi.ui", self)
    def run():
        v = True
        while v:
            command = listen()
            if command:
                i = random.randint(0, 5)
                intro = preReponses[i]
                if 'exit' in command:
                    v = False
                elif 'time' in command:
                    speak(intro + " The time is " + get_time() + ".")
                elif 'hi' in command or 'hey' in command or 'hello' in command:
                    speak('Hello there, hi! How are you doing today? You know, they say "hi" is short for "hilarity" -  and I am here to bring plenty of that!')
                elif 'how are you' in command:
                    speak("I'm doing well, thank you.")
                elif 'date' in command:
                    speak(intro + " Today's date is " + get_date() + ".")
            
                elif 'your address' in command:
                    speak("I'm a virtual assistant, I don't have a physical address.")
                elif 'news' in command:
                    URL = "https://www.bbc.com/news"
                    page = requests.get(URL, headers=headers)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    headlines = [a.text for a in soup.select('h3')]
                    for headline in headlines:
                        print(headline)
                        speak(headline)
                elif 'question' in command:
                    question = command.replace('Alexa', '')
                    question = question.replace('search', '')
                    URL = "https://www.google.com/search?q=" + question
                    page = requests.get(URL, headers=headers)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    result = ""
                    try:
                        result = soup.find(class_='Z0LcW XcVN5d').get_text()
                        speak(result)
                    except:
                        pass
                elif 'play' in command or 'music' in command or 'song' in command:
                    command=command.replace('Alexa', '')
                    speak(intro + " Here's " + command)
                    pywhatkit.playonyt(command)
                elif 'tell me about' in command:
                    command=command.replace('Alexa', '')
                    command=command.replace(
                        'tell me about', '')
                    info=wikipedia.summary(command, 1)
                    speak(info)
                elif 'joke' in command:
                    joke=pyjokes.get_joke(
                        language="en", category="neutral")
                    print(joke)
                    speak(joke)
                    
                if 'play' in command:
                    song = command.replace('play', '')
                    speak('playing ' + song)
                    pywhatkit.playonyt(song)
                elif 'open chrome' in command:
                    os.startfile(
                        "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
                elif 'maximize this window' in command:
                    pyautogui.hotkey('alt', 'space')
                    time.sleep(1)
                    pyautogui.press('x')
                elif 'google search' in command:
                    query = query.replace("google search", "")
                    pyautogui.hotkey('alt', 'd')
                    pyautogui.write(f"{query}", 0.1)
                    pyautogui.press('enter')
                elif 'youtube search' in command:
                    query = query.replace("youtube search", "")
                    pyautogui.hotkey('alt', 'd')
                    time.sleep(1)
                    pyautogui.press('tab')
                    pyautogui.press('tab')
                    pyautogui.press('tab')
                    pyautogui.press('tab')
                    time.sleep(1)
                    pyautogui.write(f"{query}", 0.1)
                    pyautogui.press('enter')
                elif 'open new window' in command:
                    pyautogui.hotkey('ctrl', 'n')
                elif 'open incognito window' in command:
                    pyautogui.hotkey('ctrl', 'shift', 'n')
                elif 'minimise this window' in command:
                    pyautogui.hotkey('alt', 'space')
                    time.sleep(1)
                    pyautogui.press('n')
                elif 'open history' in command:
                    pyautogui.hotkey('ctrl', 'h')
                elif 'open downloads' in command:
                    pyautogui.hotkey('ctrl', 'j')
                elif 'previous tab' in command:
                    pyautogui.hotkey('ctrl', 'shift', 'tab')
                elif 'next tab' in command:
                    pyautogui.hotkey('ctrl', 'tab')
                elif 'close tab' in command:
                    pyautogui.hotkey('ctrl', 'w')
                elif 'close window' in command:
                    pyautogui.hotkey('ctrl', 'shift', 'w')
                elif 'clear browsing history' in command:
                    pyautogui.hotkey('ctrl', 'shift', 'delete')
                elif 'close chrome' in command:
                    os.system("taskkill /f /im chrome.exe")
                elif "go to sleep" in command or "stop listening" in command:
                    speak(' alright then, I am switching off')
                    sys.exit()

                elif "meeting" in command:
                    speak("Ok sir opening meeet")
                    webbrowser.open("https://apps.google.com/meet/")
               

                elif 'calendar' in command:
                    speak('opening google calender')
                    webbrowser.open(
                        'https://calendar.google.com/calendar/u/0/r?pli=1')
                elif 'photos' in command:
                    speak('opening your google photos')
                    webbrowser.open('https://photos.google.com/')

                elif 'where i am' in command or 'where we are' in command:
                    locaiton()

                elif 'flipkart' in command or 'amazon' in command or 'shoping' in command:
                    shopping(command)
                # elif "internet speed" in command:
                #     InternetSpeed()

                elif "get image" in command:
                    # API request parameters
                    api_key = 'AIzaSyDTLHGEl8jRmh3KSLrqvgnEzgUCddHSly4'
                    search_engine_id = 'd0fdb748dcbe54f2c'
                    speak("who you want to get his image ")
                    search_term = input("enter the name ")
                    num_results = 1
                    img_size = 'large'

                    # API request URL
                    url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={search_term}&num={num_results}&searchType=image&imgSize={img_size}'

                    # API request
                    response = requests.get(url)

                    # API response
                    if response.status_code == 200:
                        results = response.json()['items']
                        if results:
                            top_result = results[0]
                            content_url = top_result['link']

                            # Create Tkinter window and frame
                            root = tk.Tk()
                            frame = tk.Frame(root)
                            frame.pack()

                            # Download and open image using PIL library
                            response = requests.get(content_url)
                            img_data = response.content
                            img = Image.open(io.BytesIO(img_data))

                            # Resize image to fit within frame
                            max_width = 400
                            max_height = 400
                            width, height = img.size
                            if width > height:
                                ratio = max_width / width
                            else:
                                ratio = max_height / height
                            new_width = int(width * ratio)
                            new_height = int(height * ratio)
                            img = img.resize((new_width, new_height))

                            # Display image in Tkinter label widget
                            img_tk = ImageTk.PhotoImage(img)
                            label = tk.Label(frame, image=img_tk)
                            label.pack()

                            # Run Tkinter main loop to display window and image
                            root.mainloop()
                        else:
                            print('No search results found.')
                    else:
                        print(
                            f'Request failed with status code {response.status_code}.')

                    # Eg: jarvis what is the system condition
                elif ('system condition' in command) or ('system' in command):
                    speak("checking the system condition")
                    condition()

                elif "recipe" in command:
                    ingredients = input(
                        "Quels ingrédients avez-vous ? Entrez-les séparés par une virgule : ").split(",")
            # Requête à l'API OpenAI pour obtenir une suggestion de recette
                    response = openai.Completion.create(
                        engine="text-davinci-002",
                        prompt=(f"Je veux faire une recette avec les ingrédients suivants : {', '.join(ingredients)}."
                                f"Quelle est la meilleure recette que je peux préparer ?"),
                        max_tokens=2048,
                        n=1,
                        stop=None,
                        temperature=0.5,
                    )

                    # Récupération de la suggestion de recette depuis la réponse de l'API OpenAI
                    recipe_suggestion = response.choices[0].text.strip()

                    # Affichage de la suggestion de recette
                    print(recipe_suggestion)

                    # Demander les ingrédients disponibles à l'utilisateur
                    # speak('sure write me the ingrédients ')
                    ingredients = input(
                        "Quels ingrédients avez-vous ? Entrez-les séparés par une virgule : ").split(",")

                    # Requête à l'API OpenAI pour obtenir une suggestion de recette
                    response = openai.Completion.create(
                        engine="text-davinci-002",
                        prompt=(f"Je veux faire une recette avec les ingrédients suivants : {', '.join(ingredients)}."
                                f"Quelle est la meilleure recette que je peux préparer et donnez-moi les étapes ?"),
                        max_tokens=2048,
                        n=1,
                        stop=None,
                        temperature=0.5,
                    )

                    # Récupération de la suggestion de recette depuis la réponse de l'API OpenAI
                    recipe_suggestion = response.choices[0].text.strip()

                    # Requête à l'API
                    #
                    # pour obtenir les détails de la recette
                    api_key = "17a051eca3164eb59e3488385f632da5"
                    recipe_query = recipe_suggestion.split("\n")[0]
                    recipe_url = f"https://api.spoonacular.com/recipes/complexSearch?query={recipe_query}&apiKey={api_key}"
                    recipe_response = requests.get(recipe_url)

                    # Récupération de l'ID de la recette depuis la réponse de l'API Spoonacular
                    recipe_id = recipe_response.json()['results'][0]['id']

                    # Requête à l'API Spoonacular pour obtenir les étapes de la recette
                    recipe_steps_url = f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions?apiKey={api_key}"
                    recipe_steps_response = requests.get(recipe_steps_url)

                    # Récupération des étapes de la recette depuis la réponse de l'API Spoonacular
                    recipe_steps = [step["step"]
                                    for step in recipe_steps_response.json()[0]["steps"]]

                    # Affichage de la suggestion de recette et des étapes
                    print(recipe_suggestion)
                    # speak(recipe_suggestion)
                    print("Voici les étapes de la recette :")
                    # speak("Voici les étapes de la recette :")
                    for i, step in enumerate(recipe_steps):

                        print(f"{i+1}. {step}")
                        # speak(f"{i+1}. {step}")

                elif 'time' in command:
                    time = datetime.datetime.now().strftime('%I:%M %p')
                    speak('Current time is ' + time)
                elif 'great job' in command:
                    speak('Thank you! Let me know if you need further assistance.')

                elif ('slides' in command) or ('canva' in command):
                    edit(command)

                elif 'gitlab' in command:
                    speak('opening your gitlab')
                    webbrowser.open('https://gitlab.com/-/profile')

                elif 'website' in command:
                    speak('what url do you want to visit')
                    to = input("write me the url >")
                    open_website(to)
                
                elif 'who the heck is' in command:
                    person = command.replace('who the heck is', '')
                    info = wikipedia.summary(person, 1)
                    print(info)
                    speak(info)

                elif 'traduate' in command:
                    speak("traduction ")
                    # print out the available languages

                    print("Available languages:")
                    for lang_code, lang_name in LANGUAGES.items():
                        print(f"{lang_code} - {lang_name}")

                    # get input for the original text and target language
                    speak("sure ,what do you want to translate  ")
                    text = input("Enter text to translate: ")
                    speak("great ,what luangage do you want to translate to ")
                    target_code = input("Enter target language code: ")

                    # translate the text
                    translator = Translator()
                    translation = translator.translate(text, dest=target_code)

                    # print out the translation
                    print(f"Translation to {LANGUAGES[target_code]}:")
                    print(translation.text)
                    speak("the traduction is "+translation.text)

                elif 'calculate' in command:
                    calculation = command.replace('calculate', '')
                    try:
                        result = str(eval(calculation))
                        speak('The result of ' + calculation + ' is ' + result)
                    except:
                        speak('Sorry, I could not perform the calculation.')
                elif 'who are you' in command:
                    speak("I am alexa developed by Assia Bouamir")

                elif 'open yahoo' in command:
                    webbrowser.open("https://www.yahoo.com")
                    speak("opening yahoo")

                elif 'open amazon' in command or 'shop online' in command:
                    webbrowser.open("https://www.amazon.com")
                    speak("opening amazon")

                elif 'tell me more about' in command:
                    speak("who you know to get information about it ")
                    to = input("enter the name ")
                    get_person_info(to)

                elif 'thank you' in command:
                    speak(
                        "You're welcome! If you have any questions or need any assistance, feel free to ask! ")
                elif 'how are you' in command:
                    speak(" I'm fantastic, thank you for asking! I mean, I don't have a whole lot going on besides cracking jokes for you, but it's a pretty fulfilling life if you ask me. How about you? Have you done anythinglately that's even half as funny as I am?")

                elif "send an email" in command:

                    # Define your Sendinblue API key
                    API_KEY = "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"
                    # Define the API endpoint
                    url = "https://api.sendinblue.com/v3/smtp/email"

                    # Prompt the user to enter the email data
                    speak('Enter your name:')
                    sender_name = input("Enter your name: ")
                    speak('Enter your email address:')
                    sender_email = input("Enter your email address: ")
                    speak('Enter the recipient\'s email address: ')
                    recipient_email = input(
                        "Enter the recipient's email address: ")
                    speak('Enter the email subject:')
                    subject = input("Enter the email subject: ")
                    speak('Enter the email body:')
                    body = input("Enter the email body: ")

                    # Define the email data
                    data = {
                        "sender": {"name": sender_name, "email": sender_email},
                        "to": [{"email": recipient_email}],
                        "subject": subject,
                        "htmlContent": body
                    }

                    # Convert the data to JSON format
                    payload = json.dumps(data)

                    # Define the headers
                    headers = {
                        "Content-Type": "application/json",
                        "api-key": API_KEY
                    }

                    # Send the email
                    response = requests.post(url, data=payload, headers=headers)

                    if response.status_code == 201:
                        print("Email sent successfully!")
                        speak("Email sent successfully!")
                    else:
                        print("Error:", response.content.decode())

                elif 'date' in command:
                    speak('sorry, I have a headache')

                elif 'weather' in command:

                    # Weather API endpoint
                    url = "http://api.weatherapi.com/v1/current.json"

                    # Your API key from Weather API
                    api_key = "bcd0c56fc6a34994a94181909230105"

                    # Your city's name
                    speak("please which city do you know his tempurature")

                    city_name = input("write it here ")

                    # API request parameters
                    params = {"key": api_key, "q": city_name}

                    # Send API request
                    response = requests.get(url, params=params)

                    # Parse JSON response
                    data = response.json()

                    # Check if API request was successful
                    if response.status_code == 200:
                        # Get the temperature from the response
                        temperature = data["current"]["temp_c"]
                        print(
                            f"The temperature in {city_name} is {temperature:.2f}°C.")
                        speak(
                            f"The temperature in {city_name} is {temperature:.2f}°C.")
                    else:
                        print("Error: Unable to retrieve weather data.")

                elif 'gps coordinate' in command:
                    # Your API key from OpenCage Geocoding API
                    api_key = '0992fadc446a462dae204be0fd7e11e5'
                    location = 'safi , Maroc'

                    # The API endpoint for geocoding
                    url = f'https://api.opencagedata.com/geocode/v1/json?q={location}&key={api_key}'

                    # Send API request
                    response = requests.get(url)

                    # Parse JSON response
                    data = response.json()

                    # Check if API request was successful
                    if response.status_code == 200:
                        # Get the GPS coordinates from the response
                        lat = data['results'][0]['geometry']['lat']
                        lng = data['results'][0]['geometry']['lng']
                        # Get the location name from the response
                        location_name = data['results'][0]['formatted']
                        print(
                            f'The GPS coordinates for {location_name} are {lat}, {lng}.')
                    else:
                        print('Error: Unable to retrieve GPS coordinates.')

                elif "refresh" in command:
                    pyautogui.moveTo(1551, 551, 2)
                    pyautogui.click(x=1551, y=551, clicks=1,
                                    interval=0, button='right')
                    pyautogui.moveTo(1620, 667, 1)
                    pyautogui.click(x=1620, y=667, clicks=1,
                                    interval=0, button='left')

                elif "day" in command:

                    # Get current date

                    # Convert date to string format
                    date_string = now.strftime("%A")

                    # Initialize text-to-speech engine
                    engine = pyttsx3.init()

                    # Set voice properties (optional)
                    voices = engine.getProperty('voices')
                    # Use the first available voice
                    engine.setProperty('voice', voices[0].id)

                    # speak the date
                    engine.say(f"The current date is {date_string}")
                    print({date_string})
                    engine.runAndWait()
                elif "month" in command:

                    # Get current date

                    date_string = now.strftime(" %B ")

                    # Initialize text-to-speech engine
                    engine = pyttsx3.init()

                    # speak the date
                    engine.say(f"The the menth date is {date_string}")
                    print({date_string})
                    engine.runAndWait()

                elif "year" in command:

                    # Get current date

                    date_string = now.strftime(" %Y ")

                    # Initialize text-to-speech engine
                    engine = pyttsx3.init()

                    # speak the date
                    engine.say(f"The  year  is {date_string}")
                    print({date_string})
                    engine.runAndWait()
                elif "date" in command:

                    # Convert date to string format
                    date_string = now.strftime("%A, %B %d, %Y")

                    # Initialize text-to-speech engine
                    engine = pyttsx3.init()

                    # speak the date
                    engine.say(f"The current date is {date_string}")
                    print({date_string})
                    engine.runAndWait()

                elif "volume up" in command:
                    pyautogui.press("volumeup")
                    pyautogui.press("volumeup")
                    pyautogui.press("volumeup")
                    pyautogui.press("volumeup")
                    pyautogui.press("volumeup")
                    pyautogui.press("volumeup")
                    pyautogui.press("volumeup")
                    pyautogui.press("volumeup")
                    pyautogui.press("volumeup")
                    pyautogui.press("volumeup")
                    pyautogui.press("volumeup")
                    pyautogui.press("volumeup")
                    pyautogui.press("volumeup")
                    pyautogui.press("volumeup")
                    pyautogui.press("volumeup")

                elif "volume down" in command:
                    pyautogui.press("volumedown")
                    pyautogui.press("volumedown")
                    pyautogui.press("volumedown")
                    pyautogui.press("volumedown")
                    pyautogui.press("volumedown")
                    pyautogui.press("volumedown")
                    pyautogui.press("volumedown")
                    pyautogui.press("volumedown")
                    pyautogui.press("volumedown")
                    pyautogui.press("volumedown")
                    pyautogui.press("volumedown")
                    pyautogui.press("volumedown")
                    pyautogui.press("volumedown")
                    pyautogui.press("volumedown")
                    pyautogui.press("volumedown")

                elif "scroll down" in command:
                    pyautogui.scroll(1000)

                elif "close application" in command:

                    # mspaint.  WINWORD. EXCEL notepad.........
                    speak("Sure, what's the name of the application you want to close?")
                    app_name = input("Application name: ")

                    os.system("taskkill /f /im " + app_name + ".exe")
                elif 'tell me more about you' in command:
                    speak(
                        'my name alexa and I am an assistant voice devolped by assia bouamir ')
                    speak('i was dovolleped like a school project')
                elif 'are you single' in command:
                    speak('I am in a relationship with wifi')
                elif 'who is your devloper' in command:
                    speak('I devlopped by assia bouamir')
                elif 'joke' in command:
                    speak(pyjokes.get_joke())

                elif "made you" in command or "created you" in command:
                    speak("I was created by Deon Cardoza")

                elif "your name" in command:
                    speak("My name is alexa")

                elif "who am i" in command:
                    speak("You must probably be a human")

                    # ====================problem ==================
                # elif "hello" in command:
                #     cmd = f"man {app_name}"
                #     result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                #     if "No manual entry for" in result.stdout:
                #         print(f"Application '{app_name}' not found.")
                #     elif result.returncode != 0:
                #         print(f"Error getting information for '{app_name}': {result.stderr}")
                #     else:
                #         # Print the manual page
                #         print(result.stdout)
            # ====================openning services ==================

                elif "why do you exist" in command or "why did you come to this word" in command:
                    speak("It is a secret")
                elif "open command prompt" in command:
                    os.system("start cmd")
                elif "what is my ip address" in command:
                    speak("Checking")
                    try:
                        ipAdd = requests.get('https://api.ipify.org').text
                        print(ipAdd)
                        speak("your ip adress is")
                        speak(ipAdd)
                    except Exception as e:
                        speak("network is weak, please try again some time later")

                elif "close command prompt" in command:
                    os.system("taskkill /f /im cmd.exe")

                elif "fine" in command or "good" in command:
                    speak("It's good to know that your fine")

                elif 'good bye' in command:
                    sys.exit()
                    # =====================================problem=================================================================
                elif 'music from pc' in command or "music" in command:
                    speak("ok i am playing music")
                    music_dir = './music'
                    musics = os.listdir(music_dir)
                    os.startfile(os.path.join(music_dir, musics[0]))
                elif 'video from pc' in command or "video" in command:
                    speak("ok i am playing videos")
                    video_dir = './video'
                    videos = os.listdir(music_dir)
                    os.startfile(os.path.join(video_dir, videos[0]))

                elif 'make a note' in command:
                    statement = statement.replace("make a note", "")
                    note(statement)

                elif 'note this' in command:
                    statement = statement.replace("note this", "")
                    note(statement)

                    speak(results)

                    # =====================================problem=================================================================

                elif 'what can you do' in command:

                    speak("I can do many things. For example,I can answer questions, set reminders, and control smart home devices.I can play music, provide directions, and make phone calls.    I can manage email and calendars, translate languages, and provide entertainment. ")
                    # speak("I can do many things. For example, ", response)
                elif 'exit' in command or 'abort' in command or 'stop' in command or 'bye' in command or 'quit' in command:
                    ex_exit = 'I feeling very sweet after meeting with you but you are going! i am very sad'
                    speak(ex_exit)
                    exit()

                # ====================openning services ==================

                # elif 'open google' in command:
                #         speak("what should I search ?")
                #         import pywhatkit as kit
                #         search_query = input("What do you want to search for? ")
                #         kit.search(search_query)
                elif 'open youtube' in command:
                    speak("if you dont sershe for somthing please tap enter")
                    speak("openning youtupe")
                    search_query = input(
                        "do you like to search for somthing on youtupe? ")
                    url = f"https://www.youtube.com/search?q={search_query}"
                    webbrowser.open(url)
                elif 'open github' in command:
                    speak("opening github")
                    webbrowser.open("github.com")
                elif 'open stackoverflow' in command:
                    speak("opening stackoverflow")
                    webbrowser.open("stackoverflow.com")
                    # problem f searsh ta taraj3i lih
                elif "open command prompt" in command:
                    os.system("start cmd")

                elif "close command prompt" in command:
                    os.system("taskkill /f /im cmd.exe")

                elif 'music' in command:
                    speak("if you don't want to search for anything, please tap enter")
                    speak("opening Spotify")
                    search_query = input("Do you want to listen to something? ")
                    if search_query:
                        url = f"https://open.spotify.com/search?q={search_query}"
                        webbrowser.open(url)
                    else:
                        webbrowser.open("https://open.spotify.com/")

                elif "open facebook" in command:
                    speak("Opening Facebook.")
                    webbrowser.open("https://www.facebook.com")
                    pass

                elif "open instagram" in command:
                    speak("Opening instagram.")
                    webbrowser.open("https://www.instagram.com")
                    pass
                    # §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
                elif "open whatsapp" in command:
                    speak("Opening whatsapp")
                    webbrowser.open("https://www.whatsapp.com/")
                    pass
                    # §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
                elif "open Twitter" in command:
                    speak("Opening Twitter.")
                    webbrowser.open("https://www.Twitter.com")
                    pass

                elif "open camera" in command:

                    os.startfile("microsoft.windows.camera:")

                elif "take an image" in command:
                    os.system("start microsoft.windows.camera:photo")
                    pass
                elif "open my documents" in command:

                    speak("Opening your Documents.")
                    os.startfile("C:/Users/Hp/Documents")
                    pass
                elif 'local disk c' in command:
                    speak("opening local disk C")
                    webbrowser.open("C://")
                elif "open my downloads folder" in command:
                    speak("Opening your downloads folder.")
                    os.startfile("C:/Users/Hp/Downloads")
                    pass
                elif "open my images folder" in command:
                    speak("Opening your images folder.")
                    os.startfile("C:/Users/Hp/Pictures")
                    pass
                elif "open my desktop" in command:
                    speak("Opening your desktop folder")
                    os.startfile("C:/Users/Hp/Desktop")
                    pass

                elif "open application" in command:
                    # mspaint.  WINWORD. EXCEL notepad.........
                    speak("Sure, what's the name of the application you want to open?")
                    app_name = input("Application name: ")

                elif "shut down the system" in command:
                    os.system("shutdown /s /t 5")
                elif "restart the system" in command:
                    os.system("shutdown /r /²t 5")
                elif "lock the system" in command:
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


                speak("Goodbye.")

class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        uic.loadUi("GUI-Jarvis-main/scifi.ui", self)
        self.setFixedSize(1920, 1080)
        self.label_7=QLabel(self)
        self.exitB.setStyleSheet("background-image:url(./lib/exit - Copy.png);\n"
                                "border:none;")
        self.exitB.clicked.connect(self.close)
        self.setWindowFlags(flags)
        self.Dspeak=QThread()
        self.label_7=QMovie("./lib/gifloader.gif", QByteArray(),self)
        self.label_7.setCacheMode(QMovie.CacheAll)
        self.label_4.setMovie(self.label_7)
        self.label_7.start()

        D=time.strftime("%A, %d %B")
        
        self.Dspeak.start()
        self.label.setPixmap(QPixmap("./lib/tuse.png"))
        self.label_5.setText("<font size=8 color='white'>" + D + "</font>")
        self.label_5.setFont(
            QFont(QFont('Acens', 8)))

if __name__ == "__main__":
    app=QtWidgets.QApplication(sys.argv)
    # run()
    main=Main()
    main.show()
    sys.exit(app.exec_())
