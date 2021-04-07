import socket
# socket is used for networking and sending information over the internet
import pickle
# pickle is used for converting objects into bytes that can be sent over the internet
import _thread
# _thread is used for creating seperate threads for clients that connect to the server(this file)
from data.game_classes import OnlineGame
# OnlineGame has all the classes that the server and clients use to communicate with eachother
import time
# time is used to slow down the execution of loops within the program, to reduce CPU strain

host = socket.gethostname()
# gets the name of the host used for creating their socket
port = 65432
# specifies the port number used for communication

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
# the creation of the socket itself

games = {}
id_count = 0
# variables that keep track of the games currently in play


def handle_client(clientsocket, clientaddress, game_id, player):
    """A fucntion that's threaded each time a new client connects, to allow the server to communicate with them"""
    global id_count
    clientsocket.send(str.encode(str(p)))
    if player == 0:
        games[game_id].player_one_name = clientsocket.recv(2048).decode()
    elif player == 1:
        games[game_id].player_two_name = clientsocket.recv(2048).decode()

    while True:
        time.sleep(0.1)
        try:
            if games[game_id].ready:

                if games[game_id].player_one_name == games[game_id].player_two_name:
                    break

                clientsocket.sendall(pickle.dumps(games[game_id]))
                data = pickle.loads(clientsocket.recv(2048))
                if player == games[game_id].player_turn:
                    games[game_id] = data
                else:
                    pass
            else:
                clientsocket.sendall(pickle.dumps(games[game_id]))
                clientsocket.recv(2048)

        except:
            break

    try:
        del games[game_id]
    except:
        pass
    id_count -= 1
    clientsocket.close()


while True:
    # the infinite loop that keeps listening for clients and allows them to connect
    time.sleep(0.1)
    conn, addr = s.accept()

    id_count += 1
    game_id = (id_count - 1) // 2
    if id_count % 2 == 1:
        games[game_id] = OnlineGame(game_id)
        p = 0

    else:
        games[game_id].ready = True
        p = 1

    _thread.start_new_thread(handle_client, (conn, addr, game_id, p))

s.close()
# closes the socket once the main part of the program is over
