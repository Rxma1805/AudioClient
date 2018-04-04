from socket import *
from threading import Timer
from threading import Thread
import time
import sys
sys.path.append("../tools")
import record
import sendAudioRealTime
import threading 


HOST ='192.168.2.19'
PORT = 12345
FILE_PORT = 12347
BUFFSIZE=1024
ADDR = (HOST,PORT) 
real_stream=[]    
   
while True:    
    state=False       
    while not state:
        try:
            tctimeClient = socket(AF_INET,SOCK_STREAM)
            tctimeClient.connect(ADDR)            
        except:
            state = False
            continue        
        state=True
        print("server connected successful!")
    
    
    dispose_event = threading.Event() 
    
    while True:       
        try:
            data = tctimeClient.recv(BUFFSIZE).decode()
        except:
            break   
        if(not data ):
            break
         
        elif(data.find("START") != -1):#CMD_START_DESTIP_SRCIP
            tctimeClient.send(data.encode(encoding='utf_8'))             
            rec = record.recorder(HOST,FILE_PORT,dispose_event)            
            if(not rec.get_state()):
                start = Thread(target=rec.my_record)
                start.start()
        elif(data.find("PLAY") != -1):
            tctimeClient.send(data.encode(encoding='utf_8'))  
            stop_real_time = threading.Event()
            real_stream = sendAudioRealTime.RealTimeStream(tctimeClient,dispose_event,stop_real_time)
            if(not real_stream.get_state()):
                play = Thread(target=real_stream.real_time_play,args=(data.split('_')[3],))
                play.start()
    #         play = Thread(target=record.play) 
    #         play.start()
        elif(data.find("STOP") != -1):                     
            if(real_stream.get_state()):
                stop_real_time.set()
            time.sleep(1)
            tctimeClient.send(data.encode(encoding='utf_8'))   
        
        elif(data.find("EXIT") != -1):
            state=False
            tctimeClient.send(data.encode(encoding='utf_8'))
            dispose_event.set()
            break      
    
