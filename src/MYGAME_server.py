from time import sleep, localtime, time
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

import socket
import pygame
import toolbox

from lobbyAvatar import LobbyAvatar

class ClientChannel(Channel):
    """
    This is the server representation of a single connected client.
    """

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.number = 0
        self.lobby_avatar = None
        self.color = None

    def Close(self):
        self._server.DelPlayer(self)

    def is_Valid(self):
        return self.number >= 1 and self.number <= 5

    #####################################
    ### Server-side Network functions ###
    #####################################

    """
    Each one of these "Network_" functions defines a command
    that the client will ask the server to do.
    """

    def Network_hi(self, data):
        """
        Network_hi just prints a message
        """
        print("OMG a client just said hi to me")

    def Network_keys(self, data):
        """send the keys that are being pressed."""
        if self.lobby_avatar:
            self.lobby_avatar.HandleInput(data["keys"])


class MyGameServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        """
        Server constructor function. This is the code that runs once
        when the server is made.
        """
        Server.__init__(self, *args, **kwargs)
        self.clock = pygame.time.Clock()
        self.players = WeakKeyDictionary()

        self.game_width = 1000
        self.game_height = 650

        self.LOBBYCOORDS = [None, (300, 200), (400, 200), (500, 200), (600, 200), (700, 200)]
        self.COLORS = [None, (255,0,0), (0, 255, 0), (0,0,255), (255,255,0), (0,255,255)]

        self.in_lobby = True

        print('Server launched')

    def Connected(self, player, addr):
        """
        Connected function runs every time a client
        connects to the server.
        """
        self.players[player] = True
        self.AssignNumber(player)
        if player.is_Valid():
            self.AssignLobbyAvatar(player)
            self.AssignColor(player)
            print("Player " + str(player.number) + " joined from " + str(addr))
            self.PrintPlayers()
        else:
            player.Send({"action": "disconnected"})
            print("Extra player kicked; sorry!")
    def AssignNumber(self, player):
        if self.in_lobby:
            numbers_in_use = [p.number for p in self.players]
            new_number = 1
            found_it = False
            while not found_it:
                if new_number in numbers_in_use:
                    new_number += 1
                else:
                 found_it = True
            player.number = new_number
        else:
            player.number = -1


    def AssignLobbyAvatar(self, player):
        player.lobby_avatar = LobbyAvatar(self.LOBBYCOORDS[player.number])
    def AssignColor(self, player):
        player.color = self.COLORS[player.number]

    def StartGame(self):
        self.in_lobby = False

    def DelPlayer(self, player):
        """
        DelPlayer function removes a player from the server's list of players.
        In other words, 'player' gets kicked out.
        """
        del (self.players[player])
        print("Deleting Player" + str(player.addr))
        self.PrintPlayers()

    def PrintPlayers(self):
        """
        PrintPlayers prints the number of each connected player.
        """
        print("players: ", [p.number for p in self.players])

    def SendToAll(self, data):
        """
        SendToAll sends 'data' to each connected player.
        """
        for p in self.players:
            p.Send(data)

    def Update(self):
        """
        Server Update function. This is the function that runs
        over and over again.
        """
        self.Pump()

        self.SendToAll({"action": "draw_background"})

        if self.in_lobby:
            all_ready = True
            for p in self.players:
                if p.is_Valid():
                    self.SendToAll({"action": "draw_avatar",
                                    "coords": p.lobby_avatar.coords,
                                    "ready": p.lobby_avatar.ready,
                                    "number": p.number,
                                    "color": p.color})
                    if not p.lobby_avatar.ready:
                        all_ready = False
            if all_ready and len(self.players) >= 1:
                self.StartGame()


        self.SendToAll({"action": "flip"})

        self.clock.tick(30)


ip = toolbox.getMyIP()
port = 5555
server = MyGameServer(localaddr=(ip, port))
print("host ip: " + ip)

"""This is the loop that keeps going until the server is killed"""
while True:
    server.Update()
