## Author: Aaron Ennis
## Title: Music Application
##
## Description: 
## A music application that allows the user to record/play back WAV files.
## The application transcribes the audio data from the WAV files and
## transcribes the notes to tabliture form and displays it.
#______________________________________________________________________________

import wave, struct, os, time, json
import scipy.io.wavfile
import pyaudio
import numpy as np
from array import array
from struct import pack


def info(_file):
    #Current working dir
    cwd = os.getcwd()  
    existing_files = os.listdir(cwd + '\Recordings')
    if _file in existing_files:
        file_path = os.path.join(cwd + '\Recordings', _file)    
        #open a wav format music  
        f = wave.open(file_path,"rb")  
    
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
    else:
        print('This file does not exist')
    
#plays audio
def play(_file):
    #Current working dir
    cwd = os.getcwd() 
    existing_files = os.listdir(cwd + '\Recordings')
    if _file in existing_files:      
        file_path = os.path.join(cwd + '\Recordings', _file)
        
        #open a wav format music  
        f = wave.open(file_path,"rb")  
        
        #define stream chunk   
        chunk = 1024 
        
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
    else:
        print('This file does not exist')

        
def delete(_file):
    #Current working dir
    cwd = os.getcwd()
    existing_files = os.listdir(cwd + '\Recordings')
    tab = _file[:-4]
    tab = tab + '.json'
    if _file in existing_files:
        file_path = os.path.join(cwd + '\Recordings', _file)
        tab_file_path = os.path.join(cwd + '\Tabs', tab)
        if os.path.isfile(file_path) and os.path.isfile(tab_file_path):
            os.unlink(file_path)
            os.unlink(tab_file_path)
        else:
            pass
    else:
        print('This file does not exist')

def check_tab():
    #Current working dir
    cwd = os.getcwd()
    existing_files = os.listdir(cwd + '\Recordings')
    if len(os.listdir(cwd + '\Tabs')) > 0:
        existing_tabs = os.listdir(cwd + '\Tabs')
        tabs = []
        files = []
        for t in existing_tabs:
            t=t[:-5]
            tabs.append(t)
        for f in existing_files:
            f=f[:-4]
            files.append(f)   
            
        for t in tabs: 
            if t not in files:
                tab_file_path = os.path.join(cwd + '\Tabs', t + '.json')
                if os.path.isfile(tab_file_path):
                    os.unlink(tab_file_path)
            else:
                pass
    else:
        pass
    
def get_tab(_file):
    #strings on the guitar
    e = ''  
    B = ''
    G = ''
    D = ''
    A = ''
    E = ''
    #Current working dir
    cwd = os.getcwd()
    existing_tabs = os.listdir(cwd + '\Tabs')
    json_file = _file[:-4] + '.json'
    if len(os.listdir(cwd + '\Tabs')) > 0:
        if json_file in existing_tabs:
            with open(os.path.join(cwd + '\Tabs', '%s' % (json_file)), 'r') as f:
                data = json.load(f)
        
            if json_file in os.listdir(cwd + '\Tabs'):
                notes = []
                count = 0
                tab = []
                #gets every fourth note
                for v in data.values():
                    notes.append(v)
                for i in notes:
                    if count == 3:
                        tab.append(i)
                        count = 0
                    else:
                        count += 1   
                #Creating the tab        
                for n in tab:   
                    if n[0] == 'A':                 #Note
                        if n[-1:] == '3':           #Octave
                            e = e + '- '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '0 '
                            E = E + '- '
                        elif n[-1:] == '4':
                            e = e + '- '
                            B = B + '- '
                            G = G + '2 '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                        elif n[-1:] == '5':
                            e = e + '5 '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                            
                    elif n[0] == 'A#':
                        if n[-1:] == '3':
                            e = e + '- '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '1 '
                            E = E + '- '
                        elif n[-1:] == '4':
                            e = e + '- '
                            B = B + '- '
                            G = G + '3 '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                        elif n[-1:] == '5':
                            e = e + '6 '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                            
                    elif n[0] == 'B':
                        if n[-1:] == '3':
                            e = e + '- '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '2 '
                            E = E + '- '
                        elif n[-1:] == '4':
                            e = e + '- '
                            B = B + '- '
                            G = G + '4 '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                        elif n[-1:] == '5':
                            e = e + '7 '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                            
                    elif n[0] == 'C':
                        if n[-1:] == '3':
                            e = e + '- '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '3 '
                            E = E + '- '
                        elif n[-1:] == '4':
                            e = e + '- '
                            B = B + '- '
                            G = G + '5 '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                        elif n[-1:] == '5':
                            e = e + '8 '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                            
                    elif n[0] == 'C#':
                        if n[-1:] == '3':
                            e = e + '- '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '4 '
                            E = E + '- '
                        elif n[-1:] == '4':
                            e = e + '- '
                            B = B + '- '
                            G = G + '6 '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                        elif n[-1:] == '5':
                            e = e + '9 '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                            
                    elif n[0] == 'D':
                        if n[-1:] == '3':
                            e = e + '- '
                            B = B + '- '
                            G = G + '- '
                            D = D + '0 '
                            A = A + '- '
                            E = E + '- '
                        elif n[-1:] == '4':
                            e = e + '- '
                            B = B + '3 '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                        elif n[-1:] == '5':
                            e = e + '10 '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                            
                    elif n[0] == 'D#':
                        if n[-1:] == '3':
                            e = e + '- '
                            B = B + '- '
                            G = G + '- '
                            D = D + '1 '
                            A = A + '- '
                            E = E + '- '
                        elif n[-1:] == '4':
                            e = e + '- '
                            B = B + '4 '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                        elif n[-1:] == '5':
                            e = e + '11 '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                            
                    elif n[0] == 'E':
                        if n[-1:] == '3':
                            e = e + '- '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '0 '
                        elif n[-1:] == '4':
                            e = e + '- '
                            B = B + '- '
                            G = G + '- '
                            D = D + '2 '
                            A = A + '- '
                            E = E + '- '
                        elif n[-1:] == '5':
                            e = e + '0 '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                            
                    elif n[0] == 'F':
                        if n[-1:] == '3':
                            e = e + '- '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '1 '
                        elif n[-1:] == '4':
                            e = e + '- '
                            B = B + '- '
                            G = G + '- '
                            D = D + '3 '
                            A = A + '- '
                            E = E + '- '
                        elif n[-1:] == '5':
                            e = e + '1 '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- ' 
                            
                    elif n[0] == 'F#':
                        if n[-1:] == '3':
                            e = e + '- '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '2 '
                        elif n[-1:] == '4':
                            e = e + '- '
                            B = B + '- '
                            G = G + '- '
                            D = D + '4 '
                            A = A + '- '
                            E = E + '- '
                        elif n[-1:] == '5':
                            e = e + '2 '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                            
                    elif n[0] == 'G':
                        if n[-1:] == '3':
                            e = e + '- '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '3 '
                        elif n[-1:] == '4':
                            e = e + '- '
                            B = B + '- '
                            G = G + '0 '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                        elif n[-1:] == '5':
                            e = e + '3 '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                            
                    elif n[0] == 'G#':
                        if n[-1:] == '3':
                            e = e + '- '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                        elif n[-1:] == '4':
                            e = e + '- '
                            B = B + '- '
                            G = G + '1 '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- '
                        elif n[-1:] == '5':
                            e = e + '4 '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- ' 
                    elif n[0] == '-': 
                            e = e + '- '
                            B = B + '- '
                            G = G + '- '
                            D = D + '- '
                            A = A + '- '
                            E = E + '- ' 
                         
                return e,B,G,D,A,E
                        
        else:
            e = e + '-'
            B = B + '-'
            G = G + 'No Tab Found'
            D = D + '-'
            A = A + '-'
            E = E + '-' 
            return e,B,G,D,A,E
    else:
        e = e + '-'
        B = B + '-'
        G = G + 'No Tab Found'
        D = D + '-'
        A = A + '-'
        E = E + '-' 
        return e,B,G,D,A,E
    

def record(_recording_lenght):        
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

    #frequency to MIDI number    
    def freq_to_number(f): return 76 + 12 * np.log2(f / 659.255)
    
    #MIDI number to frequency    
    def number_to_freq(n): return 659.255 * 2.0**((n - 76) / 12.0)
    
    #Gets the names of the notes + octaves    
    def note_name(n):
        return NOTE_NAMES[n % NOTE_MIN % len(NOTE_NAMES)] + str(int(n / 12 - 1))
    
    #Gets discrete FFT bin
    def note_to_fftbin(n): return number_to_freq(n) / FREQ_STEP
    
    #Gets real Min and Max freq
    imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN - 1))))
    imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX + 1))))
    
    # Allocate space to run an FFT. 
    buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
    num_frames = 0
        
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
    notes = {}
    num_frames = 0
    print('recording')
    #normalizes the audio to reduce white noise
    audio_normalize = 'normalize.wav'
    root = 'C:/Users/aaron/Desktop/Music-Application/Static'
    normalize_rate, normalize_data = scipy.io.wavfile.read(os.path.join(root, audio_normalize)) 
    snd_data = array('h', normalize_data)
    r.extend(snd_data)
    #records for x amount of seconds
    while elapsed < _recording_lenght:
        elapsed = time.time() - start 
        read = np.fromstring(stream.read(FRAME_SIZE), np.int16)
        # Shift the buffer down and new data in
        buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
        buf[-FRAME_SIZE:] = read

        snd_data = array('h', read)

        r.extend(snd_data)
        idx = np.abs(read).argmax()

        if np.abs(read[idx]) > 300:
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
            notes[elapsed] = note_name(n0)
        else:
            print ('---')
            notes[elapsed] = '---'
    
    return notes, len(normalize_data), r, p, stream

def create_file(_file, _notes, _normalize_data_lenght, r, p, stream):
    #Current working dir
    cwd = os.getcwd()
    FSAMP = 22050       # Sampling frequency in Hz
    
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
        
    sample_width = p.get_sample_size(pyaudio.paInt16)
    stream.stop_stream()
    stream.close()
    p.terminate() 
    r = normalize(r)
    #removes the normalizing sound
    r = r[_normalize_data_lenght:] 
    
    path = os.path.join(cwd + '\Recordings', _file)
    record_to_file(path,r,sample_width)
    
    json_data = {}
    json_data[_file] = _notes
    #create JSON
    with open(os.path.join(cwd+ '\Tabs', '%s.json' % (_file[:-4])), 'w') as f:
        json.dump(_notes, f)

     