from random import randint

import pygame


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

# Скорость движения змейки:
SPEED = 12

INITIAL_POSITION = ((GRID_WIDTH // 2), (GRID_HEIGHT // 2))

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.

class GameObject():
    """Родительский класс."""

    def __init__(self, body_color=None):
        """Инициализирует объект.

        Args:
            body_color (optional): Цвет объекта. Defaults to None.
        """
        self.position = INITIAL_POSITION
        self.body_color = body_color

    def draw(self):
        """Метод для переопределения в подклассах."""
        pass


class Apple(GameObject):
    """Класс яблока, определяет цвет, позицию и отрисовку объекта."""

    def __init__(self):
        """Инициализирует объект."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Генерирует рандомную позицию яблока."""
        self.position = (randint(0, GRID_WIDTH - 1),
                         randint(0, GRID_HEIGHT - 1))

    def draw(self):
        """Отрисовывает яблоко на экроане."""
        pixel_position = (self.position[0] * GRID_SIZE,
                          self.position[1] * GRID_SIZE)
        rect = pygame.Rect(pixel_position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс объекта змейка, отвечает за обработку все характеристик змейки."""

    def __init__(self):
        """Инициализирует объект.

        Параметры цвета тела, длины, списка позиций, направления
        движения, next_direction и last для дальнейшего использования,
        флаг grow для определения увеличения длины змейки.
        """
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.grow = False

    def update_direction(self):
        """Обновняет направвление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def change_direction(self, direction):
        """Изменяет направление движенеия змейки."""
        self.next_direction = direction

    def move(self, apple):
        """Обрабатыввает движение змейки и столкновения.

        Args:
            apple (Apple()): принимает экземпляр класса Apple()

        Returns:
            bool: True - при продожении движения, False - при прекращении.
        """
        self.update_direction()
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_x = (head_x + dx) % GRID_WIDTH
        new_y = (head_y + dy) % GRID_HEIGHT
        new_head = (new_x, new_y)

        if new_head in self.positions[1:]:
            return False

        self.last = self.positions[-1] if self.positions else None

        self.positions.insert(0, new_head)

        if new_head == apple.position:
            self.grow = True
            apple.randomize_position()
            while apple.position in self.positions:
                apple.randomize_position()

        if self.grow:
            self.grow = False
            self.length += 1
        else:
            if self.positions:
                self.positions.pop()

        return True

    def draw(self):
        """Отрисовывает тело змейки и затирает последний сегмент."""
        for position in self.positions:
            pixel_position = (position[0] * GRID_SIZE,
                              position[1] * GRID_SIZE)
            rect = pygame.Rect(pixel_position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            last_pixel = (self.last[0] * GRID_SIZE,
                          self.last[1] * GRID_SIZE)
            last_rect = pygame.Rect(last_pixel, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def apple_collision(self, apple):
        """Проверяет столкновение змейки я яблоком."""
        return self.get_head_position() == apple.position

    def self_collision(self):
        """Проверяет столкновение змейки с самой собой."""
        return self.get_head_position() in self.positions[1:]

    def reset(self):
        """Сброс змейки в начальное стостояние."""
        self.length = 1
        self.positions = [INITIAL_POSITION]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обрабатывает пользовательский ввод."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Инициализирует pygame, создает экземпляры классов Apple() и Snake().

    Запускает основной игровой цикл.
    """
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move(apple)

        if not snake.move(apple):
            pygame.display.flip()
            pygame.time.wait(1600)

            snake.reset()
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

    # Тут опишите основную логику игры.
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
