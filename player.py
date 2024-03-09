from settings import *
from collections import deque


class Element:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        return self.x == int(other.x) and self.y == int(other.y)


class Snake:
    def __init__(self, head: Element):
        self.snake = deque()
        self.snake.appendleft(head)
        self.direction = Direction.RIGHT  # текущий вектор движения

    def set_direction(self, new_direction) -> None:
        # ограниение направления в обратную сторону,
        # когда размер змейки больше одного
        if len(self.snake) == 1 or (
                new_direction.value % 2 != self.direction.value % 2):
            self.direction = new_direction

    def enqueue(self, new_head: Element):
        self.snake.appendleft(new_head)

    def dequeue(self):
        self.snake.pop()

    def get_new_head(self) -> Element:   # направление движения
        head = self.snake[0]
        if self.direction == Direction.UP:
            return Element(head.x, head.y + 1)
        if self.direction == Direction.RIGHT:
            return Element(head.x + 1, head.y)
        if self.direction == Direction.DOWN:
            return Element(head.x, head.y - 1)
        if self.direction == Direction.LEFT:
            return Element(head.x - 1, head.y)

    def is_contains(self, element: Element) -> bool:
        # проверка находится ли элемент на змейке
        try:
            self.snake.index(element)
            return True
        except ValueError:
            return False


# получение центра поля для начальной позиции змеи
def gen_center_element() -> Element:
    return Element(WIDTH // 2, HEIGHT // 2)


# проверка что элемент внутри поля
def is_field_containts(e: Element) -> bool:
    return 0 <= e.x < WIDTH and 0 <= e.y < HEIGHT


# функция для проверки что внутри не находится на змейке
def is_good_head(head: Element, snake: Snake) -> bool:
    return is_field_containts(head) and not snake.is_contains(head)
