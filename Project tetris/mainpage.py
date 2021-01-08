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

    # проверка на выход фигуры за поле или столкновение с находящейся рядом фигурой
    def check_borders(self, figure, field):
        if figure[i].x < 0 or figure[i].x > 10 - 1:
            return False
        elif figure[i].y > 20 - 1 or field[figure[i].y][figure[i].x]:
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
figure_rect = pygame.Rect(0, 0, 38, 38)  # рисование фигуры
field = [[0] * 10 for _ in range(20)]  # поле, чтобы отмечать на нем уже упаввшие фигуры
speed, maxx_speed = 0, 2000  # скорость для плавного движения вниз
figure = deepcopy(choice(figures))  # рандомно выбираем фигуру
while running:
    move_gorizont = 0  # переменная, чтобы двигать по горизонтали
    rotate = False  # переменная чтобы поворачивать фигуру
    screen.fill("black")
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # сдвиг влево
                move_gorizont = -1
            elif event.key == pygame.K_RIGHT:  # двигаем вправо
                move_gorizont = 1
            elif event.key == pygame.K_DOWN:  # при нажатии кнопки вниз, фигура ускоряется
                maxx_speed = 150
            elif event.key == pygame.K_UP:  # поворачиваем
                rotate = True
    figure_old = deepcopy(figure)  # копия чтобы вернуть предыдущее положение, если будет выход за границу
    for i in range(4):  # меняем координаты, чтобы сдвинуть по горизонтали
        figure[i].x += move_gorizont
        if not board.check_borders(figure, field):
            figure = deepcopy(figure_old)
            break
    # движение фигурки вниз
    speed += 50
    if speed > maxx_speed:
        speed = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not board.check_borders(figure, field):
                for j in range(4):
                    field[figure_old[j].y][figure_old[j].x] = "white"
                figure = deepcopy(choice(figures))
                maxx_speed = 2000
                break
    # поворот фигуры
    center = figure[0]  # центр вращения - первая координата из списка
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            # считаем разницу между координатами каждого квадрата фигуры и центра вращения
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            #  теперь вычитаем из иксовой координаты среднюю и прибавляем среднюю к игриковой коордигнате
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not board.check_borders(figure, field):
                figure = deepcopy(figure_old)
                break

    line, lines = 19, 0  # первая для кол-ва линий на поле, вторая считает сколько линий ушло(те которые полностью собраны)
    for row in range(19, -1, -1):  # идем по списку линий от последней до начальной
        k = 0
        # считаем сколько заполненных клеточек в горизонтальной линии
        for i in range(10):
            if field[row][i]:
                k += 1
            # если линия оказалась полностью закрашена, то мы заменяем ее на следущую
            # если нет, то линия еще раз перерисуется
            field[line][i] = field[row][i]
        # если закрашена не вся линия, то проверяем следующую
        if k < 10:
            line -= 1
        else:
            speed += 3
            lines += 1

    board.render()  # отрисовываем доску
    for i in range(4):  # отрисовываем фигуры (т.к. они из 4 клеток каждая)
        figure_rect.x = 5 + figure[i].x * 40
        figure_rect.y = 5 + figure[i].y * 40
        pygame.draw.rect(screen, "white", figure_rect)
    # рисуем поле с фигурами, которые уже на нем
    # смотрим по цвету, если в ячейке не ноль, а цвет, то рисуем этот квадрат( закрашиваем)
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = 5 + x * 40, 5 + y * 40
                pygame.draw.rect(screen, col, figure_rect)
    pygame.display.flip()
pygame.quit()
