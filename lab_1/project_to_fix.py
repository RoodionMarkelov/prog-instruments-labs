import time
import random
from typing import Any

import pygame

from constants import (GRAY, BLACK, RED, GREEN,
                       BLUE, BRIGHT_RED, BRIGHT_GREEN,
                       BRIGHT_BLUE, DISPLAY_WIDTH, DISPLAY_HEIGHT, CAR_WIDTH)

gamedisplays = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("car game")
clock = pygame.time.Clock()
carimg = pygame.image.load('car1.jpg')
backgroundpic = pygame.image.load("download12.jpg")
yellow_strip = pygame.image.load("yellow strip.jpg")
strip = pygame.image.load("strip.jpg")
intro_background = pygame.image.load("background.jpg")
instruction_background = pygame.image.load("background2.jpg")
pause = False


def programm_inicialization() -> object:
    """
    Функция для инициализации программы.
    Возвращает объект.
    """
    pygame.init()


def intro_loop() -> object:
    """
    Функция выполняет вступительный цикл программы.
    Возвращает объект.
    """
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        gamedisplays.blit(intro_background, (0, 0))
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("CAR GAME", largetext)
        TextRect.center = (400, 100)
        gamedisplays.blit(TextSurf, TextRect)
        button("START", 150, 520, 100, 50, GREEN, BRIGHT_GREEN, "play")
        button("QUIT", 550, 520, 100, 50, RED, BRIGHT_RED, "quit")
        button("INSTRUCTION", 300, 520, 200, 50, BLUE, BRIGHT_BLUE, "intro")
        pygame.display.update()
        clock.tick(50)


def button(msg: Any, x: float, y: float, w: float, h: float, ic: Any, ac: Any, action: object = None) -> object:
    """
    Функция для взаимодействия с кнопками. Рассчитывает координаты кнопки и
    выводит текст при наведении или выполняет определенное действие при клике.
    :param msg: сообщение
    :param x: координата по горизонтали
    :param y: координата по вертикали
    :param w: ширины кнопки
    :param h: высота кнопки
    :param ic: параметр
    :param ac: параметр
    :param action: код действия
    Возвращает объект.
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gamedisplays, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "play":
                countdown()
            elif action == "quit":
                pygame.quit()
                quit()
                sys.exit()
            elif action == "intro":
                introduction()
            elif action == "menu":
                intro_loop()
            elif action == "pause":
                paused()
            elif action == "unpause":
                unpaused()
    else:
        pygame.draw.rect(gamedisplays, ic, (x, y, w, h))
    smalltext = pygame.font.Font("freesansbold.ttf", 20)
    textsurf, textrect = text_objects(msg, smalltext)
    textrect.center = ((x + (w / 2)), (y + (h / 2)))
    gamedisplays.blit(textsurf, textrect)


def introduction() -> object:
    """
    Функция вызова начальнго экрана.
    """
    introduction = True
    while introduction:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        gamedisplays.blit(instruction_background, (0, 0))
        largetext = pygame.font.Font('freesansbold.ttf', 80)
        smalltext = pygame.font.Font('freesansbold.ttf', 20)
        mediumtext = pygame.font.Font('freesansbold.ttf', 40)
        textSurf, textRect = text_objects("This is an car game in which you need dodge the coming cars", smalltext)
        textRect.center = (350, 200)
        TextSurf, TextRect = text_objects("INSTRUCTION", largetext)
        TextRect.center = (400, 100)
        gamedisplays.blit(TextSurf, TextRect)
        gamedisplays.blit(textSurf, textRect)
        stextSurf, stextRect = text_objects("ARROW LEFT : LEFT TURN", smalltext)
        stextRect.center = (150, 400)
        hTextSurf, hTextRect = text_objects("ARROW RIGHT : RIGHT TURN", smalltext)
        hTextRect.center = (150, 450)
        atextSurf, atextRect = text_objects("A : ACCELERATOR", smalltext)
        atextRect.center = (150, 500)
        rtextSurf, rtextRect = text_objects("B : BRAKE ", smalltext)
        rtextRect.center = (150, 550)
        ptextSurf, ptextRect = text_objects("P : PAUSE  ", smalltext)
        ptextRect.center = (150, 350)
        sTextSurf, sTextRect = text_objects("CONTROLS", mediumtext)
        sTextRect.center = (350, 300)
        gamedisplays.blit(sTextSurf, sTextRect)
        gamedisplays.blit(stextSurf, stextRect)
        gamedisplays.blit(hTextSurf, hTextRect)
        gamedisplays.blit(atextSurf, atextRect)
        gamedisplays.blit(rtextSurf, rtextRect)
        gamedisplays.blit(ptextSurf, ptextRect)
        button("BACK", 600, 450, 100, 50, BLUE, BRIGHT_BLUE, "menu")
        pygame.display.update()
        clock.tick(30)


def paused() -> object:
    """
    Функция вызова паузы.
    """
    global pause
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        gamedisplays.blit(instruction_background, (0, 0))
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("PAUSED", largetext)
        TextRect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2))
        gamedisplays.blit(TextSurf, TextRect)
        button("CONTINUE", 150, 450, 150, 50, GREEN, BRIGHT_GREEN, "unpause")
        button("RESTART", 350, 450, 150, 50, BLUE, BRIGHT_BLUE, "play")
        button("MAIN MENU", 550, 450, 200, 50, RED, BRIGHT_RED, "menu")
        pygame.display.update()
        clock.tick(30)


def unpaused() -> object:
    """
    Функция убирает паузу.
    """
    global pause
    pause = False


def countdown_background() -> object:
    """
    Функция ведет подсчет очков за игру.
    """
    font = pygame.font.SysFont(None, 25)
    x = (DISPLAY_WIDTH * 0.45)
    y = (DISPLAY_HEIGHT * 0.8)
    gamedisplays.blit(backgroundpic, (0, 0))
    gamedisplays.blit(backgroundpic, (0, 200))
    gamedisplays.blit(backgroundpic, (0, 400))
    gamedisplays.blit(backgroundpic, (700, 0))
    gamedisplays.blit(backgroundpic, (700, 200))
    gamedisplays.blit(backgroundpic, (700, 400))
    gamedisplays.blit(yellow_strip, (400, 100))
    gamedisplays.blit(yellow_strip, (400, 200))
    gamedisplays.blit(yellow_strip, (400, 300))
    gamedisplays.blit(yellow_strip, (400, 400))
    gamedisplays.blit(yellow_strip, (400, 100))
    gamedisplays.blit(yellow_strip, (400, 500))
    gamedisplays.blit(yellow_strip, (400, 0))
    gamedisplays.blit(yellow_strip, (400, 600))
    gamedisplays.blit(strip, (120, 200))
    gamedisplays.blit(strip, (120, 0))
    gamedisplays.blit(strip, (120, 100))
    gamedisplays.blit(strip, (680, 100))
    gamedisplays.blit(strip, (680, 0))
    gamedisplays.blit(strip, (680, 200))
    gamedisplays.blit(carimg, (x, y))
    text = font.render("DODGED: 0", True, BLACK)
    score = font.render("SCORE: 0", True, RED)
    gamedisplays.blit(text, (0, 50))
    gamedisplays.blit(score, (0, 30))
    button("PAUSE", 650, 0, 150, 50, BLUE, BRIGHT_BLUE, "pause")


def countdown() -> object:
    """
    Функция вызывает обратный отстчет до начала игры.
    """
    countdown = True
    while countdown:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        gamedisplays.fill(GRAY)
        countdown_background()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("3", largetext)
        TextRect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2))
        gamedisplays.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        gamedisplays.fill(GRAY)
        countdown_background()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("2", largetext)
        TextRect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2))
        gamedisplays.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        gamedisplays.fill(GRAY)
        countdown_background()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("1", largetext)
        TextRect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2))
        gamedisplays.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        gamedisplays.fill(GRAY)
        countdown_background()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("GO!!!", largetext)
        TextRect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2))
        gamedisplays.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        game_loop()


def obstacle(obs_startx: float, obs_starty: float, obs: Any) -> object:
    """
    Функция создает случной препятсвие в виде машины случайного цвета и формы.
    :param obs_startx: начальная координата x для препятствия
    :param obs_starty: начальная координата y для препятствия
    :param obs: случайное значение для выбора машины-препятствия
    """
    if obs == 0:
        obs_pic = pygame.image.load("car.jpg")
    elif obs == 1:
        obs_pic = pygame.image.load("car1.jpg")
    elif obs == 2:
        obs_pic = pygame.image.load("car2.jpg")
    elif obs == 3:
        obs_pic = pygame.image.load("car4.jpg")
    elif obs == 4:
        obs_pic = pygame.image.load("car5.jpg")
    elif obs == 5:
        obs_pic = pygame.image.load("car6.jpg")
    elif obs == 6:
        obs_pic = pygame.image.load("car7.jpg")
    gamedisplays.blit(obs_pic, (obs_startx, obs_starty))


def score_system(passed: Any, score: int) -> object:
    """
    Функция подсчитывает пройденный путь игроком и количество очков,
    накопленных игроком.
    :param passed: пройденный путь
    :param score: очки накопленные за игру
    """
    font = pygame.font.SysFont(None, 25)
    text = font.render("Passed" + str(passed), True, BLACK)
    score = font.render("Score" + str(score), True, RED)
    gamedisplays.blit(text, (0, 50))
    gamedisplays.blit(score, (0, 30))


def text_objects(text: str, font: Any) -> tuple:
    """
    Функция отображает текстовые объекты.
    :param text: текст объекта
    :param font: шрифт текста
    :return: tuple[font.render(text, True, BLACK), font.render(text, True, BLACK)]
    """
    textsurface = font.render(text, True, BLACK)
    return textsurface, textsurface.get_rect()


def message_display(text: str) -> object:
    """
    Функция вызова дисплея с сообщением.
    :param text: сообщение
    """
    largetext = pygame.font.Font("freesansbold.ttf", 80)
    textsurf, textrect = text_objects(text, largetext)
    textrect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2))
    gamedisplays.blit(textsurf, textrect)
    pygame.display.update()
    time.sleep(3)
    game_loop()


def crash() -> object:
    """
    Функция выводит сообщение о крушение автомобиля. то есть конца игры.
    """
    message_display("YOU CRASHED")


def background() -> object:
    """
    Функция отоброжает задний фон игры.
    """
    gamedisplays.blit(backgroundpic, (0, 0))
    gamedisplays.blit(backgroundpic, (0, 200))
    gamedisplays.blit(backgroundpic, (0, 400))
    gamedisplays.blit(backgroundpic, (700, 0))
    gamedisplays.blit(backgroundpic, (700, 200))
    gamedisplays.blit(backgroundpic, (700, 400))
    gamedisplays.blit(yellow_strip, (400, 0))
    gamedisplays.blit(yellow_strip, (400, 100))
    gamedisplays.blit(yellow_strip, (400, 200))
    gamedisplays.blit(yellow_strip, (400, 300))
    gamedisplays.blit(yellow_strip, (400, 400))
    gamedisplays.blit(yellow_strip, (400, 500))
    gamedisplays.blit(strip, (120, 0))
    gamedisplays.blit(strip, (120, 100))
    gamedisplays.blit(strip, (120, 200))
    gamedisplays.blit(strip, (680, 0))
    gamedisplays.blit(strip, (680, 100))
    gamedisplays.blit(strip, (680, 200))


def car(x: float, y: float) -> object:
    """
    Функция вычисляет координаты автомобиля игрока.
    :param x: координата x автомобиля игрока
    :param y: координата y автомобиля игрока
    """
    gamedisplays.blit(carimg, (x, y))


def game_loop() -> object:
    """
    Функция запускает игровой цикл.
    """
    global pause
    x = (DISPLAY_WIDTH * 0.45)
    y = (DISPLAY_HEIGHT * 0.8)
    x_change = 0
    obstacle_speed = 9
    obs = 0
    y_change = 0
    obs_startx = random.randrange(200, (DISPLAY_WIDTH - 200))
    obs_starty = -750
    obs_width = 56
    obs_height = 125
    passed = 0
    level = 0
    score = 0
    y2 = 7
    fps = 120

    bumped = False
    while not bumped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_a:
                    obstacle_speed += 2
                if event.key == pygame.K_b:
                    obstacle_speed -= 2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        x += x_change
        pause = True
        gamedisplays.fill(GRAY)

        rel_y = y2 % backgroundpic.get_rect().width
        gamedisplays.blit(backgroundpic, (0, rel_y - backgroundpic.get_rect().width))
        gamedisplays.blit(backgroundpic, (700, rel_y - backgroundpic.get_rect().width))
        if rel_y < 800:
            gamedisplays.blit(backgroundpic, (0, rel_y))
            gamedisplays.blit(backgroundpic, (700, rel_y))
            gamedisplays.blit(yellow_strip, (400, rel_y))
            gamedisplays.blit(yellow_strip, (400, rel_y + 100))
            gamedisplays.blit(yellow_strip, (400, rel_y + 200))
            gamedisplays.blit(yellow_strip, (400, rel_y + 300))
            gamedisplays.blit(yellow_strip, (400, rel_y + 400))
            gamedisplays.blit(yellow_strip, (400, rel_y + 500))
            gamedisplays.blit(yellow_strip, (400, rel_y - 100))
            gamedisplays.blit(strip, (120, rel_y - 200))
            gamedisplays.blit(strip, (120, rel_y + 20))
            gamedisplays.blit(strip, (120, rel_y + 30))
            gamedisplays.blit(strip, (680, rel_y - 100))
            gamedisplays.blit(strip, (680, rel_y + 20))
            gamedisplays.blit(strip, (680, rel_y + 30))

        y2 += obstacle_speed
        obs_starty -= (obstacle_speed / 4)
        obstacle(obs_startx, obs_starty, obs)
        obs_starty += obstacle_speed
        car(x, y)
        score_system(passed, score)
        if x > 690 - CAR_WIDTH or x < 110:
            crash()
        if x > DISPLAY_WIDTH - (CAR_WIDTH + 110) or x < 110:
            crash()
        if obs_starty > DISPLAY_HEIGHT:
            obs_starty = 0 - obs_height
            obs_startx = random.randrange(170, (DISPLAY_WIDTH - 170))
            obs = random.randrange(0, 7)
            passed = passed + 1
            score = passed * 10
            if int(passed) % 10 == 0:
                level = level + 1
                obstacle_speed + 2
                largetext = pygame.font.Font("freesansbold.ttf", 80)
                textsurf, textrect = text_objects("LEVEL" + str(level), largetext)
                textrect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2))
                gamedisplays.blit(textsurf, textrect)
                pygame.display.update()
                time.sleep(3)
        if y < obs_starty + obs_height:
            if (x > obs_startx and
                x < obs_startx + obs_width or
                x + CAR_WIDTH > obs_startx and
                x + CAR_WIDTH < obs_startx + obs_width):
                crash()
        button("Pause", 650, 0, 150, 50, BLUE, BRIGHT_BLUE, "pause")
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    programm_inicialization()
    intro_loop()
    game_loop()
    pygame.quit()
    quit()
