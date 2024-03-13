from enum import Enum

#  устанавливаем константы для змейки
WIDTH = 50
HEIGHT = 50
SCALE = 12
RADIUS = 1
ELEMENT_SIZE = 10
FPS = 60
GAME_SPEED_INIT = 3 # начальная сокрость игры
INITIAL_SPEED_DELAY = FPS // 2
SNAKE_COLOR = "yellow"
APPLE_COLOR = "red"
SCORE_COLOR = "white"
SCREEN_COLOR = "black"
GAME_OVER_COLOR = "red"
PEAR_COLOR = "orange"
WALL_COLOR = "white"


# направление для змейки
class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


# вычисление прибавки очков для новго уровня
def delta_score_per_level(lvl: int):
    """Функция рассчета необходимой прибавки очков для повышения уровня
    Примеры: 
    Для перехода с 1 по 2 уровень игрок должен повысить свои очки на 5
    Для перехода с 2 на 3 уровень - на 10 очков. 
    Это значит, что в сумме у игрока должно быть 15 очков, чтобы перейти 
    с 1 на 3 уровень

    Parameters:
    ----------
    lvl: int
        Текущий уровень игрока
    """
    return (5 + 5 * (lvl - 1))
