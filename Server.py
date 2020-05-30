import socket
from _thread import *
from RPSgame import Game
import pickle

host="HOST_ID" #Ex: 192.168.1.1
port=5555

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    s.bind((host,port))
except socket.error as e:
    str(e)

s.listen()
print("Server Started, Waiting for the connection")

connect=set()
games={}
idcount=0

def thread_c(conn,p,gameid):
    global idcount
    conn.send(str.encode(str(p)))
    reply=""
    while True:
        try:
            data=conn.recv(4096).decode()
            if gameid in games:
                game=games[gameid]

                if not data:
                    break
                else:
                    if data=="reset":
                        game.reset()
                    elif data!="get":
                        game.play(p,data)
                    reply=game
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break
    print("Connection Lost")
    try:
        del games[gameid]
        print("Game Closed",gameid)
    except:
        pass
    idcount-=1
    conn.close()
while True:
    conn, addr=s.accept()
    print("Connected to:",addr)
    idcount+=1
    p=0
    gameid=(idcount-1)//2
    if idcount%2==1:
        games[gameid]=Game(gameid)
        print("Creating a new game...")
    else:
        games[gameid].ready=True
        p=1

    start_new_thread(thread_c,(conn,p,gameid))
