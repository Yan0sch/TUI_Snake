from time import sleep
from threading import Thread

import keyboard

user_input = ""
def on_key_event(e):
    global user_input
    if e.event_type == keyboard.KEY_DOWN:
        user_input = e.name
        print(f"Benutzereingabe: {user_input}")


class Snake:
    def __init__(self, pos, size):
        self.pos = pos[0]+1, pos[1]+1
        self.size = size
        self.snake = []
        self.direction = 0
        self.initSnake()
    
    def initSnake(self):
        for i in range(4):
            self.snake.append((self.pos[0], self.pos[1]+i))
    
    def user_input(self):
        global user_input
        while 1:
            if user_input == "w": self.direction = 0
            if user_input == "a": self.direction = 1
            if user_input == "s": self.direction = 2
            if user_input == "d": self.direction = 3
            print("\033[u%s"%user_input)

    def move(self):
        if self.snake[0][1] == 2:
            self.direction = 1
        if self.snake[0][0] == 2:
            self.direction = 2
        if self.snake[0][1] == self.size[1] + 1:
            self.direction = 3
        
        if self.snake[0][0] == self.size[0] + 1:
            self.direction = 0

        for i in range(1, len(self.snake)):
            self.snake[-i] = self.snake[-i-1]
            # print("\033[u%s%s\n\033[s"%(str(self.snake[-i]), str(self.snake[-i-1])), end="\r")
        if self.direction == 0:
            self.snake[0] = self.snake[0][0], self.snake[0][1] - 1
        if self.direction == 1:
            self.snake[0] = self.snake[0][0]-1, self.snake[0][1]
        if self.direction == 2:
            self.snake[0] = self.snake[0][0], self.snake[0][1] + 1
        if self.direction == 3:
            self.snake[0] = self.snake[0][0] + 1, self.snake[0][1]
        
        # print("\033[u%s\n\033[s"%str(self.snake), end="\r")
            

class Grid:
    def __init__(self, size):
        self.size = size[0]*2, size[1]
        self.drawGrid()

        self.snake = Snake((self.size[0]//2, self.size[1]//2), self.size)

        self.drawSnake()

        # keyboard.hook(on_key_event)
    
    def drawGrid(self):
        print("\033[2J\033[0;0H", end="\r")
        
        for y in range(self.size[1]+2):
            if y == 0:
                print("┌"+"─"*(self.size[0])+"┐")
                continue
            if y == self.size[1] + 1:
                print("└"+"─"*(self.size[0])+"┘")
                continue
            print("│"+" "*(self.size[0])+"│")
        
        print("\033[s", end="\r")
    
    def drawSnake(self):
        for idx, s in enumerate(self.snake.snake):
            print("\033[%d;%dH#"%(s[1],s[0]))
        	
        print("\033[u", end="")

    def run(self):
        while 1:
            for idx, s in enumerate(self.snake.snake):
                print("\033[%d;%dH "%(s[1],s[0]))
            self.snake.move()
            self.drawSnake()
            sleep(0.5)

            

try:
    if __name__ == "__main__":
        keyboard.hook(on_key_event)
        grid = Grid((20, 20))
        Thread(target=grid.run).start()
finally:
    # keyboard.unhook_all()
    print("\033[u", end="\r")