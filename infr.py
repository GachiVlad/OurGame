# from settings import *
import pygame
from settings import *


#  Настрока интерфейса pygame, методы для обращения к библиотеке PyGame
class Infrastructure:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 5 * SCALE)  # шрифт
        self.screen = pygame.display.set_mode(
            [WIDTH * SCALE, HEIGHT * SCALE])   # дисплей с заданными размерами
        self.clock = pygame.time.Clock()
        self.speed = 3  # скорость змейки

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

    def fill_screen(self):    # заполнение эрана цветом
        self.screen.fill(SCREEN_COLOR)

    def draw_element(self, x, y, color):  # прямоуголиник на эране
        pygame.draw.rect(
            self.screen,
            pygame.Color(color),
            (x * SCALE, y * SCALE, ELEMENT_SIZE, ELEMENT_SIZE),
            0,
            RADIUS,
        )

    # отображение текста на экране
    def draw_score(self, score: int) -> None:
        self.screen.blit(
            self.font.render(f"Score: {score}", True, pygame.Color(
                SCORE_COLOR)),
            (5, 5),
        )

    # отображение уровня
    def draw_level(self, lvl: int) -> None:
        self.screen.blit(
            self.font.render(f"Level: {lvl}", True, pygame.Color(
                SCORE_COLOR)),
            (5, 50),
        )

    def draw_health(self, health: int) -> None:
        self.screen.blit(
            self.font.render(f"Health: {health}", True, pygame.Color(
                SCORE_COLOR)),
            (225, 5),
        )

    # создание текстовой надписи с определенным текстом и определенным размером
    def draw_game_over(self) -> None:
        message = self.font.render("GAME OVER", True, pygame.Color(
            GAME_OVER_COLOR))
        self.screen.blit(
            message,
            message.get_rect(center=((WIDTH // 2 * SCALE), (
                HEIGHT // 2 * SCALE))),
        )

    def update_and_tick(self) -> None:  # обновление экрана
        pygame.display.update()
        self.clock.tick(FPS * self.speed)

    def quit(self) -> None:  # завершение работы
        pygame.quit()
