## Author: Aaron Ennis
## Title: Music Application
##
## Description: 
## A music application that allows the user to record/play back WAV files.
## The application transcribes the audio data from the WAV files and
## transcribes the notes to tabliture form and displays it.
#______________________________________________________________________________

import wave, struct
import scipy.io.wavfile
import pyaudio
import numpy as np
import matplotlib.pyplot as plt

a4 = 'a4'
rateA4, dataA4 = scipy.io.wavfile.read('a4.wav')

g4 = 'g4'
rateG4, dataG4 = scipy.io.wavfile.read('g4.wav')

tone = 'tone'
rateTone, dataTone = scipy.io.wavfile.read('tone.wav')

beep = 'beep'
rateBeep, dataBeep = scipy.io.wavfile.read('beep.wav')

siren = 'siren'
rateSiren, dataSiren = scipy.io.wavfile.read('siren.wav')

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

def tuner(data):
    
    NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()
    
    def freq_to_number(f): return 69 + 12*np.log2(f/440.0)
    def note_name(n): return NOTE_NAMES[n % 12] + str(round(n/12 - 2))  #note and octave

    
    print ('sampling at', 22050, 'Hz with max resolution of', 0.67291259765625, 'Hz')

    #split the audio data in to even chunks
    def chunks(data, frame_size):
        for i in range(0, len(data), frame_size):
            yield data[i:i + frame_size]
    
    buf = chunks(data,2048)
    window_buf = []
    for i in buf:
        window_buf.append(i)

    for j in window_buf:
        # Run the FFT on the windowed buffer
        fft = np.fft.fft(j)
        # Get frequency of maximum response in range
        freqs = np.fft.fftfreq(len(fft))
        idx = np.argmax(np.abs(fft))
        for k in freqs:            
            freq = freqs[idx]
            freq_in_hertz = abs(freq * 11025)
            if freq_in_hertz >= 1:
                n = freq_to_number(np.floor(freq_in_hertz))
                n0 = int(round(n))
                print('freq: {:7.2f} Hz     note: {:>3s} {:+.2f}'.format(
                        freq_in_hertz, note_name(n0), n-n0))
        
    
    

        




#def liveTuner():
#    
#    NOTE_MIN = 40       # E2
#    NOTE_MAX = 84       # C6
#    FSAMP = 22050       # Sampling frequency in Hz
#    FRAME_SIZE = 2048   # How many samples per frame?
#    FRAMES_PER_FFT = 16 # FFT takes average across how many frames?
#    
#    ######################################################################
#    # Derived quantities from constants above. Note that as
#    # SAMPLES_PER_FFT goes up, the frequency step size decreases (so
#    # resolution increases); however, it will incur more delay to process
#    # new sounds.
#    
#    SAMPLES_PER_FFT = FRAME_SIZE*FRAMES_PER_FFT
#    FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT
#    
#    ######################################################################
#    # For printing out notes
#    
#    NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()
#    
#    ######################################################################
#    # These three functions are based upon this very useful webpage:
#    # https://newt.phys.unsw.edu.au/jw/notes.html
#    
#    def freq_to_number(f): return 69 + 12*np.log2(f/440.0)
#    def number_to_freq(n): return 440 * 2.0**((n-69)/12.0)
#    def note_name(n): return NOTE_NAMES[n % 12] + str(n/12 - 1)
#    
#    ######################################################################
#    # Ok, ready to go now.
#    
#    # Get min/max index within FFT of notes we care about.
#    # See docs for numpy.rfftfreq()
#    def note_to_fftbin(n): return number_to_freq(n)/FREQ_STEP
#    imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN-1))))
#    imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX+1))))
#    
#    # Allocate space to run an FFT. 
#    buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
#    num_frames = 0
#    
#    # Initialize audio
#    stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
#                                    channels=1,
#                                    rate=FSAMP,
#                                    input=True,
#                                    frames_per_buffer=FRAME_SIZE)
#    
#    stream.start_stream()
#    
#    # Create Hanning window function
#    window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, SAMPLES_PER_FFT, False)))
#    
#    # Print initial text
#    print ('sampling at ', FSAMP, 'Hz with max resolution of ', FREQ_STEP, 'Hz')
#    print('')
#    
#    # As long as we are getting data:
#    while stream.is_active():
#    
#        # Shift the buffer down and new data in
#        buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
#        buf[-FRAME_SIZE:] = np.fromstring(stream.read(FRAME_SIZE), np.int16)
#
#        # Run the FFT on the windowed buffer
#        fft = np.fft.rfft(buf * window)
#    
#        # Get frequency of maximum response in range
#        freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP
#
#        # Get note number and nearest note
#        n = freq_to_number(freq)
#        n0 = int(round(n))
#    
#        # Console output once we have a full buffer
#        num_frames += 1
#    
#        if num_frames >= FRAMES_PER_FFT:
#            print('freq: {:7.2f} Hz     note: {:>3s} {:+.2f}'.format(
#                freq, note_name(n0), n-n0))
#                