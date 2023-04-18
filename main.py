import tkinter
import random

class SnakeGame:
    def __init__(self):
        self.width = 608
        self.height = 608
        
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width = self.width, 
                                     height = self.height, bg="black")
        self.canvas.pack()
        
        self.snake_size = 32
        self.snake_direction = "Right"
        
        self.score_label = tkinter.Label(self.window, text=f"Score: {self.score}")
        self.score_label.pack(pady = 8)

        self.x_center = self.width // 2
        self.y_center = self.height // 2
        
        self.window.bind("<Key>", self.on_key_press)
        self.window.mainloop()
    
    def start_game(self):
        self.score = 0
        
        self.snake = [
            self.canvas.create_rectangle(self.x_center - self.snake_size//2 + self.snake_size*i, self.y_center - self.snake_size//2, 
            self.x_center + self.snake_size//2 + self.snake_size*i, self.y_center + self.snake_size//2, fill="green", outline="") for i in range(1, 5)]
        
        self.spawn_food()
        self.move_snake()

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
        valid_food_x_coordinates = [self.snake_size*i for i in range(self.width//self.snake_size)]
        valid_food_y_coordinates = [self.snake_size*i for i in range(self.height//self.snake_size)]
        self.food_x = random.choice(valid_food_x_coordinates)
        self.food_y = random.choice(valid_food_y_coordinates)

        self.food = self.canvas.create_rectangle(
            self.food_x, self.food_y, 
            self.food_x + self.snake_size, self.food_y + self.snake_size, fill="red", outline="")
            
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
        
        if self.canvas.coords(self.snake[-1]) == self.canvas.coords(self.food):
            self.canvas.delete(self.food)
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.spawn_food()          
            
            self.snake.insert(0, self.canvas.create_rectangle(
                self.canvas.coords(self.snake[0])[0], self.canvas.coords(self.snake[0])[1], 
                self.canvas.coords(self.snake[0])[2], self.canvas.coords(self.snake[0])[3], fill="green", outline=""))
        
        head_x_1 = self.canvas.coords(self.snake[-1])[0]
        head_y_1 = self.canvas.coords(self.snake[-1])[1]
        head_x_2 = self.canvas.coords(self.snake[-1])[2]
        head_y_2 = self.canvas.coords(self.snake[-1])[3]
        
        if (head_x_1 + x > self.width or head_x_1 + x < 0 or
            head_y_1 + y > self.width or head_y_1 + y < 0 or
            head_x_2 + x > self.width or head_x_2 + x < 0 or
            head_y_2 + y > self.width or head_y_2 + x < 0):
            self.game_over()

        else:
            self.canvas.move(self.snake[-1], x, y)
        
            for i in range(len(self.snake)-1):
                self.canvas.coords(self.snake[i], self.canvas.coords(self.snake[i+1]))
        
            for segment in self.snake[:-2]:
                if self.canvas.coords(segment) == self.canvas.coords(self.snake[-1]):
                    self.snake_direction = None
        
            if self.snake_direction != None:
                self.window.after(100, self.move_snake)        
        
            else:
                self.game_over()

    def game_over(self):
        self.snake_direction = None
        text = self.canvas.create_text(self.width//2, self.height//2, anchor="center")
        self.canvas.insert(text, 12, "Game Over")

SnakeGame()
