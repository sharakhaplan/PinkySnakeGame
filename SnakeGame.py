import pygame
import sys
import random

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 30
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

PINK = (255, 192, 203)
DARK_PINK = (255, 105, 180)
FOOD_COLOR = (153, 255, 51)
SNAKE_COLOR = (0, 0, 0)


class Snake:
    def __init__(self):
        self.positions = [(WIDTH // 2, HEIGHT // 2)]
        self.length = 1
        self.direction = random.choice([(0, -1), (0, 1), (1, 0), (-1, 0)])
        self.color = SNAKE_COLOR
        self.score = 0

    def draw(self, surface):
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.color, rect)

    def move(self):
        current = self.positions[0]
        x, y = self.direction

        new = (
            (current[0] + x * GRID_SIZE) % WIDTH,
            (current[1] + y * GRID_SIZE) % HEIGHT
        )

        # self collision check
        if new in self.positions[1:]:
            return False

        self.positions.insert(0, new)

        if len(self.positions) > self.length:
            self.positions.pop()

        return True

    def turn(self, direction):
        # prevent reversing
        if (direction[0] * -1, direction[1] * -1) == self.direction:
            return
        self.direction = direction


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.color, rect)


def draw_grid(surface):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if (x + y) % 2 == 0:
                pygame.draw.rect(surface, PINK, rect)
            else:
                pygame.draw.rect(surface, DARK_PINK, rect)


def show_game_over(screen, score):
    font = pygame.font.SysFont("Arial", 60, bold=True)
    text = font.render("GAME OVER", True, (0, 0, 0))
    score_font = pygame.font.SysFont("Arial", 30, bold=True)
    score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))

    screen.blit(text, (WIDTH // 2 - 180, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - 70, HEIGHT // 2 + 10))

    pygame.display.update()
    pygame.time.delay(2000)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()

    while True:
        clock.tick(10)

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.turn((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.turn((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.turn((1, 0))

        # MOVE
        alive = snake.move()
        if not alive:
            show_game_over(screen, snake.score)
            pygame.quit()
            sys.exit()

        # FOOD CHECK
        if snake.positions[0] == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()

        # DRAW
        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)

        score_font = pygame.font.SysFont("Arial", 30, bold=True)
        score_text = score_font.render(f"Score: {snake.score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.update()


main()
