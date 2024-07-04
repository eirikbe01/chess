import pygame

class Sound:

    def __init__(self, path):
        self.path = path
        self.sound = pygame.mixer.Sound(path)


    # Methods which plays the sound when piece is moved
    def play(self):
        pygame.mixer.Sound.play(self.sound)
