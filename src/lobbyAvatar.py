import pygame
import toolbox

class LobbyAvatar():
    def __init__(self, coords):
        self.coords = coords
        self.ready = False

        self.ready_key = toolbox.keyDownListener()

    def HandleInput(self, keys):
        self.ready_key.update(keys[pygame.K_SPACE])
        if self.ready_key.down:
            self.ready = not self.ready