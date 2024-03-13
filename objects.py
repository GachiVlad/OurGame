from settings import *
from random import randrange
import player as pl


# класс объектов
class Object:
    # общая инициализация объектов. Создает объект
    def __init__(self, snake: pl.Snake, walls) -> None:
        self.gen_object(snake, walls)

    # генерирует случайное положение на игровом поле
    def get_random_element() -> pl.Element:
        return pl.Element(randrange(2, WIDTH - 2), randrange(2, HEIGHT - 2))

    # генерирует наш объект, проверяя, что он вне стенки и змеи
    def gen_object(self, snake: pl.Snake, walls):
        candidate = None
        while candidate is None:
            candidate = Object.get_random_element()
            # проверка находится ли яблоко уже в теле змеи
            if snake.is_contains(candidate):
                candidate = None
            if len(walls) > 0:
                for wall in walls:
                    if candidate == wall.obj:
                        candidate = None
        self.obj = candidate


# класс яблока. Яблоко - стандартный фрукт
class Apple(Object):
    # создание яблока, придаем ему цвет яблока
    def __init__(self, snake: pl.Snake, walls) -> None:
        Object.__init__(self, snake, walls)
        self.color = APPLE_COLOR

    # метод, вызываемый когда яблоко съели.
    # Генерирует новое яблоко и увеличивает очки на 1
    def eaten(self, score, snake, walls):
        score += 1
        self.gen_object(snake, walls)
        return score


# класс груши. Груша - наше нововведение.
# отличается от яблкоа тем, что перемещается по полю и дает больше очков
class Pear(Object):
    # создание груши, придаем ей цвет груши
    def __init__(self, snake: pl.Snake, walls) -> None:
        Object.__init__(self, snake, walls)
        self.color = PEAR_COLOR

    # метод, вызываемый когда грушу съели.
    # Генерирует новую грушу и увеличивает очки на 4
    def eaten(self, score, snake, walls):
        score += 4
        self.gen_object(snake, walls)
        return score

    # метод перемещения груши.
    def move(self):
        direction = randrange(1, 4)
        if direction == 1:
            self.obj.y += 0.5
        if direction == 2:
            self.obj.x += 0.5
        if direction == 3:
            self.obj.y += -0.5
        if direction == 4:
            self.obj.x += -0.5

    # если груша выходит за грани игрового поля, то она появляется
    # на другом конце поля
        if self.obj.x == WIDTH + 1:
            self.obj.x = 1
        if self.obj.y == HEIGHT + 1:
            self.obj.y = 1
        if self.obj.x < 0:
            self.obj.x = WIDTH - 1
        if self.obj.y < 0:
            self.obj.y = HEIGHT - 1


# класс стены - непроходимого препятствия
class Wall(Object):
    def __init__(self, snake: pl.Snake, walls) -> None:
        Object.__init__(self, snake, walls)
        self.color = WALL_COLOR
