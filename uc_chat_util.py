import socket 
import pdb

try:
    MAX_CLIENTS = 30
    PORT = 8767
    QUIT_STRING = '<$quit$>'
    isAlreadyConnect = 0
    
    def create_socket(address):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setblocking(0)
        s.bind(address)
        s.listen(MAX_CLIENTS)
        print('Server successful started at ', address)
        return s

    class Hall:
        def __init__(self):
            self.rooms = {} # {room_name: Room}
            self.room_player_map = {} # {playerName: roomName}

        def welcome_new(self, new_player):
            new_player.socket.sendall(b'\n<Usu4lC0d3r ch4t>\nMaximum Clients: 30\n\nWelome to the chat, %username%! Please, enter you nickname below:\n')

        def list_rooms(self, player):
            
            if len(self.rooms) == 0:
                msg = 'There is no active rooms currently. Create your own!\n' \
                    + 'Use [<join> room_name] to create a room, or connect, if room with the same name already exist.\n'
                player.socket.sendall(msg.encode())
            else:
                msg = 'Listing current rooms...\n'
                for room in self.rooms:
                    msg += room + ': ' + str(len(self.rooms[room].players)) + ' user(s)\n'
                player.socket.sendall(msg.encode())
        
        def handle_msg(self, player, msg):
            
            instructions = b'[MANUAL]:\n'\
                + b'[<list>] to list all rooms\n'\
                + b'[<join> room_name] to join/create/switch to a room\n' \
                + b'[<help>] to show this manual\n' \
                + b'[<quit>] or [<exit>] to leave\n' \
                + b'Otherwise start typing and enjoy!' \
                + b'\n'

            print(player.name + ' send: ' + msg)
            if 'below:' in msg:
                name = msg.split()[1]
                player.name = name
                print('New chat member:  ', player.name)
                player.socket.sendall(instructions)
            
            elif '<join>' in msg:
                same_room = False
                if len(msg.split()) >= 2: # error check
                    room_name = msg.split()[1]
                    if player.name in self.room_player_map: # switching?
                        if self.room_player_map[player.name] == room_name:
                            player.socket.sendall(b'You are already in room: ' + room_name.encode())
                            same_room = True
                        else: # switch
                            old_room = self.room_player_map[player.name]
                            self.rooms[old_room].remove_player(player)
                    if not same_room:
                        if not room_name in self.rooms: # new room:
                            new_room = Room(room_name)
                            self.rooms[room_name] = new_room
                        self.rooms[room_name].players.append(player)
                        self.rooms[room_name].welcome_new(player)
                        self.room_player_map[player.name] = room_name
                else:
                    player.socket.sendall(instructions)

            elif '<list>' in msg:
                self.list_rooms(player) 

            elif '<help>' in msg:
                player.socket.sendall(instructions)
            
            elif '<quit>' in msg:
                player.socket.sendall(QUIT_STRING.encode())
                self.remove_player(player)

            elif '<exit>' in msg:
                player.socket.sendall(QUIT_STRING.encode())
                self.remove_player(player)


            #pntexp easter egg :>
            elif ('<planetexpress>' and '<reunion>') in msg:
                player.socket.sendall(b'\nPlanet express? Hmm..\nIf you are a part of this good team, i love you! Or if you just a dirty cocksucker, so fuck you! How you even find this??\nFuck, we are like USSR. So we have new chat - reunion!')

            #my nickname is easter egg too :>
            elif '<usu4lc0d3r>' in msg:
                player.socket.sendall(b'\nI heard about this programmer. https://usu4lc0d3r.su, updates soon!\n')

            else:
                # check if in a room or not first
                if player.name in self.room_player_map:
                    self.rooms[self.room_player_map[player.name]].broadcast(player, msg.encode())
                else:
                    msg = 'You are currently not in any room! \n' \
                        + 'Use [<list>] to see available rooms! \n' \
                        + 'Use [<join> room_name] to join a room! \n'
                    player.socket.sendall(msg.encode())
        
        def remove_player(self, player):
            if player.name in self.room_player_map:
                self.rooms[self.room_player_map[player.name]].remove_player(player)
                del self.room_player_map[player.name]
            print(player.name + ' has left the room\n')

        
    class Room:
        def __init__(self, name):
            self.players = [] # a list of sockets
            self.name = name

        def welcome_new(self, from_player):
            msg = self.name + ' welcomes: ' + from_player.name + '\n'
            for player in self.players:
                player.socket.sendall(msg.encode())
        
        def broadcast(self, from_player, msg):
            msg = from_player.name.encode() + b': ' + msg
            for player in self.players:
                player.socket.sendall(msg)

        def remove_player(self, player):
            self.players.remove(player)
            leave_msg = player.name.encode() + b' has left the room\n'
            self.broadcast(player, leave_msg)

    class Player:
        def __init__(self, socket, name = '0xDF'):
            socket.setblocking(0)
            self.socket = socket
            self.name = name

        def fileno(self):
            return self.socket.fileno()
        
except SyntaxError:
    print('Завали ебучку, тупой удав, XD')
    exit()
