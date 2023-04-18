import tkinter
import random

class SnakeGame:
    def __init__(self):
        self.width = 512
        self.height = 512
        
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width = self.width, 
                                     height = self.height, bg="black")
        self.canvas.pack()
        
        self.snake_size = 16 
        self.snake_direction = "Right"

        self.x_center = self.width // 2
        self.y_center = self.height // 2
        
        self.food_x = 0
        self.food_y = 0
        
        self.snake = [self.canvas.create_rectangle(
            self.x_center - self.snake_size//2 + i*self.snake_size, self.y_center - self.snake_size//2, 
            self.x_center + self.snake_size//2 + i*self.snake_size, self.y_center + self.snake_size//2, fill="green") for i in range(4)]
        
        self.spawn_food()
        self.move_snake()
        
        self.window.bind("<Key>", self.on_key_press)
        self.window.mainloop()
    
    def on_key_press(self, event):
        if event.keysym == "w" and self.snake_direction != "Down":
            self.snake_direction = "Up"
        elif event.keysym == "a" and self.snake_direction != "Right":
            self.snake_direction = "Left"
        elif event.keysym == "s" and self.snake_direction != "Up":
            self.snake_direction = "Down"
        elif event.keysym == "d" and self.snake_direction != "Left":
            self.snake_direction = "Right"
    
    def spawn_food(self):
        self.food_x = random.randint(0, (self.width/self.snake_size)-1 * self.snake_size)
        self.food_y = random.randint(0, (self.height/self.snake_size)-1 * self.snake_size)

        food = self.canvas.create_rectangle(
            self.food_x - self.snake_size//2, self.food_y - self.snake_size//2, 
            self.food_x + self.snake_size//2, self.food_y + self.snake_size//2, fill="red")
            
    def move_snake(self):
        x = 0
        y = 0

        if self.snake_direction == "Right":
            x += self.snake_size
        elif self.snake_direction == "Left":
            x -= self.snake_size
        elif self.snake_direction == "Up":
            y -= self.snake_size
        elif self.snake_direction == "Down":
            y += self.snake_size
        
        for value in self.canvas.coords(self.snake[-1]):
            if value+x < 0 or value +y < 0:
                self.snake_direction = None
        
        if (self.canvas.coords(self.snake[-1])[0] == self.food_x or
            self.canvas.coords(self.snake[-1])[1] == self.food_y or
            self.canvas.coords(self.snake[-1])[2] == self.food_x or
            self.canvas.coords(self.snake[-1])[3] == self.food_y):
            self.canvas.delete(food)
            self.spawn_food()          

        if (self.canvas.coords(self.snake[-1])[0]+x > self.width or
            self.canvas.coords(self.snake[-1])[1]+y > self.height or
            self.canvas.coords(self.snake[-1])[2]+x > self.width or
            self.canvas.coords(self.snake[-1])[3]+y > self.height):
            self.snake_direction = None
        
        else:
            self.canvas.move(self.snake[-1], x, y)
        
            for i in range(len(self.snake)-1):
                self.canvas.coords(self.snake[i], self.canvas.coords(self.snake[i+1]))
        

                
            self.window.after(200, self.move_snake)        
    

SnakeGame()
