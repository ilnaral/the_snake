"""Классическая игра змейка суть которой заключается в том, что при
поедании яблока змейка растет, а при столкновении с самой собой или камнем
игра заканчивается.
"""

from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет камушка
STONE_COLOR = (128, 128, 128)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

# Настройка отображения счета и подбор шрифта:
pg.font.init()
font = pg.font.Font(None, 30)


# Тут опишем все классы игры
class GameObject:
    """Описание родительского класса."""

    def __init__(self) -> None:
        self.position = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.body_color = BOARD_BACKGROUND_COLOR

    def draw(self) -> None:
        """Метод отрисовки, который будет определен в дочерних классах."""
        pass


class Apple(GameObject):
    """Описание дочернего класса яблока."""
       
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Метод, при котором яблоко спавнится в рандомном месте."""

        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Метод отрисовки яблока."""        
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stone(GameObject):
    """Описание дочернего класса камушка."""

    def __init__(self):
        super().__init__()
        self.body_color = STONE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Метод рандомного появления камушка."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Метод отрисовки камушка."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)       


class Snake(GameObject):
    """Описание дочернего класса змейки."""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None       

    def update_direction(self):
        """Метод обновления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод движения змейки."""
        head_snake, head_snake_1 = self.get_head_position()
        if self.direction == UP:
            head_snake_1 -= GRID_SIZE
        elif self.direction == DOWN:
            head_snake_1 += GRID_SIZE
        elif self.direction == LEFT:
            head_snake -= GRID_SIZE
        elif self.direction == RIGHT:
            head_snake += GRID_SIZE

    # Движение/выход змейки за текстуры
        if head_snake < 0:
            head_snake = SCREEN_WIDTH - GRID_SIZE
        elif head_snake >= SCREEN_WIDTH:
            head_snake = 0
        if head_snake_1 < 0:
            head_snake_1 = SCREEN_HEIGHT - GRID_SIZE
        elif head_snake_1 >= SCREEN_HEIGHT:
            head_snake_1 = 0

        new_head = (head_snake, head_snake_1)

    # Добавление головы змейки в начало списка
        self.positions.insert(0, new_head)

    # Удаление последнего сегмента
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
    
    """Метод отрисовки змейки."""
    def draw(self):
        for position in self.positions[0:]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    """Метод возвращения текущей позиции головы змейки."""
    def get_head_position(self):
        return self.positions[0]

    """Метод сбрасывания игры при столкновении."""
    def reset(self) -> None:
        print('GAME OVER!')
        # Сбрасываем змейку при проигрыше
        self. length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None

def handle_keys(game_object):
    """Метод управления змейкой при помощи клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT

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
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            stone.randomize_position()
            score += 1
        if snake.get_head_position() in snake.positions[1:] or snake.get_head_position() == stone.position:
            snake.reset()
            score = 0           
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        stone.draw()
        score_text = font.render(f'SCORE: {score}', True, (180, 180, 180))
        screen.blit(score_text, (10, 10))
        pg.display.update()


if __name__ == "__main__":
    main()
