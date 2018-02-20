## Author: Aaron Ennis
## Title: Music Application
##
## Description: 
## A music application that allows the user to record/play back WAV files.
## The application transcribes the audio data from the WAV files and
## transcribes the notes to tabliture form and displays it.
#______________________________________________________________________________

import wave, struct, os, time, math
import scipy.io.wavfile
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from sys import byteorder
from array import array
from struct import pack

paul = 'paul'
ratePaul, dataPaul = scipy.io.wavfile.read('paul.wav')
recording = 'recording'
rateRecording, dataRecording = scipy.io.wavfile.read('recording.wav')
E = 'E'
rateE, dataE = scipy.io.wavfile.read('E.wav')
A = 'A'
rateA, dataA = scipy.io.wavfile.read('A.wav')
D = 'D'
rateD, dataD = scipy.io.wavfile.read('D.wav')
G = 'G'
rateG, dataG = scipy.io.wavfile.read('G.wav')
B = 'B'
rateB, dataB = scipy.io.wavfile.read('B.wav')
highE = 'highE'
ratehighE, datahighE = scipy.io.wavfile.read('highE.wav')
#############################################################################################
FSAMP = 22050.0       # Sampling frequency in Hz    
NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()

def freq_to_number(f): return 69 + 12*np.log2(f/440.0)
def note_name(n): return NOTE_NAMES[n % 12] + str(round(n/12 - 1))  #note and octave

def freq_from_fft(sig, fs):
    """
    Get fft of a signal
    """
    # Compute Fourier transform of windowed signal
    windowed = sig * signal.blackmanharris(len(sig))
    f = np.fft.rfft(windowed)

    # Find the peak and interpolate to get a more accurate peak
    i = np.argmax(abs(f))  # Just use this for less-accurate, naive version
    #true_i = parabolic(log(abs(f)), i)[0]
    
    # Convert to equivalent frequency
    return fs * i / len(windowed)




def getData(data): #elements in data (16-bit PCM	-32768	+32767	int16)
    for i in data:
        print(i)

def info(_file):
    
    file = _file + ".wav"
    f = wave.open(file, 'rb')

    print("channels")
    print(f.getnchannels()) ##Returns number of audio channels (1 for mono, 2 for stereo).
    print(" ")
    print("get samp width")
    print(f.getsampwidth()) ##Returns sample width in bytes.
    print(" ")
    print("get frame rate(sample rate)")
    print(f.getframerate()) ##Returns sampling frequency
    print(" ")
    print("get n frames(number of samples)")
    print(f.getnframes()) ##Returns number of audio frames.
    print(" ")
    print("lenght of audio in seconds ")
    print(f.getnframes() / f.getframerate())
    print(" ")
    print("get file params")
    print(f.getparams()) ##Returns a namedtuple() (nchannels, sampwidth, framerate, nframes, comptype, compname), equivalent to output of the get*() methods.
    print(" ")
    wave_data = f.readframes(1) ##Reads and returns at most n frames of audio, as a bytes object.
    print(wave_data)
    print(struct.unpack("hh", b"\x00\x00\x00\x00"))

    f.close()
    

def playAudio(_file):
    #define stream chunk   
    chunk = 1024  
    
    file = _file + ".wav"
    
    #open a wav format music  
    f = wave.open(file,"rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(chunk)  
    
    #play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  
    
    #stop stream  
    stream.stop_stream()  
    stream.close()  
    
    #close PyAudio  
    p.terminate() 
    
def display(data):
    plt.plot(data)     
    plt.show()
       
    
def record():
    CHUNK_SIZE = 1024
    FORMAT = pyaudio.paInt16
    RATE = 44100

    def normalize(snd_data):
        #Average the volume out"
        MAXIMUM = 16384
        times = float(MAXIMUM)/max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i*times))
        return r
    

    def recording():
        #creates WAV file with these parameters
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=1, rate=RATE,
            input=True, output=True,
            frames_per_buffer=CHUNK_SIZE)

        start = time.time()
        time.clock()    
        elapsed = 0
        r = array('h')
        print('recording')
        #records for x amount of seconds
        while elapsed < 10:           
            elapsed = time.time() - start          
            # little endian, signed short
            snd_data = array('h', stream.read(CHUNK_SIZE))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)
            

        sample_width = p.get_sample_size(FORMAT)
        stream.stop_stream()
        stream.close()
        p.terminate()

        r = normalize(r)
        return sample_width, r

    def record_to_file(path):
        #Records from the microphone and outputs the resulting data to 'path'
        sample_width, data = recording()
        data = pack('<' + ('h'*len(data)), *data)

        wf = wave.open(path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(RATE)
        wf.writeframes(data)
        wf.close()
    path = os.path.join('C:/Users/aaron/Desktop/Music-Application','recording.wav')
    record_to_file(path)


def tuner(data):   
    print ('sampling at', FSAMP)

    #split the audio data in to even chunks
    def chunks(data, frame_size):
        for i in range(0, len(data), frame_size):
            yield data[i:i + frame_size]
    #creates chunks of 1/4 of a second of audio
    buf = chunks(data,round(FSAMP/2))
    window_buf = []  
    
    for i in buf:
        window_buf.append(i)

    for j in window_buf:

        freq = freq_from_fft(j,44100)
        
        if freq >= 27:
            n = freq_to_number(np.floor(freq))
            n0 = int(round(n))
            print('freq: ',round(freq),note_name(n0))
            
        else:
            print('-------------------')
                    