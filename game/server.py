import socket
import pickle
import _thread
from game import OnlineGame
import time

host = socket.gethostname()
port = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

games = {}
id_count = 0


def handle_client(clientsocket, clientaddress, game_id, player):
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
