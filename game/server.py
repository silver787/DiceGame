import socket
import pickle
import _thread
import time


HOST = socket.gethostname()
PORT = 65432

games = {}
id_count = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

def handle_client(client_socket, client_address, game_id, player):


if __name__ == '__main__'
    while True:
        time.sleep(0.1)
        conn, addr = s.accept()

        id_count += 1
        game_id = (id_count - 1) // 2
        if id_count % 2 == 1:
            games[game_id] = OnlineGame(game_id)
            p = 1

        else:
            games[game_id].ready = True
            p = 2

        _thread.start_new_thread(handle_client, (conn, addr, game_id, p))
