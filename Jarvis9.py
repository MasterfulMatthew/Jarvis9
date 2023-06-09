'''
Coded by Masterful Matthew
Jarvis 9
9/6/2023
'''

import openai, pyttsx3, datetime, requests
import speech_recognition as sr
from wakepy import set_keepawake
from datetime import timedelta

openai.api_key = "YOUR-OPENAI-KEY"

#sets up the voice
engine = pyttsx3.init()
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[1].id)
engine.setProperty('voice', 'en-us')
engine.setProperty('rate', 170)

#sets up weather stuff
weather_key = "YOUR-OPENWEATHERMAP-KEY"
base_url = "http://api.openweathermap.org/data/2.5/"
latitude = "YOUR-LATITUDE"
longitude = "YOUR-LONGITUDE"
weather_url = base_url + "weather?" + "appid=" + weather_key + "&lat=" + latitude + "&lon=" + longitude + "&units=metric"
forecast_url = base_url + "forecast?" + "appid=" + weather_key + "&lat=" + latitude + "&lon=" + longitude

#converts speech to text
def transcribe_audio_to_text(filename):
    #print("transcribing") #for debugging
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping unknown error")
        return None

#generates response
def generate_response(prompt):
    chatgpt_response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 4000,
        n = 1,
        stop = None,
        temperature = 1,
    )
    return chatgpt_response["choices"][0]["text"]

#says everthing in "text"
def speak_text(text):
    engine.say(text)
    engine.runAndWait()
    
def main():
    set_keepawake(keep_screen_awake = False) #(supposedly) keeps microphone awake
    #sets up microphone
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    #n = 0 #sets up listening counter
    
    while True:
        #initializes the microphone to start listening
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            #n=n+1 #adds one to listening counter every time it listens
            #print("listening" + str(n))
            audio = recognizer.listen(source, phrase_time_limit = 3, timeout = None)
            #print("done listening") #for debugging
            
            try:
                #print("trying") #for debugging
                transcription = recognizer.recognize_google(audio)
                #print(transcription) #prints transcription
                if transcription.lower() == "hey jarvis" or transcription.lower() == "jarvis": #the activation call is "hey Jarvis" or "Jarvis"
                    filename = "input.wav" #creates a file to store what you say
                    print("Greetings sir.") #prints out a greeting, meaning it's ready to listen to you
                    engine.say("Greetings sir") #says "Greetings sir."
                    engine.runAndWait()
                    #print("getting audio") #for debugging
                    #initializes the microphone to listen to your question
                    audio2 = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                    filename = "input.wav"
                    with open(filename, "wb") as f:
                        f.write(audio2.get_wav_data())
                    
                    time = datetime.datetime.now() #gets the current time
                    text = transcribe_audio_to_text(filename) #stores transcription
                    if text == "are you there":
                        print("For you, always sir.")
                        engine.say("for you. always sir")
                        engine.runAndWait()
                        
                    elif text == "what day is it today" or text == "what day is it" or text == "what's the date today":
                        print(f"You said: {text}")
                        print("Today is " + time.strftime("%A, %d %B %Y"))
                        engine.say("today is " + time.strftime("%A, %B %d %Y"))
                        engine.runAndWait()
                        
                    elif text == "what time is it" or text == "what's the time" or text == "what's the time right now":
                        print(f"You said: {text}")
                        print("The time is " + time.strftime("%I:%M %p"))
                        #removes leading 0 from hour number, so that it says the time properly
                        I = str(int(time.strftime("%I")))
                        if time.strftime("%M") == "00":
                            engine.say("the time is " + I + time.strftime("%p"))
                            engine.runAndWait()
                        else:
                            engine.say("the time is " + I + time.strftime("%M %p"))
                            engine.runAndWait()
                            
                        #morning milk reminder
                        today930am = time.replace(hour=9, minute=30, second=0, microsecond=0)
                        today10am = time.replace(hour=10, minute=0, second=0, microsecond=0)
                        #afternoon milk reminder
                        today230pm = time.replace(hour=14, minute=30, second=0, microsecond=0)
                        today3pm = time.replace(hour=15, minute=0, second=0, microsecond=0)
                        #evening milk reminder
                        today430pm = time.replace(hour=16, minute=30, second=0, microsecond=0)
                        today5pm = time.replace(hour=17, minute=0, second=0, microsecond=0)
                        #bedtime reminder
                        today930pm = time.replace(hour=21, minute=30, second=0, microsecond=0)
                        today10pm = time.replace(hour=22, minute=0, second=0, microsecond=0)
                        
                        if time > today930am and time < today10am:
                            print("You should have your morning milk soon.")
                            engine.say("you should have your morning milk soon")
                            engine.runAndWait()
                            
                        elif time > today230pm and time < today3pm:
                            print("You should have your afternoon milk soon.")
                            engine.say("you should have your afternoon milk soon")
                            engine.runAndWait()
                            
                        elif time > today430pm and time < today5pm:
                            print("You should have your evening milk soon.")
                            engine.say("you should have your evening milk soon")
                            engine.runAndWait()
                            
                        elif time > today930pm and time < today10pm:
                            print("You should consider going to bed soon.")
                            engine.say("you should consider going to bed soon")
                            engine.runAndWait()
                        
                    elif text == "what's the weather" or text == "what's the weather right now":
                        weather_response = requests.get(weather_url)
                        weather_response_json = weather_response.json()
                        weather = weather_response_json["weather"]
                        weather_description = weather[0]["description"]
                        print(f"You said: {text}")
                        print(str(weather_description).capitalize() + ".")
                        engine.say(str(weather_description))
                        engine.runAndWait()
                        
                    elif text == "what's the temperature" or text == "what's the temperature right now":
                        temperature_response = requests.get(weather_url)
                        temperature_response_json = temperature_response.json()["main"]
                        temperature = round(temperature_response_json["temp"])
                        print(f"You said: {text}")
                        print("The temperature is " + str(temperature) + "°C.")
                        engine.say("the temperature is " + str(temperature) + "degrees celsius")
                        engine.runAndWait()
                        
                    elif text == "what's the forecast":
                        target_time = datetime.datetime.now() + timedelta(hours=2) #sets the time for the forecast reading Fto two hours from now
                        target_time_unix = int(target_time.timestamp())
                        forecast_response = requests.get(forecast_url)
                        forecast_data = forecast_response.json()

                        if forecast_response.status_code == 200: #code 200 means it's working
                            forecasts = forecast_data["list"]
                            forecast_found = False
                            
                            for forecast in forecasts:
                                forecast_time_unix = forecast["dt"]
                                
                                if forecast_time_unix > target_time_unix:
                                    forecast_found = True
                                    forecast_description = forecast["weather"][0]["description"]
                            
                            if forecast_found:
                                print(f"There will be {forecast_description} in 2 hours.")
                                engine.say(f"there will be {forecast_description}) in two hours")
                                engine.runAndWait()
                            else:
                                print("Weather information for the next 2 hours not found.")
                                engine.say("weather information for the next 2 hours not found")
                                engine.runAndWait()
                        else:
                            print(f"Error: {forecast_response.status_code}")
                        
                    else:
                        print(f"You said: {text}")               
                        chatgpt_response = generate_response(text)
                        if len(chatgpt_response) < 4000: #max response length is 4000 characters
                            print(chatgpt_response) #prints the response
                            speak_text(chatgpt_response) #speaks the response
                            
                        #if the response is too long, it won't print or say it
                        else:
                            print("The response was too long.")
                            engine.say("The response was too long.")
                            engine.runAndWait()
                        
            except Exception as e:
                pass
                    
if __name__ == "__main__":
    main()