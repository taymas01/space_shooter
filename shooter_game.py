from pygame import *
from random import *
from time import time as timer

window = display.set_mode((700, 500))
display.set_caption('Шутер')

background = transform.scale(image.load('space3.jpg'), (700, 500))
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.2)
mixer.music.play()

fire = mixer.Sound('fire.ogg')

class Gamesprite(sprite.Sprite):
    def __init__(self, player_image, x, y, widht, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (widht, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 'l'
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Gamesprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 1:
            self.rect.x -= self.speed
        if keys[K_a] and self.rect.x >1:
            self.rect.x -= self.speed

        if keys[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
        if keys[K_d] and self.rect.x < 630:
            self.rect.x += self.speed

        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed

        if keys[K_DOWN] and self.rect.y < 435:
            self.rect.y += self.speed
        if keys[K_s] and self.rect.y <435:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx-10, self.rect.top, 20, 50, 15)
        bullets.add(bullet)                                                                                                                 

lost = 0
