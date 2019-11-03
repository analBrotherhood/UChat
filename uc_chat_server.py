import uc_chat_util
from uc_chat_util import Hall, Room, Player
import select
import socket
import sys
import pdb

try:
    READ_BUFFER = 8192

    host = sys.argv[1] if len(sys.argv) >= 2 else ''
    listen_sock = uc_chat_util.create_socket((host, uc_chat_util.PORT))

    hall = Hall()
    connection_list = []
    connection_list.append(listen_sock)

    while True:
        read_players, write_players, error_sockets = select.select(connection_list, [], [])
        for player in read_players:
            if player is listen_sock: # new connection, player is a socket
                new_socket, add = player.accept()
                new_player = Player(new_socket)
                connection_list.append(new_player)
                hall.welcome_new(new_player)

            else: # new message
                msg = player.socket.recv(READ_BUFFER)
                if msg:
                    msg = msg.decode().lower()
                    hall.handle_msg(player, msg)
                else:
                    player.socket.close()
                    connection_list.remove(player)

        for sock in error_sockets: # close error sockets
            sock.close()
            connection_list.remove(sock)
except KeyboardInterrupt:
    print('\n\nCancelled. Exiting..')
    listen_sock.close()
    exit()

except SyntaxError:
    print('\n\nAre you try to launch me on python3? My code is created for python 3.X.X, if you launch me using python 2, my code didn\'nt execute successful. Try \'python3\', or contact me: coderusual00@protonmail.com')
    exit()
