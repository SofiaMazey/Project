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


def continue_game():
    fon = pygame.transform.scale(load_image('mainphoto.jpeg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font1 = pygame.font.Font('start&endscreen.ttf', 40)
    end_text = font1.render("Нажмите пробел для следующей попытки", True, pygame.Color("black"))
    screen.blit(end_text, (5, 200))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


def load_image(name):
    fullname = os.path.join(name)
    return pygame.image.load(fullname)


def start_screen():
    intro_text = ["Тетрис", "",
                  "Правила игры:",
                  "Переворачивайте фигурки клавишей 'вверх';",
                  "Ускоряйте фигурки клавишей 'вниз';",
                  "Двигайте фигурки вправо/влево соответствующими клавишами;",
                  "Собирайте целую строчку, тогда она исчезнет;",
                  "Ловите звезды, чтобы заработать +20 очков;",
                  "Игра закончится, когда не останется места на поле."]

    fon = pygame.transform.scale(load_image('mainphoto.jpeg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font("start&endscreen.ttf", 27)
    text_coord = 30
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
                pygame.draw.rect(screen, pygame.Color("black"),
                                 (5 + j * self.cell_size, 5 + i * self.cell_size,
                                  self.cell_size, self.cell_size), 0)

    # проверка на выход фигуры за поле или столкновение с находящейся рядом фигурой
    def check_borders(self, figure, field):
        if figure[i].x < 0 or figure[i].x > 9:
            return False
        elif figure[i].y > 19 or field[figure[i].y][figure[i].x]:  # либо уже есть цвет, либо 0
            return False
        return True

    # когда игрок доходит до верха, то игра заканчивается, выводится разноцветное поле
    def end(self):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (randrange(0, 256), randrange(0, 256), randrange(0, 256)),
                                 (5 + j * self.cell_size, 5 + i * self.cell_size,
                                  self.cell_size, self.cell_size), 0)
                pygame.display.flip()
                clock.tick(200)

        pygame.init()
        font1 = pygame.font.Font('end_txt.ttf', 70)
        end_text = font1.render("The end", True, pygame.Color("black"))
        screen.blit(end_text, (100, 300))
        pygame.display.flip()
        pygame.time.wait(1000)


# список для координат х клетчатого поля
stars_x = []
for i in range(10):
    stars_x.append(5 + 40 * i)


class Star(pygame.sprite.Sprite):
    star_image = load_image("star.jpg")
    star_image.set_colorkey((255, 255, 255))
    star_image = pygame.transform.scale(star_image, (40, 40))

    def __init__(self, group):
        super().__init__(group)
        self.image = Star.star_image
        self.rect = self.image.get_rect()
        self.rect.x = choice(stars_x)
        self.rect.y = 0

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.kill()
            mainsound.stop()
            shotsound.play()
            global score
            global starsnumber
            score += 20
            starsnumber += 1
        else:
            self.rect.y += 6
            clock.tick(100)


# храним рекорд в файле, если файла нет, создаем его, если есть, открываем и считываем предыдущий рекорд
def get_record():
    try:
        with open("record") as f:
            return f.readline()
    except FileNotFoundError:
        with open("record", "w") as f:
            f.write('0')


# записываем новый рекорд, либо оставляем предыдущий, если он больше
def set_record(record, score):
    maxx = max(int(record), score)
    with open("record", "w") as f:
        f.write(str(maxx))


pygame.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris")
board = Board(10, 20)
all_sprites = pygame.sprite.Group()
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
speed_up = 50

bg = pygame.image.load('mainbackground.jpg').convert()

main_font = pygame.font.Font('mainfont.ttf', 70)
font = pygame.font.Font('mainfont.ttf', 60)
title = main_font.render("Tetris", True, pygame.Color(75, 0, 130))
score_text = font.render("score:", True, pygame.Color(255, 0, 255))
record_text = font.render('record:', True, pygame.Color(148, 0, 211))

mainsound = pygame.mixer.Sound('mainsound.wav')
shotsound = pygame.mixer.Sound('shot_sound.wav')

score, lines = 0, 0
linesnumber = 0
starsnumber = 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}  # зависит от кол-ва линий, убранных одновременно

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))   # рандомно выбираем фигуру
color, next_color = (randrange(0, 256), randrange(0, 256), randrange(0, 256)),\
                    (randrange(0, 256), randrange(0, 256), randrange(0, 256))
FIRE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(FIRE_EVENT, 10000)
while running:
    mainsound.play()
    move_gorizont = 0  # переменная, чтобы двигать по горизонтали
    rotate = False  # переменная чтобы поворачивать фигуру
    screen.blit(bg, (0, 0))
    record = get_record()
    clock.tick(FPS)
    for i in range(lines):
        pygame.time.wait(400)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # сдвиг влево
                move_gorizont = -1
            elif event.key == pygame.K_RIGHT:  # двигаем вправо
                move_gorizont = 1
            elif event.key == pygame.K_DOWN:  # при нажатии кнопки вниз, фигура ускоряется
                maxx_speed = 150
            elif event.key == pygame.K_UP:  # поворачиваем
                rotate = True
        if event.type == FIRE_EVENT:
            Star(all_sprites)
        all_sprites.update(event)
        mainsound.play()

    figure_old = deepcopy(figure)  # копия чтобы вернуть предыдущее положение, если будет выход за границу
    for i in range(4):  # меняем координаты, чтобы сдвинуть по горизонтали
        figure[i].x += move_gorizont
        if not board.check_borders(figure, field):
            figure = deepcopy(figure_old)
            break
    # движение фигурки вниз
    speed += speed_up
    if speed > maxx_speed:
        speed = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not board.check_borders(figure, field):
                for j in range(4):
                    field[figure_old[j].y][figure_old[j].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)),\
                                          (randrange(0, 256), randrange(0, 256), randrange(0, 256))
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
    all_sprites.update()
    line, lines = 19, 0  # первая для кол-ва линий на поле,вторая считает сколько линий ушло(полностью собранные)
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
            speed_up += 1
            lines += 1

    linesnumber += lines
    score += scores[lines]  # очки в зависимости с правилами
    board.render()  # отрисовываем доску
    all_sprites.draw(screen)
    for i in range(4):  # отрисовываем фигуры (т.к. они из 4 клеток каждая)
        figure_rect.x = 5 + figure[i].x * 40
        figure_rect.y = 5 + figure[i].y * 40
        pygame.draw.rect(screen, color, figure_rect)
    # рисуем поле с фигурами, которые уже на нем
    # смотрим по цвету, если в ячейке не ноль, а цвет, то рисуем этот квадрат
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = 5 + x * 40, 5 + y * 40
                pygame.draw.rect(screen, col, figure_rect)
    # рисуем следующую фигуру сбоку
    for i in range(4):
        figure_rect.x = 5 + next_figure[i].x * 40 + 330
        figure_rect.y = 5 + next_figure[i].y * 40 + 150
        pygame.draw.rect(screen, next_color, figure_rect)
    # рисуем текст
    screen.blit(title, (460, 10))

    screen.blit(score_text, (470, 350))
    txt = font.render(str(score), True, pygame.Color(255, 0, 255))
    txt_rect = txt.get_rect(center=(520, 440))
    screen.blit(txt, txt_rect)

    star_im = load_image("star.jpg")
    star_im.set_colorkey((255, 255, 255))
    star_im = pygame.transform.scale(star_im, (40, 40))
    star_rect = (480, 490)
    screen.blit(star_im, star_rect)
    st_num = font.render(str(starsnumber), True, pygame.Color(25, 25, 112))
    st_rect = txt.get_rect(center=(560, 505))
    screen.blit(st_num, st_rect)

    screen.blit(record_text, (460, 530))
    txt2 = font.render(str(record), True, pygame.Color(148, 0, 211))
    txt_rect2 = txt.get_rect(center=(500, 630))
    screen.blit(txt2, txt_rect2)

    txt3 = font.render("lines:", True, pygame.Color(199, 21, 133))
    screen.blit(txt3, (470, 660))
    time_txt = font.render(str(linesnumber), True, pygame.Color(199, 21, 133))
    time_rect = txt.get_rect(center=(520, 760))
    screen.blit(time_txt, time_rect)

    # окончание игры
    for i in range(10):
        if field[0][i]:
            set_record(record, score)
            field = [[0] * 10 for _ in range(20)]
            speed, maxx_speed = 0, 2000
            speed_up = 50
            score = 0
            board.end()
            mainsound.stop()
            continue_game()
            linesnumber = 0
    pygame.display.flip()
pygame.quit()
