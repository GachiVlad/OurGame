import pygame
from collections import deque
from random import randrange
from settings import *

import player as pl
import objects as obj

# code reminder:  you make new classes for apples and peaches
# then you make code for final boss


# получение центра поля для начальной позиции змеи
def gen_center_element() -> pl.Element:
    return pl.Element(WIDTH // 2, HEIGHT // 2)


# проверка что элемент внутри поля
def is_field_containts(e: pl.Element) -> bool:
    return 0 <= e.x < WIDTH and 0 <= e.y < HEIGHT


# функция для проверки что внутри не находится на змейке
def is_good_head(head: pl.Element, snake: pl.Snake) -> bool:
    return is_field_containts(head) and not snake.is_contains(head)


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

# Собираем все


class Game:
    def __init__(self, infrastructure: Infrastructure) -> None:
        self.infrastructure = infrastructure
        head = gen_center_element()
        self.snake = pl.Snake(head)
        self.walls = []
        self.fruits = [obj.Apple(self.snake, self.walls)]
        self.tick_counter = 0
        self.score = 9
        self.snake_speed_delay = INITIAL_SPEED_DELAY
        self.is_running = True
        self.is_game_over = False
        self.lvl = 1  # уровень змейки

    # Обработка событий, таких как нажатия клавиш и выход из игры
    def process_events(self) -> None:
        if self.infrastructure.is_quit_event():
            self.is_running = False
        new_direction = self.infrastructure.get_pressed_key()
        if new_direction is not None:
            self.snake.set_direction(new_direction)

    def newlevel(self):
        if self.lvl == 1 and self.score >= 10:
            self.lvl = 2
            self.infrastructure.speed += 1
            self.walls.append(obj.Wall(self.snake, self.walls))
            self.fruits.append(obj.Pear(self.snake, self.walls))
        if self.lvl == 2 and self.score >= 25:
            self.lvl = 3
            self.infrastructure.speed += 1
            self.walls.extend([obj.Wall(self.snake, self.walls),
                               obj.Wall(self.snake, self.walls)])
            self.fruits.extend([obj.Apple(self.snake, self.walls),
                                obj.Apple(self.snake, self.walls)])

    def update_state(self) -> None:
        if self.is_game_over:
            return
        self.tick_counter += 1
        if not self.tick_counter % self.snake_speed_delay:
            head = self.snake.get_new_head()
            if is_good_head(head, self.snake):
                if any(head == wall.obj for wall in self.walls):
                    self.is_game_over = True
                self.snake.enqueue(head)
                ate = 0
                for object in self.fruits:
                    if head == object.obj:
                        self.score = object.eaten(
                            self.score, self.snake, self.walls)
                        ate = 1
                        self.newlevel()
                if ate == 0:
                    self.snake.dequeue()
                for i in range(0, len(self.fruits)):
                    if type(self.fruits[i]) is obj.Pear:
                        self.fruits[i].move()
            else:
                self.is_game_over = True

    def render(self) -> None:
        self.infrastructure.fill_screen()
        for e in self.snake.snake:
            self.infrastructure.draw_element(e.x, e.y, SNAKE_COLOR)

        for object in self.fruits:
            object.draw_obj(self.infrastructure)

        if len(self.walls) > 0:
            for wall in self.walls:
                wall.draw_obj(self.infrastructure)

        self.infrastructure.draw_score(self.score)

        self.infrastructure.draw_level(self.lvl)

        if self.is_game_over:
            self.infrastructure.draw_game_over()
        self.infrastructure.update_and_tick()

    def loop(self):
        while self.is_running:
            self.process_events()
            self.update_state()
            self.render()
        self.infrastructure.quit()


if __name__ == "__main__":
    game = Game(Infrastructure())
    game.loop()
