import pygame
import random

from pygame.math import Vector2

class Game:
    def __init__(self, snake, food):
        self.running = False

        self.snake = snake
        self.food = food
        
    def update(self):
        self.snake.move()
        self.collision_checker()
    
    def display_elements(self):
        self.food.display()
        self.snake.display()
       
    def start(self):
        return            
    
    def over(self):
        self.running = False
        
    def collision_checker(self):
        if self.food.position == self.snake.body[-1]:
            self.food.new_position()
            self.snake.ate = True 
        
        if (not 0 <= self.snake.body[-1].x <= row_count or 
            not 0 <= self.snake.body[-1].y <= row_count): 
            self.over()
        
        for segment in self.snake.body[:-1]:
            if segment == self.snake.body[-1]:
                self.over()


class Food:
    def __init__(self, snake):
        self.snake = snake

        self.new_position()
        
# Appends all pairs of values up to row_count to self.position 
# if they aren't inside the snake        
    
    def new_position(self):
        self.positions = []
        
        for x in range(row_count):
            for y in range(row_count):
                position = Vector2(x, y)
                
                if position not in self.snake.body:
                    self.positions.append(position)        

        self.position = random.choice(self.positions)
    
    def display(self):
        self.food = pygame.Rect(self.position.x * cell_size, 
                                self.position.y * cell_size, 
                                cell_size, cell_size)
         
        pygame.draw.rect(screen, (255, 63, 31), self.food)


class Snake:
    def __init__(self):
        self.body = [Vector2(i, 15) for i in range(15, 19)]
        self.direction = Vector2(1, 0)        
        self.ate = False
         
    def display(self):
        for segment_position in self.body:
            segment = pygame.Rect(int(segment_position.x * cell_size), 
                                  int(segment_position.y * cell_size), 
                                  cell_size, cell_size)
            
            if segment_position == self.body[-1]:
                screen.blit(self.head_image(), segment)
            elif segment_position == self.body[0]:
                screen.blit(self.tail_image(), segment)
            else:
                screen.blit(self.body_image(segment_position), segment)
                
        
    def move(self):
        if self.ate == False:
            self.body.remove(self.body[0])
        
        self.body.append(self.body[-1]+self.direction)        
        
        self.ate = False


    def head_image(self):
        head_facing = self.body[-2] - self.body[-1]
        
        if head_facing == Vector2(0, -1):
            return pygame.image.load("snake_head.png").convert_alpha()
        
        elif head_facing == Vector2(0, 1):
            return pygame.transform.rotate(pygame.image.load("snake_head.png").convert_alpha(), 180)
        
        elif head_facing == Vector2(1, 0):
            return pygame.transform.rotate(pygame.image.load("snake_head.png").convert_alpha(), -90)
        
        elif head_facing == Vector2(-1, 0):
            return pygame.transform.rotate(pygame.image.load("snake_head.png").convert_alpha(), 90)
    
    def tail_image(self):
        tail_facing = self.body[1] - self.body[0]

        if tail_facing == Vector2(0, -1):
            return pygame.transform.rotate(pygame.image.load("snake_tail.png").convert_alpha(), -90)
        
        elif tail_facing == Vector2(0, 1):
            return pygame.transform.rotate(pygame.image.load("snake_tail.png").convert_alpha(), 90)
        
        elif tail_facing == Vector2(1, 0):
            return pygame.transform.rotate(pygame.image.load("snake_tail.png").convert_alpha(), 180)
        
        elif tail_facing == Vector2(-1, 0):
            return pygame.image.load("snake_tail.png").convert_alpha()
    
    def body_image(self, segment):
        index = self.body.index(segment)
        
        # Above, Below
        if self.body[index-1] - segment == Vector2(0, -1) == segment - self.body[index+1]:
            return pygame.transform.rotate(pygame.image.load("snake_straight.png").convert_alpha(), 90)
        # Below, Above        
        elif self.body[index-1] - segment == Vector2(0, 1) == segment - self.body[index+1]:
            return pygame.transform.rotate(pygame.image.load("snake_straight.png").convert_alpha(), 90)
        
        elif self.body[index-1] - segment == Vector2(-1, 0) == segment - self.body[index+1]:
            return pygame.image.load("snake_straight.png").convert_alpha()
        
        elif self.body[index-1] - segment == Vector2(1, 0) == segment - self.body[index+1]:
            return pygame.image.load("snake_straight.png").convert_alpha()
        
        elif (self.body[index-1] - segment == Vector2(-1, 0) and self.body[index+1] - segment == Vector2(0, -1) or 
              self.body[index-1] - segment == Vector2(0, -1) and self.body[index+1] - segment == Vector2(-1, 0)):
            return pygame.transform.rotate(pygame.image.load("snake_turn.png").convert_alpha(), -90)
        elif (self.body[index-1] - segment == Vector2(1, 0) and self.body[index+1] - segment == Vector2(0, 1) or
              self.body[index-1] - segment == Vector2(0, 1) and self.body[index+1] - segment == Vector2(1, 0)):
            return pygame.transform.rotate(pygame.image.load("snake_turn.png").convert_alpha(), 90)
        
        elif (self.body[index-1] - segment == Vector2(0, -1) and self.body[index+1] - segment == Vector2(-1, 0) or
              self.body[index-1] - segment == Vector2(-1, 0) and self.body[index+1] - segment == Vector2(0, -1)):
            return pygame.transform.rotate(pygame.image.load("snake_turn.png").convert_alpha(), 90)
        
        elif (self.body[index-1] - segment == Vector2(0, 1) and self.body[index+1] - segment == Vector2(1, 0) or
              self.body[index-1] - segment == Vector2(1, 0) and self.body[index+1] - segment == Vector2(0, 1)):
            return pygame.transform.rotate(pygame.image.load("snake_turn.png").convert_alpha(), 90)
        else:
            return pygame.image.load("snake_straight.png").convert_alpha()

        
pygame.init()

cell_size = 32
row_count = 29

screen = pygame.display.set_mode((row_count*cell_size, row_count*cell_size))

snake = Snake()
food = Food(snake) 
game = Game(snake, food)

screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update, 200)

game.running = True

while game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == screen_update:
            game.update()

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w and 
                snake.direction.y != 1):
                snake.direction = Vector2(0, -1)
            
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s and
                snake.direction.y != -1):
                snake.direction = Vector2(0, 1)
            
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d and
                snake.direction.x != -1):
                snake.direction = Vector2(1, 0)
                 
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a and 
                snake.direction.x != 1):
                snake.direction = Vector2(-1, 0)
    
    screen.fill((31, 31, 31))
   
    game.display_elements() 

    pygame.display.update()
