import uc_chat_util
from uc_chat_util import Room, Hall, Player
import select
import socket
import sys

try:
    READ_BUFFER = 8192
    
    if len(sys.argv) < 2:
        print('Missing argument.', file=sys.stderr)
        sys.exit(1)
    else:
        server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_connection.connect((sys.argv[1], uc_chat_util.PORT))

    def prompt():
        print('> ', end=' ', flush = True)

    print('\nSuccessful connecting to the server #0!\n')
    msg_prefix = ''

    socket_list = [sys.stdin, server_connection]

    while True:
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        for s in read_sockets:
            if s is server_connection: # incoming message 
                msg = s.recv(READ_BUFFER)
                if not msg:
                    print('\n\nError 0xFUUUUUCK\nServer down!')
                    sys.exit(2)
                else:
                    if msg == uc_chat_util.QUIT_STRING.encode():
                        sys.stdout.write('\n\nHave a good time!\n')
                        sys.exit(2)
                    else:
                        sys.stdout.write(msg.decode())
                        if 'Please, enter you nickname below' in msg.decode():
                            msg_prefix = 'below: ' # identifier for name
                        else:
                            msg_prefix = ''
                        prompt()

            else:
                msg = msg_prefix + sys.stdin.readline()
                server_connection.sendall(msg.encode())

except KeyboardInterrupt:
    print('\n\nCancelled by user. Exiting...')
    exit()

except OSError:
    print('\nInvalid argument. Please, make sure what you are using programm correctly.\n\nUsage: python (or python3, if on \'python\' starting python2) uc_chat_client.py <host_ip>. Example: \n\t python3 uc_chat_client.py 127.0.0.1')
    exit()

except ConnectionRefusedError:
    print('\nConnection refused. Please, make sure what host ip address what you trying to connect is entered correctly. \nIf you trying to connect to remote machine, who run \'uc_chat_server.py\', contact with the administrator of remote network: is 8767 port opened for remote connections?')
    exit()

except socket.gaierror:
    print('\nUnknown name or service. Please, re-enter host IP address correctly.')
    exit()

except SyntaxError:
    print('\nAre you try to launch me on python3? My code is created for python 3.X.X, if you launch me using python 2, my code didn\'nt execute successful. Try \'python3\', or contact me: coderusual00@protonmail.com')
    exit()
