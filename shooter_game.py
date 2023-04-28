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

class Enemy(Gamesprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(5, 630)
            self.speed = randint(1, 7)
            lost += 1

class Bullet(Gamesprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <0:
            self.kill()

font.init()
font1 = font.SysFont('Calibri', 40)



space_ship = Player('rocket.png', 300, 435,65,65, 5)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(5, 630), -40,65,65 ,randint(1, 7))
    monsters.add(monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(5, 630), -40,65,65 ,randint(1, 7))
    asteroids.add(asteroid)

finish = False
game = True
kills = 0
lifes = 10
num_fire = 0
rel_time = False

y = 0
y1 = -500

while game:
    print(clock.get_fps())

    for e in event.get():
        if e.type==QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    space_ship.fire()
                    fire.play()
                    num_fire +=1
                if num_fire >= 10 and rel_time ==False:
                    start =timer()
                    rel_time = True  

    if finish != True:
        window.blit(background, (0, y))
        y += 2
        window.blit(background, (0, y1))
        y1 += 2

        if y > 500:
            y = -500
        if y1 > 500:
            y1 = -500

        space_ship.reset()
        space_ship.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()

        if rel_time == True:
            end = timer()
            if end - start >= 3:
                num_fire = 0
                rel_time = False
            else:
                rel = font1.render("ПЕРЕЗАРЯДКА", True, (255,0,255))
                window.blit(rel, (230 , 300))

        lifes_text = font1.render("Жизни:"+str(lifes), True,(255,255,255))
        window.blit(lifes_text,(540,5))
        text_lost = font1.render('Пропущено: '+str(lost), True, (255,255,255))
        window.blit(text_lost, (5, 5))

        if sprite.spritecollide(space_ship, monsters, False) or sprite.spritecollide(space_ship, asteroids, False):
            sprite.spritecollide(space_ship, monsters, True)
            sprite.spritecollide(space_ship, asteroids, True)
            monster = Enemy('ufo.png', randint(5, 630), -40,65,65 ,randint(1, 7))
            monsters.add(monster)
            asteroid = Enemy('asteroid.png', randint(5, 630), -40,65,65 ,randint(1, 7))
            asteroids.add(asteroid)
            lifes -= 1
            

        if lifes <= 0 or lost >= 10:
            game_over = font1.render('YOU_LOST!', True, (255, 0, 0))
            window.blit(game_over, (260, 200))
            finish = True
            mixer.music.stop()

        lifes_text = font1.render("Жизни:"+str(lifes), True,(255,255,255))
        window.blit(lifes_text,(540,5))
        text_lost = font1.render('Пропущено: '+str(lost), True, (255,255,255))
        window.blit(text_lost, (5, 5))

        collides = sprite.groupcollide(bullets, monsters, True, True)
        for c in collides:
            kills += 1
            monster = Enemy('ufo.png', randint(5, 630), -40,65,65 ,randint(1, 7))
            monsters.add(monster)
        kills_text = font1.render('Уничтожено:' + str(kills),True, (255, 255, 255))
        window.blit(kills_text,(5,40))

        if kills >= 10:
            win_text = font1.render('YOU_WIN!', True, (0, 255, 0))
            window.blit(win_text, (260, 200))
            finish = True
            mixer.music.stop()

    clock.tick(FPS)
    display.update()
