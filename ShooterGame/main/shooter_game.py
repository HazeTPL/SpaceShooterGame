from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.size_x = size_x
        self.size_y = size_x
        self.rect.x = player_x
        self.rect.y = player_y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed   

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 30:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 1700:
            self.rect.x += self.speed
        if keys_pressed[K_w] and self.rect.y > 30:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < 1000:
            self.rect.y += self.speed  

    def fire(self):
        global bullets
        bullet = Bullet('bullet.png', self.rect.x + 45, self.rect.y, 40, 40, 5)
        bullets.append(bullet)

miss = 0   
class Enemy(GameSprite):
    def update(self):
        global miss
        if self.rect.y >= 1080:
            self.rect.y = 0
            self.rect.x = randint(10, 1800)
            miss += 1
        self.rect.y += self.speed

class Asteroid(GameSprite):
    def update(self):
        if self.rect.y >= 1080:
            self.rect.y = 0
            self.rect.x = randint(30, 1950)
        self.rect.y += self.speed

class Area():
    def collidepoint(self, x, y):
       return self.rect.collidepoint(x, y)       
 
    def colliderect(self, rect):
       return self.rect.colliderect(rect)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.1)
mixer.music.play()

font.init()
font2 = font.SysFont('Arial', 60)
font3 = font.SysFont('Arial', 50)
style_font = font.SysFont('Arial', 80)
win = style_font.render('You Win!', True, (0, 255, 0))
lose = style_font.render('You Lose!', True, (255, 0, 0))
style_font = font.SysFont('Arial', 80)
score = 0

init()
display.set_caption('Space Shooter Game')
window = display.set_mode((1930, 1200))
background = transform.scale(image.load("galaxy.jpg"), (1980, 1200))

speed = 7
player1 = Player('rocket.png', 860, 1000, 120, 100, speed)
enemy_list = [Enemy('ufo.png', randint(10, 1800), randint(-350, 0), 110, 100,  randint(1, 3)), Enemy('ufo.png', randint(10, 1800), randint(-300, 0), 110, 100,  randint(1, 3)), Enemy('ufo.png', randint(10, 1800), randint(-250, 0), 110, 100, randint(1, 3)), Enemy('ufo.png', randint(10, 1800), randint(-200, 0), 110, 100, randint(1, 3)), Enemy('ufo.png', randint(10, 1800), randint(-150, 0), 110, 100, randint(1, 3)), Enemy('ufo.png', randint(10, 1800), randint(-100, 0), 110, 100, randint(1, 3))]
bullets = []
asteroid_list = [Asteroid('asteroid.png', randint(10, 1800), 0, 90, 80, randint(1,2)), Asteroid('asteroid.png', randint(10, 1800), 0, 70, 60, randint(1,2)), Asteroid('asteroid.png', randint(10, 1800), 0, 100, 90, randint(1,2))]


keys_pressed = key.get_pressed()
timer = 0
fire_bullets = 10
fire_sound = mixer.Sound('pistol.mp3')
finish = False
game = True
FPS = 60
clock = time.Clock()
while game:
    window.blit((background), (0, 0))
    keys_pressed = key.get_pressed()

    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if fire_bullets > 0:
                    player1.fire()
                    fire_bullets -= 1
                    fire_sound.play()
        if e.type == QUIT:
            game = False
    
#add 3 lives to the game***

    if miss >= 3:
        finish = True

    if finish == False:
        player1.draw()
        player1.update()
        for bullet in bullets:
            bullet.draw()
            bullet.update()
        for enemy in enemy_list:
            enemy.draw()
            enemy.update()
        for asteroid in asteroid_list:
            asteroid.draw()
            asteroid.update()


    for enemy in enemy_list:
        if sprite.collide_rect(player1, enemy):
            finish = True
    for bullet in bullets:
        for enemy in enemy_list:
            if sprite.collide_rect(enemy, bullet):
                enemy.rect.x = randint(20, 600)
                enemy.rect.y = 0
                if bullet in bullets: 
                    bullets.remove(bullet)
                    score += 1

    for asteroid in asteroid_list:
        if sprite.collide_rect(player1, asteroid):
            finish = True
        
    score_d = font2.render(
        'Score: ' + str(score), True, (255, 255, 255)
    )
    miss_d = font2.render(
        'Missed: ' + str(miss), True, (255, 255, 255)
    )
    if fire_bullets == 0:
        timer += 1
        window.blit(reloading_d, (840, 1060))
    if timer == 80:
        fire_bullets = 10
        timer = 0

    reloading_d = font3.render(
        'Reloading. Wait!', True, (255, 0, 0)
    )

    if keys_pressed[K_r]:
        fire_bullets = 10

    bullet_count = font2.render(
        'Ammo: 10/' + str(fire_bullets), True, (255, 255, 255)
    )

    window.blit(score_d, (7, 130))
    window.blit(miss_d, (7, 80))
    window.blit(bullet_count, (1500, 1000))

    if finish == True:
        window.blit(lose, (820, 540))

    display.update()
    clock.tick(FPS)

