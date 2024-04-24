import pygame
import sys
import random

pygame.init()

height = 800 # set height of the screen
width = 800 # set width of the screen
grid_size = 50 # set the size of the grid in the game

font = pygame.font.SysFont("calibri", grid_size*2)

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Snake")
time = pygame.time.Clock()

class Snake:
    def __init__(self):
        # starting position of the snake is random on the grid
        self.x = random.choice([x for x in range(grid_size-1, width+1-grid_size, grid_size)])
        self.y = random.choice([x for x in range(grid_size-1, height+1-grid_size, grid_size)])
        # intialize the movement direction of the snake randomly
        self.x_dir = random.choice([-1, 1]) # 1 is right and -1 is left
        self.y_dir = 0 # 1 is down and -1 is up
        # the size of the snake in the start is one grid_size
        self.head = pygame.Rect(self.x, self.y, grid_size, grid_size)
        self.body = [] # snake starts with size one
        # track if collision with self
        self.collision = False
    
    def update_position(self):
        self.body.append(self.head)
        if len(self.body) > 1:
            for i in range(len(self.body)):
                self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y
        self.head.x += self.x_dir * grid_size
        self.head.y += self.y_dir * grid_size
        if self.head.x >= width-1:
            self.head.x = 0
        if self.head.x < 0:
            self.head.x = width
        if self.head.y >= height-1:
            self.head.y = 0
        if self.head.y < 0:
            self.head.y = height
        self.body.remove(self.head)


def Grid():
    for x in range(0, width, grid_size):
        for y in range(0, height, grid_size):
            rect = pygame.Rect(x, y, grid_size, grid_size)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)



Grid()
snake = Snake()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                snake.y_dir = 1
                snake.x_dir = 0
            if event.key == pygame.K_UP:
                snake.y_dir = -1
                snake.x_dir = 0
            if event.key == pygame.K_LEFT:
                snake.y_dir = 0
                snake.x_dir = -1
            if event.key == pygame.K_RIGHT:
                snake.y_dir = 0
                snake.x_dir = 1
    
    snake.update_position()
    screen.fill("black")
    Grid()

    pygame.draw.rect(screen, "green", snake.head)
    if len(snake.body) > 0:
        for body in snake.body:
            pygame.draw.rect(screen, "green", body)


    pygame.display.update()
    time.tick(10)