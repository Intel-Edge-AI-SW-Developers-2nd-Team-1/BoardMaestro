#pip install pybluez
import bluetooth
import time
import threading
import re
from PyQt5.QtCore import QObject, pyqtSignal

class BluetoothWorker(QObject):
    
    '''
    Class that help Bluetooth connection
    
    Instance : 
        data_receivec = string
        
    Method :
        __init__() : NONE
        callstring() : string
        bluetoothsetup() : NONE
        send_data() : string
        receive_data() : string
    '''
    data_received = pyqtSignal(str)  
    
    def __init__(self, parent=None):
        '''Init parent, connect bluetooth'''
        super().__init__(parent)
        self.socket = self.bluetoothsetup()
        self.str_buf = ""
        self.number = 0
    
    def callstring(self,str_buf):
        '''receive string and store in the str_buf'''
        self.str_buf = str_buf
        
    def bluetoothsetup(self):
        '''setting MACaddress and port and open socekt'''
        serverMACAddress = '98:DA:60:07:A1:3A' 
        port = 1    
        socekt = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        socekt.connect((serverMACAddress, port))
        return socekt

    def send_data(self):
        '''
        read string and send
        
        input : string from str_buf
        output : send to socket
        '''
        while True:
            text = self.str_buf  
            print(text)
            if text.strip(): 
                try:
                    self.socket.send(text + "\r\n")
                except bluetooth.btcommon.BluetoothError as e:
                    print("Bluetooth error:", e)  
                    
            else:
                print("No text to send")
            time.sleep(1)

    def receive_data(self):
        '''
        receive string and store
        
        intput : data from socket and decoding
        output : extract numbers from the received text and stores them in the self.number variable
        '''
        while True:
             received_data = self.socket.recv(1024)
             decoded_data = received_data.decode()

             self.received_text = decoded_data
             
             extracted_number = re.search(r'\d+', self.received_text).group()

             if extracted_number:
                self.number = int(extracted_number)
                print(self.number)
             else:
                print("No number found in the text.")