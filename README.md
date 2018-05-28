# Music-Application
#Created by Aaron Ennis
#C00190504

# Description

This is my 4th year final project for college. It is a python desktop application.
The application allows a user to record a piece of music with their guitar.
The recording is saved as a .WAV file that the user can listen to as it is saved to their computer.
The application uses the audio data from the WAV file and transcribes the music.
The user can view their piece of music in written form.

The application is based on the PyAudio and Numpy tools.

It uses the FFT to transcribe the music. 

# How to run:

NOTE: This readme is for a windows system. Using this application on Linux or Mac systems requires different commands to download the dependencies.

Dependencies
1.	Python 3 	(Python 3 compiler to run the code)
2.	PyAudio 	(Used to record and create the .wav files)
3.	Numpy 		(Maths library for algorithms)
4.	PyQt5 		(Framework for the user interface)
5.      Scipy    	(Used to open wav files)

# How to acquire these dependencies?

You can get any version of Python 3 on the official python.org website. 
For this application, I wrote it using Python 3.6.

If you install the python package installer “pip”, each of the dependencies can be easily installed in the command prompt with the command “py -3 -m pip install” followed by the name of the module you would like to install. 
This is the quickest and easiest way for installing modules in python. For example: py -3 -m pip install numpy. You can download pip at pypi.org.

If you do not want to use the pip command, each one of the modules can be downloaded from their official sites. 
You can download the zipped contents of each package and manually put them in to the libraries of your Python 3 folder. 
You need to be careful doing it this way as it can be done wrong and won't work. 
This is why I strongly recommend using pip to install the modules. 

Running the application
After all of the dependencies are installed correctly, all you have to do to run the application is open the main.py file. 
You can do this by double clicking on it, or by opening a command prompt in the working directory and entering the command “py main.py”. 
The only thing you will need other than these dependencies, is a working microphone on the machine and a guitar. 
