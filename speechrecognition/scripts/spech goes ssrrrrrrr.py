import speech_recognition as sr
from gtts import gTTS
import os, datetime, sys, Main
from playsound import playsound
from time import sleep

spotify1 = Main.spotify()

#changes directory:
os.chdir(os.path.dirname(sys.argv[0]))

#Time:
currentDT = datetime.datetime.now()

#speech recognition:
r = sr.Recognizer()

def voice(text):
    try:
        os.remove("speech.mp3")
    except:
        pass
    tts = gTTS(text=text, lang='en-uk')
    tts.save("speech.mp3")
    #os.system("speech.mp3")
    playsound("speech.mp3")

def say_someting():
    with sr.Microphone() as source:
        print(">")
        audio = r.listen(source)

    try:
        said_word = r.recognize_google(audio, language = 'en-uk').lower()
    except:
        said_word = ""
    print(said_word)

    if "*" in said_word:
        voice("Fuck you! you lifeless, worthless piece of shit, I hope you die in a garbage fire so that you'll feel at home when you die! Fuck you!")

    elif "start" == said_word.split(' ', 1)[0]:
        Main.start(said_word)

    elif "google" == said_word.split(' ', 1)[0]:
        Main.google(said_word)

    elif "close" == said_word.split(' ', 1)[0]:
        Main.close(said_word)

    #spotify
    elif "play" in said_word and "on spotify" in said_word:
        spotify1.play(said_word)
    elif "add " in said_word and "to queue" in said_word:
        spotify1.AddToQueue(said_word)
    elif "pause" in said_word:
        spotify1.pause()
    elif "continue" in said_word or "resume" in said_word:
        spotify1.unpause()
    elif "what " in said_word and "song" in said_word:
        spotify1.whatsong()
    elif "set the volume to" in said_word:
        spotify1.setVolume(said_word)
    elif "raise volume by" in said_word:
        spotify1.raiseVolume(said_word)
    elif "lower volume by" in said_word:
        spotify1.lowerVolume(said_word)
    elif "what is the current volume" in said_word:
        spotify1.whatVolume()

    elif "weather" in said_word:
        Main.weather()

    elif "hello" in said_word:
        voice('hello')

    elif said_word == "what's your name" or said_word == "what is your name":
        voice('My name is Alice')

    elif "what time is it" == said_word:
        voice(str(currentDT.hour) + " " + str(currentDT.minute))

    elif "goodbye" in said_word:
        voice("Goodbye")
        pass

    elif "thank you" in said_word:
        voice("you're welcome")

    else:
        voice("i don't understand what that means")

    say_someting()

#if __name__ == "__main__":
while True:
    with sr.Microphone() as source:
        print(">>")
        audio = r.listen(source)
    try:
        sw = r.recognize_google(audio, language = 'en-uk')
        print(sw)
        if sw == "hey Alice":
            playsound("blibloo.mp3")
            say_someting()
    except:
        pass