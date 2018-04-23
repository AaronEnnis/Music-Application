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
                

        self.SMALLE_LBL = QLabel('', self)         #Creating the strongs for the tab
        self.B_LBL = QLabel('', self)         
        self.G_LBL = QLabel('', self)         
        self.D_LBL = QLabel('', self)         
        self.A_LBL = QLabel('', self)         
        self.E_LBL = QLabel('', self)
        
        self.SMALLE_LBL2 = QLabel('', self)         
        self.B_LBL2 = QLabel('', self)         
        self.G_LBL2 = QLabel('', self)         
        self.D_LBL2 = QLabel('', self)         
        self.A_LBL2 = QLabel('', self)         
        self.E_LBL2 = QLabel('', self)
        
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
        
        self.SMALLE3 = QLabel('', self)         
        self.B3 = QLabel('', self)         
        self.G3 = QLabel('', self)         
        self.D3 = QLabel('', self)         
        self.A3 = QLabel('', self)         
        self.E3 = QLabel('', self)
        
        self.SMALLE4 = QLabel('', self)         
        self.B4 = QLabel('', self)         
        self.G4 = QLabel('', self)         
        self.D4 = QLabel('', self)         
        self.A4 = QLabel('', self)         
        self.E4 = QLabel('', self)
        
        self.SMALLE5 = QLabel('', self)         
        self.B5 = QLabel('', self)         
        self.G5 = QLabel('', self)         
        self.D5 = QLabel('', self)         
        self.A5 = QLabel('', self)         
        self.E5 = QLabel('', self)
        
        self.SMALLE6 = QLabel('', self)         
        self.B6 = QLabel('', self)         
        self.G6 = QLabel('', self)         
        self.D6 = QLabel('', self)         
        self.A6 = QLabel('', self)         
        self.E6 = QLabel('', self)
        
        self.space = QLabel('', self)
        self.space2 = QLabel('', self)
        
        newfont = QFont("Times", 14, QFont.Bold)
        button_font = QFont("Times", 12, QFont.Bold)    #setting fonts of the buttons, labels and tab
        
        self.HOMESCREEN.setFont(button_font)
        
        self.SMALLE_LBL.setFont(newfont)         
        self.B_LBL.setFont(newfont)         
        self.G_LBL.setFont(newfont)        
        self.D_LBL.setFont(newfont)         
        self.A_LBL.setFont(newfont)        
        self.E_LBL.setFont(newfont)
        
        self.SMALLE_LBL2.setFont(newfont)         
        self.B_LBL2.setFont(newfont)         
        self.G_LBL2.setFont(newfont)         
        self.D_LBL2.setFont(newfont)         
        self.A_LBL2.setFont(newfont)         
        self.E_LBL2.setFont(newfont)
        
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
        
        self.SMALLE3.setFont(newfont)
        self.B3.setFont(newfont)
        self.G3.setFont(newfont)
        self.D3.setFont(newfont)
        self.A3.setFont(newfont)
        self.E3.setFont(newfont)
        
        self.SMALLE4.setFont(newfont)
        self.B4.setFont(newfont)
        self.G4.setFont(newfont)
        self.D4.setFont(newfont)
        self.A4.setFont(newfont)
        self.E4.setFont(newfont)
        
        self.SMALLE5.setFont(newfont)
        self.B5.setFont(newfont)
        self.G5.setFont(newfont)
        self.D5.setFont(newfont)
        self.A5.setFont(newfont)
        self.E5.setFont(newfont)
        
        self.SMALLE6.setFont(newfont)
        self.B6.setFont(newfont)
        self.G6.setFont(newfont)
        self.D6.setFont(newfont)
        self.A6.setFont(newfont)
        self.E6.setFont(newfont)
        
        self.space.setFont(newfont)
        self.space2.setFont(newfont)
        
        self.PLAY_LBL = QLabel('Play', self)
        self.PLAY_LBL.setFont(button_font)
        self.DELETE_LBL = QLabel('Delete', self)
        self.DELETE_LBL.setFont(button_font)
        
        cwd = music_utils.os.getcwd() 
        existing_files = music_utils.os.listdir(cwd + '\Recordings')
        self.RECORDINGS = QComboBox(self) 
        self.RECORDINGS.setFont(button_font)
        self.RECORDINGS.resize(self.RECORDINGS.sizeHint())
        self.DELETE = QComboBox(self) 
        self.DELETE.resize(self.DELETE.sizeHint())
        self.DELETE.setFont(button_font)
        
        for i in existing_files:
            #only pulls the Wav files
            if i[-4:] == '.wav':
                self.RECORDINGS.addItem(str(i))
                self.DELETE.addItem(str(i))

        self.grid.addWidget(self.SMALLE_LBL,1,0)
        self.grid.addWidget(self.B_LBL,2,0)
        self.grid.addWidget(self.G_LBL,3,0)
        self.grid.addWidget(self.D_LBL,4,0)
        self.grid.addWidget(self.A_LBL,5,0)
        self.grid.addWidget(self.E_LBL,6,0)
        self.grid.addWidget(self.SMALLE_LBL2,8,0)
        self.grid.addWidget(self.B_LBL2,9,0)
        self.grid.addWidget(self.G_LBL2,10,0)
        self.grid.addWidget(self.D_LBL2,11,0)
        self.grid.addWidget(self.A_LBL2,12,0)
        self.grid.addWidget(self.E_LBL2,13,0)
               
        self.grid.addWidget(self.SMALLE,1,1)
        self.grid.addWidget(self.B,2,1)
        self.grid.addWidget(self.G,3,1)
        self.grid.addWidget(self.D,4,1)
        self.grid.addWidget(self.A,5,1)
        self.grid.addWidget(self.E,6,1)
        self.grid.addWidget(self.SMALLE2,1,2)
        self.grid.addWidget(self.B2,2,2)
        self.grid.addWidget(self.G2,3,2)
        self.grid.addWidget(self.D2,4,2)
        self.grid.addWidget(self.A2,5,2)
        self.grid.addWidget(self.E2,6,2)
        self.grid.addWidget(self.SMALLE3,1,3)
        self.grid.addWidget(self.B3,2,3)
        self.grid.addWidget(self.G3,3,3)
        self.grid.addWidget(self.D3,4,3)
        self.grid.addWidget(self.A3,5,3)
        self.grid.addWidget(self.E3,6,3)
        
        self.grid.addWidget(self.space,7,1) 
        
        self.grid.addWidget(self.SMALLE4,8,1)
        self.grid.addWidget(self.B4,9,1)
        self.grid.addWidget(self.G4,10,1)
        self.grid.addWidget(self.D4,11,1)
        self.grid.addWidget(self.A4,12,1)
        self.grid.addWidget(self.E4,13,1)
        self.grid.addWidget(self.SMALLE5,8,2)
        self.grid.addWidget(self.B5,9,2)
        self.grid.addWidget(self.G5,10,2)
        self.grid.addWidget(self.D5,11,2)
        self.grid.addWidget(self.A5,12,2)
        self.grid.addWidget(self.E5,13,2)
        self.grid.addWidget(self.SMALLE6,8,3)
        self.grid.addWidget(self.B6,9,3)
        self.grid.addWidget(self.G6,10,3)
        self.grid.addWidget(self.D6,11,3)
        self.grid.addWidget(self.A6,12,3)
        self.grid.addWidget(self.E6,13,3)
        
        self.grid.addWidget(self.space2,14,1)
        
        self.grid.addWidget(self.HOMESCREEN,15,0)
        self.grid.addWidget(self.PLAY_LBL,14,3)
        self.grid.addWidget(self.DELETE_LBL,14,7)
        self.grid.addWidget(self.RECORDINGS,15,3)
        self.grid.addWidget(self.DELETE,15,7)
        

class UIHome(QWidget):
    def __init__(self, parent=None):
        super(UIHome, self).__init__(parent)
        
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        self.PLAYSCREEN = QPushButton("Go to play", self)
        self.PLAYSCREEN.resize(self.PLAYSCREEN.sizeHint())
        self.grid.addWidget(self.PLAYSCREEN,0,1)
       
        self.RECORDING_LBL = QLabel('Length of recording (seconds)', self)   
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
        
        button_font = QFont("Times", 12, QFont.Bold)    #setting fonts of the buttons, labels and tab
        self.PLAYSCREEN.setFont(button_font)
        self.RECORDING_LBL.setFont(button_font)
        self.RECORDED_LBL.setFont(button_font)
        self.RECORDING_TIME.setFont(button_font)
        self.RECORD.setFont(button_font)
        self.QUIT.setFont(button_font)
        
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
       
        self.RECORDING_LBL = QLabel('Length of recording (seconds)', self)   
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
        
        button_font = QFont("Times", 12, QFont.Bold)    #setting fonts of the buttons, labels and tab
        self.PLAYSCREEN.setFont(button_font)
        self.RECORDING_LBL.setFont(button_font)
        self.RECORDED_LBL.setFont(button_font)
        self.RECORDING_TIME.setFont(button_font)
        self.RECORD.setFont(button_font)
        self.QUIT.setFont(button_font)
        
#Main window of application
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(50, 50, 650, 500)
        self.setWindowTitle('Music Application')
        self.setStyleSheet('QMainWindow{background-color: darkgray;border: 5px solid black;}')
        
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
        if len(existing_files) == 0: #empty hom screen
            self.setWindowTitle("Music Application / Home")
            self.stack.setCurrentIndex( 1 )
            
            #clearing the tab when brought to empty home screen
            self.Play_Screen.SMALLE.setText('')
            self.Play_Screen.B.setText('')
            self.Play_Screen.G.setText('')
            self.Play_Screen.D.setText('')
            self.Play_Screen.A.setText('')
            self.Play_Screen.E.setText('')
            self.Play_Screen.SMALLE2.setText('')
            self.Play_Screen.B2.setText('')
            self.Play_Screen.G2.setText('')
            self.Play_Screen.D2.setText('')
            self.Play_Screen.A2.setText('')
            self.Play_Screen.E2.setText('')
            self.Play_Screen.SMALLE3.setText('')
            self.Play_Screen.B3.setText('')
            self.Play_Screen.G3.setText('')
            self.Play_Screen.D3.setText('')
            self.Play_Screen.A3.setText('')
            self.Play_Screen.E3.setText('')
            
            self.Play_Screen.SMALLE4.setText('')
            self.Play_Screen.B4.setText('')   
            self.Play_Screen.G4.setText('')
            self.Play_Screen.D4.setText('')
            self.Play_Screen.A4.setText('')
            self.Play_Screen.E4.setText('')
            self.Play_Screen.SMALLE5.setText('')
            self.Play_Screen.B5.setText('')   
            self.Play_Screen.G5.setText('')
            self.Play_Screen.D5.setText('')
            self.Play_Screen.A5.setText('')
            self.Play_Screen.E5.setText('')
            self.Play_Screen.SMALLE6.setText('')
            self.Play_Screen.B6.setText('')   
            self.Play_Screen.G6.setText('')
            self.Play_Screen.D6.setText('')
            self.Play_Screen.A6.setText('')
            self.Play_Screen.E6.setText('')
            
            self.Play_Screen.SMALLE_LBL.setText('')
            self.Play_Screen.B_LBL.setText('')   
            self.Play_Screen.G_LBL.setText('')
            self.Play_Screen.D_LBL.setText('')
            self.Play_Screen.A_LBL.setText('')
            self.Play_Screen.E_LBL.setText('')
            
            self.Play_Screen.SMALLE_LBL2.setText('')
            self.Play_Screen.B_LBL2.setText('')   
            self.Play_Screen.G_LBL2.setText('')
            self.Play_Screen.D_LBL2.setText('')
            self.Play_Screen.A_LBL2.setText('')
            self.Play_Screen.E_LBL2.setText('')
        else: #normal home screen
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
            one_third = len(e) / 3
            one_third = round(one_third)
            two_thirds = one_third * 2   
            
            self.Play_Screen.SMALLE.setText(e[:one_third])
            self.Play_Screen.B.setText(B[:one_third])
            self.Play_Screen.G.setText(G[:one_third])
            self.Play_Screen.D.setText(D[:one_third])
            self.Play_Screen.A.setText(A[:one_third])
            self.Play_Screen.E.setText(E[:one_third])
            self.Play_Screen.SMALLE2.setText(e[one_third:two_thirds])
            self.Play_Screen.B2.setText(B[one_third:two_thirds])
            self.Play_Screen.G2.setText(G[one_third:two_thirds])
            self.Play_Screen.D2.setText(D[one_third:two_thirds])
            self.Play_Screen.A2.setText(A[one_third:two_thirds])
            self.Play_Screen.E2.setText(E[one_third:two_thirds])
            self.Play_Screen.SMALLE3.setText(e[two_thirds:])
            self.Play_Screen.B3.setText(B[two_thirds:])
            self.Play_Screen.G3.setText(G[two_thirds:])
            self.Play_Screen.D3.setText(D[two_thirds:])
            self.Play_Screen.A3.setText(A[two_thirds:])
            self.Play_Screen.E3.setText(E[two_thirds:])
            
            self.Play_Screen.SMALLE4.setText('')
            self.Play_Screen.B4.setText('')   
            self.Play_Screen.G4.setText('')
            self.Play_Screen.D4.setText('')
            self.Play_Screen.A4.setText('')
            self.Play_Screen.E4.setText('')
            self.Play_Screen.SMALLE5.setText('')
            self.Play_Screen.B5.setText('')   
            self.Play_Screen.G5.setText('')
            self.Play_Screen.D5.setText('')
            self.Play_Screen.A5.setText('')
            self.Play_Screen.E5.setText('')
            self.Play_Screen.SMALLE6.setText('')
            self.Play_Screen.B6.setText('')   
            self.Play_Screen.G6.setText('')
            self.Play_Screen.D6.setText('')
            self.Play_Screen.A6.setText('')
            self.Play_Screen.E6.setText('')
            
            self.Play_Screen.SMALLE_LBL.setText('e')
            self.Play_Screen.B_LBL.setText('B')   
            self.Play_Screen.G_LBL.setText('G')
            self.Play_Screen.D_LBL.setText('D')
            self.Play_Screen.A_LBL.setText('A')
            self.Play_Screen.E_LBL.setText('E')
            
            self.Play_Screen.SMALLE_LBL2.setText('')
            self.Play_Screen.B_LBL2.setText('')   
            self.Play_Screen.G_LBL2.setText('')
            self.Play_Screen.D_LBL2.setText('')
            self.Play_Screen.A_LBL2.setText('')
            self.Play_Screen.E_LBL2.setText('')
     
            music_utils.play(_file) 
            
            self.Play_Screen.RECORDINGS.setEnabled(True)
            self.Play_Screen.DELETE.setEnabled(True)
            self.Home_Screen.RECORD.setEnabled(True)
            self.Empty_Home_Screen.RECORD.setEnabled(True)
        elif len(e) > 80:   
            one_sixth = len(e) / 6
            one_sixth = round(one_sixth)
            two_sixth = one_sixth * 2
            three_sixth = one_sixth * 3
            four_sixth = one_sixth * 4
            five_sixth = one_sixth * 5
            
            self.Play_Screen.SMALLE.setText(e[:one_sixth])
            self.Play_Screen.B.setText(B[:one_sixth])
            self.Play_Screen.G.setText(G[:one_sixth])
            self.Play_Screen.D.setText(D[:one_sixth])
            self.Play_Screen.A.setText(A[:one_sixth])
            self.Play_Screen.E.setText(E[:one_sixth])
                      
            self.Play_Screen.SMALLE2.setText(e[one_sixth:two_sixth])
            self.Play_Screen.B2.setText(B[one_sixth:two_sixth])
            self.Play_Screen.G2.setText(G[one_sixth:two_sixth])
            self.Play_Screen.D2.setText(D[one_sixth:two_sixth])
            self.Play_Screen.A2.setText(A[one_sixth:two_sixth])
            self.Play_Screen.E2.setText(E[one_sixth:two_sixth])
            
            self.Play_Screen.SMALLE3.setText(e[two_sixth:three_sixth])
            self.Play_Screen.B3.setText(B[two_sixth:three_sixth])
            self.Play_Screen.G3.setText(G[two_sixth:three_sixth])
            self.Play_Screen.D3.setText(D[two_sixth:three_sixth])
            self.Play_Screen.A3.setText(A[two_sixth:three_sixth])
            self.Play_Screen.E3.setText(E[two_sixth:three_sixth])
            
            self.Play_Screen.SMALLE4.setText(e[three_sixth:four_sixth])
            self.Play_Screen.B4.setText(B[three_sixth:four_sixth])
            self.Play_Screen.G4.setText(G[three_sixth:four_sixth])
            self.Play_Screen.D4.setText(D[three_sixth:four_sixth])
            self.Play_Screen.A4.setText(A[three_sixth:four_sixth])
            self.Play_Screen.E4.setText(E[three_sixth:four_sixth])
                      
            self.Play_Screen.SMALLE5.setText(e[four_sixth:five_sixth])
            self.Play_Screen.B5.setText(B[four_sixth:five_sixth])
            self.Play_Screen.G5.setText(G[four_sixth:five_sixth])
            self.Play_Screen.D5.setText(D[four_sixth:five_sixth])
            self.Play_Screen.A5.setText(A[four_sixth:five_sixth])
            self.Play_Screen.E5.setText(E[four_sixth:five_sixth])
            
            self.Play_Screen.SMALLE6.setText(e[five_sixth:])
            self.Play_Screen.B6.setText(B[five_sixth:])
            self.Play_Screen.G6.setText(G[five_sixth:])
            self.Play_Screen.D6.setText(D[five_sixth:])
            self.Play_Screen.A6.setText(A[five_sixth:])
            self.Play_Screen.E6.setText(E[five_sixth:])
            
            self.Play_Screen.SMALLE_LBL.setText('e')
            self.Play_Screen.B_LBL.setText('B')   
            self.Play_Screen.G_LBL.setText('G')
            self.Play_Screen.D_LBL.setText('D')
            self.Play_Screen.A_LBL.setText('A')
            self.Play_Screen.E_LBL.setText('E')
            
            self.Play_Screen.SMALLE_LBL2.setText('e')
            self.Play_Screen.B_LBL2.setText('B')   
            self.Play_Screen.G_LBL2.setText('G')
            self.Play_Screen.D_LBL2.setText('D')
            self.Play_Screen.A_LBL2.setText('A')
            self.Play_Screen.E_LBL2.setText('E')
            
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