from time import sleep
from threading import Thread
from random import randint
import keyboard
import sys
import queue

user_input = ""

# modify queue to get the last added item and the size of the queue
class Queue(queue.Queue):
    def __init__(self):
        super().__init__()
        self.last = ""
        self.size = 0
    
    def put(self, item):
        super().put(item)
        self.last = item
        self.size += 1
    
    def get(self):
        self.size -= 1
        return super().get()

class Snake:
    def __init__(self, pos, size):
        self.pos = pos[0]+1, pos[1]+1
        self.size = size
        self.snake = []
        self.direction = 0
        self.initSnake()

        self.gen_food()

        self.interval = 0.5
    
    def initSnake(self):
        # init the snake with 4 segments
        for i in range(4):
            self.snake.append((self.pos[0], self.pos[1]+i))

    def move(self):
        # check if the snake hits a wall
        if self.snake[0][1] == 1 or self.snake[0][0] == 1 or self.snake[0][1] == self.size[1] + 2 or self.snake[0][0] == self.size[0] + 2:
            return False

        # check if the snake hits itself
        for i, s in enumerate(self.snake):
            if i == 0: continue
            if s == self.snake[0]: return False
        
        # move the segments
        for i in range(1, len(self.snake)):
            self.snake[-i] = self.snake[-i-1]
            # print("\033[u%s%s\n\033[s"%(str(self.snake[-i]), str(self.snake[-i-1])), end="\r")
        
        # move the snake to the specified direction
        if self.direction == 0:
            self.snake[0] = self.snake[0][0], self.snake[0][1] - 1
        if self.direction == 1:
            self.snake[0] = self.snake[0][0] - 2, self.snake[0][1]
        if self.direction == 2:
            self.snake[0] = self.snake[0][0], self.snake[0][1] + 1
        if self.direction == 3:
            self.snake[0] = self.snake[0][0] + 2, self.snake[0][1]
        
        self.eat()
        
        # print("\033[u%s\n\033[s"%str(self.snake), end="\r")
        return True

        
    def gen_food(self):
        # generate food at a random position
        self.food = randint(1, (self.size[0]) // 2)*2+1, randint(2, self.size[1] + 1)
    
    # eat food an generate new one
    def eat(self):
        if self.snake[0] == self.food:
            self.snake.append(self.snake[-1])
            self.gen_food()
            self.interval -= 0.001
            if self.interval < 0.1: self.interval = 0.1
            

class Grid:
    def __init__(self, size):
        self.size = size[0]*2, size[1]
        self.drawGrid()

        # spawn a snake in the middle of the grid
        self.snake = Snake((self.size[0]//2, self.size[1]//2), self.size)

        self.drawSnake()

        self.running = True

        # queue for input
        self.queue = Queue()

        # hide cursor
        print("\033[?25l\r", end="")  

    
    # draw a grid with the speified size
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
    
    # draw the snake from the Snake class
    def drawSnake(self):
        for idx, s in enumerate(self.snake.snake):
            if idx == 0:
                print("\033[%d;%dH\033[92m#\033[0m"%(s[1],s[0]))
                continue
            print("\033[%d;%dH\033[32m#\033[0m"%(s[1],s[0]))
        
        print("\033[%d;%dH\033[31m@\033[0m"%(self.snake.food[1], self.snake.food[0]))
        	
        print("\033[u", end="")

    # get keybord inputs and write them to the queue
    def on_key_event(self, e):
        if e.event_type == keyboard.KEY_DOWN:
            user_input = e.name
            if user_input != self.queue.last and self.queue.size < 2:
                self.queue.put(user_input)
                self.queue_last = user_input

            # if q is pressed exit the program
            if user_input == 'q':
                self.running = False

    # process the keys from the queue
    def input(self):
        if not self.queue.empty():
            user_input = self.queue.get()
            if user_input == 'w' and self.snake.direction != 2: self.snake.direction = 0
            if user_input == 'a' and self.snake.direction != 3: self.snake.direction = 1
            if user_input == 's' and self.snake.direction != 0: self.snake.direction = 2
            if user_input == 'd' and self.snake.direction != 1: self.snake.direction = 3

    # run the game
    def run(self):
        while self.running:
            for idx, s in enumerate(self.snake.snake):
                print("\033[%d;%dH "%(s[1],s[0]))
            print("\033[%d;%dH "%(self.snake.food[1], self.snake.food[0]))
            self.input()
            if not self.snake.move():
                self.running = False
            self.drawSnake()
            sleep(self.snake.interval)
        
try:
    grid = Grid((20, 20))
    keyboard.hook(grid.on_key_event)
    th = Thread(target=grid.run)
    th.start()
finally:
    # grid.running = False
    th.join()
    keyboard.unhook_all()
    print("\033[u\033[?25h", end="\r")
