import pygame
import math
import random
import numpy as np


class Bullet:
    x = 0
    y = 0
    dir = [0, 0]

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.dir = direction

    def move(self, velocity):
        self.x += self.dir[0] * velocity
        self.y += self.dir[1] * velocity
        if self.x < 0 or self.x > win_size[0] or self.y < 0 or self.y > win_size[1]:
            return True


class Gun:
    fire_ratio = 2.5
    last_shot = 0
    bullets = []
    bullet_speed = 5
    ammo = 1

    def bullets_control(self):
        for b in self.bullets:
            if b.move(self.bullet_speed):
                self.bullets.remove(b)

    def shoot(self, px, py):
        if pygame.time.get_ticks() - self.last_shot > 1000 / self.fire_ratio:

            norm = math.sqrt((mouse.get_pos()[0] - px) ** 2 + (mouse.get_pos()[1] - py) ** 2)
            if norm == 0:
                norm = 1
            # print([(mouse.get_pos()[0] - player.x) / norm, (mouse.get_pos()[1] - player.y) / norm])

            self.bullets.append(Bullet(
                px, py, [(mouse.get_pos()[0] - px) / norm, (mouse.get_pos()[1] - py) / norm]))
            self.last_shot = pygame.time.get_ticks()

    def draw(self, win):
        for b in self.bullets:
            pygame.draw.circle(win, (220, 220, 20), [int(b.x), int(b.y)], 3)


class Drop:

    size = 15

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dropDraw(self, win):
        pass


class Shotgun(Gun, Drop):

    ammo = 20

    def shoot(self, px, py):

        if pygame.time.get_ticks() - self.last_shot > 1000 / self.fire_ratio:

            self.ammo -= 1

            aim = [mouse.get_pos()[0] - px, mouse.get_pos()[1] - py]
            for i in (-1, 0, 1):

                x = i * 15 * 2 * math.pi / 360
                sin_x = math.sin(x)
                cos_x = math.cos(x)

                rotate = np.array([[cos_x, -sin_x],
                                      [sin_x, cos_x]])

                trajectory = np.matmul(rotate, aim)
                # print(trajectory)

                norm = math.sqrt(trajectory[0] ** 2 + trajectory[1] ** 2)
                if norm == 0:
                    norm = 1
                self.bullets.append(Bullet(
                    px, py, [trajectory[0] / norm, trajectory[1] / norm]))

                self.last_shot = pygame.time.get_ticks()

    def dropDraw(self, win):
        pygame.draw.circle(win, (0, 255, 0), [int(self.x), int(self.y)], self.size - 1, 2)
        pygame.draw.circle(win, (0, 0, 0), [int(self.x), int(self.y)], self.size, 1)

        pygame.draw.circle(win, (220, 220, 20), [int(self.x) - 5, int(self.y)], 2)
        pygame.draw.circle(win, (220, 220, 20), [int(self.x), int(self.y)], 2)
        pygame.draw.circle(win, (220, 220, 20), [int(self.x) + 5, int(self.y)], 2)



class MachineGun(Gun, Drop):

    fire_ratio = 7.5
    bullet_speed = 10
    ammo = 100

    def shoot(self, px, py):
        if pygame.time.get_ticks() - self.last_shot > 1000 / self.fire_ratio:

            self.ammo -= 1

            norm = math.sqrt((mouse.get_pos()[0] - px) ** 2 + (mouse.get_pos()[1] - py) ** 2)
            if norm == 0:
                norm = 1
            # print([(mouse.get_pos()[0] - player.x) / norm, (mouse.get_pos()[1] - player.y) / norm])

            self.bullets.append(Bullet(
                px, py, [(mouse.get_pos()[0] - px) / norm, (mouse.get_pos()[1] - py) / norm]))
            self.last_shot = pygame.time.get_ticks()

    def dropDraw(self, win):
        pygame.draw.circle(win, (0, 255, 0), [int(self.x), int(self.y)], self.size - 1, 2)
        pygame.draw.circle(win, (0, 0, 0), [int(self.x), int(self.y)], self.size, 1)

        pygame.draw.circle(win, (220, 220, 220), [int(self.x) - 5, int(self.y)], 2, 1)
        pygame.draw.circle(win, (220, 220, 220), [int(self.x), int(self.y)], 2, 1)
        pygame.draw.circle(win, (220, 220, 220), [int(self.x) + 5, int(self.y)], 2, 1)

        pygame.draw.circle(win, (220, 220, 220), [int(self.x) - 3, int(self.y) - 4], 2, 1)
        pygame.draw.circle(win, (220, 220, 220), [int(self.x) + 3, int(self.y) - 4], 2, 1)

        pygame.draw.circle(win, (220, 220, 220), [int(self.x) - 3, int(self.y) + 4], 2, 1)
        pygame.draw.circle(win, (220, 220, 220), [int(self.x) + 3, int(self.y) + 4], 2, 1)

    def draw(self, win):
        for b in self.bullets:
            pygame.draw.circle(win, (220, 220, 20), [int(b.x), int(b.y)], 2)

class Laser(Gun, Drop):

    ammo = 20
    bullet_speed = 20

    def draw(self, win):
        for b in self.bullets:
            pygame.draw.line(win, (20, 60, 255),
                             [int(b.x - b.dir[0] * 2 * self.bullet_speed), int(b.y - b.dir[1] * 2 * self.bullet_speed)],
                             [int(b.x), int(b.y)], 3)

    def bullets_control(self):
        for b in self.bullets:
            if b.move(self.bullet_speed):
                self.bullets.remove(b)

    def shoot(self, px, py):
        if pygame.time.get_ticks() - self.last_shot > 1000 / self.fire_ratio:

            self.ammo -= 1

            norm = math.sqrt((mouse.get_pos()[0] - px) ** 2 + (mouse.get_pos()[1] - py) ** 2)
            if norm == 0:
                norm = 1
            # print([(mouse.get_pos()[0] - player.x) / norm, (mouse.get_pos()[1] - player.y) / norm])

            self.bullets.append(Bullet(
                px, py, [(mouse.get_pos()[0] - px) / norm, (mouse.get_pos()[1] - py) / norm]))
            self.last_shot = pygame.time.get_ticks()

    def dropDraw(self, win):
        pygame.draw.circle(win, (0, 255, 0), [int(self.x), int(self.y)], self.size - 1, 2)
        pygame.draw.circle(win, (0, 0, 0), [int(self.x), int(self.y)], self.size, 1)

        pygame.draw.line(win, (20, 60, 255), [int(self.x) - 5, int(self.y)], [int(self.x) + 5, int(self.y)], 3)

class Character:
    velocity = 5
    size = 20
    angle = 30
    killed = False

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gun = Gun()
        self.points = 0

    def move(self, dx, dy):
        self.x += dx * self.velocity
        self.y += dy * self.velocity

    def shoot(self):
        if self.gun.ammo > 0:
            self.gun.shoot(self.x, self.y)
        else:
            self.gun = Gun()

    def draw(self, win):
        if not self.killed:
            """
            shape = [(int(self.x-20), int(self.y-10)), (int(self.x-25), int(self.y)),
                     (int(self.x-20), int(self.y+10)), (int(self.x+10), int(self.y+7)),
                     (int(self.x+10), int(self.y-7)), (int(self.x-20), int(self.y-10))]

            #test
            pygame.draw.lines(win, (0, 255, 0), False, shape)
            """
            # character
            pygame.draw.circle(win, (0, 0, 0), [int(self.x), int(self.y)], 15, 5)
            pygame.draw.circle(win, (20, 255, 40), [int(self.x), int(self.y)], 14, 3)
            # aim cross
            norm = math.sqrt((mouse.get_pos()[0] - self.x) ** 2 + (mouse.get_pos()[1] - self.y) ** 2)

            pygame.draw.line(win, (0, 0, 0), [int(self.x), int(self.y)],
                             [int(self.x + ((mouse.get_pos()[0] - self.x) / norm * 20)),
                              int(self.y + ((mouse.get_pos()[1] - self.y) / norm * 20))], 5)

            pygame.draw.circle(win, (0, 0, 0), mouse.get_pos(), 5, 1)
            pygame.draw.circle(win, (255, 0, 0), mouse.get_pos(), 4, 2)

            # draw bullets
            self.gun.draw(win)

            """"
            # draw view field
            rotationL = np.array([[math.cos(self.angle), -math.sin(self.angle)],
                                [math.sin(self.angle), math.cos(self.angle)]])
    
            rotationR = np.array([[math.cos(-self.angle), -math.sin(-self.angle)],
                                [math.sin(-self.angle), math.cos(-self.angle)]])
    
            left_vec = np.matmul(rotationL ,[mouse.get_pos()[0], mouse.get_pos()[1]])
            right_vec = np.matmul(rotationR,[mouse.get_pos()[0], mouse.get_pos()[1]])
    
            pygame.draw.line(win, (0, 0, 0), [int(self.x), int(self.y)], [int(left_vec[0]), int(left_vec[1])])
            pygame.draw.line(win, (0, 0, 0), [int(self.x), int(self.y)], [int(right_vec[0]), int(right_vec[1])])
            """
        else:
            for k in range(1, 20):
                a = random.randint(-20, 20)
                r = int(math.sqrt(400 - a**2))
                b = random.randint(-r, r)
                # pygame.draw.circle(win, (40, 200, 40), [int(self.x + a), int(self.y + b)], 4)
                pygame.draw.line(win, (10, 180, 10), [int(self.x + a / 2), int(self.y) + b / 2],
                                 [int(self.x + a), int(self.y + b)], 3)

    def hit(self):
        self.killed = True
        print(self.points)


class Spawner:
    enemies = []
    killed = []
    # spawns/sec
    spawn_raito = 0.5
    last_spawn = 0

    clear_time = 180

    def spawn(self, px, py):
        if pygame.time.get_ticks() - self.last_spawn > 1000/self.spawn_raito:

            x = px
            y = py
            while math.sqrt((x-px)**2 + (y-py)**2) < 400:
                x = random.randint(20, win_size[0] - 20)
                y = random.randint(20, win_size[1] - 20)

            rand = random.randint(0, 2)

            if rand == 0:
                a = Dodger(x, y, 4)
            elif rand == 1:
                a = Mob(x, y, 2)
            else:
                a = Clon(x, y, 1)


            self.enemies.append(a)
            self.last_spawn = pygame.time.get_ticks()

    def clear(self):
        for e in self.killed:
            if pygame.time.get_ticks() - e.dead_time > self.clear_time:
                self.killed.remove(e)


class DropSpawner:

    drops = []
    # spawns/sec
    spawn_ratio = 0.1
    last_spawn = 0

    def spawn(self, px, py):
        if pygame.time.get_ticks() - self.last_spawn > 1000/self.spawn_ratio:

            x = px
            y = py
            while math.sqrt((x-px)**2 + (y-py)**2) < 400:
                x = random.randint(20, win_size[0] - 20)
                y = random.randint(20, win_size[1] - 20)

            rand = random.randint(0, 2)

            if rand == 0:
                a = Shotgun(x, y)
            elif rand == 1:
                a = Laser(x, y)
            else:
                a = MachineGun(x, y)

            self.drops.append(a)
            self.last_spawn = pygame.time.get_ticks()

"""
class ShotgunDrop(Drop):

    def draw(self, win):
        pygame.draw.circle(win, (0, 255, 0), [int(self.x), int(self.y)], self.size - 1, 2)
        pygame.draw.circle(win, (0, 0, 0), [int(self.x), int(self.y)], self.size, 1)
"""

class Enemy:
    x = 0
    y = 0
    velocity = 4
    params = [7, 15]
    delta = [-1, -1]
    dead_time = 0

    def __init__(self, x, y, v):
        self.x = x
        self.y = y
        self.velocity = v

    def move(self, dx, dy):
        pass

    def draw(self, win):
        pass

    def hit(self):
        self.dead_time = pygame.time.get_ticks()


class Mob(Enemy):
    size = 15

    def move(self, dx, dy):

        norm = math.sqrt((dx - self.x)**2 + (dy - self.y)**2)
        if norm == 0:
            norm = 1
        self.x += (dx - self.x) * self.velocity / norm
        self.y += (dy - self.y) * self.velocity / norm

    def draw(self, win):

        if self.dead_time == 0:
            pygame.draw.circle(win, (0, 0, 0), [int(self.x), int(self.y)], self.size, 1)
            pygame.draw.circle(win, (200, 40, 40), [int(self.x), int(self.y)], self.size - 1, 1)

            a = self.params[0]
            b = self.params[1]

            shape = [(int(self.x), int(self.y - b)), (int(self.x + b), int(self.y - a)),
                     (int(self.x + b), int(self.y + a)), (int(self.x), int(self.y + b)),
                     (int(self.x - b), int(self.y + a)), (int(self.x - b), int(self.y - a)),
                     [int(self.x), int(self.y - b)]]

            if self.params[0] == 0:
                self.delta[0] = 1
            elif self.params[0] == 8:
                self.delta[0] = -1

            if self.params[1] == 0:
                self.delta[1] = 1
            elif self.params[1] == 15:
                self.delta[1] = -1

            self.params[0] += self.delta[0]
            self.params[1] += self.delta[1]

            # test
            pygame.draw.lines(win, (0, 255, 0), True, shape)
        else:
            for k in range(1, 10):

                interval = (pygame.time.get_ticks() - self.dead_time)*2

                a = random.randint(-interval, interval)
                b = random.randint(-interval, interval)
                # pygame.draw.circle(win, (255, 40, 40), [int(self.x + a), int(self.y + b)], 3)
                pygame.draw.line(win, (10, 180, 180),
                                 [int(self.x + a/1.5), int(self.y + b/1.5)], [int(self.x + a), int(self.y + b)], 3)


class Dodger(Enemy):
    size = 15
    path_timer = 0

    def move(self, dx, dy):

        self.path_timer = (self.path_timer + math.pi/360) % (2*math.pi)

        sin_pt = 200 * math.sin(self.path_timer)
        cos_pt = 200 * math.cos(self.path_timer)

        norm = math.sqrt((dx - self.x + sin_pt)**2 + (dy - self.y + cos_pt)**2)
        if norm == 0:
            norm = 1

        self.x += (dx - self.x + sin_pt) * self.velocity / norm
        self.y += (dy - self.y + cos_pt) * self.velocity / norm

    def draw(self, win):

        if self.dead_time == 0:
            pygame.draw.circle(win, (0, 0, 0), [int(self.x), int(self.y)], self.size, 1)
            pygame.draw.circle(win, (200, 40, 40), [int(self.x), int(self.y)], self.size - 1, 1)

            a = self.params[0]
            b = self.params[1]

            shape = [(int(self.x), int(self.y - b)), (int(self.x - a), int(self.y + b)),
                     (int(self.x + a), int(self.y + b)), (int(self.x), int(self.y - b))]

            if self.params[0] == 0:
                self.delta[0] = 1
            elif self.params[0] == 8:
                self.delta[0] = -1

            if self.params[1] == 0:
                self.delta[1] = 1
            elif self.params[1] == 15:
                self.delta[1] = -1

            self.params[0] += self.delta[0]
            self.params[1] += self.delta[1]
            # self.params[1] = math.sqrt(math.fabs(Enemy.size**2 - self.params[0]**2))



            # test
            pygame.draw.lines(win, (255, 255, 0), True, shape)
        else:
            for k in range(1, 10):

                interval = (pygame.time.get_ticks() - self.dead_time)*2

                a = random.randint(-interval, interval)
                b = random.randint(-interval, interval)
                # pygame.draw.circle(win, (255, 40, 40), [int(self.x + a), int(self.y + b)], 3)
                pygame.draw.line(win, (10, 180, 180),
                                 [int(self.x + a/1.5), int(self.y + b/1.5)], [int(self.x + a), int(self.y + b)], 3)


class Clon(Enemy):

    size = 30

    def move(self, dx, dy):

        norm = math.sqrt((dx - self.x)**2 + (dy - self.y)**2)
        if norm == 0:
            norm = 1
        self.x += (dx - self.x) * self.velocity / norm
        self.y += (dy - self.y) * self.velocity / norm

    def draw(self, win):

        if self.dead_time == 0:
            pygame.draw.circle(win, (0, 0, 0), [int(self.x), int(self.y)], self.size, 1)
            pygame.draw.circle(win, (200, 40, 40), [int(self.x), int(self.y)], self.size - 1, 1)

            a = self.size/2

            shape = [(int(self.x - a), int(self.y - a)), (int(self.x + a), int(self.y - a)),
                     (int(self.x + a), int(self.y + a)), (int(self.x - a), int(self.y + a)),
                     (int(self.x - a), int(self.y - a))]

            # test
            pygame.draw.lines(win, (0, 120, 255), True, shape)
        else:
            for k in range(1, 10):

                interval = (pygame.time.get_ticks() - self.dead_time)*2

                a = random.randint(-interval, interval)
                b = random.randint(-interval, interval)
                # pygame.draw.circle(win, (255, 40, 40), [int(self.x + a), int(self.y + b)], 3)
                pygame.draw.line(win, (10, 180, 180),
                                 [int(self.x + a/1.5), int(self.y + b/1.5)], [int(self.x + a), int(self.y + b)], 3)

    def hit(self):

        a = self.size/2

        for k in range(0,2):
            for i in range(0,2):
                temp = SmallClon(self.x + (-1)**i * a, self.y + (-1)**k * a, 2)
                nest.enemies.append(temp)

        self.dead_time = pygame.time.get_ticks()


class SmallClon(Mob):

    def draw(self, win):

        if self.dead_time == 0:
            pygame.draw.circle(win, (0, 0, 0), [int(self.x), int(self.y)], self.size, 1)
            pygame.draw.circle(win, (200, 40, 40), [int(self.x), int(self.y)], self.size - 1, 1)

            a = self.size/2

            shape = [(int(self.x - a), int(self.y - a)), (int(self.x + a), int(self.y - a)),
                     (int(self.x + a), int(self.y + a)), (int(self.x - a), int(self.y + a)),
                     (int(self.x - a), int(self.y - a))]

            # test
            pygame.draw.lines(win, (0, 120, 255), True, shape)
        else:
            for k in range(1, 10):

                interval = (pygame.time.get_ticks() - self.dead_time)*2

                a = random.randint(-interval, interval)
                b = random.randint(-interval, interval)
                # pygame.draw.circle(win, (255, 40, 40), [int(self.x + a), int(self.y + b)], 3)
                pygame.draw.line(win, (10, 180, 180),
                                 [int(self.x + a/1.5), int(self.y + b/1.5)], [int(self.x + a), int(self.y + b)], 3)


def game_over():
    global exit_flag

    while not exit_flag:

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_flag = True

        update_window()


def update_window():
    window.fill((80, 80, 80))
    player.draw(window)

    for e in Spawner.enemies:
        e.draw(window)

    for e in Spawner.killed:
         e.draw(window)

    for d in DropSpawner.drops:
        d.dropDraw(window)

    pygame.display.update()


def collisions():
    for e in nest.enemies:
        for b in player.gun.bullets:
         if b.x > e.x - e.size and b.x < e.x + e.size:
             if b.y > e.y - e.size and b.y < e.y + e.size:
                e.hit()
                player.points += 1
                pygame.display.update()
                nest.killed.append(e)
                try:
                    nest.enemies.remove(e)
                    player.gun.bullets.remove(b)
                except:
                    print("remove err")


        if player.x + player.size > e.x - e.size and player.x - player.size < e.x + e.size:
            if player.y + player.size > e.y - e.size and player.y - player.size < e.y + e.size:
                player.hit()
                game_over()

    for loot in support.drops:
        if player.x + player.size > loot.x - loot.size and player.x - player.size < loot.x + loot.size:
            if player.y + player.size > loot.y - loot.size and player.y - player.size < loot.y + loot.size:
                player.gun = loot
                support.drops.remove(loot)

# Start of program
win_size = [1200, 900]
window = pygame.display.set_mode(win_size)
pygame.display.set_caption("2d shooter")
pygame.mouse.set_visible(False)

# initialize game
exit_flag = False
clock = pygame.time.Clock()

# spawn player
player = Character(win_size[0] / 2, win_size[1] / 2)
# enemies spawner
nest = Spawner()
# drops spawner
support = DropSpawner()

while not exit_flag:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_flag = True

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse

    if keys[pygame.K_w] and player.y > 0:
        player.move(0, -1)
    if keys[pygame.K_s] and player.y < win_size[1]:
        player.move(0, 1)
    if keys[pygame.K_d] and player.x < win_size[0]:
        player.move(1, 0)
    if keys[pygame.K_a] and player.x > 0:
        player.move(-1, 0)
    if mouse.get_pressed()[0]:
        player.shoot()

    # spawn drops
    support.spawn(player.x, player.y)

    # spawn enemies
    nest.spawn(player.x, player.y)

    for enemy in nest.enemies:
        enemy.move(player.x, player.y)

    player.gun.bullets_control()

    collisions()
    update_window()
    nest.clear()
