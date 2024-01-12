from typing import Any
from pygame import *
from random import randint, choice
from time import time as timer
font.init()
font2 = font.Font(None, 36)


window = display.set_mode((800,700))
display.set_caption("шутер")
background = transform.scale(image.load("fon4.jpg"), (800,700))

#mixer.init()
#mixer.music.load('')
#mixer.music.play()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,player_speed, w = 110, h = 130):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y



class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


class Player(GameSprite):
    def update(self):
        keys  = key.get_pressed()
        if keys [K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < win_width - 100:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("kagyne.png", self.rect.centerx, self.rect.top,-15,20,50)
        bullets.add(bullet)

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    

lost = 0
score = 0
goal = 10
max_lost = 15
life = 5

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


         
win_width = 700; win_height = 600
images = ["rise.png", "sysya.png",]





bullets = sprite.Group()
enemyes = sprite.Group()
for i in range(1,6):
    enemy = Enemy(choice(images), randint(200, 600), -40, randint(2,5))
    enemyes.add(enemy)


player = Player('kaneki.png',250,570,20)


font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 50)
win = font2.render('YOU WIN!', True, (255, 255,255))
lose = font2.render('YOU LOSE!', True, (180, 0,0))


clock = time.Clock()
FPS = 60

game = True
finish = False
while game:
    window.blit(background,(0,0))

    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    if not finish:
        window.blit(background,(0,0))
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (0,0,0))
        window.blit(text_lose, (10,20))
        text_winn = font1.render('Зібрано: ' + str(score), 1, (0,0,0))
        window.blit(text_winn, (30,50))
        player.update()
        enemyes.update()
        bullets.update()
  
        player.reset()
        enemyes.draw(window)
        bullets.draw(window)

        if sprite.groupcollide(enemyes, bullets, True, True):
            score = score + 1
            enemy = Enemy(choice(images), randint(200, 600), -40, randint(2,5))
            enemyes.add(enemy)


        if score >= goal:
            finish = True
            window.blit(win, (300, 350))


        if sprite.spritecollide(player, enemyes, True):
            life = life - 1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (300, 350))


        if life == 5 or life == 4:
            life_color = (2, 115, 0)

        if life == 3:
            life_color = (230, 205, 0)

        if life == 2 or life == 1:
            life_color = (197, 0, 0)


        text_life = font1.render('Життів: ' + str(life), 1, life_color)
        window.blit(text_life, (10,80))


    else:
        finish = False
        score = 0
        lost = 0
        life = 5
        for b in bullets:
            b.kill()
        for m in enemyes:
            m.kill()
        

        time.delay(3000)
        for i in range(1,6):
            enemy = Enemy(choice(images), randint(200, 600), -40, randint(2,5))
            enemyes.add(enemy)
        




    display.update()
    clock.tick(FPS)