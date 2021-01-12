import speech_recognition as sr
from gtts import gTTS
import os, datetime, selenium, spotipy, sys, requests, json, socket, random
import spotipy.util as util
import spotipy.oauth2 as oauth2
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
CITY = "Stockholm"
API_KEY = "a7e242e798fa74a49eda5ccdc6a659d3"

os.chdir(os.path.dirname(sys.argv[0]))

socket.getaddrinfo('localhost', 8080)

username = 'Noah Schiff'
scope = 'user-read-private user-read-playback-state user-modify-playback-state'
client_id = 'e75a4514376c4d72b1c10baee050efa1'
client_secret = '0149e43848024dcdadfedbb7bff59d38'
redirect_uri = 'https://www.google.com'

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

currentDT = datetime.datetime.now()

r = sr.Recognizer()

def convertms(ms):
    m = int(ms/60000)
    s = int(round((ms-(m*60000))/1000))

    if s < 10:
        return f"{m}:0{s}"
    else:
        return f"{m}:{s}"

def voice(text):
    try:
        os.remove("speech.mp3")
    except:
        pass
    tts = gTTS(text=text, lang='en-uk')
    tts.save("speech.mp3")
    #os.system("speech.mp3")
    playsound("speech.mp3")

def slicer(my_str,sub,ba="b"):
   index=my_str.find(sub)
   if index !=-1 and ba=="b":
       return my_str[index:] 
   elif index !=-1 and ba=="a":
       return my_str[:index] 
   else:
       raise Exception('Sub string not found!')

def extension(star, task):
    exe = star.replace(". ", ".")
    bxe = exe.split(task + " ",1)[1]
    if ".lmk" in bxe:
        bxe = bxe.replace("lmk", "lnk")
    return bxe

def weather():
    URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()

        main = data['main']
        temp = main['temp']
        report = data['weather']

        temp = int(round(float(temp)*100) - 27315)
        temp = str(int(round(temp / 100)))

        voice(f"It's {temp} degrees celsius")
        voice(f"And {report[0]['description']}")
    else:
        voice("Error in the HTTP request")

def google(word):
    googleword = word.split("google ",1)[1]
    voice("googling " + googleword)
    driver = webdriver.Chrome("D:\chromedriver\chromedriver")
    driver.get("https://www.google.com/")
    search = driver.find_element_by_name("q")
    search.send_keys(googleword)
    search.submit()

def start(program):
    os.chdir("C:/Users/Noah/Desktop")
    start_word = extension(program, "start")
    voice("starting " + start_word)
    matching_files = [f for f in os.listdir() if start_word in f]
    if len(matching_files) > 0:
        os.startfile(start_word, 'open')
    else:
        voice("I couldn't find %s" % start_word)
    os.chdir(os.path.dirname(sys.argv[0]))
    
def close(program):
    closeword = extension(program, "close")
    voice("closing " + closeword)
    if closeword == "chrome driver":
        try:
            driver.close()
        except:
            pass
    else:
        os.system("TASKKILL /F /IM %s" % closeword)

class spotify():
    def __init__(self):
        self.token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
        self.spotifyMain = spotipy.Spotify(auth=self.token)
        self.devices = self.spotifyMain.devices()
        self.deviceID = self.devices['devices'][0]['id']
    
    def play(self, song):
        self.song = song.replace("play ", "")
        self.song = self.song.replace(" on spotify", "")
        voice("playing " + self.song + "on spotify")
        self.song = self.song.replace(" ", "+")

        self.SongToPlay = self.spotifyMain.search(self.song, type="track", market="se", limit=1)
        self.SongToPlay = slicer(str(self.SongToPlay), "spotify:track:")
        self.SongToPlay = slicer(self.SongToPlay, "'", "a")

        self.spotifyMain.add_to_queue(self.SongToPlay, self.deviceID);self.spotifyMain.next_track(self.deviceID)

    def AddToQueue(self, song):
        self.song = song.replace(" ", "+")

        self.SongToPlay = self.spotifyMain.search(self.song, type="track", market="se", limit=1)
        self.SongToPlay = slicer(str(self.SongToPlay), "spotify:track:")
        self.SongToPlay = slicer(self.SongToPlay, "'", "a")

        self.spotifyMain.add_to_queue(self.SongToPlay, self.deviceID)

    def nextTrack(self):
        self.spotifyMain.next_track(self.deviceID)
    def previousTrack(self):
        self.spotifyMain.previous_track(self.deviceID)
    
    def pause(self):
        self.spotifyMain.pause_playback()

    def unpause(self):
        self.spotifyMain.start_playback()
        
    def whatsong(self):
        self.currentSong = self.spotifyMain.currently_playing()
        return(self.currentSong['item']['name'])

    def whatartist(self):
        return(self.currentSong['item']['artists'][0]['name'])

    def isPaused(self):
        self.ispaused = self.spotifyMain.currently_playing()
        try:return(self.ispaused['is_playing'])
        except TypeError: return None

    def setVolume(self, volume):
        self.volume = volume.replace("set the volume to ", "")
        try:self.volume = slicer(volume, " ", ba="a")
        except: pass
        self.spotifyMain.volume(int(self.volume))
        
    def raiseVolume(self, volume):
        self.devices = self.spotifyMain.devices()
        self.volume = volume
        try:self.volume = volume.replace("raise volume by ", "")
        except: pass
        try:self.volume = slicer(self.volume, " ", ba="a")
        except: pass
        self.currentvolume = int(self.devices['devices'][0]['volume_percent'])
        self.spotifyMain.volume(self.currentvolume+int(self.volume))

    def lowerVolume(self, volume):
        self.devices = self.spotifyMain.devices()
        self.volume = volume
        try:self.volume = volume.replace("lower volume by ", "")
        except: pass
        try:self.volume = slicer(self.volume, " ", ba="a")
        except: pass
        self.currentvolume = int(self.devices['devices'][0]['volume_percent'])
        self.spotifyMain.volume(self.currentvolume-int(self.volume))

    def whatVolume(self):
        self.devices = self.spotifyMain.devices()
        self.currentvolume = self.devices['devices'][0]['volume_percent']
        return(str(self.currentvolume))

    def addRandomSongToQueue(self, numberGenre):
        self.step1 = slicer(numberGenre, "add ")
        self.step2 = self.step1.replace("add ", "")
        self.n = int(slicer(self.step2, "random", ba='a'))
        self.genre = slicer(self.step2, "song", ba="a")
        self.genre = slicer(self.genre, "random")
        self.genre = self.genre.replace("random ", "")

        for i in range(self.n):
            self.q = self.spotifyMain.search("genre: " + self.genre, type="track", market="se", limit=50, offset=(i)*10)
            self.song=self.q["tracks"]["items"][random.randint(0,50)]
            self.songuri = self.song["uri"]
            """ self.songname = self.song["name"]
            self.songartists = []
            self.songduration = convertms(self.song["duration_ms"])
            self.songalbum = self.song["album"]["name"]
            self.songpopularity = self.song["popularity"]
            for i in range(len(self.song["artists"])):
                self.songartists.append(self.song["artists"][i]["name"])

            print(f"Name: {self.songname}\nArtist: {', '.join(self.songartists)}\nAlbum: {self.songalbum}\nDuration: {self.songduration}\nPopularity: {self.songpopularity}")
            if self.song["explicit"]:
                print("Explicit") """

            self.spotifyMain.add_to_queue(self.songuri)