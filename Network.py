import socket
import pickle

class Network:
    def __init__(self):
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host="HOST_IP" # Ex: 192.168.1.1
        self.port=5555
        self.addr=(self.host,self.port)
        self.p=self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self,data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
