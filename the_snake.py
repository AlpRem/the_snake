from random import randint

import pygame

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

SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()

traffic_manager = {
    (pygame.K_UP, RIGHT): UP,
    (pygame.K_UP, LEFT): UP,
    (pygame.K_DOWN, RIGHT): DOWN,
    (pygame.K_DOWN, LEFT): DOWN,
    (pygame.K_LEFT, UP): LEFT,
    (pygame.K_LEFT, DOWN): LEFT,
    (pygame.K_RIGHT, UP): RIGHT,
    (pygame.K_RIGHT, DOWN): RIGHT,
}

def handle_keys(game_object):
    """Обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            key = event.key
            new_direction = traffic_manager.get((key, game_object.direction))
            if new_direction:
                game_object.next_direction = new_direction


class GameObject:
    """Родитель игровых элементов."""

    def __init__(self):
        self.surface = screen
        self.body_color = BOARD_BACKGROUND_COLOR
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def draw(self):
        """Отображение игрового элемента на поле."""

    def draw_point(self, body_color, position):
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.surface, body_color, rect)
        pygame.draw.rect(self.surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Игровой элемент - Яблоко."""

    def __init__(self, body_color=APPLE_COLOR, occupied_points=None):
        super().__init__()
        self.body_color = body_color
        self.randomize_position(occupied_points)

    def randomize_position(self, occupied_points=None):
        """Получения случайного значения координат на игровом поле."""
        if occupied_points is None:
            occupied_points = {(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)}

        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            position = (x, y)

            if position not in occupied_points:
                self.position = position
                return

    def draw(self):
        """Отображение яблока на игровом поле."""
        self.draw_point(self.body_color, self.position)


class Snake(GameObject):
    """Игровой элемент - Змейка."""

    def __init__(self):
        super().__init__()
        self.last = None
        self.body_color = SNAKE_COLOR
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1

    # Метод draw класса Snake
    def draw(self):
        """Отображение змейки на игровом поле."""
        for position in self.positions[:-1]:
            self.draw_point(self.body_color, position)
        self.draw_point(self.body_color, self.positions[0])
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сброс всех атрибутов змейки и задание их по-умолчанию."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.length = 1

    def get_head_position(self):
        """Возвращение позиции головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещение змейки."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        new_head = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def check_position_head(self):
        """Проверка на пересечения головы змейки с ее туловищем."""
        head = self.get_head_position()
        return head in self.positions[1:]


def main():
    """Главная точка входа в программу."""
    pygame.init()
    snake = Snake()
    apple = Apple(occupied_points=snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.check_position_head():
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
