import random
import speech_recognition as sr
import sys
import os
import time
from Main import *
from widgets import *
import Text_recognition as tr

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtWidgets import QPushButton, QLabel, QDesktopWidget, QApplication, QMainWindow, QInputDialog, QLineEdit

ap = QApplication(sys.argv)
screen = ap.primaryScreen()
size = screen.size()

spot = spotify()

#speech recognition:
r = sr.Recognizer()

class Alice(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        os.chdir("../AliceDisplay")
        self.button = QPushButton("",self)
        try:
            if spot.isPaused():
                self.button.setIcon(QIcon("pause.png"))
            else:
                self.button.setIcon(QIcon("play.png"))
        except:
            self.button.setIcon(QIcon("pause.png"))
        self.button.setIconSize(QSize(40,40))
        self.button.setGeometry(60,10,40,40)
        self.button.setStyleSheet("border: 0px")
        try:self.button.clicked.connect(self.pause)
        except:pass
        self.button.show()

        self.exitb = QPushButton("X",self)
        self.exitb.clicked.connect(exit)
        self.exitb.setGeometry(1900, 10, 10, 10)
        self.exitb.setStyleSheet("color: white")
        self.exitb.show()

        self.nextb = QPushButton("next", self)
        self.nextb.clicked.connect(self.nextf)
        self.nextb.setGeometry(110, 10, 40, 40)
        self.nextb.setStyleSheet("""color: white;
                                    background-color: black;
                                    border-style: outset;
                                    border-width: 1.5px;
                                    border-color: grey;""")
        self.nextb.show()

        self.prevb = QPushButton("prev", self)
        self.prevb.clicked.connect(self.prevf)
        self.prevb.setGeometry(10, 10, 40, 40)
        self.prevb.setStyleSheet("""color: white;
                                    background-color: black;
                                    border-style: outset;
                                    border-width: 1.5px;
                                    border-color: grey;""")
        self.prevb.show()

        try:self.songtitle = QLabel(f"{spot.whatsong()} - {spot.whatartist()}",parent=self)
        except:self.songtitle = QLabel("", self)
        self.songtitle.setGeometry(160,15, 200, 25)
        self.songtitle.setStyleSheet("color: white")
        self.songtitle.show()

        self.gif = QMovie("loading1/Eclipse-1s-251px.gif")
        self.anim = QLabel(self)
        self.anim.setMovie(self.gif)
        self.anim.setGeometry(960-125, 540-125, 251, 251)
        self.gif.start()

        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(960-125, 400, 251, 25)
        self.textbox.setStyleSheet("""color: white;
                                    background-color: black;
                                    border-style: outset;
                                    border-width: 1.5px;
                                    border-color: grey;""")
        self.textbox.show()

        self.enter = QPushButton("Enter",self)
        self.enter.clicked.connect(self.enterf)
        self.enter.setStyleSheet("""color: white;
                                    background-color: black;
                                    border-style: outset;
                                    border-width: 1.5px;
                                    border-color: grey;""")
        self.enter.setGeometry(960+124, 400, 40, 25)
        self.enter.show()

        self.setStyleSheet("background-color: black")
        self.setWindowFlags(
            Qt.FramelessWindowHint
        )
        self.resize(size)
        self.center()
        self.setWindowTitle('Alice')
        self.show()
        self.speak()

    def center(self):
        """centers the window on the screen"""

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2),
                  int((screen.height() - size.height()) / 2))

    def pause(self):
        if not spot.isPaused():
            spot.unpause()
            self.button.setIcon(QIcon("pause.png"))
        else:
            spot.pause()
            self.button.setIcon(QIcon("play.png"))

    def nextf(self):
        try:
            spot.nextTrack()
            time.sleep(0.05)
            self.songtitle.setText(f"{spot.whatsong()} - {spot.whatartist()}")
        except:pass

    def prevf(self):
        try:
            spot.previousTrack()
            time.sleep(0.05)
            self.songtitle.setText(f"{spot.whatsong()} - {spot.whatartist()}")
        except:pass

    def enterf(self):
        tr.main(self.textbox.text())
        self.textbox.setText("")
        time.sleep(0.5)
        self.songtitle.setText(f"{spot.whatsong()} - {spot.whatartist()}")

    def speak(self):
        with sr.Microphone() as source:
            audio = r.listen(source)

        try:
            said_word = r.recognize_google(audio, language = 'en-uk').lower()
        except:
            said_word = ""
        print(said_word)

def main():

    app = QApplication([])
    alice = Alice()
    sys.exit(app.exec_())

def exit():
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()