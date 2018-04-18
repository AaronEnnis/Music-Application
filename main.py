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
        #fn = function for threads, arg/kwargs = function parameters
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)

class UIPlay(QWidget):
    def __init__(self, parent=None):
        super(UIPlay, self).__init__(parent)
       
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        self.HOMESCREEN = QPushButton('Go to home', self)
        self.HOMESCREEN.resize(self.HOMESCREEN.sizeHint())
        
        self.SMALLE = QLabel('', self)         
        self.B = QLabel('', self)         
        self.G = QLabel('', self)         
        self.D = QLabel('', self)         
        self.A = QLabel('', self)         
        self.E = QLabel('', self)         
        
        self.SMALLE2 = QLabel('', self)         
        self.B2 = QLabel('', self)         
        self.G2 = QLabel('', self)         
        self.D2 = QLabel('', self)         
        self.A2 = QLabel('', self)         
        self.E2 = QLabel('', self) 
        
        self.space = QLabel('', self)
   
        newfont = QFont("Times", 14, QFont.Bold)
        self.SMALLE.setFont(newfont)
        self.B.setFont(newfont)
        self.G.setFont(newfont)
        self.D.setFont(newfont)
        self.A.setFont(newfont)
        self.E.setFont(newfont)
                   
        self.SMALLE2.setFont(newfont)
        self.B2.setFont(newfont)
        self.G2.setFont(newfont)
        self.D2.setFont(newfont)
        self.A2.setFont(newfont)
        self.E2.setFont(newfont)  
        
        self.space.setFont(newfont)
        
        self.PLAY_LBL = QLabel('Play', self)
        self.DELETE_LBL = QLabel('Delete', self)
        
        cwd = music_utils.os.getcwd() 
        existing_files = music_utils.os.listdir(cwd + '\Recordings')
        self.RECORDINGS = QComboBox(self) 
        self.RECORDINGS.resize(self.RECORDINGS.sizeHint())
        self.DELETE = QComboBox(self) 
        self.DELETE.resize(self.DELETE.sizeHint())
        
        for i in existing_files:
            #only pulls the Wav files
            if i[-4:] == '.wav':
                self.RECORDINGS.addItem(str(i))
                self.DELETE.addItem(str(i))
               
        self.grid.addWidget(self.SMALLE,1,1)
        self.grid.addWidget(self.B,2,1)
        self.grid.addWidget(self.G,3,1)
        self.grid.addWidget(self.D,4,1)
        self.grid.addWidget(self.A,5,1)
        self.grid.addWidget(self.E,6,1)
        self.grid.addWidget(self.space,7,1)        
        self.grid.addWidget(self.SMALLE2,8,1)
        self.grid.addWidget(self.B2,9,1)
        self.grid.addWidget(self.G2,10,1)
        self.grid.addWidget(self.D2,11,1)
        self.grid.addWidget(self.A2,12,1)
        self.grid.addWidget(self.E2,13,1)
        
        self.grid.addWidget(self.HOMESCREEN,14,0)
        self.grid.addWidget(self.PLAY_LBL,13,3)
        self.grid.addWidget(self.DELETE_LBL,13,7)
        self.grid.addWidget(self.RECORDINGS,14,3)
        self.grid.addWidget(self.DELETE,14,7)
        

class UIHome(QWidget):
    def __init__(self, parent=None):
        super(UIHome, self).__init__(parent)
        
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        self.PLAYSCREEN = QPushButton("Go to play", self)
        self.PLAYSCREEN.resize(self.PLAYSCREEN.sizeHint())
        self.grid.addWidget(self.PLAYSCREEN,0,1)
       
        self.RECORDING_LBL = QLabel('Lenght of recording (seconds)', self)   
        self.RECORDING_LBL.resize(self.RECORDING_LBL.sizeHint())
        self.grid.addWidget(self.RECORDING_LBL,1,0)
        
        self.RECORDED_LBL = QLabel('', self)   
        self.RECORDED_LBL.resize(self.RECORDING_LBL.sizeHint())
        self.grid.addWidget(self.RECORDED_LBL,2,0)
       
        self.RECORDING_TIME = QComboBox(self)
        self.RECORDING_TIME.addItem(str(5))
        self.RECORDING_TIME.addItem(str(10))
        self.RECORDING_TIME.addItem(str(15))
        self.RECORDING_TIME.addItem(str(20))
        self.RECORDING_TIME.addItem(str(25))
        self.RECORDING_TIME.addItem(str(30))        
        self.RECORDING_TIME.resize(self.RECORDING_TIME.sizeHint())
        self.grid.addWidget(self.RECORDING_TIME,1,1)
        
        self.RECORD = QPushButton("Record!", self)
        self.RECORD.resize(self.RECORD.sizeHint())
        self.grid.addWidget(self.RECORD,1,2)
        
        self.QUIT = QPushButton("Quit!", self)
        self.QUIT.resize(self.QUIT.sizeHint())
        self.grid.addWidget(self.QUIT,2,1)
        
        
class UIEmptyHome(QWidget):
    def __init__(self, parent=None):
        super(UIEmptyHome, self).__init__(parent)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        self.PLAYSCREEN = QPushButton("Go to play", self)
        self.PLAYSCREEN.resize(self.PLAYSCREEN.sizeHint())
        self.PLAYSCREEN.setEnabled(False)
        self.PLAYSCREEN.setVisible(False)
        self.grid.addWidget(self.PLAYSCREEN,0,1)
       
        self.RECORDING_LBL = QLabel('Lenght of recording (seconds)', self)   
        self.RECORDING_LBL.resize(self.RECORDING_LBL.sizeHint())
        self.grid.addWidget(self.RECORDING_LBL,1,0)
        
        self.RECORDED_LBL = QLabel('', self)   
        self.RECORDED_LBL.resize(self.RECORDING_LBL.sizeHint())
        self.grid.addWidget(self.RECORDED_LBL,2,0)
       
        self.RECORDING_TIME = QComboBox(self)
        self.RECORDING_TIME.addItem(str(5))
        self.RECORDING_TIME.addItem(str(10))
        self.RECORDING_TIME.addItem(str(15))
        self.RECORDING_TIME.addItem(str(20))
        self.RECORDING_TIME.addItem(str(25))
        self.RECORDING_TIME.addItem(str(30))        
        self.RECORDING_TIME.resize(self.RECORDING_TIME.sizeHint())
        self.grid.addWidget(self.RECORDING_TIME,1,1)
        
        self.RECORD = QPushButton("Record!", self)
        self.RECORD.resize(self.RECORD.sizeHint())
        self.grid.addWidget(self.RECORD,1,2)
        
        self.QUIT = QPushButton("Quit!", self)
        self.QUIT.resize(self.QUIT.sizeHint())
        self.grid.addWidget(self.QUIT,2,1)

#Main window of application
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(50, 50, 650, 500)
        self.setWindowTitle('Music Application')
        
        #setting threads
        self.threadpool = QThreadPool()
        

        self.Home_Screen = UIHome( self )
        self.Home_Screen.PLAYSCREEN.clicked.connect( self.play_screen )
        self.Home_Screen.RECORD.clicked.connect( self.record )
        self.Home_Screen.QUIT.clicked.connect( self.quit_app )
        
        self.Empty_Home_Screen = UIEmptyHome( self )
        self.Empty_Home_Screen.PLAYSCREEN.clicked.connect( self.play_screen )
        self.Empty_Home_Screen.RECORD.clicked.connect( self.record )
        self.Empty_Home_Screen.QUIT.clicked.connect( self.quit_app )
        
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
            self.setWindowTitle("Music Application / Home")
            self.stack.setCurrentIndex( 1 )
        else:
            self.setWindowTitle("Music Application / Home")
            self.stack.setCurrentIndex(0)
            

    def home_screen(self):
        #checks if there are existing recordings
        cwd = music_utils.os.getcwd() 
        existing_files = music_utils.os.listdir(cwd + '\Recordings')
        if len(existing_files) == 0:
            self.setWindowTitle("Music Application / Home")
            self.stack.setCurrentIndex( 1 )
        else:
            self.setWindowTitle("Music Application / Home")
            self.stack.setCurrentIndex(0)
            self.Empty_Home_Screen.PLAYSCREEN.setEnabled(False)
            self.Empty_Home_Screen.PLAYSCREEN.setVisible(False) 
        
    def play_screen(self):
        self.setWindowTitle("Music Application / Play")
        self.stack.setCurrentIndex( 2 )
        
    
    def _play(self, _file):  #play audio
        self.Play_Screen.RECORDINGS.setEnabled(False)
        self.Play_Screen.DELETE.setEnabled(False)
        self.Home_Screen.RECORD.setEnabled(False)
        self.Empty_Home_Screen.RECORD.setEnabled(False)
        
        e,B,G,D,A,E = music_utils.get_tab(_file)
        
        if len(e) < 81:            
            self.Play_Screen.SMALLE.setText(e)
            self.Play_Screen.B.setText(B)
            self.Play_Screen.G.setText(G)
            self.Play_Screen.D.setText(D)
            self.Play_Screen.A.setText(A)
            self.Play_Screen.E.setText(E)
            
            self.Play_Screen.SMALLE2.setText('')
            self.Play_Screen.B2.setText('')   
            self.Play_Screen.G2.setText('')
            self.Play_Screen.D2.setText('')
            self.Play_Screen.A2.setText('')
            self.Play_Screen.E2.setText('')
     
            music_utils.play(_file) 
            
            self.Play_Screen.RECORDINGS.setEnabled(True)
            self.Play_Screen.DELETE.setEnabled(True)
            self.Home_Screen.RECORD.setEnabled(True)
            self.Empty_Home_Screen.RECORD.setEnabled(True)
        elif len(e) > 80:   
            half_way_point = len(e) / 2
            half_way_point = int(half_way_point)
            
            self.Play_Screen.SMALLE.setText(e[:half_way_point])
            self.Play_Screen.B.setText(B[:half_way_point])
            self.Play_Screen.G.setText(G[:half_way_point])
            self.Play_Screen.D.setText(D[:half_way_point])
            self.Play_Screen.A.setText(A[:half_way_point])
            self.Play_Screen.E.setText(E[:half_way_point])
                      
            self.Play_Screen.SMALLE2.setText(e[half_way_point:])
            self.Play_Screen.B2.setText(B[half_way_point:])
            self.Play_Screen.G2.setText(G[half_way_point:])
            self.Play_Screen.D2.setText(D[half_way_point:])
            self.Play_Screen.A2.setText(A[half_way_point:])
            self.Play_Screen.E2.setText(E[half_way_point:])
            
            music_utils.play(_file) 
            
            self.Play_Screen.RECORDINGS.setEnabled(True)
            self.Play_Screen.DELETE.setEnabled(True)
            self.Home_Screen.RECORD.setEnabled(True)
            self.Empty_Home_Screen.RECORD.setEnabled(True)
        
    def getText(self):
        text, okPressed = QInputDialog.getText(self, "Recording name","Enter name of recording:", QLineEdit.Normal, "")
        if okPressed:
            return text 
        else:
            self.Home_Screen.RECORDED_LBL.setText('')   
            self.Empty_Home_Screen.RECORDED_LBL.setText('')      
            self.Play_Screen.RECORDINGS.setEnabled(True)
            self.Play_Screen.DELETE.setEnabled(True) 
            self.Home_Screen.RECORD.setEnabled(True)
            self.Empty_Home_Screen.RECORD.setEnabled(True)
            self.Empty_Home_Screen.PLAYSCREEN.setEnabled(True)
            self.Empty_Home_Screen.PLAYSCREEN.setVisible(True)  
        
    def getTextError(self):
        text, okPressed = QInputDialog.getText(self, "ERROR!","Enter different name:", QLineEdit.Normal, "")
        if okPressed:
            return text 
        else:
            self.Home_Screen.RECORDED_LBL.setText('')   
            self.Empty_Home_Screen.RECORDED_LBL.setText('') 
            self.Play_Screen.RECORDINGS.setEnabled(True)
            self.Play_Screen.DELETE.setEnabled(True) 
            self.Home_Screen.RECORD.setEnabled(True)
            self.Empty_Home_Screen.RECORD.setEnabled(True)
            self.Empty_Home_Screen.PLAYSCREEN.setEnabled(True)
            self.Empty_Home_Screen.PLAYSCREEN.setVisible(True)         

    def _delete(self, _file):    #deletes audio files        
        music_utils.delete(_file)
        idx = self.Play_Screen.DELETE.currentIndex()
        self.Play_Screen.RECORDINGS.removeItem(idx)
        self.Play_Screen.DELETE.removeItem(idx)
               
    def play_audio(self, _file):  #creates thread for playing audio files  
        worker = Worker(self._play, _file)     
        self.threadpool.start(worker)
       
    def record(self): #creates thread for recording
       
        if self.stack.currentIndex() == 0:
            sec = self.Home_Screen.RECORDING_TIME.currentText()
        else:
            sec = self.Empty_Home_Screen.RECORDING_TIME.currentText()

        self.Home_Screen.RECORDED_LBL.setText('RECORDED!')   
        self.Empty_Home_Screen.RECORDED_LBL.setText('RECORDED!')       
        self.Play_Screen.RECORDINGS.setEnabled(False)
        self.Play_Screen.DELETE.setEnabled(False)       
        self.Home_Screen.RECORD.setEnabled(False)
        self.Empty_Home_Screen.RECORD.setEnabled(False)
        
        notes, norm_len, r, p, stream = music_utils.record(int(sec))
        
        self.text = self.getText()       
        self.text = self.text  + '.wav'
        
        cwd = music_utils.os.getcwd()
        existing_files = music_utils.os.listdir(cwd + "\Recordings")
        if self.text in existing_files or self.text == '.wav' or len(self.text) > 20:
            while self.text in existing_files or self.text == '.wav' or len(self.text) > 20:
                self.text = self.getTextError()       
                self.text = self.text  + '.wav'
            music_utils.create_file(self.text, notes, norm_len, r, p, stream)

            self.Home_Screen.RECORDED_LBL.setText('')   
            self.Empty_Home_Screen.RECORDED_LBL.setText('')         
            self.Play_Screen.RECORDINGS.setEnabled(True)
            self.Play_Screen.DELETE.setEnabled(True) 
            self.Home_Screen.RECORD.setEnabled(True)
            self.Empty_Home_Screen.RECORD.setEnabled(True)
            self.Empty_Home_Screen.PLAYSCREEN.setEnabled(True)
            self.Empty_Home_Screen.PLAYSCREEN.setVisible(True)        
            
            self.Play_Screen.RECORDINGS.addItem(self.text)
            self.Play_Screen.DELETE.addItem(self.text)
        else:
            music_utils.create_file(self.text, notes, norm_len, r, p, stream)
    
            self.Home_Screen.RECORDED_LBL.setText('')   
            self.Empty_Home_Screen.RECORDED_LBL.setText('')        
            self.Play_Screen.RECORDINGS.setEnabled(True)
            self.Play_Screen.DELETE.setEnabled(True) 
            self.Home_Screen.RECORD.setEnabled(True)
            self.Empty_Home_Screen.RECORD.setEnabled(True)
            self.Empty_Home_Screen.PLAYSCREEN.setEnabled(True)
            self.Empty_Home_Screen.PLAYSCREEN.setVisible(True)        
            
            self.Play_Screen.RECORDINGS.addItem(self.text)
            self.Play_Screen.DELETE.addItem(self.text)
        
    def delete_recording(self, _file): #creates thread for deleting files
        
        choice = QMessageBox.question(self, 'Delete?',
                                      "Are you sure to delete?", 
                                      QMessageBox.Yes | QMessageBox.No)

        if choice == QMessageBox.Yes:
            worker = Worker(self._delete, _file) 
            self.threadpool.start(worker)
        elif choice == QMessageBox.No:
            pass
        
    def quit_app(self): #exits out of the app
        
        choice = QMessageBox.question(self, 'Quit?',
                              "Are you sure to quit?", 
                              QMessageBox.Yes | QMessageBox.No)

        if choice == QMessageBox.Yes:
            print("Closing App!")
            sys.exit()
        elif choice == QMessageBox.No:
            pass
                

if __name__ == '__main__':
    music_utils.check_tab()
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance() 
    
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())