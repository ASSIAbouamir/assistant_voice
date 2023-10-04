
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import speech_recognition as sr
import os
import time
import psutil
import requests
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import speech_recognition as sr
import pyttsx3
import pywhatkit
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

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning sir, How can I help you")
    elif hour >= 12 and hour < 18:
        speak("Good evening sir, How can I help you")
    else:
        speak("Good aftrnoon sir, How can I help you")


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe", file_name])

        
# def get_image_url(person_name):
#     try:
#         page = wikipedia.page(person_name)
#         html = page.html()
#         soup = BeautifulSoup(html, 'html.parser')
#         image = soup.find_all('img')[0]
#         image_url = image['src']
#         return image_url
#     except:
#         return None


def open_website(url):
    webbrowser.open(url)

def edit(command):
    print(command)
    if 'slide' in command:
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
            print(city+" "+state+" "+country+" "+tZ +" "+longitude+" "+latidute+" "+org)
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
    sender_password = 'Assia2002&2001'
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
        # we use sentencec detemine le nombre de phrase dans le resulta 
    except:
        
        result = "Sorry, I could not find any information on that topic."



class mainT(QThread):
    def __init__(self):
        super(mainT, self).__init__()

    def run(self):
        self.JARVIS()

    def STT(self):
        R = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listning...........")
            audio = R.listen(source)
        try:
            print("Recog......")
            text = R.recognize_google(audio, language='en-in')
            print(">> ", text)
        except Exception:
            speak("Sorry Speak Again")
            return "None"
        text = text.lower()
        return text

   
    def JARVIS(self):
        wish()
        while True:
            self.query = self.STT()
            if 'hi' in self.query or 'hey' in self.query or 'hello' in self.query:
                speak('Hello there, hi! How are you doing today? You know, they say "hi" is short for "hilarity" -  and I am here to bring plenty of that!')
            elif 'good bye' in self.query:
                sys.exit()
            elif 'thank you' in self.query:
                speak(
                    "You're welcome! If you have any questions or need any assistance, feel free to ask! ")
            elif 'how are you' in self.query:
                speak(" I'm fantastic, thank you for asking! I mean, I don't have a whole lot going on besides cracking jokes for you, but it's a pretty fulfilling life if you ask me. How about you? Have you done anythinglately that's even half as funny as I am?")

            elif 'about you' in self.query:
                speak('my name alexa and I am an assistant voice devolped by assia bouamir ')
                speak('i was dovolleped like a school project')
            elif 'are you single' in self.query:
                speak('I am in a relationship with wifi')
            elif 'created you' in self.query:
                speak('I devlopped by assia bouamir')
            elif 'joke' in self.query:
                speak(pyjokes.get_joke())
     
            elif "your name" in self.query:
                speak("My name is alexa") 

            elif "am i" in self.query:
                speak("You must probably be a human") 
             # ====================short conversation ==================

            if 'play' in self.query:
                song = self.query.replace('play', '')
                speak('playing ' + song)
                pywhatkit.playonyt(song)
            elif 'open chrome' in self.query:
                os.startfile(
                    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
            elif 'maximize this window' in self.query:
                pyautogui.hotkey('alt', 'space')
                time.sleep(1)
                pyautogui.press('x')
            elif 'google search' in self.query:
                query = query.replace("google search", "")
                pyautogui.hotkey('alt', 'd')
                pyautogui.write(f"{query}", 0.1)
                pyautogui.press('enter')
            elif 'youtube search' in self.query:
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
            elif 'open new window' in self.query:
                pyautogui.hotkey('ctrl', 'n')
            elif 'open incognito window' in self.query:
                pyautogui.hotkey('ctrl', 'shift', 'n')
            elif 'minimise this window' in self.query:
                pyautogui.hotkey('alt', 'space')
                time.sleep(1)
                pyautogui.press('n')
            elif 'open history' in self.query:
                pyautogui.hotkey('ctrl', 'h')
            elif 'open downloads' in self.query:
                pyautogui.hotkey('ctrl', 'j')
            elif 'previous tab' in self.query:
                pyautogui.hotkey('ctrl', 'shift', 'tab')
            elif 'next tab' in self.query:
                pyautogui.hotkey('ctrl', 'tab')
            elif 'close tab' in self.query:
                pyautogui.hotkey('ctrl', 'w')
            elif 'close window' in self.query:
                pyautogui.hotkey('ctrl', 'shift', 'w')
            elif 'clear browsing history' in self.query:
                pyautogui.hotkey('ctrl', 'shift', 'delete')
            elif 'close chrome' in self.query:
                os.system("taskkill /f /im chrome.exe")
            elif "go to sleep" in self.query or "stop listening" in self.query:
                speak(' alright then, I am switching off')
                sys.exit()
                
            elif "meeting" in self.query:
                speak("Ok sir opening meeet")
                webbrowser.open("https://apps.google.com/meet/")
            # elif ('tell me news' in self.query) or ("news" in self.query) or ("todays news" in self.query):
            #    speak("Ok sir opening meeet")
            #    headers = {
            #        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
            #    }
            #    URL = "https://www.bbc.com/news"
            #    page = requests.get(URL, headers=headers)
            #    soup = BeautifulSoup(page.content, 'html.parser')
            #    l = [a.text for a in soup.select('div li a h3')]
            #    for a in l:
            #        print(a)
            #        speak(a)
                
            elif 'calendar' in self.query:
                speak('opening google calender')
                webbrowser.open('https://calendar.google.com/calendar/u/0/r?pli=1')
            elif 'photos' in self.query:
                speak('opening your google photos')
                webbrowser.open('https://photos.google.com/')
                
            elif 'where i am' in self.query or 'where we are' in self.query:
                    locaiton()
                    
            elif 'flipkart'in self.query or 'amazon'in self.query or 'shoping'in self.query :
                        shopping(self.query)
            # elif "internet speed" in self.query:
            #     InternetSpeed()
# ==============
            elif 'image' in self.query :
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
                    print(f'Request failed with status code {response.status_code}.')

                # Eg: jarvis what is the system condition
            elif ('system condition' in self.query) or ('system' in self.query):
                speak("checking the system condition")
                condition()

            elif "recipe" in self.query :
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
                    speak(f"{i+1}. {step}")


            elif 'time' in self.query:
                time = datetime.datetime.now().strftime('%I:%M %p')
                speak('Current time is ' + time)
            elif 'great job' in self.query:   
                speak('Thank you! Let me know if you need further assistance.')
                
            elif ('slide' in self.query) or ('canva' in self.query):
                edit(self.query)
                
            
            elif 'gitlab' in self.query:
                    speak('opening your gitlab')
                    webbrowser.open('https://gitlab.com/-/profile')
                
            elif 'website' in self.query:
                speak('what url do you want to visit')
                to = input("write me the url >")
                open_website(to)
            
            elif 'who the heck is' in self.query:
                person = self.query.replace('who the heck is', '')
                info = wikipedia.summary(person, 1)
                print(info)
                speak(info)
                
            elif 'traduate' in self.query:
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

            elif 'calculate' in self.query:
                calculation = self.query.replace('calculate', '')
                try:
                    result = str(eval(calculation))
                    speak('The result of ' + calculation + ' is ' + result)
                except:
                    speak('Sorry, I could not perform the calculation.')
            elif 'who are you' in self.query:
                speak("I am alexa developed by Assia Bouamir")
                
            elif 'open yahoo' in self.query:
                webbrowser.open("https://www.yahoo.com")
                speak("opening yahoo")
                
            elif 'open amazon' in self.query or 'shop online' in self.query:
                webbrowser.open("https://www.amazon.com")
                speak("opening amazon")
            
            elif 'tell me more about' in self.query:
                speak("who you know to get information about it ")
                to = input("enter the name ")
                get_person_info(to)
                
                
                
                
                
            
            
            elif "send an email" in self.query:

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
                recipient_email = input("Enter the recipient's email address: ")
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


            elif 'date' in self.query:
                speak('sorry, I have a headache')
                
            elif 'weather' in self.query:

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
                    print(f"The temperature in {city_name} is {temperature:.2f}°C.")
                    speak(f"The temperature in {city_name} is {temperature:.2f}°C.")
                else:
                    print("Error: Unable to retrieve weather data.")

            elif 'gps coordinate' in self.query:
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
                    speak(f'The GPS coordinates for {location_name} are {lat}, {lng}.')
                else:
                    speak('Error: Unable to retrieve GPS coordinates.')


                
            elif "refresh" in self.query:
                pyautogui.moveTo(1551,551, 2)
                pyautogui.click(x=1551, y=551, clicks=1, interval=0, button='right')
                pyautogui.moveTo(1620,667, 1)
                pyautogui.click(x=1620, y=667, clicks=1, interval=0, button='left')
                
            elif "day" in self.query:

                    # Get current date
                

                # Convert date to string format
                date_string = now.strftime("%A")

                # Initialize text-to-speech engine
                engine = pyttsx3.init()

                # Set voice properties (optional)
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[0].id)  # Use the first available voice

                # speak the date
                engine.say(f"The current date is {date_string}")
                print({date_string})
                engine.runAndWait()
            elif "month" in self.query:

                # Get current date
            
                date_string = now.strftime(" %B ")


                # Initialize text-to-speech engine
                engine = pyttsx3.init()

                # speak the date
                engine.say(f"The the menth date is {date_string}")
                print({date_string})
                engine.runAndWait()
            
            elif "year" in self.query:
            
                # Get current date
            
                date_string = now.strftime(" %Y ")


                # Initialize text-to-speech engine
                engine = pyttsx3.init()

            
                # speak the date
                engine.say(f"The  year  is {date_string}")
                print({date_string})
                engine.runAndWait()
            elif "date" in self.query:
                
                        # Convert date to string format
                date_string = now.strftime("%A, %B %d, %Y")

                # Initialize text-to-speech engine
                engine = pyttsx3.init()

                # speak the date
                engine.say(f"The current date is {date_string}")
                print({date_string})
                engine.runAndWait()

            elif "volume up" in self.query:
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

            elif "volume down" in self.query:
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
                        

            elif "scroll down" in self.query:
                pyautogui.scroll(100)

                        
            elif "close application" in self.query:
            
                    # mspaint.  WINWORD. EXCEL notepad.........
                    speak("Sure, what's the name of the application you want to close?")
                    app_name = input("Application name: ")

                    os.system("taskkill /f /im " + app_name + ".exe")
            
            
            
                # ====================problem ==================
            # elif "hello" in self.query:
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
            
            elif "existe" in self.query or "why did you come to this word" in self.query:
                speak("It is a secret") 
            elif "open cmd" in self.query:
                os.system("start cmd")
            elif "what is my ip address" in self.query:
                speak("Checking")
                try:
                    ipAdd = requests.get('https://api.ipify.org').text
                    print(ipAdd)
                    speak("your ip adress is")
                    speak(ipAdd)
                except Exception as e:
                    speak("network is weak, please try again some time later")

            elif "close cmd" in self.query:
                os.system("taskkill /f /im cmd.exe")

            elif "fine" in self.query or "good" in self.query:
                speak("It's good to know that your fine") 

            elif 'good bye' in self.query:
                sys.exit()
                # =====================================problem=================================================================
            elif 'music from pc' in  self.query or "music" in  self.query:
                speak("ok i am playing music")
                music_dir = './music'
                musics = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir,musics[0]))
            elif 'video from pc' in  self.query or "video"  in self.query:
                speak("ok i am playing videos")
                video_dir = './video'
                videos = os.listdir(music_dir)
                os.startfile(os.path.join(video_dir,videos[0])) 
                

                    
            elif 'note' in self.query:
                statement = statement.replace("make a note", "")
                note(statement)
                
            elif 'note this' in self.query:
                statement = statement.replace("note this", "")
                note(statement)

                speak(results)

                # =====================================problem=================================================================

            elif 'what can you do' in self.query:

                speak("I can do many things. For example,I can answer questions, set reminders, and control smart home devices.I can play music, provide directions, and make phone calls.    I can manage email and calendars, translate languages, and provide entertainment. ")
                # speak("I can do many things. For example, ", response)
            elif 'exit' in  self.query or 'abort' in  self.query or 'stop'  in self.query or 'bye' in  self.query or 'quit'  in self.query :
                ex_exit = 'I feeling very sweet after meeting with you but you are going! i am very sad'
                speak(ex_exit)
                exit()  

            
            # ====================openning services ==================
            
            # elif 'open google' in self.query:
            #         speak("what should I search ?")
            #         import pywhatkit as kit
            #         search_query = input("What do you want to search for? ")        
            #         kit.search(search_query)
            elif 'open youtube' in self.query:
                speak("if you dont sershe for somthing please tap enter")
                speak("openning youtupe")
                search_query = input("do you like to search for somthing on youtupe? ")
                url = f"https://www.youtube.com/search?q={search_query}"
                webbrowser.open(url)
            elif 'github' in self.query:
                    speak("opening github")
                    webbrowser.open("github.com")
            elif 'open stack overflow' in self.query:
                    speak("opening stackoverflow")
                    webbrowser.open("stackoverflow.com")
                # problem f searsh ta taraj3i lih 
     
            elif 'music' in self.query:
                speak("if you don't want to search for anything, please tap enter")
                speak("opening Spotify")
                search_query = input("Do you want to listen to something? ")
                if search_query:
                    url = f"https://open.spotify.com/search?q={search_query}"
                    webbrowser.open(url)
                else:
                    webbrowser.open("https://open.spotify.com/")
                    
            elif "open facebook" in self.query:
                    speak("Opening Facebook.")
                    webbrowser.open("https://www.facebook.com")
                    pass

            elif "open instagram" in self.query:
                    speak("Opening instagram.")
                    webbrowser.open("https://www.instagram.com")
                    pass
                # §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
            elif "open whatsapp" in self.query:
                speak("Opening whatsapp")
                webbrowser.open("https://www.whatsapp.com/")
                pass
                # §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
            elif "open Twitter" in self.query:
                speak("Opening Twitter.")
                webbrowser.open("https://www.Twitter.com")
                pass
            
            elif "open caméra" in self.query:
            
                os.startfile("microsoft.windows.camera:")
            
            elif "take an image" in self.query:
                os.system("start microsoft.windows.camera:photo")
                pass
            elif "open my documents" in self.query:
                
                    speak("Opening your Documents.")
                    os.startfile("C:/Users/Hp/Documents")
                    pass
            elif 'local disk c' in self.query:
                speak("opening local disk C")
                webbrowser.open("C://")
            elif "open my download folder" in self.query:
                    speak("Opening your downloads folder.")
                    os.startfile("C:/Users/Hp/Downloads")
                    pass
            elif "open my image folder" in self.query:
                speak("Opening your images folder.")
                os.startfile("C:/Users/Hp/Pictures")
                pass
            elif "open my desktop" in self.query:
                speak("Opening your desktop folder")
                os.startfile("C:/Users/Hp/Desktop")
                pass

            elif "open application" in self.query:
                # mspaint.  WINWORD. EXCEL notepad.........
                    speak("Sure, what's the name of the application you want to open?")
                    app_name = input("Application name: ")

            elif "shut down the system" in self.query:
                os.system("shutdown /s /t 5")
            elif "restart the system" in self.query:
                os.system("shutdown /r /²t 5")
            elif "lock the system" in self.query:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            



FROM_MAIN, _ = loadUiType(os.path.join(
    os.path.dirname(__file__), "./scifi.ui"))


class Main(QMainWindow, FROM_MAIN):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(1920, 1080)
        self.label_7 = QLabel
        self.exitB.setStyleSheet("background-image:url(./lib/exit - Copy.png);\n"
                                 "border:none;")
        self.exitB.clicked.connect(self.close)
        self.setWindowFlags(flags)
        Dspeak = mainT()
        self.label_7 = QMovie("./lib/gifloader.gif", QByteArray(), self)
        self.label_7.setCacheMode(QMovie.CacheAll)
        self.label_4.setMovie(self.label_7)
        self.label_7.start()

        self.D = time.strftime("%A, %d %B")

        Dspeak.start()
        self.label.setPixmap(QPixmap("./lib/tuse.png"))
        self.label_5.setText("<font size=8 color='white'>"+self.D+"</font>")
        self.label_5.setFont(QFont(QFont('Acens', 8)))


app = QtWidgets.QApplication(sys.argv)
main = Main()
main.show()
exit(app.exec_())

