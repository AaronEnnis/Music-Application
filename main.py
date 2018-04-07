## Author: Aaron Ennis
## Title: Music Application
##
## Description: 
## A music application that allows the user to record/play back WAV files.
## The application transcribes the audio data from the WAV files and
## transcribes the notes to tabliture form and displays it.
#______________________________________________________________________________

import sys
import music_utils
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and 
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        self.fn(*self.args, **self.kwargs)

class UIPlay(QWidget):
    def __init__(self, parent=None):
        super(UIPlay, self).__init__(parent)
        self.PlayBTN = QPushButton('go to home', self)
        self.PlayBTN.move(50, 350)
        
        cwd = music_utils.os.getcwd() 
        existing_files = music_utils.os.listdir(cwd + '\Recordings')
        self.RECORDINGS = QComboBox(self)        
        
        for i in existing_files:
            self.RECORDINGS.addItem(str(i))
        self.RECORDINGS.move(200, 350)
        
class UIHome(QWidget):
    def __init__(self, parent=None):
        super(UIHome, self).__init__(parent)
        self.CPSBTN = QPushButton("go to play", self)
        self.CPSBTN.move(100, 350)
        
class UIEmptyHome(QWidget):
    def __init__(self, parent=None):
        super(UIEmptyHome, self).__init__(parent)
        self.CPSBTN1 = QPushButton("empty go to play", self)
        self.CPSBTN1.move(150, 350)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(50, 50, 800, 500)
        self.setWindowTitle('Music Application')
        
        #setting threads
        self.threadpool = QThreadPool()
        self.threadpool.maxThreadCount()


        Home = UIHome( self )
        Home.CPSBTN.clicked.connect( self.play_screen )
        
        EmptyHome = UIEmptyHome( self )
        EmptyHome.CPSBTN1.clicked.connect( self.play_screen )
        
        Play = UIPlay( self )
        Play.PlayBTN.clicked.connect( self.home_screen )
        Play.RECORDINGS.activated[str].connect(self.play_audio)
        self.stack = QStackedWidget(self)
        self.stack.addWidget(Home)
        
        self.stack.addWidget(EmptyHome)
        
        self.stack.addWidget( Play )
        self.setCentralWidget( self.stack )
        #checks if there are existing recordings
        cwd = music_utils.os.getcwd() 
        existing_files = music_utils.os.listdir(cwd + '\Recordings')
        if len(existing_files) == 0:
            self.setWindowTitle("Home")
            self.stack.setCurrentIndex( 1 )
        else:
            self.setWindowTitle("Home")
            self.stack.setCurrentIndex(0)
            
        self.show()

    def home_screen(self):
        #checks if there are existing recordings
        cwd = music_utils.os.getcwd() 
        existing_files = music_utils.os.listdir(cwd + '\Recordings')
        if len(existing_files) == 0:
            self.setWindowTitle("Page2")
            self.stack.setCurrentIndex( 1 )
        else:
            self.setWindowTitle("Page1")
            self.stack.setCurrentIndex(0)
        
    def play_screen(self):
        self.setWindowTitle("Page2")
        self.stack.setCurrentIndex( 2 )
    
    def _play(self, file):
        music_utils.play(file)  
        
    def play_audio(self, file):
        worker = Worker(self._play,file) 
        self.threadpool.start(worker)
                



if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance() 
    w = MainWindow()
    sys.exit(app.exec_())