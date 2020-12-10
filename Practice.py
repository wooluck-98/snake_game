import pygame
import random

pygame.init()                       #pygame 모듈 초기화

RED = 255, 0, 0                     #색 정의
GREEN = 0, 255, 0
WHITE = 255, 255, 255

SCREEN_WIDTH = 500                  #화면 크기
SCREEN_HEIGHT = 500
BLOCK_SIZE = 20                     #블록 크기
GAME_SCREEN_RECT = pygame.Rect((0, 100), (500, 400))             #실제 게임 화면 크기
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  #GUI 출력
pygame.display.set_caption("무려 스네이크 게임 ")                   #GUI 이름
pygame.draw.rect(SCREEN, WHITE, GAME_SCREEN_RECT)                #게임판 그리기

FONT_1 = pygame.font.SysFont("gulim.ttc", 60)                    #텍스트 그리기
TITLE = FONT_1.render("S~NAKE!", True, WHITE)

DIRECTION_KEY = {                                                #방향 딕셔너리
    pygame.K_UP: 'UP',
    pygame.K_DOWN: 'DOWN',
    pygame.K_LEFT: 'LEFT',
    pygame.K_RIGHT: 'RIGHT'
}

def DRAW_BACKGROUND(screen):                                     #배경 그리기 함수
    BACKGROUND = pygame.Rect((0, 100), (500, 400))
    pygame.draw.rect(screen, WHITE, BACKGROUND)

def DRAW_BLOCK(screen, color, position):                         #블럭을 그리는 함수
    BLOCK = pygame.Rect((position[0] * BLOCK_SIZE, position[1] * BLOCK_SIZE), \
                        (BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, color, BLOCK)

class SNAKE:                                                     #뱀 클래스
    color = GREEN                                                #뱀 색깔
    def __init__(self):                                          #뱀 형태 함수
        self.positions = [(3, 5), (2, 5), (1, 5), (0, 5)]
        self.direction = pygame.K_RIGHT
    def DRAW(self, screen):                                      #뱀 자기자신 그리기 함수
        for position in self.positions:
            DRAW_BLOCK(screen, self.color, position)
    def CRAWL(self):                                             #뱀 전체 움직이기 함수
        HEAD = self.positions[0]
        X, Y = HEAD
        if self.direction == 'UP':
            self.positions = [(X, Y-1)] + self.positions[:-1]
        elif self.direction == 'DOWN':
            self.positions = [(X, Y+1)] + self.positions[:-1]
        elif self.direction == 'LEFT':
            self.positions = [(X-1, Y)] + self.positions[:-1]
        elif self.direction == 'RIGHT':
            self.positions = [(X+1, Y)] + self.positions[:-1]
    def TURN(self,direction):                                   #뱀 방향 바꾸기 함수
        self.direction = direction
    def GROW(self):                                             #뱀 자라나기 함수
        GAMESPEED.FPS += 1                                      #게임속도 빨리지는 장치
        TAIL = self.positions[-1]
        X, Y = TAIL
        if self.direction == 'UP':
            self.positions.append((X, Y-1))
        elif self.direction == 'DOWN':
            self.positions.append((X, Y+1))
        elif self.direction == 'LEFT':
            self.positions.append((X-1, Y))
        elif self.direction == 'RIGHt':
            self.positions.append((X+1, Y))

class APPLE:                                                  #사과 클래스
    color = RED                                               #사과 색깔
    def __init__(self, position=(random.randint(0,24), random.randint(5,24))): #사과 위치 함수
        self.position = position
    def DRAW(self, screen):                                   #사과 그리기 함수
        DRAW_BLOCK(screen, self.color, self.position)

class GAMEBOARD:                                             #게임판 클래스(뱀과 사과를 포함)
    WIDTH = 25
    HEIGHT = 25
    def __init__(self):                                      #게임판에서의 뱀과 사과 속성 갖는 함수
        self.snake = SNAKE()
        self.apple = APPLE()
    def DRAW(self, screen):                                  #게임판위에 뱀, 사과 그리기 함수
        self.apple.DRAW(screen)
        self.snake.DRAW(screen)
    def PUT_APPLE(self):                                     #사과 랜덤 생성 함수
        self.apple = APPLE((random.randint(0,24), random.randint(5,24)))
        for position in self.snake.positions:
            if self.apple.position == position:
                self.PUT_APPLE()
                break
    def PROCESS_TURN(self):                                 #한 차례씩 진행시키는 함수
        self.snake.CRAWL()                                  #뱀의 전체 움직이기 함수
        if self.snake.positions[0] in self.snake.positions[1:]:  #뱀 충돌
            raise SNAKECOLLISION()
        if self.snake.positions[0] == self.apple.position:       #뱀이 사과를 먹음
            self.snake.GROW()                                    #뱀 자라나기, 사과 생성
            self.PUT_APPLE()

class SNAKECOLLISION:                                       #뱀 충돌
    pass
class GAMESPEED:                                            #게임 스피드 클래스
    FPS = 5
    CLOCK = pygame.time.Clock()

GAME_BOARD = GAMEBOARD()                                  #GAMEBOARD 인스턴스 생성
GAME_SPEED = GAMESPEED                                    #GAME_SPEED 인스턴스 생성

while True:                                              #메인 루프문
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:                   #창 닫기 누르면 꺼지기
            exit()
        if event.type == pygame.KEYDOWN:                #뱀 움직이기
            if event.key in DIRECTION_KEY:
                GAME_BOARD.snake.TURN(DIRECTION_KEY[event.key])

    try:                                         #try: 처리중 오류 발생 시 except: 처리
        GAME_BOARD.PROCESS_TURN()

    except SNAKECOLLISION():
        exit()

    GAME_SPEED.CLOCK.tick(GAME_SPEED.FPS)              #프레임 실행
    SCREEN.blit(TITLE, (15, 30))                       #폰트 출력
    DRAW_BACKGROUND(SCREEN)                            #배경 그리기 함수
    GAME_BOARD.DRAW(SCREEN)                            #게임 보드에 뱀, 사과 그리기 함수
    pygame.display.update()                            #화면 업데이트
