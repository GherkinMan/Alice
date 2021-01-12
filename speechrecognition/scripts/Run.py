import pygame, os, random, time, sys, datetime
os.chdir(os.path.dirname(sys.argv[0]))
import Main
os.chdir("../AliceDisplay")

username = 'Noah Schiff'
scope = 'user-read-private user-read-playback-state user-modify-playback-state'
client_id = 'e75a4514376c4d72b1c10baee050efa1'
client_secret = '0149e43848024dcdadfedbb7bff59d38'
redirect_uri = 'https://www.google.com'
spotify1 = Main.spotify()

currentDT = datetime.datetime.now()

pygame.init()
 
_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
        return image

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (40, 125, 0)
RED = (255, 0, 0)
BLUE = (84, 111, 245)
 
font = pygame.font.Font('Font/Roboto/Roboto-Thin.ttf', 80)

font1 = pygame.font.Font('Font/Roboto/Roboto-Thin.ttf', 50)

font2 = pygame.font.Font('Font/Roboto/Roboto-Thin.ttf', 40)

font3 = pygame.font.Font('Font/Roboto/Roboto-Thin.ttf', 30)

font4 = pygame.font.Font('Font/Roboto/Roboto-Thin.ttf', 20)
 
size = (1920, 1080)
 
screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
 
pygame.display.set_caption('Example')
 
clock = pygame.time.Clock()

timer = 0

class SpotifyBar():
    def __init__(self):
        self.ispaused = spotify1.isPaused()
        try:self.currentsong = f"{spotify1.whatsong()} - {spotify1.whatartist()}"
        except: self.currentsong = ""
        self.song = self.currentsong
        self.soundLevel = int(spotify1.whatVolume())
    def draw(self):
        pygame.draw.rect(screen, (20,20,20), [85,50-3,110,15])
        pygame.draw.rect(screen, (50,194,61), [85,50-3,self.soundLevel,15])
        pygame.draw.rect(screen, (255,255,255), [85+self.soundLevel,49-3,15,17])
        screen.blit(get_image("SpotifyBar.png"), (10,10))
        if self.ispaused:
            screen.blit(get_image("pause.png"), (30,35))
        elif not self.ispaused:
            screen.blit(get_image("play.png"), (30,35))
        self.TxT = font2.render(self.song, True, WHITE)
        screen.blit(self.TxT, [20, 90])
    def update(self):
        self.soundLevel = int(spotify1.whatVolume())
        self.ispaused = spotify1.isPaused()
        self.currentsong = f"{spotify1.whatsong()} - {spotify1.whatartist()}"
        self.song = self.currentsong

SpotifyUI = SpotifyBar()

class gif():
    def __init__(self, Dir, imageCount, sleepTime, pos):
        self.Dir = Dir
        self.pos = pos
        self.sleepTime = sleepTime
        self.imageCount = imageCount
        self.count = 1
        self.wait = 0
    def draw(self):
        screen.blit(get_image(self.Dir + str(self.count) + ".png"), (self.pos))
        self.wait += 1
        if self.wait == self.sleepTime:
            self.count += 1
            self.wait = 0
            if self.count == self.imageCount+1:
                self.count = 1

load1 = gif("loading1/load", 31, 3, (1920/2-125, 1080/2-125))

word = '"Go suck my nards!"'

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_SPACE:
                try: spotify1.pause()
                except: spotify1.unpause()
                SpotifyUI.update()
            if event.key == pygame.K_UP:
                if SpotifyUI.soundLevel != 100:
                    spotify1.raiseVolume(10)
                SpotifyUI.update()
            if event.key == pygame.K_DOWN:
                if SpotifyUI.soundLevel != 0:
                    spotify1.lowerVolume(10)
                SpotifyUI.update()
            if event.key == pygame.K_RIGHT:
                spotify1.nextTrack()
                SpotifyUI.update()
            if event.key == pygame.K_LEFT:
                spotify1.previousTrack()
                SpotifyUI.update()
            if event.key == pygame.K_t:
                SpotifyUI.update()
 
    screen.fill((0,0,0))

    load1.draw()

    SpotifyUI.draw()

    if timer < 6000:
        timer += 1
    else:
        SpotifyUI.update()
        timer = 0

    TxT = font.render(word, True, WHITE)
    screen.blit(TxT, [1920/2-((TxT.get_rect().width)/2), 290])
    TxT2 = font.render(str(currentDT.hour) + ":" + str(currentDT.minute), True, WHITE)
    screen.blit(TxT2, [1920/2-((TxT2.get_rect().width)/2), 0])
 
    pygame.display.flip()
 
    clock.tick(100)
 
pygame.quit()