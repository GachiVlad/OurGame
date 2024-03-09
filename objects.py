from settings import *
from random import randrange
import player as pl


# класс объектов
class Object:
    def __init__(self, snake: pl.Snake, walls) -> None:
        self.color = None
        self.gen_object(snake, walls)

    def get_random_element() -> pl.Element:
        return pl.Element(randrange(0, WIDTH - 2), randrange(0, HEIGHT - 2))

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

    def draw_obj(self, infrastructure):
        infrastructure.draw_element(
            self.obj.x, self.obj.y, self.color)


class Apple(Object):
    def __init__(self, snake: pl.Snake, walls) -> None:
        Object.__init__(self, snake, walls)
        self.color = APPLE_COLOR

    def eaten(self, score, snake, walls):
        score += 1
        self.gen_object(snake, walls)
        return score


class Pear(Object):
    def __init__(self, snake: pl.Snake, walls) -> None:
        Object.__init__(self, snake, walls)
        self.color = PEAR_COLOR

    def eaten(self, score, snake, walls):
        score += 4
        self.gen_object(snake, walls)
        return score

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

        if self.obj.x == WIDTH + 1:
            self.obj.x = 1
        if self.obj.y == HEIGHT + 1:
            self.obj.y = 1
        if self.obj.x < 0:
            self.obj.x = WIDTH - 1
        if self.obj.y < 0:
            self.obj.y = HEIGHT - 1


class Wall(Object):
    def __init__(self, snake: pl.Snake, walls) -> None:
        Object.__init__(self, snake, walls)
        self.color = WALL_COLOR
