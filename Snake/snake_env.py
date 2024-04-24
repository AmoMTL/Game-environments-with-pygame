import random
import pygame

class Snake:
    def __init__(self, height, width, grid_size):
        self.x = random.choice([x for x in range(grid_size, width+1-grid_size, grid_size)])
        self.y = random.choice([x for x in range(grid_size, height+1-grid_size, grid_size)])
        # intialize the movement direction of the snake randomly
        self.x_dir = random.choice([-1, 1]) # 1 is right and -1 is left
        self.y_dir = 0 # 1 is down and -1 is up
        # the size of the snake in the start is one grid_size
        self.head = pygame.Rect(self.x, self.y, grid_size, grid_size)
        self.body = [] # snake starts with size one


class Apple:
    def __init__(self, height, width, grid_size):
        self.x = random.choice([x for x in range(0, width+1-grid_size, grid_size)])
        self.y = random.choice([x for x in range(0, height+1-grid_size, grid_size)])
        


class SnakeEnv:
    # Initialize the environment
    def __init__(self, height=800, width=800, grid_size=50, max_steps=500):
        self.height = height
        self.width = width
        self.grid_size = grid_size
        self.max_steps = max_steps
        self.action_space = 4
        self.reward = 0
        self.done = False
        
    def step(self, action):
        self.steps += 1
        if action == 1:
            self.snake.y_dir = -1
            self.snake.x_dir = 0
        elif action == 2:
            self.snake.y_dir = 1
            self.snake.x_dir = 0
        elif action == 3:
            self.snake.y_dir = 0
            self.snake.x_dir = -1
        elif action == 4:
            self.snake.y_dir = 0
            self.snake.x_dir = 1
        #  update state of the game
        self.snake.body.append(self.snake.head)
        if len(self.snake.body) > 1:
            for i in range(len(self.snake.body)-1):
                self.snake.body[i].x, self.snake.body[i].y = self.snake.body[i+1].x, self.snake.body[i+1].y
        # new position of the snake
        self.snake.head.x += self.x_dir * self.grid_size
        self.snake.head.y += self.y_dir * self.grid_size
        # allow continuity
        if self.snake.head.x >= self.width-1:
            self.snake.head.x = 0
        if self.snake.head.x < 0:
            self.snake.head.x = self.width
        if self.snake.head.y >= self.height-1:
            self.snake.head.y = 0
        if self.snake.head.y < 0:
            self.snake.head.y = self.height
        self.snake.body.remove(self.snake.head)
        # check for collision with self
        if len(self.snake.body) >= 1:
            for square in self.snake.body:
                if self.snake.head.x == square.x and self.snake.head.y == square.y:
                    self.done = True
                    step_reward = -100
        # check if ate an apple, i.e. scored a point
        if self.snake.head.x == self.apple.x and self.snake.head.y == self.apple.y:
            # increase the body size by one block
            self.snake.score += 1
            self.snake.body.append(pygame.Rect(self.snake.head.x, self.snake.head.y, self.grid_size, self.grid_size))
            self.apple = Apple()
            step_reward = 1
        self.reward += step_reward
        new_state = (self.snake.head.x, self.snake.head.y, self.snake.x_dir, self.snake.y_dir, self.apple.x, self.apple.y)
        return new_state, step_reward, self.done

    def Grid(self, screen):
        for x in range(0, self.width, self.grid_size):
            for y in range(0, self.height, self.grid_size):
                rect = pygame.Rect(x, y, self.grid_size, self.grid_size)
                pygame.draw.rect(screen, "#3c3c3b", rect, 1)

    def render(self, model):
        render_flag = False
        state = self.reset()

        pygame.init()
        font = pygame.font.SysFont("calibri", self.grid_size*2)
        score_font = pygame.font.SysFont("calibri", 40)

        screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption("Snake")

        self.Grid(screen)

        ep_reward = 0
        for step in range(0, self.max_steps):
            action = model.predict(state)
            new_state, reward, render_flag = self.step(action)
            state = new_state
            ep_reward += reward
            if render_flag:
                pygame.quit()
                break
            screen.fill("black")
            self.Grid(screen)
            pygame.draw.rect(screen, "green", self.snake.head)
            if len(self.snake.body) > 0:
                for body in self.snake.body:
                    pygame.draw.rect(screen, "green", body)
        
        pygame.quit()

    # Resets the environment and returns the initial state
    def reset(self):
        self.steps = 0
        self.reward = 0
        self.done = False
        self.apple = Apple(self.height, self.width, self.grid_size)
        self.snake = Snake(self.height, self.width, self.grid_size)
        return (self.snake.head.x, self.snake.head.y, self.snake.x_dir, self.snake.y_dir, self.apple.x, self.apple.y)