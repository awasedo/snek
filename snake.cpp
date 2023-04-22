#include <iostream>
#include <vector>
#include <algorithm>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>
#include <cstdlib>
#include <ctime>

int width = 16;
int height = width/2;
int score = 0;

bool ate = false;
bool running = true;

std::vector<std::vector<int>> snake = {{8, 8}, {9, 8}, {10, 8}};
std::vector<int> snake_direction = {1, 0};

std::vector<int> food = {rand() % width-1, rand() % height-1};

void move() {
    std::vector<int> new_position = {snake[snake.size()-1][0]+snake_direction[0], snake[snake.size()-1][1]+snake_direction[1]};
	
    snake.insert(snake.end(), new_position);
    
	if (!ate) {
        snake.erase(snake.begin());
    }
    else {
        ate = false;
    }
}

void new_food() {
	food = {rand() % width, rand() % height};
}

void collision_checker() {
	if (snake[snake.size()-1] == food) {
		ate = true;
		new_food();
		score += 1;
	}
	
	int x = snake[snake.size()-1][0];
	int y = snake[snake.size()-1][1];
	
	if (x <= 0 || x > width || y <= 0 || y > height) {
		running = false;
	}
	
	for (int i = 0; i < snake.size()-1; i++) {
		if (snake[i] == snake[snake.size()-1]) {
			running = false;
		}
	}
}

void update() {
	system("clear");

	for (int y = 0; y < height+2; y++) 
	{
		for (int x = 0; x < width+2; x++) 
		{
			std::vector<int> position = {x, y};
			bool snake_here = (std::find(snake.begin(), snake.end(), position) != snake.end());			
			bool food_here = (position == food);			
			
			if (x == 0 || x == width+1) {
				std::cout << "▒";
			}
			else if (y == 0 || y == height+1) {
				std::cout << "▒";
			}
			else if (snake_here) {
				std::cout << "█";
			}
			else if (food_here) {
				std::cout << "O";
			}
			else {
				std::cout << " ";
			}

		} 
		
		std::cout << std::endl;
	}	
}

void keyboard_input() {
    struct termios old_tio, new_tio;
    tcgetattr(STDIN_FILENO, &old_tio);
    new_tio = old_tio;
    new_tio.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &new_tio);
    int old_flags = fcntl(STDIN_FILENO, F_GETFL);
    fcntl(STDIN_FILENO, F_SETFL, old_flags | O_NONBLOCK);

    int ch = getchar();
    if (ch != EOF) {
        switch(ch) {
            case 'w':
                snake_direction = {0, -1};
                break;

            case 'a':
                snake_direction = {-1, 0};
                break;

            case 's':
                snake_direction = {0, 1};
                break;

            case 'd':
                snake_direction = {1, 0};
                break;
        }
    }

    tcsetattr(STDIN_FILENO, TCSANOW, &old_tio);
    fcntl(STDIN_FILENO, F_SETFL, old_flags);
}

int main() {
	while (running) {
		sleep(1);
		keyboard_input();
		update();
		collision_checker();
		move();
	}
	
	std::cout << "Score: " << score << std::endl;
	return 0;
}
