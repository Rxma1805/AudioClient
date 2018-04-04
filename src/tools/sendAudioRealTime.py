import wave
from pyaudio import PyAudio,paInt16
import os 
import subprocess
from threading import Timer
import socket
import sys

class RealTimeStream(object):
    
    def __init__(self,tctimeClient,dispose_signal,stop_real_time):
        self.is_succeeeful_client = False
        self.state=False#network occupy state
        self.framerate=8000
        self.NUM_SAMPLES=2000
        self.channels=1
        self.sampwidth=2        
        self.isRecord=False
#         self.IP=IP
#         self.PORT=PORT
        self.dispose_signal = dispose_signal #init is False
        self.stop_event = stop_real_time
        self.tcp_clent = tctimeClient
     
    
    def connect(self):
        while not self.is_succeeeful_client:
            try:
                self.tcp_clent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.tcp_clent.connect((self.IP,self.PORT))
#             except ConnectionRefusedError:
#                 self.is_succeeeful_client = False
#                 continue
#             except TimeoutError:
#                 self.is_succeeeful_client = False
#                 continue
            except :
                self.is_succeeeful_client = False
                continue
        
            self.is_succeeeful_client = True   
            print("real_time stream create successful!")
        
    
    
    def real_time_play(self,srcIp):
        try:
            self.isRecord=True
            pa=PyAudio()
            stream=pa.open(format = paInt16,channels=self.channels,
                           rate=self.framerate,input=True,
                           frames_per_buffer=self.NUM_SAMPLES) 
            while (True):
                try:                    
                    if self.stop_event.isSet():
                        break
                    if self.dispose_signal.isSet():
                        break            
                    string_audio_data = stream.read(self.NUM_SAMPLES)
                    try:    
                        self.tcp_clent.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,4096)                    
                        self.tcp_clent.send(("DATA_"+srcIp+"_").encode()+string_audio_data)
                    except:
                        
                        print(sys.exc_info())
                        break
                except:
                    print(sys.exc_info())
                    break
            print("stop real time send!")
            stream.close()
            self.isRecord=False 
        except:
            self.isRecord=False 
            print("please check audio card!open filed!") 
                  
            

    def get_state(self):  
        return self.isRecord
    
    def get_network_state(self):
        return self.state