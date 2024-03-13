from settings import *
import infr
import player as pl
import objects as obj


class Game:
    """Класс Игры
    Это сама игра, здесь задает взаимодействие инфраструктуры со змейкой
    и объектами

    Attributes
    ----------
    infrastructure : infr.Infrastructure
        Инфраструктура игры
    snake : pl.Snake
        Змейка
    walls : list
        Список стен в текущй игры
    fruits : list
        Список фруктов в текущей игре
    tick_counter : int
        Внутренние часы игры
    score : int
        Количество очков
    snake_speed_delay : int
    is_running : bool
        Флаг, показывает, запущена игра или нет
    is_game_over : bool
        Флаг, показывает, проиграл ли игрок или нет
    lvl : int
        уровень игрока
    health : int
        Здоровье змейки
    hit : bool
        Флаг, показывает, ударилась ли змейка на предыдущем шаге
    req_score : int
        Очки, требуемые для повышения уровня

    Methods
    ----------
    __init__(snake, walls)
        Запуск игры
    process_events()
        Обработка событий, таких как нажатия клавиш и выход из игры
    newlevel()
        Работа с новым уровнем змейки
    update_state()
        Обновление состояния игры на новом шаге
    render()
        Отрисовка игры
    loop()
        Цикл прохождения игры
    """
    def __init__(self, infrastructure: infr.Infrastructure) -> None:
        """
         Parameters:
        ----------
        infrastructure : infr.Infrastructure
            Инфраструктура игры
        """
        self.infrastructure = infrastructure
        head = pl.gen_center_element()
        self.snake = pl.Snake(head)
        self.walls = []  # стены
        self.fruits = [obj.Apple(self.snake, self.walls)]  # фрукты
        self.tick_counter = 0
        self.score = 0  # очки
        self.snake_speed_delay = INITIAL_SPEED_DELAY
        self.is_running = True
        self.is_game_over = False
        self.lvl = 1  # уровень змейки
        self.health = 1  # здоровье змейки
        self.hit = False  # флаг, получила ли змейка удар
        self.req_score = 0  # очки, требуемые для получения нового уровня

    # Обработка событий, таких как нажатия клавиш и выход из игры
    def process_events(self) -> None:
        if self.infrastructure.is_quit_event():
            self.is_running = False
        new_direction = self.infrastructure.get_pressed_key()
        if new_direction is not None:
            self.snake.set_direction(new_direction)

    def newlevel(self):  # это функция работы с уровнями
        if self.score >= self.req_score + delta_score_per_level(self.lvl):
            # повышение требуемых очков для повышения уровня
            self.req_score += delta_score_per_level(self.lvl)

            self.lvl += 1  # повышение уровня
            self.health += 1  # доп здоровье
            self.infrastructure.speed += 1  # увеличение скорости игры

            # добавление новых стенок, в зависисмости от уровня
            for i in range(0, self.lvl):
                self.walls.append(obj.Wall(self.snake, self.walls))
            # если уровень четный - добавляет персик
            # если нечетный - добавляет 2 яблока
            if (self.lvl % 2) == 0:
                self.fruits.append(obj.Pear(self.snake, self.walls))
            else:
                self.fruits.append(obj.Apple(self.snake, self.walls))
                self.fruits.append(obj.Apple(self.snake, self.walls))

    def update_state(self) -> None:
        if self.is_game_over:
            return
        self.tick_counter += 1
        if not self.tick_counter % self.snake_speed_delay:
            head = self.snake.get_new_head()
            # если игрок не столкнулся сам с собой, границей и стеной
            # или столкнулся на прошлом кадре (чтобы пройти сквозь препятствие)
            if pl.is_good_head(head, self.snake) and all(
                    head != wall.obj for wall in self.walls) or self.hit:

                #  увеличивает длину хмейки в направлении движения
                self.snake.enqueue(head)

                ate = False  # показывает, съели фрукт или нет

                # проверка, съела ли змейка один из фруктов
                for object in self.fruits:
                    if head == object.obj:  # проверка, съела ли змейка фрукт

                        # генерация нового фрукта и изменение очков
                        self.score = object.eaten(
                            self.score, self.snake, self.walls)

                        ate = True  # флаг, что фрукт съеден
                        self.newlevel()  # работа с новым уровнем
                # если змейка ничего не ела - не увеличивает длину
                if ate is False:
                    self.snake.dequeue()

                # движение пресиков
                for i in range(0, len(self.fruits)):
                    if type(self.fruits[i]) is obj.Pear:
                        self.fruits[i].move()

                # флаг, что змейка не ударилась
                self.hit = False
            # если змейка ударилась в объект, снимает здоровье
            # и запоминает, что на этом кадре змейка ударилась
            else:
                self.health += -1
                self.hit = True

            # игра кончается, если здоровье на нуле
            if self.health == 0:
                self.is_game_over = True

    def render(self) -> None:
        self.infrastructure.fill_screen()

        # отрисовка змеи
        for e in self.snake.snake:
            self.infrastructure.draw_element(e.x, e.y, SNAKE_COLOR)

        # отрисовка фруктов
        for object in self.fruits:
            self.infrastructure.draw_element(
                object.obj.x, object.obj.y, object.color)

        # отрисовка стен
        for wall in self.walls:
            self.infrastructure.draw_element(
                wall.obj.x, wall.obj.y, wall.color)

        # отрисовка очков
        self.infrastructure.draw_score(self.score)

        # отрисовка уровня
        self.infrastructure.draw_level(self.lvl)

        # отрисовка здоровья
        self.infrastructure.draw_health(self.health)

        # отрисовка окончания игры
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
    game = Game(infr.Infrastructure())
    game.loop()
