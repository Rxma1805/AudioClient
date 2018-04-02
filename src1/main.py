from socket import *
from threading import Timer
from threading import Thread
import time
import record

state=True
ID=0
HOST ='192.168.2.19'
PORT = 12345
BUFFSIZE=1024
ADDR = (HOST,PORT)
tctimeClient = socket(AF_INET,SOCK_STREAM)
tctimeClient.connect(ADDR)

def heart_test(client,ID):    
    if(not state):
        return
    client.send("Test".encode())
    ID+=1
    print(str(ID))
    global timer
    timer = Timer(5.0, heart_test, (client,ID))
    timer.start() 
     

t = Timer(5.0,heart_test,(tctimeClient,ID))
t.start()

while True:       
    data = tctimeClient.recv(BUFFSIZE).decode()   
    print(data) 
    if(data == "START"):
        tctimeClient.send("START".encode())   
        if(not record.get_state()):
            start = Thread(target=record.my_record)
            start.start()
    elif(data == "STOP"):
        tctimeClient.send("STOP".encode())
        stop = Thread(target=record.stop)
        stop.start()
    elif(data == "PLAY"):
        tctimeClient.send("PLAY".encode())   
        play = Thread(target=record.play) 
        play.start()
    elif(data == "EXIT"):
        state=False
        tctimeClient.send("EXIT".encode())
        t.cancel()
        break
    else:
        continue   

# while True:       
#     data = tctimeClient.recv(BUFFSIZE).decode()   
#     print(data) 
#     if(data == "START"):
#         tctimeClient.send("START".encode())   
#         if(not recoder.get_state()):
#             recoder.my_record()
#     elif(data == "STOP"):
#         tctimeClient.send("STOP".encode())
#         recoder.stop()
#     elif(data == "PLAY"):
#         tctimeClient.send("PLAY".encode())    
#         recoder.play()
#     elif(data == "EXIT"):
#         state=False
#         tctimeClient.send("EXIT".encode())
#         t.cancel()
#         break
#     else:
#         continue      
          
tctimeClient.close()