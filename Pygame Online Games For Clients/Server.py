"""Pygame Online Tutorial Part-2"""
import socket
from _thread import *
import sys
from player import Player
from game import *
import pickle
from game import Game

server = "192.168.43.204"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started....")

connected = set()
games = []

idcount = 0


def threaded_client(conn, p, gameId):
    global idcount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameID in games:
                games = games[gameID]

                if not data:
                    break
                else:
                    if data == "Reset":
                        Game.resetWent()
                    elif data != "Get":
                        Game.play(p, data)

                    reply = games
                    conn.sendall(pickle.dumps(reply))
            else:
                break

        except:
            break

    print("Lost Connection")
    print("Closing Game",gameId)
    try:
        del games[gameID]
    except:
        pass
    idcount -= 1
    conn.close()
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idcount += 1
    p = 0
    gameID = (idcount - 1) // 2
    if idcount % 2 == 1:
        games[gameID] = Game(gameID)
        print("Creating a new Game...")
    else:
        games[gameID].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameID))
