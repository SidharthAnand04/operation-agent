import pygame
import random
from config import WIDTH, HEIGHT, WHITE, RED, GREEN, BLOCK_SIZE

# Initialize Pygame
pygame.init()

# Snake class
class Snake:
    def __init__(self):
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.length = 1
        self.body = [(self.x, self.y)]
        self.direction = (0, 0)

    def update_pos(self):
        new_pos = (self.x + self.direction[0] * BLOCK_SIZE,
                   self.y + self.direction[1] * BLOCK_SIZE)
        self.body.append(new_pos)
        if len(self.body) > self.length:
            self.body.pop(0)
        self.x, self.y = new_pos
        return self.body.count(new_pos) > 1

# Apple class
class Apple:
    def __init__(self):
        self.x, self.y = self.generate_new_position()
        self.score = random.randint(1, 3)

    def generate_new_position(self):
        return (
            random.randint(0, WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE,
            random.randint(0, HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE
        )

# SnakeGame class
class SnakeGame:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.score = 0
        self.snake = Snake()
        self.apple = Apple()
        self.display = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.paused = False
        pygame.display.set_caption('Snake Game')
        self.show_start_screen()

    def show_start_screen(self):
        self.display.fill(WHITE)
        font = pygame.font.Font(None, 48)
        text = font.render('Press any key to start', True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.width/2, self.height/2))
        self.display.blit(text, text_rect)
        pygame.display.update()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting = False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.toggle_pause()
                elif event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                    self.update_direction(event.key)

    def update_direction(self, key):
        dir_map = {
            pygame.K_w: (0, -1),
            pygame.K_s: (0, 1),
            pygame.K_a: (-1, 0),
            pygame.K_d: (1, 0),
        }
        if key in dir_map:
            new_direction = dir_map[key]
            # Prevent reversing direction
            if (self.snake.direction[0] + new_direction[0] != 0 or 
                self.snake.direction[1] + new_direction[1] != 0):
                self.snake.direction = new_direction

    def toggle_pause(self):
        self.paused = not self.paused

    def game_loop(self):
        running = True
        while running:
            self.handle_input()
            if not self.paused:
                # Update and check snake position
                if self.snake.update_pos():
                    running = False
                if (self.snake.x, self.snake.y) == (self.apple.x, self.apple.y):
                    self.score += self.apple.score
                    self.snake.length += 1
                    self.apple = Apple()

                # Check wall collision
                if not (0 <= self.snake.x < self.width and 0 <= self.snake.y < self.height):
                    running = False

                self.display_screen()
                self.clock.tick(15)

        self.end_game()

    def end_game(self):
        self.display.fill(WHITE)
        font = pygame.font.Font(None, 36)
        text = font.render(f'Game Over! Score: {self.score}', True, RED)
        text_rect = text.get_rect(center=(self.width/2, self.height/2))
        self.display.blit(text, text_rect)
        pygame.display.update()
        pygame.time.wait(3000)
        self.__init__()
        self.game_loop()

    def display_screen(self):
        self.display.fill(WHITE)
        for segment in self.snake.body:
            pygame.draw.rect(self.display, GREEN, (*segment, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.circle(self.display, RED, (self.apple.x + BLOCK_SIZE // 2, self.apple.y + BLOCK_SIZE // 2), BLOCK_SIZE // 2)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.display.blit(score_text, (10, 10))
        pygame.display.update()

# Run game
if __name__ == "__main__":
    game = SnakeGame()
    game.game_loop()
