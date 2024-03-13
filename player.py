from settings import *
from collections import deque


class Element:
    """Класс Элемента Поля
    Элемент поля - это объект с определнными координатами

    Attributes
    ----------
    x : float
        Позиция по оси x
    y : float
        Позиция по оси y

    Methods
    ----------
    __init__(x, y)
        Генерация элемента
    __eq__(other)
        Сравнение позиций двух объектов.
    """
    def __init__(self, x: float, y: float) -> None:
        """
        Parameters:
        ----------
        x : float
            Положение элемента по оси x
        y : float
            Положение элемента по оси y
        """
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        """
        Parameters:
        ----------
        other : Element
            Другой элемент, с которым сравниваем
        """
        return self.x == int(other.x) and self.y == int(other.y)


class Snake:
    """Класс Змейки
    Змейка - это и есть игрок

    Attributes
    ----------
    snake : deque
        Список координат составляющих змеи
    direction: Direction
        Направление змейки

    Methods
    ----------
    __init__(head)
        Создание змейки
    set_direction(new_direction)
        Смена направления движения змейки
    enqueue(new_head)
        Новоая голова змейки
    dequeue()
        убирает последний элемент составляющих змейки
    get_new_head()
        получает координату новой головы змеи
    is_contains(element)
        проверка находится ли элемент в змейке
    """
    def __init__(self, head: Element):
        """
        Parameters:
        ----------
        head : Element
            положение змейка в начале игры
        """
        self.snake = deque()
        self.snake.appendleft(head)
        self.direction = Direction.RIGHT  # текущий вектор движения

    def set_direction(self, new_direction) -> None:
        """
        Parameters:
        ----------
        new_direction : Direction
            Новое направление змейки
        """
        # ограниение направления в обратную сторону,
        # когда размер змейки больше одного
        if len(self.snake) == 1 or (
                new_direction.value % 2 != self.direction.value % 2):
            self.direction = new_direction

    def enqueue(self, new_head: Element):
        """
        Parameters:
        ----------
        new_head : Element
            Новая голова змейки
        """
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
        """
        Parameters:
        ----------
        element : Element
            Проверяемый элемент
        """
        # проверка находится ли элемент на змейке
        try:
            self.snake.index(element)
            return True
        except ValueError:
            return False


# получение центра поля для начальной позиции змеи
def gen_center_element() -> Element:
    """Генерирует центральный элемент"""
    return Element(WIDTH // 2, HEIGHT // 2)


# проверка что элемент внутри поля
def is_field_containts(e: Element) -> bool:
    """Проверка, что элемент внутри поля
    Parameters:
        ----------
        e : Element
            Проверяемый элемент
    """
    return 0 <= e.x < WIDTH and 0 <= e.y < HEIGHT


# функция для проверки что внутри не находится на змейке
def is_good_head(element: Element, snake: Snake) -> bool:
    """Проверка, что элемент внутри поля и не на змейке
    Parameters:
        ----------
        element : Element
            Проверяемый элемент
        snake: Snake
            Змейка
    """
    return is_field_containts(element) and not snake.is_contains(element)
