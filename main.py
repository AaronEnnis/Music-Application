## Author: Aaron Ennis
## Title: Music Application
##
## Description: 
## A music application that allows the user to record/play back WAV files.
## The application transcribes the audio data from the WAV files and
## transcribes the notes to tabliture form and displays it.
#______________________________________________________________________________

import wave, struct, os, time
import scipy.io.wavfile
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
#import parabolic
from scipy import signal
from sys import byteorder
from array import array
from struct import pack
from numpy import polyfit, arange

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
def note_name(n): return NOTE_NAMES[n % 12] + str(np.floor(n/12 - 1))  #note and octave
def parabolic(f, x):
    """Quadratic interpolation for estimating the true position of an
    inter-sample maximum when nearby samples are known.
   
    f is a vector and x is an index for that vector.
   
    Returns (vx, vy), the coordinates of the vertex of a parabola that goes
    through point x and its two neighbors.
   
    Example:
    Defining a vector f with a local maximum at index 3 (= 6), find local
    maximum if points 2, 3, and 4 actually defined a parabola.
   
    In [3]: f = [2, 3, 1, 6, 4, 2, 3, 1]
   
    In [4]: parabolic(f, argmax(f))
    Out[4]: (3.2142857142857144, 6.1607142857142856)
   
    """
    xv = 1/2. * (f[x-1] - f[x+1]) / (f[x-1] - 2 * f[x] + f[x+1]) + x
    yv = f[x] - 1/4. * (f[x-1] - f[x+1]) * (xv - x)
    return (xv, yv)


def freq_from_fft(sig, fs):
    """
    Estimate frequency from peak of FFT
    """
    # Compute Fourier transform of windowed signal
    windowed = sig * signal.blackmanharris(len(sig))
    f = np.fft.rfft(windowed)

    # Find the peak and interpolate to get a more accurate peak
    i = np.argmax(abs(f))  # Just use this for less-accurate, naive version
    true_i = parabolic(np.log(abs(f)), i)[0]

    # Convert to equivalent frequency
    return fs * true_i / len(windowed)




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


def func():            
    NOTE_MIN = 40       # E2
    NOTE_MAX = 76       # E4
    FSAMP = 22050       # Sampling frequency in Hz
    FRAME_SIZE = 2048   # samples per frame
    FRAMES_PER_FFT = 16  # FFT takes average across how many frames?
    
    ######################################################################
    # Derived quantities from constants above. Note that as
    # SAMPLES_PER_FFT goes up, the frequency step size decreases (sof
    # resolution increases); however, it will incur more delay to process
    # new sounds.
    
    SAMPLES_PER_FFT = FRAME_SIZE * FRAMES_PER_FFT
    FREQ_STEP = float(FSAMP) / SAMPLES_PER_FFT
    
    ######################################################################
    # For printing out notes
    
    NOTE_NAMES = 'E F F# G G# A A# B C C# D D#'.split()
    
    
    ######################################################################
    # These three functions are based upon this very useful webpage:
    # https://newt.phys.unsw.edu.au/jw/notes.html
    
    def freq_to_number(f): return 76 + 12 * np.log2(f / 659.255)
    
    
    def number_to_freq(n): return 659.255 * 2.0**((n - 76) / 12.0)
    
    
    def note_name(n):
        return NOTE_NAMES[n % NOTE_MIN % len(NOTE_NAMES)] + str(int(n / 12 - 1))
    
    ######################################################################
    # Ok, ready to go now.
    
    # Get min/max index within FFT of notes we care about.
    # See docs for numpy.rfftfreq()
    
    
    def note_to_fftbin(n): return number_to_freq(n) / FREQ_STEP
    
    
    imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN - 1))))
    imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX + 1))))
    
    # Allocate space to run an FFT. 
    buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
    num_frames = 0
    
    def normalize(snd_data):
        #Average the volume out"
        MAXIMUM = 16384
        times = float(MAXIMUM)/max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i*times))
        return r

    def record_to_file(path,data,sW):
        #Records from the microphone and outputs the resulting data to 'path'
        data = pack('<' + ('h'*len(data)), *data)

        wf = wave.open(path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(sW)
        wf.setframerate(FSAMP)
        wf.writeframes(data)
        wf.close()
    
    p = pyaudio.PyAudio()    
    # Initialize audio
    stream = p.open(format=pyaudio.paInt16,
                                    channels=1,
                                    rate=FSAMP,
                                    input=True,
                                    frames_per_buffer=FRAME_SIZE)
    
    
    # Create Hanning window function
    window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, SAMPLES_PER_FFT, False)))
    
    # Print initial text
    print ('sampling at', FSAMP, 'Hz with max resolution of', FREQ_STEP, 'Hz')
    
    stream.start_stream()    
    # As long as we are getting data:
    start = time.time()
    time.clock()    
    elapsed = 0
    r = array('h')
    notes = []
    print('recording')
    #records for x amount of seconds
    while elapsed < 10:
        elapsed = time.time() - start 
        read = np.fromstring(stream.read(FRAME_SIZE), np.int16)
        # Shift the buffer down and new data in
        buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
        buf[-FRAME_SIZE:] = read
        snd_data = array('h', read)

        r.extend(snd_data)
    
        # Run the FFT on the windowed buffer
        fft = np.fft.rfft(buf * window)
    
        # Get frequency of maximum response in range
        freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP

        # Get note number and nearest note
        n = freq_to_number(freq)
        n0 = int(round(n))
    
        # Console output once we have a full buffer
        num_frames += 1

        print ('freq: ', freq, '  ', note_name(n0))
        notes.append(note_name(n0))
    
    sample_width = p.get_sample_size(pyaudio.paInt16)
    stream.stop_stream()
    stream.close()
    p.terminate() 
    r = normalize(r)

    path = os.path.join('C:/Users/aaron/Desktop/Music-Application','recording.wav')
    record_to_file(path,r,sample_width)

    #roughly the note being played every half a second    
    num_of_notes = len(notes) 
    notes_per_sec = num_of_notes / elapsed
    note_per_hsec = notes_per_sec / 2
    c = 1
    p = 1
    for i in notes:
        if c == np.floor(note_per_hsec):
            print(i)
            c = 0
            p += 1
        c += 1
        
    print(p)
        



                