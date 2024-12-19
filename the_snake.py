"""Классическая игра змейка суть которой заключается в том, что при
поедании яблока змейка растет, а при столкновении с самой собой или камнем
игра заканчивается.
"""

from random import randint

import pygame as pg


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

STONE_COLOR = (128, 128, 128)

COLOR = (0, 0, 0)

SPEED = 10

some_dict = {
    (pg.K_UP, LEFT): UP,
    (pg.K_UP, RIGHT): UP,
    (pg.K_DOWN, LEFT): DOWN,
    (pg.K_DOWN, RIGHT): DOWN,
    (pg.K_LEFT, UP): LEFT,
    (pg.K_LEFT, DOWN): LEFT,
    (pg.K_RIGHT, UP): RIGHT,
    (pg.K_RIGHT, DOWN): RIGHT,
}

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

clock = pg.time.Clock()


class GameObject:
    """Описание родительского класса."""

    def __init__(self) -> None:
        """Метод инициализации."""
        self.position = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.body_color = BOARD_BACKGROUND_COLOR

    def draw(self):
        """Метод отрисовки, определим в дочерних классах."""
        pass

    def draw_cell(self, position: tuple[int], color: tuple[int]) -> None:
        """Метод отрисовки, особенности которых будут прописаны
        в дочерних классах.
        """
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def free_cell(self, position: tuple[int]) -> None:
        """Метод для затирания ячейки."""
        pg.draw.rect(
            screen, BOARD_BACKGROUND_COLOR,
            pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        )


class Apple(GameObject):
    """Описание дочернего класса яблока."""

    def __init__(self):
        """Метод инициализации."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        """Метод, при котором яблоко спавнится в рандомном месте.
        Но не змейке.
        """
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in snake_positions:
                break

    def draw(self):
        """Метод отрисовки яблока."""
        self.draw_cell(self.position, APPLE_COLOR)


class Stone(GameObject):
    """Описание дочернего класса камушка."""

    def __init__(self):
        """Метод инициализации."""
        super().__init__()
        self.body_color = STONE_COLOR
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        """Метод рандомного появления камушка, но не змейке."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in snake_positions:
                break

    def draw(self):
        """Метод отрисовки камушка."""
        self.draw_cell(self.position, STONE_COLOR)


class Snake(GameObject):
    """Описание дочернего класса змейки."""

    def __init__(self):
        """Метод инициализации."""
        super().__init__()
        self.reset()

    def update_direction(self, new_direction):
        """Метод обновления движения змейки."""
        self.direction = new_direction

    def move(self):
        """Метод движения змейки."""
        head_x, head_y = self.get_head_position()
        value_x, value_y = self.direction
        head_x += value_x * GRID_SIZE
        head_y += value_y * GRID_SIZE

        # Движение/выход змейки за текстуры
        head_x %= SCREEN_WIDTH
        head_y %= SCREEN_HEIGHT

        new_head = (head_x, head_y)

        # Добавление головы змейки в начало списка
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

        return True

    def draw(self):
        """Метод отрисовки змейки."""
        self.draw_cell(self.positions[0], SNAKE_COLOR)
        # Затирание последнего сегмента
        if self.last:
            self.free_cell(self.last)

    def get_head_position(self):
        """Метод возвращения текущей позиции головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Метод сбрасывания игры при столкновении."""
        print("GAME OVER!")

        # Сбрасываем змейку при проигрыше
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2 // GRID_SIZE * GRID_SIZE,
                           SCREEN_HEIGHT // 2 // GRID_SIZE * GRID_SIZE)]

        # Инициализация направления и следующего направления
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(snake):
    """Метод управления змейкой при помощи клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit("GAME OVER!")
        if event.type == pg.KEYDOWN:
            new_direction = some_dict.get(
                (event.key, snake.direction), snake.direction)
            snake.update_direction(new_direction)


def main():
    """Метод инициализации pg."""
    pg.init()
    # Создание экземпляров класса
    apple = Apple()
    snake = Snake()
    stone = Stone()
    score = 0
    # Описание основного игрового цикла
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            stone.free_cell(stone.position)
            screen.fill(BOARD_BACKGROUND_COLOR)
            score = 0
        elif snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
            stone.free_cell(stone.position)
            stone.randomize_position(snake.positions)
            score += 1
        elif snake.get_head_position() == stone.position:
            stone.free_cell(stone.position)
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            score = 0
        apple.draw()
        snake.draw()
        stone.draw()
        score = snake.length
        pg.display.set_caption(
            "Змейка. "
            f"Длина змейки: {score}"
        )
        pg.display.update()


if __name__ == "__main__":
    main()
