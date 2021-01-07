import pygame
import os
import sys
FPS = 50
WIDTH, HEIGHT = 650, 800


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name):
    fullname = os.path.join(name)
    return pygame.image.load(fullname)


def start_screen():
    intro_text = ["Тетрис", "",
                  "Правила игры:",
                  "Переворачивайте фигурки клавишами управления курсором;",
                  "Собирайте целую строчку, тогда она исчезнет;",
                  "Игра закончится, когда не останется места на поле."]

    fon = pygame.transform.scale(load_image('mainphoto.jpeg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


pygame.init()
WIDTH2, HEIGHT2 = 650, 800
size = WIDTH2, HEIGHT2
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris")
running = True
clock = pygame.time.Clock()
start_screen()
while running:
    screen.fill("black")
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()