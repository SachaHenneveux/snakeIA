import random

GRID_SIZE = 10
GRID_WIDTH = 30
GRID_HEIGHT = 30
SCREEN_SIZE = (GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

ACTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
NUM_ACTIONS = 3

class SnakeGame:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction_index = random.randint(0, 3)
        self.direction = ACTIONS[self.direction_index]
        self.food = self.spawn_food()
        self.done = False
        self.score = 0
        return self.get_state()
    
    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food
    
    def check_collision(self, position):
        x, y = position
        if x < 0 or y < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
            return True
        if position in self.snake:
            return True
        return False

    def get_state(self):
        head = self.snake[0]
        next_straight = (head[0] + self.direction[0], head[1] + self.direction[1])
        danger_straight = 1 if self.check_collision(next_straight) else 0
        
        right_index = (self.direction_index + 1) % 4
        left_index = (self.direction_index - 1) % 4
        right_direction = ACTIONS[right_index]
        left_direction = ACTIONS[left_index]
        
        next_right = (head[0] + right_direction[0], head[1] + right_direction[1])
        next_left = (head[0] + left_direction[0], head[1] + left_direction[1])
        
        danger_right = 1 if self.check_collision(next_right) else 0
        danger_left = 1 if self.check_collision(next_left) else 0
        
        food_dx = self.food[0] - head[0]
        food_dy = self.food[1] - head[1]
        food_dx = -1 if food_dx < 0 else (1 if food_dx > 0 else 0)
        food_dy = -1 if food_dy < 0 else (1 if food_dy > 0 else 0)
        food_dx_idx = food_dx + 1
        food_dy_idx = food_dy + 1
        
        length = len(self.snake)
        if length < 3:
            snake_size = 0
        elif length < 7:
            snake_size = 1
        else:
            snake_size = 2
        
        return (danger_straight, danger_right, danger_left, self.direction_index, food_dx_idx, food_dy_idx, snake_size)
    
    def update_direction(self, action):
        if action == 0:
            new_direction_index = self.direction_index
        elif action == 1:
            new_direction_index = (self.direction_index + 1) % 4
        elif action == 2:
            new_direction_index = (self.direction_index - 1) % 4
        self.direction_index = new_direction_index
        self.direction = ACTIONS[self.direction_index]
    
    def step(self, action):
        if self.done:
            return self.get_state(), 0, True
        
        self.update_direction(action)
        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        
        if self.check_collision(new_head):
            self.done = True
            return self.get_state(), -20, True
        
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            reward = 15
            self.food = self.spawn_food()
        else:
            self.snake.pop()
            reward = -0.1
        
        return self.get_state(), reward, False
