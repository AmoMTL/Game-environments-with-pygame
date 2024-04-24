import pygame
import sys
import random

pygame.init()

height = 800 # set height of the screen
width = 800 # set width of the screen
grid_size = 50 # set the size of the grid in the game

font = pygame.font.SysFont("calibri", grid_size*2)
score_font = pygame.font.SysFont("calibri", 40)

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Snake")
time = pygame.time.Clock()

# Function to display text
def draw_text(text, size, color, surface, x, y, max_width=None):
    font = pygame.font.Font(None, size)
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    # Adjust font size to fit within max_width if specified
    while max_width and textrect.width > max_width:
        size -= 1
        font = pygame.font.Font(None, size)
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def restart_game():
    snake = Snake()
    apple = Apple()
    return snake, apple

def display_score():
    score_text = f"Score: {snake.score}"
    text_surf = score_font.render(score_text, True, "white")
    text_rect = text_surf.get_rect()
    text_rect.centerx = width // 2  # Center text horizontally
    text_rect.top = 10  # Set top margin of 10 pixels
    screen.blit(text_surf, text_rect)

class Snake:
    def __init__(self):
        # starting position of the snake is random on the grid
        self.x = random.choice([x for x in range(grid_size, width+1-grid_size, grid_size)])
        self.y = random.choice([x for x in range(grid_size, height+1-grid_size, grid_size)])
        # intialize the movement direction of the snake randomly
        self.x_dir = random.choice([-1, 1]) # 1 is right and -1 is left
        self.y_dir = 0 # 1 is down and -1 is up
        # the size of the snake in the start is one grid_size
        self.head = pygame.Rect(self.x, self.y, grid_size, grid_size)
        self.body = [] # snake starts with size one
        # track if collision with self
        self.collision = False
        self.score = 0
    
    def update_position(self):
        self.body.append(self.head)
        if len(self.body) > 1:
            for i in range(len(self.body)-1):
                self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y
        self.head.x += self.x_dir * grid_size
        self.head.y += self.y_dir * grid_size
        # allow continuity off the grid
        if self.head.x >= width-1:
            self.head.x = 0
        if self.head.x < 0:
            self.head.x = width
        if self.head.y >= height-1:
            self.head.y = 0
        if self.head.y < 0:
            self.head.y = height
        self.body.remove(self.head)
        if len(self.body) >= 1:
            for square in self.body:
                if self.head.x == square.x and self.head.y == square.y:
                    self.collision = True

class Apple:
    def __init__(self):
        self.x = random.choice([x for x in range(0, width+1-grid_size, grid_size)])
        self.y = random.choice([x for x in range(0, height+1-grid_size, grid_size)])
        self.rect = pygame.Rect(self.x, self.y, grid_size, grid_size)

    def update_position(self):
        pygame.draw.rect(screen, "red", self.rect)

def Grid():
    for x in range(0, width, grid_size):
        for y in range(0, height, grid_size):
            rect = pygame.Rect(x, y, grid_size, grid_size)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)



Grid()
snake = Snake()
apple = Apple()

game_failed = False


while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                snake.y_dir = 1
                snake.x_dir = 0
            elif event.key == pygame.K_UP:
                snake.y_dir = -1
                snake.x_dir = 0
            elif event.key == pygame.K_LEFT:
                snake.y_dir = 0
                snake.x_dir = -1
            elif event.key == pygame.K_RIGHT:
                snake.y_dir = 0
                snake.x_dir = 1
        if snake.collision:
            game_failed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the restart button is clicked
                mouse_x, mouse_y = event.pos
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    snake, apple = restart_game()
                    game_failed = False
                    

    snake.update_position()

    screen.fill("black")
    Grid()

    apple.update_position()

    pygame.draw.rect(screen, "green", snake.head)
    if len(snake.body) > 0:
        for body in snake.body:
            pygame.draw.rect(screen, "green", body)

    if snake.head.x == apple.x and snake.head.y == apple.y:
        # increase the body size by one block
        snake.score += 1
        snake.body.append(pygame.Rect(snake.head.x, snake.head.y, grid_size, grid_size))
        apple = Apple()

    if snake.collision:
        box_width = width * 0.5
        box_height = height * 0.375
        box_x = (width - box_width) / 2
        box_y = (height - box_height) / 2
        button_width = box_width * 0.5
        button_height = 50
        button_x = box_x + (box_width - button_width) / 2
        button_y = box_y + box_height * 0.67
        
        pygame.draw.rect(screen, "gray", [box_x, box_y, box_width, box_height], 0, 5)
        draw_text('Failed!', 48, "red", screen, width / 2, box_y + box_height * 0.33)
        # Draw a restart button
        pygame.draw.rect(screen, "white", [button_x, button_y, button_width, button_height], 0, 5)
        draw_text('Restart', 36, "black", screen, button_x + button_width / 2, button_y + button_height / 2, max_width=button_width - 10)


    

    if not game_failed:
        display_score()
        pygame.display.update()

    time.tick(10)