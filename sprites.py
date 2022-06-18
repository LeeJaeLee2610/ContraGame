# sprites of the game


import pygame
from camera import *
from settings import *
from graphics import *

# D : đi sang phải
# A : đi sang trái
# X : nằm
# e : hướng bắn lên
# S : nhảy xuống
# w : nhảy
# chuột trái : bắn
# chuột phải : tăng tốc
# vị trí chuột trên background : xác định hướng bắn

vec = pygame.math.Vector2

all_sprites = pygame.sprite.Group()
# Tất cả trạng thái nhân vật có thể hoạt động
# quay, chéo trên, chéo dưới, nằm, hướng lên (mỗi trạng thái đều có kiểu bên trái và bên phải)
RIGHT = 0
LEFT = 1
RIGHT_DOWN = 2
RIGHT_UP = 3
LEFT_UP = 4
LEFT_DOWN = 5
PRONE_RIGHT = 6
PRONE_LEFT = 7
UP_RIGHT = 8
UP_LEFT = 9


#   Tạo Class Player extend class pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    # Tạo Functions __init__ load các sprite cung cấp thông số là game
    #  Khởi động class Player
    def __init__(self, game):

        pygame.sprite.Sprite.__init__(self)

        # Copy of Game
        self.game = game

        # Tạo và cài đặt thông số cho nhân vật Player ban đầu
        # Lưu vào ảnh của đối tượng sprite
        self.image = pygame.transform.scale(PLAYER_RIGHT_0, (PLAYER_WIDTH, PLAYER_HEIGHT))

        #  Xóa nền ảnh (nền ảnh có màu vàng)
        self.image.set_colorkey(YELLOW)

        # Tạo một hình chữ nhật bao quanh ảnh
        self.rect = self.image.get_rect()

        #  Đặt ảnh ở vị trí center của hình chữ nhật và cài đặt khoảng cách với trục x,y
        self.rect.center = (PLAYER_POSX, 0)

        # Tạo một giá trị health
        self.health = PLAYER_HEALTH

        # Cài đặt  giá trị trạng thái Player ban đầu
        #  Trạng thái xoay, hướng bắn
        self.state = RIGHT
        self.up = False
        self.down = False

        #  có vai trò như vị trí,vận tốc, gia tốc trong function update ( sử dụng công thức chuyển động cơ học)
        self.pos = vec(30, 30)
        self.vel = vec(0, 0)
        self.acc = vec(0, GRAVITY)

        #  Kiểm tra trạng thái chuyển động
        self.canMove = True
        self.jumping = True
        self.facing = 1
        # Nhảy
        self.canJump = False
        self.collisions = True
        # Tăng tốc
        self.blinkTime = BLINK_TIME
        self.canBlink = 1
        self.blinking = False
        self.blinkRetract = BLINK_RETRACT
        # Mất mạng
        self.dead = False
        self.score = SCORE
        # Tốc độ chuyển ảnh
        self.animCounter = ANIM_SPEED

        # Tạo các list ảnh để tạo hiệu ứng chuyển động
        self.jumpFrames = [PLAYER_JUMP_0, PLAYER_JUMP_1, PLAYER_JUMP_2, PLAYER_JUMP_3]
        self.jumpIndex = 0

        self.rightFrames = [PLAYER_RIGHT_0, PLAYER_RIGHT_1, PLAYER_RIGHT_2, PLAYER_RIGHT_3, PLAYER_RIGHT_4,
                            PLAYER_RIGHT_5]
        self.rightIndex = 0

        self.rightUpFrames = [PLAYER_RIGHT_UP_0, PLAYER_RIGHT_UP_1, PLAYER_RIGHT_UP_2]
        self.rightUpIndex = 0

        self.rightDownFrames = [PLAYER_RIGHT_DOWN_0, PLAYER_RIGHT_DOWN_1, PLAYER_RIGHT_DOWN_2]
        self.rightDownIndex = 0

        self.deadFrames = [PLAYER_DEAD_0, PLAYER_DEAD_1, PLAYER_DEAD_2, PLAYER_DEAD_3, PLAYER_DEAD_4]
        self.deadIndex = 0

        self.playerProne = PLAYER_PRONE

        self.playerUp = PLAYER_UP_RIGHT

    # Update trang thái player
    def update(self):

        # Hướng bắn
        self.calcState()

        # Xác định trạng thái

        # Trạng thái mất mạng
        if self.dead:
            # Xóa sprite ra khỏi tất cả các groups
            self.kill()
            return

        # Trạng thái nhảy
        if self.jumping:
            # Tạo hiệu ứng chuyển động cho trạng thái
            self.jumpIndex = self.animate(self.jumpFrames, self.jumpIndex, int(PLAYER_HEIGHT / 2), PLAYER_WIDTH)

        # Trạng thái khác
        else:
            # Cài đặt hình ảnh nhân vật khi ở trạng thái đứng yên ban đầu
            self.setImageByState()

            # Trạng thái di chuyển
            if self.isMoving():
                # Set the animation depending on the state
                # Gọi hàm animate() tạo hiệu ứng chuyển động cho trạng thái
                if self.state == RIGHT:
                    self.rightIndex = self.animate(self.rightFrames, self.rightIndex, PLAYER_WIDTH, PLAYER_HEIGHT)
                elif self.state == RIGHT_DOWN:
                    self.rightDownIndex = self.animate(self.rightDownFrames, self.rightDownIndex, PLAYER_WIDTH,
                                                       PLAYER_HEIGHT)
                elif self.state == RIGHT_UP:
                    self.rightUpIndex = self.animate(self.rightUpFrames, self.rightUpIndex, PLAYER_WIDTH, PLAYER_HEIGHT)
                elif self.state == LEFT:
                    self.rightIndex = self.animate(self.rightFrames, self.rightIndex, PLAYER_WIDTH, PLAYER_HEIGHT, True)
                elif self.state == LEFT_DOWN:
                    self.rightDownIndex = self.animate(self.rightDownFrames, self.rightDownIndex, PLAYER_WIDTH,
                                                       PLAYER_HEIGHT, True)
                elif self.state == LEFT_UP:
                    self.rightUpIndex = self.animate(self.rightUpFrames, self.rightUpIndex, PLAYER_WIDTH, PLAYER_HEIGHT,
                                                     True)
            else:
                # Trạng thái đứng yên
                # Else a stationary image
                # Truyền ảnh và thiết lập lại kích thức ảnh, (lật ảnh)
                if self.state == RIGHT:
                    self.image = pygame.transform.scale(PLAYER_RIGHT_0, (PLAYER_WIDTH, PLAYER_HEIGHT))
                elif self.state == UP_RIGHT:
                    self.image = pygame.transform.scale(PLAYER_UP_RIGHT, (PLAYER_WIDTH + 7, PLAYER_HEIGHT + 22))
                elif self.state == RIGHT_DOWN:
                    self.image = pygame.transform.scale(PLAYER_RIGHT_DOWN_0, (PLAYER_WIDTH, PLAYER_HEIGHT))
                elif self.state == RIGHT_UP:
                    self.image = pygame.transform.scale(PLAYER_RIGHT_UP_0, (PLAYER_WIDTH, PLAYER_HEIGHT))
                elif self.state == PRONE_RIGHT:
                    self.image = pygame.transform.scale(PLAYER_PRONE, (PLAYER_HEIGHT - 10, PLAYER_WIDTH - 10))
                elif self.state == LEFT:
                    self.image = pygame.transform.flip(
                        pygame.transform.scale(PLAYER_RIGHT_0, (PLAYER_WIDTH, PLAYER_HEIGHT)), True, False)
                elif self.state == UP_LEFT:
                    self.image = pygame.transform.flip(
                        pygame.transform.scale(PLAYER_UP_RIGHT, (PLAYER_WIDTH + 7, PLAYER_HEIGHT + 22)), True, False)
                elif self.state == LEFT_DOWN:
                    self.image = pygame.transform.flip(
                        pygame.transform.scale(PLAYER_RIGHT_DOWN_0, (PLAYER_WIDTH, PLAYER_HEIGHT)), True, False)
                elif self.state == LEFT_UP:
                    self.image = pygame.transform.flip(
                        pygame.transform.scale(PLAYER_RIGHT_UP_0, (PLAYER_WIDTH, PLAYER_HEIGHT)), True, False)
                elif self.state == PRONE_LEFT:
                    self.image = pygame.transform.flip(
                        pygame.transform.scale(PLAYER_PRONE, (PLAYER_HEIGHT - 10, PLAYER_WIDTH - 10)), True, False)

        # Blinking and Motion are Disjoint. All others can occur simultaneously
        # Thực hiện trạng thái tăng tốc
        if self.blinking:
            self.acc = vec(0, 0)
            self.vel.y = 0
            self.vel.x = self.facing * BLINK_SPEED
            self.blinkTime -= 1
            self.blinkRetract -= 1
            if self.blinkTime == 0:
                self.blinking = False
                self.blinkTime = BLINK_TIME
                self.blinkRetract = BLINK_RETRACT
        # Trạng thái thường và phục hồi chức năng tăng tốc
        else:
            self.acc = vec(0, GRAVITY)
            if self.blinkRetract == 0:
                pass
            else:
                self.blinkRetract -= 1

        #  pygame.key.get_pressed() lấy trạng thái của tất cả các nút bàn phím -> bools
        #  pygame.mouse.get_pressed() lấy trạng thái của tất cả các nút chuột -> bools
        keystate = pygame.key.get_pressed()
        mousestate = pygame.mouse.get_pressed()
        #  Xác định hướng đi --> xác định vị trí và hướng tăng tốc

        #  Sang phải
        if keystate[pygame.K_a]:
            self.acc.x = -PLAYER_ACC
            self.facing = -1
        #  Sang trái
        if keystate[pygame.K_d]:
            self.score += 1
            self.acc.x = PLAYER_ACC
            self.facing = 1
        #  Nằm
        if keystate[pygame.K_x]:
            self.acc = vec(0, GRAVITY)
            self.vel = vec(0, 0)
        #  Hướng bắn lên
        if keystate[pygame.K_e]:
            self.acc = vec(0, GRAVITY)
            self.vel = vec(0, 0)
        #  Nhảy xuống
        if keystate[pygame.K_s]:
            self.drop()
        if mousestate[2]:  # RMB
            if self.canBlink:
                self.blink()

        # Sử dụng công thức chuyển động cơ học
        # Tìm gia tốc
        # Vân tốc : v = vo + at
        # vị trí : x = xo + vt + 0.5at^2
        # Nếu quãng đường còn nằm trong khoảng dải game
        if not self.pos.x < -LEFT_BOUND and not self.pos.x > -RIGHT_BOUND:
            self.acc.x += self.vel.x * PLAYER_FRC
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
        else:
            if self.pos.x <= -LEFT_BOUND:
                self.pos.x += 1
            else:
                self.pos.x -= 1
        # vị trí cạnh bên dưới hình chữ nhật
        self.rect.bottom = self.pos.y
        self.image.set_colorkey(YELLOW)

    # Kiểm tra di chuyển
    def isMoving(self):
        if int(self.vel.x):
            return True
        return False

    #  Nhảy
    def jump(self):
        if self.canMove and self.canJump and self.vel.y == 0:
            self.vel.y = -JUMP_HEIGHT
            self.jumping = True
            self.canJump = False

    # Nằm
    def prone(self):
        if self.facing == 1:
            self.state = PRONE_RIGHT
        else:
            self.state = PRONE_LEFT

    # Hướng ngẩng lên
    def playerup(self):
        if self.facing == 1:
            self.state = UP_RIGHT
        else:
            self.state = UP_LEFT

    # Tăng tốc
    def blink(self):
        if self.canMove and self.blinkRetract == 0:
            self.blinkRetract = BLINK_RETRACT
            dash_sound.play()
            self.blinking = True

    # Reset trạng thái nhảy
    def stopJumping(self):
        self.jumpIndex = 0
        self.jumping = False

    # Tạo hiệu ứng chuyển động cho trạng thái
    # animate(self,list ảnh,Index list,width,height,trạng thái để lật ảnh)
    def animate(self, frames, index, width, height, flip=False):
        self.animCounter -= 1
        if self.animCounter == 0:
            index += 1
            index %= len(frames)
            if not flip:
                # chỉnh kích thước ảnh
                self.image = pygame.transform.scale(frames[index], (width, height))
            else:
                # Lật ngang ảnh và chỉnh kích thước ảnh
                self.image = pygame.transform.flip(pygame.transform.scale(frames[index], (width, height)), True, False)
            # Tốc độ chuyển ảnh
            self.animCounter = ANIM_SPEED
        rx = self.rect.left
        ry = self.rect.top
        # chèn ảnh vào hình chữ nhật
        self.rect = self.image.get_rect()
        self.rect.left = rx
        self.rect.top = ry
        return index

    # Nhảy xuống
    def drop(self):
        if self.canMove:
            self.collisions = False

    #  Hướng đạn ( truyền vào vị trí chuột)
    def shoot(self, mousePos):
        # Hướng bắn
        self.calcState()

        # quay phải
        if self.state == RIGHT:
            speedx, speedy = 1, 0
            pass
        # chéo lên bên phải
        elif self.state == RIGHT_UP:
            speedx, speedy = 1, 1
            pass
        # chéo xuống bên phải
        elif self.state == RIGHT_DOWN:
            speedx, speedy = 1, -1
            pass
        # nằm bên phải
        elif self.state == PRONE_RIGHT:
            speedx, speedy = 1, 0
            pass
        # ngẩng lên bên phải
        elif self.state == UP_RIGHT:
            speedx, speedy = 0, -1
            pass
        # quay trái
        elif self.state == LEFT:
            speedx, speedy = -1, 0
            pass
        # chéo lên bên trái
        elif self.state == LEFT_UP:
            speedx, speedy = -1, 1
            pass
        # chéo xuống bên trái
        elif self.state == LEFT_DOWN:
            speedx, speedy = -1, -1
            pass
        # nằm bên trái
        elif self.state == PRONE_LEFT:
            speedx, speedy = -1, 0
            pass
        # ngẩng lên bên trái
        elif self.state == UP_LEFT:
            speedx, speedy = 0, -1
            pass
        #  chèn âm thanh bắn đạn
        shoot_sound.play()

        #  vị trí đạn ban đầu
        if self.state == PRONE_RIGHT or self.state == PRONE_LEFT:
            b = Bullet(PLAYER_POSX, self.pos.y + 20, speedx, speedy)
        elif self.state == UP_RIGHT or self.state == UP_LEFT:
            b = Bullet(PLAYER_POSX + 10, self.pos.y, speedx, speedy)
        else:
            b = Bullet(PLAYER_POSX, self.pos.y, speedx, speedy)
        return b

    #  Hướng bắn xác định trạng thái player
    def calcState(self):
        #  Lấy vi trí con trỏ chuột trong màn hình
        mouseX, mouseY = pygame.mouse.get_pos()
        keystate = pygame.key.get_pressed()

        #  Xác định hướng (hướng lên, hướng xuống, cân bằng)
        if mouseY > self.pos.y + BULLET_THRESHOLD:
            self.up = True
            self.down = False
        elif mouseY < self.pos.y - BULLET_THRESHOLD:
            self.up = False
            self.down = True
        else:
            self.up = False
            self.down = False

        #  self.facing xác định trạng thái xoay
        if self.facing == 1:
            if self.up:
                self.state = RIGHT_UP
            elif self.down:
                self.state = RIGHT_DOWN
            else:
                self.state = RIGHT
        else:
            if self.up:
                self.state = LEFT_UP
            elif self.down:
                self.state = LEFT_DOWN
            else:
                self.state = LEFT
        #  Xác định trạng thái nút bàn phím --> trạng thái player
        if keystate[pygame.K_x]:
            self.prone()
        elif keystate[pygame.K_e]:
            self.playerup()

    # Cài đặt hình ảnh nhân vật khi ở trạng thái đứng yên ban đầu
    def setImageByState(self):
        if self.state == RIGHT and not self.isMoving():
            self.image = pygame.transform.scale(PLAYER_RIGHT_0, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left = PLAYER_POSX

    #  Cập nhật trạng thái và reset máu
    def die(self):
        print("DEAD")
        self.dead = True
        self.health = 0

    # Chuyên động khi mất mạng
    def deathAnima(self, index):
        if self.facing == 1:
            self.image = pygame.transform.scale2x(self.deadFrames[index])
            self.image.set_colorkey(YELLOW)
            self.rect = self.image.get_rect()
            self.rect.left = 100 - (index + 1) * 10
            self.rect.bottom = self.pos.y + (index - 4) * 7
        else:
            self.image = pygame.transform.flip(pygame.transform.scale2x(self.deadFrames[index]), True, False)
            self.image.set_colorkey(YELLOW)
            self.rect = self.image.get_rect()
            self.rect.left = 100 + (index + 1) * 10
            self.rect.bottom = self.pos.y + (index - 4) * 7


# Enemies

class Sniper(pygame.sprite.Sprite):
    # Trạng thái của enemies
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.up = False
        self.down = False
        self.speedy = 0
        self.defaultx = x
        self.defaulty = y
        self.counter = 60
        self.state = LEFT

    def update(self):
        if self.state == LEFT:
            self.image = pygame.transform.scale(SNIPER_LEFT, (PLAYER_WIDTH, PLAYER_HEIGHT))
        elif self.state == LEFT_UP:
            self.image = pygame.transform.scale(SNIPER_LEFT_UP, (PLAYER_WIDTH, PLAYER_HEIGHT))
        else:
            self.image = pygame.transform.scale(SNIPER_LEFT_DOWN, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.set_colorkey(YELLOW)
        self.rect.x = self.defaultx + camera.pos.x
        self.rect.y = self.defaulty + camera.pos.y
        pass

    # Hướng bắn của enemi
    def shoot_towards(self, player):
        if player.rect.top < self.rect.top:
            self.down = True
            self.up = False
            self.state = LEFT_DOWN
        elif player.rect.center[1] > self.rect.bottom:
            self.up = True
            self.down = False
            self.state = LEFT_UP
        else:
            self.up, self.down = False, False
            self.state = LEFT
        if PLAYER_POSX + SNIPER_RANGE > self.rect.x > PLAYER_POSX:
            if self.counter == 0:
                self.counter = 60
                return self.shoot(self.up, self.down)
            else:
                self.counter -= 1
                return None

    def shoot(self, up, down):
        sx = -1
        if up:
            sy = 1
        elif down:
            sy = -1
        else:
            sy = 0
        b = Bullet(self.rect.left, self.rect.bottom, sx, sy)
        return b


class Soldier(pygame.sprite.Sprite):
    # Trạng thái của lính
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(SOLDIER_0, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.vel = vec(-SOLDIER_SPEEDX, 0)
        self.acc = vec(0, GRAVITY)

        # Animation
        self.soldier_frames = [SOLDIER_0, SOLDIER_1, SOLDIER_2, SOLDIER_3, SOLDIER_4, SOLDIER_5, SOLDIER_6, SOLDIER_7,
                               SOLDIER_8]
        self.animIndex = 0
        self.animCounter = ANIM_SPEED

    def animate(self):
        self.animCounter -= 1
        if self.animCounter == 0:
            self.animIndex += 1
            self.animIndex %= len(self.soldier_frames)
            self.image = pygame.transform.scale(self.soldier_frames[self.animIndex], (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.animCounter = ANIM_SPEED
        self.image.set_colorkey(YELLOW)

    def update(self):
        if self.rect.right < 0:
            self.kill()
        self.animate()
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.x = self.pos.x + camera.pos.x
        self.rect.bottom = self.pos.y + camera.pos.y

    def shoot_towards(self, player):
        pass


# Tank
class Tank(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = TANK_0
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.counter = 60

    def update(self):
        self.rect.x = self.pos.x + camera.pos.x
        self.counter -= 1
        pass

    def shoot(self):
        if self.rect.x > PLAYER_POSX:
            if self.counter == 0 or self.counter == 5:
                if self.counter == 0:
                    self.counter = 60
                return Bullet(self.rect.x, self.rect.bottom, -1, 0)
        return None


# Bullet

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = bulletImage
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.rect.left = x
        self.rect.top = y - 50
        self.speedx = speedx
        self.speedy = speedy

    def update(self):
        self.rect.left += self.speedx * BULLET_SPEED
        self.rect.top += self.speedy * BULLET_SPEED
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()


# Platform
class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.defaultx = x
        self.defaulty = y

    def update(self):
        self.rect.x = self.defaultx + camera.pos.x
        self.rect.y = self.defaulty + camera.pos.y


# Background Sprite
class Background(pygame.sprite.Sprite):
    def __init__(self, bg):
        pygame.sprite.Sprite.__init__(self)
        self.image = bg
        self.rect = self.image.get_rect()
        self.rect.left = camera.pos.x
        self.rect.y = camera.pos.y

    def update(self):
        self.rect.x = camera.pos.x
        self.rect.y = camera.pos.y


class HUD(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pygame.font.init()
        self.surface = pygame.Surface((WIDTH, 40))
        self.surface.fill(WHITE)
        self.image = self.surface
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 0
        self.font = pygame.font.SysFont("monospace", 20)

    def update(self):
        pass

    # Thanh điểm, hp, cd flash
    def update_HUD(self, game):
        self.surface = pygame.Surface((WIDTH, 30))
        self.surface.fill(WHITE)
        self.drawScore(game.score)
        self.drawHealth(game.health)
        self.drawBlink(game.blinkRetract)
        self.drawPowerup()
        pass

    def drawScore(self, score):
        text = self.font.render("Score: " + str(score), 1, GREEN)
        textPos = text.get_rect()
        textPos.centerx = 100
        self.surface.blit(text, textPos)
        self.image = self.surface

    def drawHealth(self, health):
        if health > PLAYER_HEALTH - 5:
            text = self.font.render("Health: " + str(health), 1, GREEN)
        elif health > 10:
            text = self.font.render("Health: " + str(health), 1, GREEN)
        else:
            text = self.font.render("Health: " + str(health), 1, RED)
        textPos = text.get_rect()
        textPos.centerx = 300
        self.surface.blit(text, textPos)
        self.image = self.surface

    def drawBlink(self, retract):
        retractPerc = str(100 - int(retract / BLINK_RETRACT * 100))
        if retractPerc == '100':
            retractPerc = "OK"
            text = self.font.render("Flash: " + retractPerc, 1, GREEN)
        else:
            text = self.font.render("FLash: " + retractPerc, 1, RED)
        textPos = text.get_rect()
        textPos.centerx = 500
        self.surface.blit(text, textPos)
        self.image = self.surface

    def drawPowerup(self):
        pass


class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, ptype):
        pygame.sprite.Sprite.__init__(self)
        if ptype == 1:
            self.image = HEATH
        elif ptype == 0:
            self.image = FLASH
        else:
            self.image = DROP
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        if x > 6164:
            x = 6160
        self.rect.x = x
        self.defaultx = x
        self.rect.y = -5

        self.ptype = ptype

    def update(self):
        if not self.rect.y >= 170:
            self.rect.y += POWERUP_SPEED

        self.rect.x = camera.pos.x + self.defaultx
        if self.rect.x < 0:
            self.kill()

    def powerup(self):
        return self.ptype
        pass


# Hiệu ứng đạn
class Death(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = EXPLOSION_0
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.defaultx = x
        self.rect.top = y
        self.time = 0
        self.image.set_colorkey(WHITE)
        self.explosionFrames = [EXPLOSION_0, EXPLOSION_1, EXPLOSION_2, EXPLOSION_3, EXPLOSION_4]
        explosion_sound.play()

    def update(self):
        self.time += 1
        if self.time == 5:
            self.kill()
            return
        self.image = self.explosionFrames[self.time]
        self.image.set_colorkey(WHITE)
        pass
