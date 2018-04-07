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
import matplotlib.pyplot as plt
from array import array
from struct import pack

#elements in data (16-bit PCM	-32768	+32767	int16)
def getData(_file): 
    #Current working dir
    cwd = os.getcwd()
    existing_files = os.listdir(cwd + '\Recordings')
    if _file in existing_files:
        rate, data = scipy.io.wavfile.read(os.path.join(cwd + '\Recordings', _file))
        for i in data:
            print(i)
    else:
        print('This file does not exist')

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

#Displays audio data to graph    
def display(_file,sec):
    #Current working dir
    cwd = os.getcwd()
    existing_files = os.listdir(cwd + '\Recordings')
    if _file in existing_files:
        rate, data = scipy.io.wavfile.read(os.path.join(cwd + '\Recordings', _file))
        t = np.linspace(0, sec, len(data))   
        plt.plot(t,data)    
        plt.show()
    else:
        print('This file does not exist')  
        
def remove_key(d, key):
    r = dict(d)
    del r[key]
    return r
        
def delete(_file):
    #Current working dir
    cwd = os.getcwd()
    existing_files = os.listdir(cwd + '\Recordings')
    
    for i in existing_files:
        file_path = os.path.join(cwd + '\Recordings', _file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
            
            with open(os.path.join(cwd + '\Tabs', 'tabs.json'), 'r') as f:
                data = json.load(f) 
            
            data = remove_key(data, _file)
            
            with open(os.path.join(cwd + '\Tabs', 'tabs.json'), 'w') as f:
                json.dump(data, f)
        else:
            print('This file does not exist')

def check_tab():
    #Current working dir
    cwd = os.getcwd()
    existing_files = os.listdir(cwd + '\Recordings')
    if len(os.listdir(cwd + '\Tabs')) > 0:
        with open(os.path.join(cwd + '\Tabs', 'tabs.json'), 'r') as f:
            data = json.load(f)
    
        for tab in data.keys(): 
            if tab not in existing_files:
                data = remove_key(data, tab)
                
                with open(os.path.join(cwd + '\Tabs', 'tabs.json'), 'w') as f:
                    json.dump(data, f)
            else:
                pass
    else:
        pass
    
def get_tab(_file):
        #Current working dir
    cwd = os.getcwd()

    if len(os.listdir(cwd + '\Tabs')) > 0:
        with open(os.path.join(cwd + '\Tabs', 'tabs.json'), 'r') as f:
            data = json.load(f)
    
        if _file in data.keys():
            tab = data[_file]
            
            
        else:
            tab = 'Tab does not exist'
            return tab
    else:
        pass
    

def record(): 
    #Current working dir
    cwd = os.getcwd()  
       
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
    while elapsed < 5:
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
    

    sample_width = p.get_sample_size(pyaudio.paInt16)
    stream.stop_stream()
    stream.close()
    p.terminate() 
    r = normalize(r)
    #removes the normalizing sound
    r = r[len(normalize_data):] 
    file = input('File name? ')
    file = file + '.wav'
    existing_files = os.listdir(cwd + "\Recordings")
    
    while file in existing_files:
            print('This file name already in use!')
            file = input('File name? ')
            file = file + '.wav'
            

    path = os.path.join(cwd + '\Recordings', file)
    record_to_file(path,r,sample_width)
    
    cwd = cwd + '\Tabs'    
    existing_files = os.listdir(cwd)
  
    json_data = {}
    json_data[file] = notes
    
    if len(existing_files) == 0:
        #Write notes to JSON
        with open(os.path.join(cwd, 'tabs.json'), 'w') as f:
            json.dump(json_data, f)
        print(notes)
    else:
        #Open JSON file
        with open(os.path.join(cwd, 'tabs.json'), 'r') as f:
            data = json.load(f) 
            
        data.update(json_data)
        
        with open(os.path.join(cwd, 'tabs.json'), 'w') as f:
            json.dump(data, f)
        
        print(data)
     