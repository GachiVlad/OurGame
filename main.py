import pygame 
import time 
import random

#  устанавливаем константы и доплолняем по ходу 
WIDTH = 10
HEIGHT = 20
SCALE = 40
RADIUS = 5
ELEMENT_SIZE = 38
FPS = 60
INITIAL_SPEED_DELAY = FPS // 2
SNAKE_COLOR = "yellow"
APPLE_COLOR = "red"
SCORE_COLOR = "white"
SCREEN_COLOR = "black"
GAME_OVER_COLOR = "red"

pygame.init()
screen = pygame.display.set_mode([1050,480]) # устанавливаем маштаб окна
clock = pygame.time.Clock()

is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            print(" quit event")
            is_running = False
    pygame.display.update()
    clock.tick(60)
pygame.quit()

# направление для змейки 
from enum import Enum 
class  Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4 

class Element:
    def __init__(self, x: int, y: int) -> None:  
        self.x = x 
        self.y = y 

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y



from collections import deque


class Snake:
    def __init__(self, head: Element):
        self.snake = deque()
        self.snake.appendleft(head)
        self.direction = Direction.RIGHT # текущий вектор движения 


    def set_direction(self, new_direction) -> None:
        if len(self.deque) == 1 or new_direction.value % 2 != self.direction.value % 2:
            self.direction = new_direction  # ограниение направления в обратную сторону, когда размер змейки больше одного 

         
    def enqueue(self, new_head: Element):
        self.snake.appendleft(new_head)

    def dequeue(self):
        self.snake.pop()  

    def get_new_head(self) ->Element:   # направление движения
        head = self.deque[0]
        if self.direction == Direction.UP:
            return Element (head.x, head.y +1)
        if self.direction == Direction.RIGHT:
            return Element (head.x +1,  head.y)
        if self.direction == Direction.DOWN:
            return Element (head.x, head.y -1)
        if self.direction == Direction.LEFT:
            return Element (head.x -1 , head.y)

    def is_contains(self, element: Element) -> bool:  # проверка находится ли элемент на змейке
        try:
            self.snake.index(element)
            return True
        except ValueError:
            return False

from random import randrange   # генератор случайного элемента нашего поля для появления, например, яблока

def get_random_element() -> Element:
    return Element(randrange(0, WIDTH), randrange(0, HEIGHT))
    
def gen_apple(snake: Snake):
    candidate = None
    while candidate is None:
        candidate = get_random_element()
        if snake.is_contains(candidate):    # проверка находится ли яблоко уже в теле змеи
            candidate = None
    return candidate


def gen_center_element() -> Element:  # получение центра поля для начально позиции змеи
    return Element(WIDTH // 2, HEIGHT // 2)


def is_field_containts(e: Element) -> bool:  # проверка что элемент внутри поля 
    return 0 <= e.x < WIDTH and 0 <=e.y < HEIGHT


def is_good_head ( head: Element, snake: Snake) -> bool:    # функция для проверки что внутри не находится на змейке
    return is_field_containts(head) and not snake.is_contains(head)


#  Настрока интерфейса pygame, методы для обращения к библиотеке PyGame

class Infrastructure:
    def __init__(self):    
        pygame.init()
        self.font = pygame.font.Font(None, SCALE)  # шрифт
        self.screen = pygame.display.set_mode([WIDTH * SCALE, HEIGHT * SCALE])   # дисплей с заданными размерами
        self.clock = pygame.time.Clock()  
        
    def is_quit_event(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # проверка на выход из игры
                print("quit event")
                return True    
        return False
       
    def get_pressed_key(self) -> Direction | None:  # работа с клавишами
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

    def fill_screen(self):    #заполнение эрана цветом
        self.screen.fill(SCREEN_COLOR)
        
    def draw_element(self, x, y, color):  # прямоуголиник на эране 
        pygame.draw.rect(
            self.screen,
            pygame.Color(color),
            (x * SCALE, y * SCALE, ELEMENT_SIZE, ELEMENT_SIZE),
            0,
            RADIUS,
        )
        
    def draw_score(self, score: int) -> None:   # отображение текста на экране 
        self.screen.blit(
            self.font.render(f"Score: {score}", True, pygame.Color(SCORE_COLOR)),
            (5, 5),
        )

    def draw_game_over(self) -> None:    # создание текстовой надписи с определенным текстом и определенным размером
        message = self.font.render("GAME OVER", True, pygame.Color(GAME_OVER_COLOR))
        self.screen.blit(
            message,
            message.get_rect(center=((WIDTH // 2 * SCALE), (HEIGHT // 2 * SCALE))),
        )

    def update_and_tick(self) -> None:  #  обновление экрана 
        pygame.display.update()
        self.clock.tick(FPS)

    def quit(self) -> None:  # завершение работы 
        pygame.quit()
        
        
        
# Собираем все 


class Game:
    def __init__(self, infrastructure: Infrastructure) -> None:
        self.infrastructure = infrastructure
        head = gen_center_element()
        self.snake = Snake(head)
        self.apple = gen_apple(self.snake)
        self.tick_counter = 0
        self.score = 0
        self.snake_speed_delay = INITIAL_SPEED_DELAY
        self.is_running = True
        self.is_game_over = False

        
    def process_events(self) -> None : #Обработка событий, таких как нажатия клавиш и выход из игры
            if self.infrastructure.is_quit_event():
                self.is_running = False
            new_direction = self.infrastructure.get_pressed_key()
            if new_direction is not None:
                self.snake.set_direction(new_direction)
                
    def update_state(self) -> None:
        if self.is_game_over:
            return
        self.tick_counter +=1
        if not self.tick_counter % self.snake_speed_delay:
            head = self.snake.get_new_head()
            if is_good_head( self.head, self.snake):
                self.snake.enqueue(head)
                if head == self.apple:
                    self.score += 1
                    self.apple = gen_apple(self.snake)
                else:
                    self.snake.dequeue()
            else:
                self.is_game_over = True

    def render(self) -> None:
        self.infrastructure.fill_screen()
        for e in self.snake.snake:
            self.infrastructure.draw_element(e.x, e.y, SNAKE_COLOR)
        self.infrastructure.draw_element(self.apple.x, self.apple.y, APPLE_COLOR)
        self.infrastructure.draw_score(self.score)
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
