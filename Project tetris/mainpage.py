import pygame
import os
from copy import deepcopy
from random import choice, randrange
import sys
FPS = 50
WIDTH, HEIGHT = 650, 900


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


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 5
        self.top = 5
        self.cell_size = 40

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (5 + j * self.cell_size, 5 + i * self.cell_size,
                                  self.cell_size, self.cell_size), 1)

    # проверка на выход фигуры за поле
    def check_borders(self, figure):
        if figure[i].x < 0 or figure[i].x > 10 - 1:
            return False
        elif figure[i].y > 20 - 1 or self.board[figure[i].y][figure[i].x]:
            return False
        return True


pygame.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris")
board = Board(10, 20)
running = True
clock = pygame.time.Clock()
start_screen()
#  позиции каждой фигуры, если распологать их о  начала координат (первая координата - центр вращения фигуры)
figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]
figures = [[pygame.Rect(x + 5, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, 40, 40)  # рисование фигуры
speed, maxx_speed = 0, 2000
figure = deepcopy(choice(figures))
while running:
    move_gorisont = 0  # переменная, чтобы двигать по горизонтали
    screen.fill("black")
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # сдвиг влево
                move_gorisont = -1
            elif event.key == pygame.K_RIGHT:  # двигаем вправо
                move_gorisont = 1
            elif event.key == pygame.K_DOWN:  # при нажатии кнопки вниз, фигура ускоряется
                maxx_speed = 150
    figure_old = deepcopy(figure)  # копия чтобы вернуть предыдущее положение, если будет выход за границу
    for i in range(4):  # меняем координаты, чтобы сдвинуть по горизонтали
        figure[i].x += move_gorisont
        if not board.check_borders(figure):
            figure = deepcopy(figure_old)
            break
    # движение фигурки вниз
    speed += 50
    if speed > maxx_speed:
        speed = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not board.check_borders(figure):
                figure = deepcopy(choice(figures))
                maxx_speed = 2000
                break
    board.render()  # отрисовываем доску
    for i in range(4):  # отрисовываем фигуры (т.к. они из 4 клеток каждая)
        figure_rect.x = 5 + figure[i].x * 40
        figure_rect.y = 5 + figure[i].y * 40
        pygame.draw.rect(screen, "white", figure_rect)
    pygame.display.flip()
pygame.quit()
