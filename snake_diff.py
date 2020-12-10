import pygame               #파이게임 모듈 임포트
import random               #랜덤 생성
from datetime import datetime
from datetime import timedelta #일정 시각마다 블록 움직이기

pygame.init()               #파이게임 초기화

red = 255, 0, 0        # 적색:   적 255, 녹   0, 청   0  #색 정의
green = 0, 255, 0      # 녹색:   적   0, 녹 255, 청   0
blue = 0, 0, 255       # 청색:   적   0, 녹   0, 청 255
puple = 127, 0, 127   # 보라색: 적 127, 녹   0, 청 127
black = 0, 0, 0        # 검은색: 적   0, 녹   0, 청   0
gray = 127, 127, 127   # 회색:   적 127, 녹 127, 청 127
white = 255, 255, 255  # 하얀색: 적 255, 녹 255, 청 255

screen_width = 500          #게임 화면 높낮이
screen_height = 500
block_size = 10

def draw_background(screen):    #배경 그리기 함수
    background = pygame.Rect((0, 0), (screen_width, screen_height))
    pygame.draw.rect(screen, white, background)

def draw_block(screen, color, position):    #블록 그리기 함수
    block = pygame.Rect((position[1]*block_size, position[0]*block_size), \
                        (block_size, block_size))
    pygame.draw.rect(screen, color, block)

direction_on_key = {
    pygame.K_UP: 'north',
    pygame.K_DOWN: 'south',
    pygame.K_LEFT: 'west',
    pygame.K_RIGHT: 'east'
} #방향 설정

screen = pygame.display.set_mode((screen_width, screen_height))
                            #게임 화면 창 크기 조절

class snake:        #뱀 클래스
    color = blue
    def __init__(self):
        self.positions = [(9, 6), (9,7), (9,8), (9,9)]
        self.direction = 'north'
    def draw(self, screen):
        for position in self.positions:
            draw_block(screen, self.color, position)
    def crawl(self):
        head_position = self.positions[0]
        y, x = head_position
        if self.direction == 'north':
            self.positions = [(y-1, x)] + self.positions[:-1]
        elif self.direction == 'south':
            self.positions = [(y+1, x)] + self.positions[:-1]
        elif self.direction == 'west':
            self.positions = [(y, x-1)] + self.positions[:-1]
        elif self.direction == 'east':
            self.positions = [(y, x+1)] + self.positions[:-1]
    def turn(self, direction):
        self.direction = direction
    def grow(self):
        tail_position = self.positions[-1]
        y, x = tail_position
        if self.direction == 'north':
            self.positions.append((y-1, x))
        elif self.direction == 'south':
            self.positions.append((y+1, x))
        elif self.direction == 'west':
            self.positions.append((y, x-1))
        elif self.direction == 'east':
            self.positions.append((y, x+1))

class apple:        #사과 클래스
    color = red
    def __init__(self, position=(5, 5)):
        self.position = position
    def draw(self, screen):
        draw_block(screen, self.color, self.position)

class gameboard:
    width = 20
    heigh = 20
    def __init__(self):
        self.snake = snake()
        self.apple = apple()
    def draw(self, screen):
        self.apple.draw(screen)
        self.snake.draw(screen)
    def put_new_apple(self):
        self.apple = apple((random.randint(0, 19), (random.randint(0, 19))))
        for position in self.snake.positions:
            if self.apple.position == position:
                self.put_new_apple()
                break
    def process_turn(self):
        self.snake.crawl()
        if self.snake.positions[0] in self.snake.positions[1:]:
            raise snakecollisionexception()
        if self.snake.positions[0] ==self.apple.position:
            self.snake.grow()
            self.put_new_apple()

class snakecollisionexception(Exception):
    pass

game_board = gameboard()
block_position = [0, 0]
last_turn_time = datetime.now()

TURN_INTERVAL = timedelta(seconds=0.2)
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key in direction_on_key:
                game_board.snake.turn(direction_on_key[event.key])


    if TURN_INTERVAL < datetime.now() - last_turn_time:
        try:
            game_board.process_turn()
        except snakecollisionexception():
            exit()
        last_turn_time = datetime.now()

    draw_background(screen)
    game_board.draw(screen)
    pygame.display.update()  # 화면 업데이트