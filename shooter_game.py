from random import randint
from pygame import *
font.init()
mixer.init()

#переменные
clock = time.Clock()
run = True
win_width = 800
win_height = 600
mode = 'menu'
lost = 0
fire_time = 45
res_time = 180
res_text = None
points = 0

class Button(sprite.Sprite):
    def __init__ (self, x, y, w, h, color, text):
        self.image = Rect(x, y, w, h)
        self.img = Surface((w, h))
        self.rect = self.img.get_rect()
        self.text = font.SysFont('arial', 24).render(text, True, (0,0,0))
        self.rect.x = x
        self.rect.y = y
        self.color = color
    def fill_rect(self):
        draw.rect(main_win, self.color, self.image)
    def outline(self, size): #обводка прямоугольника
        draw.rect(main_win, (0,0,0),self.image, size)
    def txt_render(self):
        main_win.blit(self.text,(self.rect.x + 50, self.rect.y + 15))
    def collidepoint(self, x, y):
        return self.image.collidepoint(x, y)


class GameSprite(sprite.Sprite):
    def __init__ (self, img, x, y, speed):
        super(). __init__()
        self.image = transform.scale(image.load(img), (int(win_width/10), int(win_width/10)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def update(self):
        main_win.blit(self.image, (self.rect.x, self.rect.y))

class Hero(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 10 - win_width/10:
            self.rect.x += self.speed
    def fire(self):
        global fire_time
        keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE] and fire_time <= 0:
            bullet = Bullet('bullet.png', self.rect.centerx - 12, self.rect.top, 10)
            bullets.add(bullet)
            fire_time = 25

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = randint(-100, 0)
            self.rect.x = randint(int(win_width/10), int(win_width*0.9))
            self.speed = randint(1,2)
            lost += 1

class Bullet(sprite.Sprite):
    def __init__ (self, img, x, y, speed):
        super(). __init__()
        self.image = transform.scale(image.load(img), (int(win_width/30), int(win_width/30)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

#главное окно
main_win = display.set_mode((win_width, win_height))
display.set_caption('Space Shooter')
bg = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

#спрайты
spaceShip = Hero('rocket.png', int(win_width/2), int(win_height - win_width/9), 6)
win = font.SysFont('arial', 100).render('Ты все равно проиграл', True, (255,255,255))
lose = font.SysFont('arial', 100).render('Потрачено', True, (255,255,255))
pointsText = font.SysFont('arial', 25).render('Очки:', True, (255,255,255))
lostText = font.SysFont('arial', 25).render('Пропущенные:' + str(lost), True, (255,255,255))
enemies = sprite.Group()
for i in range(6 ):
    enemy = Enemy('ufo.png', randint(int(win_width/10), int(win_width*0.9)), randint(-100, 0), randint(1,3))
    enemies.add(enemy)
    points += 1

    btn_start = Button(
    win_width/2 - win_width/10,
    win_height/2 - win_height/10,
    win_width/5, 
    win_height/10,
    (0, 255, 0),
    'Начать')
btn_exit = Button(
    win_width/2 - win_width/10,
    win_height/2 + win_height/10,
    win_width/5,
    win_height/10,
    (0, 255, 0),
    '  Выход')
bullets = sprite.Group()

#музыка и звуки
mixer.music.load('space.ogg')
mixer.music.play()

#игровой цикл
while run:
    fire_time -= 1
    main_win.blit(bg, (0,0))
    pointsText = font.SysFont('arial', 25).render('Очки:' + str(points), True, (255,255,255))
    main_win.blit(pointsText, (int(win_width/70), int(win_width/70)))
    lostText = font.SysFont('arial', 25).render('Пропущенные:' + str(lost), True, (255,255,255))
    main_win.blit(lostText, (int(win_width/50), int(win_width/20)))
    
    if mode == 'menu':
        btn_start.fill_rect()
        btn_start.outline(3)
        btn_start.txt_render()
        btn_exit.fill_rect()
        btn_exit.outline(3)
        btn_exit.txt_render()
        

    elif mode == 'game':
        spaceShip.move()
        spaceShip.update()
        spaceShip.fire()
        enemies.update()
        enemies.draw(main_win)
        bullets.update() 
        bullets.draw(main_win)
        if lost > 2:
            mode = 'endGame'
            res_text = lose
        sprites_list = sprite.spritecollide(spaceShip, enemies, False)
        if len(sprites_list) > 0:
            mode = 'endGame'
            res_text = lose
        sprites_list = sprite.groupcollide(enemies, bullets, True, True)
        if len(sprites_list) > 0:
            for i in range(len(sprites_list)):
                enemy = Enemy('ufo.png', randint(int(win_width/10), int(win_width*0.9)), randint(-100, 0), randint(1,3))
                enemies.add(enemy)
                points += 1
        if points > 9:
            mode = 'endGame'
            res_text += 1

    elif mode == 'endGame':
        res_time -= 1
        main_win.blit(res_text, (100, 100))
        if res_time <= 0:
            mode = 'menu'

    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == MOUSEBUTTONDOWN:
            x, y = e.pos
            if btn_start.collidepoint(x,y):
                mode = 'game'
                res_time = 180
                lost = 0
                points = 0
                enemies = sprite.Group()
                for i in range(6):
                    enemy = Enemy('ufo.png', randint(int(win_width/10), int(win_width*0.9)), randint(-100, 0), randint(1,3))
                    enemies.add(enemy)
                    spaceShip.rect.x = int(win_width/2)
                    for b in bullets:
                        b.kill()
            if btn_exit.collidepoint(x,y):
                run = False

    display.update()
    clock.tick(60)