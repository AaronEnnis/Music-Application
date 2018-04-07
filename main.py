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

#Thread class
class Worker(QRunnable):
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
        self.HOMESCREEN = QPushButton('go to home', self)
        self.HOMESCREEN.move(100, 350)
        
        cwd = music_utils.os.getcwd() 
        existing_files = music_utils.os.listdir(cwd + '\Recordings')
        self.RECORDINGS = QComboBox(self)        
        self.DELETE = QComboBox(self) 
        
        for i in existing_files:
            self.RECORDINGS.addItem(str(i))
        self.RECORDINGS.move(200, 350)
        
        for i in existing_files:
            self.DELETE.addItem(str(i))
        self.DELETE.move(300, 350)
        
        
class UIHome(QWidget):
    def __init__(self, parent=None):
        super(UIHome, self).__init__(parent)
        self.PLAYSCREEN = QPushButton("go to play", self)
        self.PLAYSCREEN.move(100, 350)
        self.RECORD = QPushButton("Record!", self)
        self.RECORD.move(200, 350)
        
class UIEmptyHome(QWidget):
    def __init__(self, parent=None):
        super(UIEmptyHome, self).__init__(parent)
        self.RECORD = QPushButton("Record!", self)
        self.RECORD.move(200, 350)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(50, 50, 800, 500)
        self.setWindowTitle('Music Application')
        
        #setting threads
        self.threadpool = QThreadPool()
        self.threadpool.maxThreadCount()


        self.Home_Screen = UIHome( self )
        self.Home_Screen.PLAYSCREEN.clicked.connect( self.play_screen )
        self.Home_Screen.RECORD.clicked.connect( self.record )
        
        self.Empty_Home_Screen = UIEmptyHome( self )
        self.Empty_Home_Screen.RECORD.clicked.connect( self.record )
        
        self.Play_Screen = UIPlay( self )
        self.Play_Screen.HOMESCREEN.clicked.connect( self.home_screen )
        self.Play_Screen.RECORDINGS.activated[str].connect(self.play_audio)
        self.Play_Screen.DELETE.activated[str].connect(self.delete_recording)
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.Home_Screen)
        
        self.stack.addWidget(self.Empty_Home_Screen)
        
        self.stack.addWidget( self.Play_Screen )
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
        self.Play_Screen.RECORDINGS.setEnabled(False)
        self.Play_Screen.DELETE.setEnabled(False)
        self.Home_Screen.RECORD.setEnabled(False)
        self.Empty_Home_Screen.RECORD.setEnabled(False)
        music_utils.play(file) 
        self.Play_Screen.RECORDINGS.setEnabled(True)
        self.Play_Screen.DELETE.setEnabled(True)
        self.Home_Screen.RECORD.setEnabled(True)
        self.Empty_Home_Screen.RECORD.setEnabled(True)
        
    def _record(self):
        print("RECORDING")       
        self.Play_Screen.RECORDINGS.setEnabled(False)
        self.Play_Screen.DELETE.setEnabled(False)
        self.Home_Screen.RECORD.setEnabled(False)
        self.Empty_Home_Screen.RECORD.setEnabled(False)
        music_utils.record() 
        self.Play_Screen.RECORDINGS.setEnabled(True)
        self.Play_Screen.DELETE.setEnabled(True)   
        self.Home_Screen.RECORD.setEnabled(True)
        self.Empty_Home_Screen.RECORD.setEnabled(True)
        
    def _delete(self, file):
        music_utils.delete(file)
        
    def play_audio(self, file):
        worker = Worker(self._play,file)     
        self.threadpool.start(worker)
    
    def record(self):
        worker = Worker(self._record) 
        self.threadpool.start(worker)
        
    def delete_recording(self,file):
        worker = Worker(self._delete,file) 
        self.threadpool.start(worker)
                

if __name__ == '__main__':
    music_utils.check_tab()
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance() 
    w = MainWindow()
    sys.exit(app.exec_())