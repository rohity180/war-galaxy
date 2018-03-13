import pygame
import random
import math
from os import path

'''basic settings'''
win_height=400
win_width=700
fps=60

'''color settings'''
black=(0,0,0)
white=(255,255,255)
red=(200,0,0)
green=(0,200,0)
blue=(0,0,200)
bright_red=(255,0,0)
bright_green=(0,255,0)
bright_blue=(0,0,255)
yellow=(200,200,0)
bright_yellow=(255,255,0)
purple=(200,0,200)
bright_purple=(255,0,255)
orange=(255,128,0)

img_folder=path.join(path.dirname(__file__),"img")#creating a shortcut for
                                                  #our image resource folder


#************************************#
''' setting up the Game environment'''
#************************************#
pygame.init()
screen = pygame.display.set_mode((win_width,win_height))
pygame.display.set_caption("Space War")
icon = pygame.image.load("icon.png")
icon.set_colorkey(black)
pygame.display.set_icon(icon)
clock = pygame.time.Clock()


#**************************#
'''load graphic resources'''
#**************************#
SCREEN=pygame.image.load(path.join(img_folder,"background.jpg")).convert()
background = pygame.transform.scale(background,(width,height))
introbackground = pygame.image.load(path.join(img_dir,"introbackground.jpg")).convert()
introbackground = pygame.transform.scale(introbackground,(width,height))
infobackground = pygame.image.load(path.join(img_dir,"infobackground.jpg")).convert()
infobackground = pygame.transform.scale(infobackground,(width,height))
gameoverbackground = pygame.image.load(path.join(img_dir,"gameover.jpg")).convert()
gameoverbackground = pygame.transform.scale(gameoverbackground,(width,height))
r_ship= pygame.image.load(path.join(img_dir,"r_ship.png")).convert()
asteroid_list=["a1.png","a2.png","a3.png","a4.png","a5.png","a6.png","a7.png","a8.png"]
r_bullets = pygame.image.load(path.join(img_dir,"r_bullet1.png")).convert()
bulletupimg = pygame.image.load(path.join(img_dir,"bulletup.png")).convert()
enemy_army= pygame.image.load(path.join(img_dir,"enemy_army.png")).convert()
enemy_boss = pygame.image.load(path.join(img_dir,"enemy_boss.png")).convert()

explosion={}
explosion['large']=[]
explosion['small']=[]
explosion['finish']=[]

for i in range(9):
    fname= "regularExplosion0{}.png".format(i)
    img = pygame.image.load(path.join(img_folder,fname)).convert()
    img.set_colorkey(black)
    img_large = pygame.transform.scale(img,(100,100))
    explosion['large'].append(img_large)
    img_small = pygame.transform.scale(img,(50,50))
    explosion['small'].append(img_small)
    fname = "sonicExplosion0{}.png".format(i)
    img = pygame.image.load(path.join(img_folder,fname)).convert()
    img.set_colorkey(black)
    explosion['finish'].append(img)



#******************#
'''Game functions'''
#******************#
def quitgame():
    pygame.quit()
    quit()

def newasteroid():
    a = asteroid()
    asteroid_sprites.add(a)
    all_sprites.add(a)

def newbullet(x,y,radian):
    bullet = r_bullet(x, y, radian)
    bullet_sprites.add(bullet)
    all_sprites.add(bullet)

def newhealthup():
    healthup = Healthup()
    healthup_sprites.add(healthup)
    all_sprites.add(healthup)

def newliveup():
    liveup = Liveup()
    liveup_sprites.add(liveup)
    all_sprites.add(liveup)

def newenemy_army():
    enemy = Enemy_army()
    enemy_sprites.add(enemy)
    all_sprites.add(enemy)
    return enemy

def newboss():
    boss = Boss()
    boss_sprites.add(boss)
    all_sprites.add(boss)
    return boss

def health(ph,x,y):
    if ph <= 0:
        ph = 0
    container = pygame.Rect(x,y,150,20)
    blood = pygame.Rect(x+1,y+1,150*ph/100-2,20-2)
    pygame.draw.rect(screen,white,container,1)
    pygame.draw.rect(screen,red,blood)

def drawscore(score,x,y):
    label("Score: ",x,y,25,purple)
    label(str(score),x+100,y,25,orange)

def drawlive(live,x,y):
    liveimg = pygame.transform.scale(playerimg,(42,30))
    liveimg.set_colorkey(black)
    for i in range(live):
        screen.blit(liveimg,(x+i*50,y))

def label(msg,x,y,size,color):
    font = pygame.font.SysFont("comicsansms",size)
    text = font.render(msg,True,color)
    screen.blit(text,(x,y))


def Button(msg,x,y,width,height,i_color,a_color,command=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen,a_color,(x,y,width,height))
        if click[0] == 1 and command != None:
            command()
    else:
        pygame.draw.rect(screen,i_color,(x,y,width,height))
    buttontext = pygame.font.SysFont("comicsansms",20)
    buttonmsg = buttontext.render(msg,True,black)
    buttonmsgrect = buttonmsg.get_rect()
    buttonmsgrect.center = ((x+width/2),(y+height/2))
    screen.blit(buttonmsg,buttonmsgrect)

#***************#
'''class'''
#***************#
class player(pygame.sprite.Sprite):
    def _init_(self):
        pygame.sprite.Sprite._init_(self)
        self.image==pygame.transform.scale(r_ship,(70,50))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = width/2
        self.rect.bottom = height - 20
        self.radius = 27
        self.speedx = 0
        self.speedy = 0
        self.lastshoot = pygame.time.get_ticks()
        self.score = 0
        self.ph = 100
        self.live = 3
        self.shootdelay = 400
        self.bulletpower = 1
        self.bulletpower_delay = 20000
        self.bulletpower_time = pygame.time.get_ticks()
        self.bulletpower_now = pygame.time.get_ticks()
        self.speedup_delay = 20000
        self.speedup_time = pygame.time.get_ticks()


    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.lastshoot > self.shootdelay:
                self.lastshoot = now
                if self.bulletpower == 1:
                    newbullet(self.rect.x+29,self.rect.y,math.pi/2)
                if self.bulletpower == 2:
                    newbullet(self.rect.x-5,self.rect.y,math.pi/2)
                    newbullet(self.rect.x+70-8,self.rect.y,math.pi/2)
                if self.bulletpower == 3:
                    newbullet(self.rect.x+29,self.rect.y,math.pi/2)
                    newbullet(self.rect.x-7, self.rect.y, math.pi / 2)
                    newbullet(self.rect.x + 70-6, self.rect.y, math.pi / 2)
                if self.bulletpower == 4:
                    newbullet(self.rect.x+29,self.rect.y,math.pi/2)
                    newbullet(self.rect.x-7, self.rect.y, math.pi / 2)
                    newbullet(self.rect.x + 70-6, self.rect.y, math.pi / 2)
                    newbullet(self.rect.x-5-20,self.rect.y-10,math.pi*(7/18))
                    newbullet(self.rect.x+70-8+20,self.rect.y-10,math.pi*(1-7/18))

                if self.bulletpower >= 5:
                    newbullet(self.rect.x+29,self.rect.y,math.pi/2)
                    newbullet(self.rect.x-7, self.rect.y, math.pi / 2)
                    newbullet(self.rect.x + 70-6, self.rect.y, math.pi / 2)
                    newbullet(self.rect.x-5-20,self.rect.y-10,math.pi*(7/18))
                    newbullet(self.rect.x+70-8+20,self.rect.y-10,math.pi*(1-7/18))
                    newbullet(self.rect.x-5-20-10,self.rect.y-15,math.pi*1/4)
                    newbullet(self.rect.x+70-8+20+10,self.rect.y-15,math.pi*(1-1/4))


    def update(self):
        self.speedx = 0
        self.speedy = 0
        # set for bullet power
        self.bulletpower_now = pygame.time.get_ticks()
        if self.bulletpower_now - self.bulletpower_time > self.bulletpower_delay:
            self.bulletpower_time = pygame.time.get_ticks()
            self.bulletpower -= 1
        if self.bulletpower < 1:
            self.bulletpower = 1
        # set for speedup
        self.speedup_now = pygame.time.get_ticks()
        if self.speedup_now - self.speedup_time > self.speedup_delay:
            self.speedup_time = pygame.time.get_ticks()
            self.shootdelay += 50
        if self.shootdelay < 100:
            self.shootdelay = 100
        if self.shootdelay > 400:
            self.shootdelay = 400
        # player ph and live
        if self.ph > 100:
            self.ph = 100
        if self.ph < 0:
            expl = Explosion(self.rect.center, 'death')
            explodedeath_sound.play()
            all_sprites.add(expl)
            self.live -= 1
            self.ph = 100
            self.rect.centerx = width / 2
            self.rect.bottom = height - 20
        if player.live < 0:
            player.kill()
            gameover()
        # key event
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            self.speedx = 6
        if keystate[pygame.K_LEFT]:
            self.speedx = -6
        if keystate[pygame.K_UP]:
            self.speedy = -6
        if keystate[pygame.K_DOWN]:
            self.speedy = 6
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
            

class asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.astochoice = random.choice(asteroid_list)
        self.asteroid_img_orig = pygame.image.load(path.join(img_dir, self.meteochoice)).convert()
        self.asteroid_img_orig.set_colorkey(black)
        self.asteroid_img = self.asteroid_img_orig.copy()
        self.image = self.asteroid_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width)
        self.rect.y = -500
        self.radius = int(self.rect.width * 0.85 / 2)
        self.speedx = random.randrange(-10,10)
        self.speedy = random.randrange(3,13)
        self.rot = 0
        self.rotspeed = random.randrange(-15,15)
        self.last_update = pygame.time.get_ticks()        

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot+self.rotspeed)%360
            newimage = pygame.transform.rotate(self.asteroid_img_orig,self.rot)
            old_center = self.rect.center
            self.image = newimage
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.right < 0) or (self.rect.left > width) or (self.rect.top > height):
            self.rect.x = random.randrange(0, width)
            self.rect.y = -500
            self.speedx = random.randrange(-10, 10)
            self.speedy = random.randrange(3, 13)



class Mybullet(pygame.sprite.Sprite):
    def __init__(self,x,y,radian):
        pygame.sprite.Sprite.__init__(self)
        self.image = r_bullet
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.x = x
        self.speed = -15
        self.speedx = math.cos(radian)*self.speed
        self.speedy = math.sin(radian)*self.speed

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.bottom < 0) or (self.rect.right < 0) or (self.rect.left > width):
            self.kill()



class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,mode):
        pygame.sprite.Sprite.__init__(self)
        self.mode = mode
        self.image = explosion[self.mode][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.update_rate = 90

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.update_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion[self.mode]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion[self.mode][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Bulletup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bulletupimg
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width-self.rect.width)
        self.rect.y = -500
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y > height:
            self.kill()


class Speedup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = speedupimg
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width-self.rect.width)
        self.rect.y = -500
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y > height:
            self.kill()


class Healthup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = healthupimg
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width-self.rect.width)
        self.rect.y = -500
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y > height:
            self.kill()

class Liveup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(playerimg,(35,25))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width-self.rect.width)
        self.rect.y = -500
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y > height:
            self.kill()
