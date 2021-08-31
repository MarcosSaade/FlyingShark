import sys
import pygame
import random
import time
from pygame import mixer


class Main():
    def __init__(self):
        self.shark = Shark()
        self.blitter = Bliter()
        self.menus = Menus()

        self.choose = True
        self.spwn = False
        self.spawn_num = 4
        self.spawn_list = []
        self.spawn_x = []
        self.spawn_y = []

        self.points = 0
        self.lives = 3
        self.game_over = False

    def update(self):
        if self.menus.mm:
            self.menus.main_menu()
        elif self.menus.pm:
            self.menus.pause_menu()

        elif self.game_over:
            self.menus.game_over_menu()

        else:
            self.blitter.points()
            self.blitter.lives()

            self.shark.draw()
            self.shark.move()

            if self.choose:
                self.choice()
            elif self.spwn:
                self.spawn()

    def choice(self):
        for i in range(self.spawn_num):
            x = random.choice([0, 0, 1])
            self.spawn_list.append(x)
            self.spawn_x.append(random.randrange(1000, 10000, 1000))
            self.spawn_y.append(random.randrange(50, 550, 100))

        self.choose = False
        self.spwn = True

    def spawn(self):
        for i in range(len(self.spawn_list)):
            self.move_object()
            if self.spawn_list[i] == 0:
                screen.blit(rock, (self.spawn_x[i], self.spawn_y[i]))
            elif self.spawn_list[i] == 1:
                screen.blit(bird, (self.spawn_x[i], self.spawn_y[i]))

        if len(self.spawn_list) == 0:
            self.spwn = False

    def move_object(self):
        for i in range(len(self.spawn_list)):
            self.spawn_x[i] -= 5

            # Respawn
            if self.spawn_x[i] <= 0:
                if self.spawn_y[i] + 60 in range(self.shark.y - 10, self.shark.y + 83):
                    if self.spawn_list[i] == 0:
                        self.damage()
                    elif self.spawn_list[i] == 1:
                        self.gain_points()

                self.spawn_x[i] = random.randrange(1000, 3000, 100)
                self.spawn_y[i] = random.randrange(50, 550, 100)
                self.spawn_list[i] = random.choice([0, 0, 1])

    def gain_points(self):
        self.points += 1

    def damage(self):
        color_image = pygame.Surface(shark.get_size()).convert_alpha()
        color_image.fill((192, 0, 0))

        shark_copy = shark.copy()
        shark_copy.blit(color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        screen.blit(shark_copy, (0, self.shark.y))

        self.lives -= 1

        if self.lives == 0:
            self.game_over = True
            self.menus.game_over_menu()


class Shark():
    def __init__(self):
        self.y = 300
        self.speed = 0

    def draw(self):
        screen.blit(shark, (10, self.y))

    def move(self):
        if self.y <= 0: self.y = 0
        if self.y >= 470: self.y = 470
        self.y += self.speed


class Bliter():
    def __init__(self):
        self.font_1 = pygame.font.Font("pricedown bl.ttf", 32)
        self.font_2 = pygame.font.Font("pricedown bl.ttf", 64)
        self.heart = pygame.image.load("heart.png")

    def points(self):
        points_text = self.font_1.render(f"Score: {points}", True, (255, 255, 255))
        screen.blit(points_text, (10, 0))

    def lives(self):
        if lives == 3:
            screen.blit(self.heart, (800, 0))
            screen.blit(self.heart, (860, 0))
            screen.blit(self.heart, (920, 0))
        elif lives == 2:
            screen.blit(self.heart, (860, 0))
            screen.blit(self.heart, (920, 0))
        elif lives == 1:
            screen.blit(self.heart, (920, 0))

    def paused(self):
        paused = self.font_2.render("Paused", True, (255, 255, 255))
        cont = self.font_1.render("Press C to continue", True, (0, 0, 0))

        screen.blit(paused, (400, 30))
        screen.blit(cont, (350, 500))

    def menu(self):
        title = pygame.image.load("title.png")
        to_play = main.blitter.font_1.render("Press space to play", True, (0, 0, 0))

        screen.blit(title, (250, 30))

        if round(time.time()) % 10 in [1, 3, 5, 7, 9]:
            screen.blit(to_play, (320, 500))
        else:
            pass

    def game_over(self):
        main.lives = 3
        main.points = 0

        game_over_font = self.font_2.render("GAME OVER", True, (192, 0, 0))
        cont = self.font_1.render("Press P to play again", True, (0, 0, 0))

        screen.blit(game_over_font, (350, 400))
        screen.blit(cont, (350, 500))


class Menus():
    def __init__(self):
        self.mm = True
        self.pm = False

    def main_menu(self):
        main.blitter.menu()

    def pause_menu(self):
        clock.tick(0)
        main.blitter.paused()

    def game_over_menu(self):
        clock.tick(0)
        main.blitter.game_over()




pygame.init()
main = Main()
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
shark = pygame.image.load("shark.png").convert_alpha()
bird = pygame.image.load("bird.png")
rock = pygame.image.load("rock.png")

background = pygame.image.load("background.png").convert()
bg_x = 0

mixer.music.load("flying_shark.wav")
mixer.music.play(-1)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if main.menus.mm:
                if event.key == pygame.K_SPACE:
                    main.menus.mm = False
            if main.menus.pm:
                if event.key == pygame.K_c:
                    main.menus.pm = False
            if not main.menus.pm and not main.menus.mm and not main.game_over:
                if event.key == pygame.K_p:
                    main.menus.pm = True
            if main.game_over:
                if event.key == pygame.K_p:
                    main.game_over = False

            if event.key == pygame.K_w or event.key == pygame.K_UP:
                main.shark.speed = -10
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                main.shark.speed = 10

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                if main.shark.speed == -10:
                    main.shark.speed = 0
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if main.shark.speed == 10:
                    main.shark.speed = 0

    rel_x = bg_x % background.get_width()
    screen.blit(background, (rel_x - background.get_width(), 0))

    if rel_x < 1000:
        screen.blit(background, (rel_x, 0))

    if not main.menus.pm:
        bg_x -= 10

    points = main.points
    lives = main.lives
    main.update()
    pygame.display.update()
    clock.tick(60)
