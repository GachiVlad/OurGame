from enum import Enum

#  устанавливаем константы для змейки
WIDTH = 50
HEIGHT = 50
SCALE = 10
RADIUS = 1
ELEMENT_SIZE = 10
FPS = 60
INITIAL_SPEED_DELAY = FPS // 2
SNAKE_COLOR = "yellow"
APPLE_COLOR = "red"
SCORE_COLOR = "white"
SCREEN_COLOR = "black"
GAME_OVER_COLOR = "red"


# направление для змейки
class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
