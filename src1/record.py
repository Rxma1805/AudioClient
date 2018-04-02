import wave
import threading
from pyaudio import PyAudio,paInt16
import os 
import subprocess
import timer

framerate=8000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=2
isRecord=False
chunk=2048
    
def save_wave_file(filename,data):
    global framerate    
    global channels
    global sampwidth    
    global isRecord
    
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()



def my_record():    
    global isRecord  

    
    isRecord=True
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=channels,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]   
    while (True):
        if not get_state():
            break            
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)        
        print('.')
    save_wave_file('1.wav',my_buf)
    stream.close()    
    print("stop record!")

def get_state():    
    global isRecord
    return isRecord

def stop():       
    global isRecord 
    isRecord=False
    
def play():     
    global chunk  
     
    wav = "1.wav"
    cmd = 'lame --preset insane %s' % wav        
    subprocess.call(cmd, shell=True)   
     
    wf=wave.open(r"1.wav",'rb')
    p=PyAudio()
    stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),
                  channels=wf.getnchannels(),
                  rate=wf.getframerate(),
                  output=True)
    while True:
        data=wf.readframes(chunk)
        if data=="":
            break
        stream.write(data)
    stream.close()
    p.terminate()
    print('Over!') 