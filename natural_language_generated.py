import random
import time

class SnakeGame:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.score = 0
        self.board = [[None for _ in range(width)] for _ in range(height)]
        self.snake = Snake(5, 5)
        self.apple = Apple(width, height, self.snake.body)
        self.running = True

    def handle_input(self, direction: str) -> None:
        if direction in ['w', 'a', 's', 'd']:
            self.snake.change_direction(direction)
        else:
            print("Invalid input. Use 'w', 'a', 's', 'd' for movement.")

    def game_loop(self) -> None:
        while self.running:
            self.snake.update_position()
            if self.snake.check_self_collision():
                self.running = False
            if self.snake.head_position() == (self.apple.x, self.apple.y):
                self.score += self.apple.score
                self.snake.grow()
                self.apple = Apple(self.width, self.height, self.snake.body)
            if self.snake.head_x < 0 or self.snake.head_x >= self.width or self.snake.head_y < 0 or self.snake.head_y >= self.height:
                self.running = False
            time.sleep(0.2)  # Control the game speed
        self.end_game()

    def end_game(self) -> None:
        print(f"Game Over. Your score: {self.score}")


class Snake:
    def __init__(self, x: int, y: int):
        self.head_x = x
        self.head_y = y
        self.length = 1
        self.body = [(x, y)]
        self.direction = 'RIGHT'

    def change_direction(self, direction: str) -> None:
        opposite_directions = {'w': 'DOWN', 's': 'UP', 'a': 'RIGHT', 'd': 'LEFT'}
        if opposite_directions[direction] != self.direction:
            self.direction = {'w': 'UP', 's': 'DOWN', 'a': 'LEFT', 'd': 'RIGHT'}[direction]

    def update_position(self) -> None:
        direction_moves = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}
        move_x, move_y = direction_moves[self.direction]
        new_head_x, new_head_y = self.head_x + move_x, self.head_y + move_y

        if len(self.body) == self.length:
            self.body.pop(0)  # Remove tail if not growing

        self.body.append((new_head_x, new_head_y))
        self.head_x, self.head_y = new_head_x, new_head_y

    def check_self_collision(self) -> bool:
        # Returns True if the snake collides with itself
        return (self.head_x, self.head_y) in self.body[:-1]

    def head_position(self) -> tuple:
        return self.head_x, self.head_y

    def grow(self) -> None:
        self.length += 1


class Apple:
    def __init__(self, board_width: int, board_height: int, snake_body: list):
        self.x, self.y = self.place_apple(board_width, board_height, snake_body)
        self.score = self.generate_score()

    def place_apple(self, board_width: int, board_height: int, snake_body: list) -> tuple:
        while True:
            x = random.randint(0, board_width - 1)
            y = random.randint(0, board_height - 1)
            if (x, y) not in snake_body:
                return x, y

    def generate_score(self) -> int:
        return random.randint(1, 10)


if __name__ == "__main__":
    # Initialize game
    game = SnakeGame(width=20, height=20)
    
    # Main game loop
    while True:
        # Handle input and update game state
        game.handle_input()
        game.game_loop()
        
        # Check if game is over
        if game.is_game_over():
            game.end_game()
            break
        
        # Add a small delay between frames
        time.sleep(0.1)
