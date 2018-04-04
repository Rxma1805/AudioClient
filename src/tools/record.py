import wave
from pyaudio import PyAudio,paInt16
import os 
import subprocess
from threading import Timer
import socket
import numpy as np
import sys

class recorder(object):
    
    def __init__(self,IP,PORT,signal):
        self.is_succeeeful_client = False
        self.state=False#network occupy state
        self.framerate=8000
        self.numSampls=2048
        self.channels=1
        self.sampwidth=2        
        self.isRecord=False
#         self.chunk=2048
        self.time = 20.0
        self.IP=IP
        self.PORT=PORT
        self.signal = signal #init is False
        self.connect()
     
    
    def connect(self):
        while not self.is_succeeeful_client:
            try:
                self.tcp_clent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.tcp_clent.connect((self.IP,self.PORT))
            except :
                self.is_succeeeful_client = False
                continue
        
            self.is_succeeeful_client = True   
            print("Create audio file send client successful!")
        
    def save_wave_file(self,filename,data):
        wf=wave.open(filename,'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.sampwidth)
        wf.setframerate(self.framerate)
        wf.writeframes(b"".join(data))
        wf.close()
        
    def send_wave_file(self,path,filename,data): 
        try:
            mp3File = path+'/mp3'
            waveFile = path+'/wav'             
            if not os.path.isdir(waveFile):
                os.makedirs(waveFile)   
            if not os.path.isdir(mp3File):
                os.makedirs(mp3File) 
            self.save_wave_file(waveFile+"/"+filename,data)
            self.convert_to_mp3(waveFile,mp3File)            
            self.tcp_clent.send("SEND".encode())
            data = self.tcp_clent.recv(16).decode()  
            self.tcp_clent.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,4096)
            if(data == "OK"):
                try:
                    self.state = True
                    fo = open(mp3File+'/1.mp3','rb')
                    while True:
                        filedata = fo.read(2048)
                        if not filedata:
                            self.tcp_clent.send(b"1END")
                            break
                        self.tcp_clent.send("DATA".encode()+filedata)
                    fo.close()
                except: 
                    print(sys.exc_info())
                
                finally:
                    self.state = False  
                    self.delete_file(waveFile,mp3File)
            elif not data:
                self.connect()
            else:
                pass
                
        except :
            print(sys.exc_info())
    
    def my_record(self):
       
        while True:
            try:
                self.isRecord=True
                try:
                    pa=PyAudio()
                    stream=pa.open(format = paInt16,channels=self.channels,
                               rate=self.framerate,input=True,
                               frames_per_buffer=self.numSampls)
                    my_buf=[]
                    count=0   
                    while (count < self.time * self.framerate/self.numSampls): 
                        try:
                            string_audio_data = stream.read(self.numSampls)#return bytes
                            print(".")
                        except :
                            print(sys.exc_info())
                            break
                        my_buf.append(string_audio_data)                     
                        #temp = np.max(np.fromstring(my_buf,dtype = np.int16))       
                        #print('temp=',temp)#30000
                        count+=1
                    stream.close() 
                    self.stop()
                    if(len(my_buf) >0):
                        self.send_wave_file(os.path.abspath('..')+'/audio','1.wav',my_buf)                       
                        print("stop record!")
                    if self.signal.isSet():
                        print("send file process is dispose!")
                        break
                except:
                    print("please check audio card!open filed! %s" % sys.exc_info())
                    break
            except Exception :
                print("please check audio then resend Start ")
                break
#                 continue

    def get_state(self):  
        return self.isRecord
    
    def get_network_state(self):
        return self.state
    
    def stop(self):      
        self.isRecord=False
        
    def delete_file(self,waveFile,mp3File):
        try:                
            convert = waveFile+'/1.wav  ' + mp3File+'/1.mp3'
            cmd = "rm -rf  %s" % convert 
            subprocess.call(cmd,shell = True)         
            print('delete!') 
        except :
            pass
            
    def convert_to_mp3(self,waveFile,mp3File):  
        try:
                
            convert = waveFile+'/1.wav  ' + mp3File+'/1.mp3'
            cmd = 'lame --preset insane %s' % convert 
            subprocess.call(cmd,shell = True)         
            print('Over!') 
        except :
            pass