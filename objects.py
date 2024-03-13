from settings import *
from random import randrange
import player as pl


# класс объектов
class Object:
    """Класс объектов
    Родительский класс для неподконтрольных игроку элементов поля:
    1) Яблоко
    2) Груша
    3) Стена

    Attributes
    ----------
    obj : pl.Element
        Позиция объекта

    Methods
    ----------
    __init__(snake, walls)
        Генерация объекта
    get_random_element()
        Генерация случайного элемента поля
    gen_object(snake, walls)
        Генерация объекта со случайным положением, чтобы он
        не находился внутри стены или змейки
    """
    # общая инициализация объектов. Создает объект
    def __init__(self, snake: pl.Snake, walls) -> None:
        """
        Parameters:
        ----------
        snake : pl.Snake
            Змейка,положение ее элементов
        walls : list
            Стены, их положения
        """
        self.gen_object(snake, walls)

    # генерирует случайное положение на игровом поле
    def get_random_element() -> pl.Element:
        return pl.Element(randrange(2, WIDTH - 2), randrange(2, HEIGHT - 2))

    # генерирует наш объект, проверяя, что он вне стенки и змеи
    def gen_object(self, snake: pl.Snake, walls):
        """
        Parameters:
        ----------
        snake : pl.Snake
            Змейка,положение ее элементов
        walls : list
            Стены, их положения
        """
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
    """Класс Яблок
    Яблоко. При съедении дает 1 очко, статично

    Attributes
    ----------
    obj : pl.Element
        Позиция объекта
    color : str
        Цвет Яблока

    Methods
    ----------
    __init__(snake, walls)
        Генерация объекта
    eaten(score, snake, walls)
        Метод съедения яблока. Вызывается когда яблоко съели, генерирует новое
    """

    # создание яблока, придаем ему цвет яблока
    def __init__(self, snake: pl.Snake, walls) -> None:
        """
        Parameters:
        ----------
        snake : pl.Snake
            Змейка,положение ее элементов
        walls : list
            Стены, их положения
        """
        Object.__init__(self, snake, walls)
        self.color = APPLE_COLOR

    # метод, вызываемый когда яблоко съели.
    # Генерирует новое яблоко и увеличивает очки на 1
    def eaten(self, score, snake, walls):
        """
        Возвращает кол-во очков после съедения яблока
        Parameters:
        ----------
        score : int
            Текущие очки игрока
        snake : pl.Snake
            Змейка,положение ее элементов
        walls : list
            Стены, их положения
        """
        score += 1
        self.gen_object(snake, walls)
        return score


# класс груши. Груша - наше нововведение.
# отличается от яблкоа тем, что перемещается по полю и дает больше очков
class Pear(Object):
    """Класс Груши
    Груша - наше нововведение.
    Отличается от яблкоа тем, что перемещается по полю и дает больше очков

    Attributes
    ----------
    obj : pl.Element
        Позиция объекта
    color : str
        Цвет Груши

    Methods
    ----------
    __init__(snake, walls)
        Генерация объекта
    eaten(score, snake, walls)
        Метод съедения груши. Вызывается когда грушу съели, генерирует новую
    move()
        Метод перемещения груши
    """
    # создание груши, придаем ей цвет груши
    def __init__(self, snake: pl.Snake, walls) -> None:
        """
        Parameters:
        ----------
        snake : pl.Snake
            Змейка,положение ее элементов
        walls : list
            Стены, их положения
        """
        Object.__init__(self, snake, walls)
        self.color = PEAR_COLOR

    # метод, вызываемый когда грушу съели.
    # Генерирует новую грушу и увеличивает очки на 4
    def eaten(self, score, snake, walls):
        """
        Возвращает кол-во очков после съедения груши
        Parameters:
        ----------
        score : int
            Текущие очки игрока
        snake : pl.Snake
            Змейка,положение ее элементов
        walls : list
            Стены, их положения
        """
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
    """Класс Стены.
    Стена - еще  одно наше нововведение.
    При столкновении со стеной змейка теряет жизни

    Attributes
    ----------
    obj : pl.Element
        Позиция объекта
    color : str
        Цвет Стены
    """
    def __init__(self, snake: pl.Snake, walls):
        """
        Parameters:
        ----------
        score : int
            Текущие очки игрока
        snake : pl.Snake
            Змейка,положение ее элементов
        walls : list
            Стены, их положения
        """
        Object.__init__(self, snake, walls)
        self.color = WALL_COLOR
