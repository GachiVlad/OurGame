# from settings import *
import pygame
from settings import *


#  Настрока интерфейса pygame, методы для обращения к библиотеке PyGame
class Infrastructure:
    """Класс работы с pygame (инфраструктура проекта)
    Задает взаимодействие игрока с игрой и отрисовку объектов и элементов игры.
    Attributes
    ----------
    font : pygame.font
        шрифт игры
    screen : pygame.display
        экран с заданными размерами
    clock : pygame.time.Clock()
        внутренние часы игры
    speed: int
        скорость игры, скорость змейки

    Methods
    ----------
    __init__()
        Инифиализирует pygame
    is_quit_event()
        Обработка выхода из игры
    get_pressed_key()
        Обработка нажатия клавиш стрелочек, управление игроком игрой
    fill_screen()
        Заполнение эрана цветом
    draw_element(x, y, color)
        Отрисовка элемента поля с заданными координатами и цветом
    draw_score(score)
        Отображение очков на экране
    draw_level(lvl)
        Отображение уровня на экране
    draw_health(health)
        Отображение здоровья на экране
    draw_game_over()
        Отображение надписи окончания игры
    update_and_tick()
        Обновление экрана и состояния игры
    quit()
        Завершение работы
    """
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 5 * SCALE)  # шрифт
        self.screen = pygame.display.set_mode(
            [WIDTH * SCALE, HEIGHT * SCALE])   # дисплей с заданными размерами
        self.clock = pygame.time.Clock()
        self.speed = GAME_SPEED_INIT  # скорость игры, скорость змейки

    def is_quit_event(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # проверка на выход из игры
                print("quit event")
                return True
        return False

    def get_pressed_key(self) -> Direction:  # работа с клавишами
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            return Direction.DOWN
        if key[pygame.K_RIGHT]:
            return Direction.RIGHT
        if key[pygame.K_DOWN]:
            return Direction.UP
        if key[pygame.K_LEFT]:
            return Direction.LEFT
        return None

    def fill_screen(self):
        self.screen.fill(SCREEN_COLOR)

    def draw_element(self, x, y, color):
        """
        Parameters:
        ----------
        x : float
            положение по оси x
        y : float
            положение по оси y
        color : str
            цвет
        """
        pygame.draw.rect(
            self.screen,
            pygame.Color(color),
            (x * SCALE, y * SCALE, ELEMENT_SIZE, ELEMENT_SIZE),
            0,
            RADIUS,
        )

    def draw_score(self, score: int) -> None:
        """
        Parameters:
        ----------
        score : int
            Количество очков игрока
        """
        self.screen.blit(
            self.font.render(f"Score: {score}", True, pygame.Color(
                SCORE_COLOR)),
            (5, 5),
        )

    def draw_level(self, lvl: int) -> None:
        """
        Parameters:
        ----------
        lvl : int
            Уровень игрока
        """
        self.screen.blit(
            self.font.render(f"Level: {lvl}", True, pygame.Color(
                SCORE_COLOR)),
            (5, 50),
        )

    def draw_health(self, health: int) -> None:
        """
        Parameters:
        ----------
        health : int
            Здоровье игрока
        """
        self.screen.blit(
            self.font.render(f"Health: {health}", True, pygame.Color(
                SCORE_COLOR)),
            (225, 5),
        )

    def draw_game_over(self) -> None:
        message = self.font.render("GAME OVER", True, pygame.Color(
            GAME_OVER_COLOR))
        self.screen.blit(
            message,
            message.get_rect(center=((WIDTH // 2 * SCALE), (
                HEIGHT // 2 * SCALE))),
        )

    def update_and_tick(self) -> None:
        pygame.display.update()
        self.clock.tick(FPS * self.speed)

    def quit(self) -> None:
        pygame.quit()
