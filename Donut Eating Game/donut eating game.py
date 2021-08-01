# 도넛을 먹어라!
# 캐릭터를 상하좌우로 움직이며 스페이스를 통해 도넛을 먹는 게임
# 도넛은 랜덤한 위치와 갯수로 위에서 아래로 내려오는 구조
# 도넛은 기본 도넛(핑크도넛, 초코도넛)과 방해물 도넛으로 구성됨
# 기본 도넛을 먹을시 점수 +1, 방해물 도넛을 먹을 시 점수 -3
# 캐릭터 목숨은 3으로 기본 도넛이 먹히지 않고 화면을 통과 할 때 목숨 -1
# 점수가 0 아래로 떨어지거나 목숨이 0이 될 때 game over
# 점수가 30점 이상일 시 win!

import pygame, random

# 게임 초기화  >> 필수로 해야 하는 과정
pygame.init()

# 게임창 옵션 설정
size = [480, 640]
screen = pygame.display.set_mode(size)  # 창 크기

title = "도넛 먹기"
pygame.display.set_caption(title)  # 창 제목

# 배경이미지 불러오기 > bilt()메소드로 화면에 띄어줘야 나타남
background = pygame.image.load("background.png.jpeg")

# 게임 내 필요한 설정
clock = pygame.time.Clock()  # FPS 설정하기 위해 필요한 코드


# 캐릭터 클래스
class Character:
    def __init__(self, width, height, v):
        self.width = width  # 이미지 가로길이
        self.height = height  # 이미지 세로높이
        self.v = v  # 속도
        self.x = 0  # x좌표
        self.y = 0  # y좌표

    def put_img(self, address):  # 이미지 불러오기
        if address[-3:] == "png":
            self.img = pygame.image.load(address).convert_alpha()
        else:
            self.img = pygame.image.load(address)

    def change_size(self):  # 새로운 해상도 크기조절
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
        self.width, self.height = self.img.get_size()

    def show(self):  # 화면에 나타내기
        screen.blit(self.img, (self.x, self.y))


# 캐릭터 인스턴스 생성
charater = Character(60, 60, 5)
charater.put_img("character1.png")
charater.change_size()
charater.x = round(size[0] / 2 - charater.height / 2)  # 이미지 크기 만큼 보정
charater.y = size[1] - charater.height - 15  # 이미지 크기 만큼 보정해줘야함

# 게임 시작 대기 화면
start = False
while start == False:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # 엔터 누르면 시작
                start = True

    screen.blit(background, (0, 0))
    font = pygame.font.Font("DXWRbtStd-B.otf", 35)
    text = font.render("Doughnut Eating Game!", True, (255, 255, 0))  # 이미지화 된 텍스트
    screen.blit(text, (90, size[1] / 2 - 200))

    font = pygame.font.Font("THEjunggt160.otf", 20)
    text = font.render("<< 게임 룰 >>", True, (0, 0, 0))
    screen.blit(text, (90, size[1] / 2 - 130))
    text = font.render("시작 - Enter", True, (0, 0, 0))
    screen.blit(text, (90, size[1] / 2 - 85))
    text = font.render("상: ↑, 하: ↓, 좌: ←, 우: →", True, (0, 0, 0))
    screen.blit(text, (90, size[1] / 2 - 55))
    text = font.render("도넛먹기 - Space", True, (0, 0, 0))
    screen.blit(text, (90, size[1] / 2 - 25))
    text = font.render("핑크도넛, 초코도넛 : 점수 + 1", True, (0, 0, 0))
    screen.blit(text, (90, size[1] / 2 + 5))
    text = font.render("핑크도넛, 초코도넛 놓쳤을 시: 목숨 - 1", True, (0, 0, 0))
    screen.blit(text, (90, size[1] / 2 + 35))
    text = font.render("누가 먹던 도넛: 점수 - 3", True, (0, 0, 0))
    screen.blit(text, (90, size[1] / 2 + 65))
    text = font.render("점수가 0보다 작을시 & 목숨 0:", True, (0, 0, 0))
    screen.blit(text, (90, size[1] / 2 + 95))
    text = font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(text, (90, size[1] / 2 + 125))
    text = font.render("점수 30점이상: WIN!", True, (0, 0, 0))
    screen.blit(text, (90, size[1] / 2 + 155))
    pygame.display.update()

# 메인 이벤트
running = True
end = False  # eat >= 30 일때 종료하기 위한 변수

left_go = False
right_go = False
up_go = False
down_go = False
space_go = False

donut_list = []
obstacle_list = []

# 점수
eat = 0
# 캐릭터 목숨
life = 3


# 충돌감지 함수
def crash(donut, charater):
    if donut.x <= charater.x <= donut.x + donut.width:
        if donut.y - charater.height <= charater.y <= donut.y + donut.height:
            return True


while running:
    # FPS 설정
    clock.tick(60)  # 1초에 60번 while 문을 돌게 함.

    for event in pygame.event.get():  # 이벤트를 리스트 형태 pygame.event.get()에 저장
        #pygame.QUIT 게임 종료 버튼(창 닫기 버튼) 클릭 시 발생하거나 커맨드창에서 Ctrl + C를 입력하면 발생
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_go = True
            elif event.key == pygame.K_RIGHT:
                right_go = True
            elif event.key == pygame.K_UP:
                up_go = True
            elif event.key == pygame.K_DOWN:
                down_go = True
            elif event.key == pygame.K_SPACE:
                space_go = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_go = False
            elif event.key == pygame.K_RIGHT:
                right_go = False
            elif event.key == pygame.K_UP:
                up_go = False
            elif event.key == pygame.K_DOWN:
                down_go = False
            elif event.key == pygame.K_SPACE:
                space_go = False

    # 캐릭터 키에 따라 이동
    if left_go == True:
        charater.x -= charater.v
        if charater.x <= 0:  # 화면 밖으로 나가지 않도록 하는 코드
            charater.x = 0

    elif right_go == True:
        charater.x += charater.v
        if charater.x >= size[0] - charater.width:
            charater.x = size[0] - charater.width

    elif up_go == True:
        charater.y -= charater.v
        if charater.y <= 0:
            charater.y = 0

    elif down_go == True:
        charater.y += charater.v
        if charater.y >= size[1] - charater.height:
            charater.y = size[1] - charater.height

    # 도넛 생성
    if random.random() > 0.98:  # 0과 1사이에 수 랜덤 : 0.98인 이유 2프로의 확률로 나타났음 해서
        two_donut = ("핑크 도넛.png", "초코 도넛.png")
        donut = Character(40, 40, 1)
        donut.put_img(random.choice(two_donut))
        donut.change_size()
        donut.x = random.randrange(
            0, size[0] - donut.width - round(charater.width / 2))
        donut_list.append(donut)

    # 도넛 아래로 이동
    death = []
    for i in range(len(donut_list)):
        d = donut_list[i]
        d.y += d.v
        if d.y >= size[1]:  # 메모리를 위해 화면 밖으로 나간 도넛 처리
            death.append(i)

    death.reverse()
    for d in death:  # 화면 밖으로 나간 도넛 목숨 감점 코드
        del donut_list[d]
        life -= 1
        if life == 0:
            running = False

    # 방해물 도넛 생성
    if 0 < eat <= 10:
        if random.randint(1, 300) > 299:
            obstacle = Character(40, 40, 3)
            obstacle.put_img("감점 도넛.png")
            obstacle.change_size()
            obstacle.x = random.randrange(
                0, size[0] - obstacle.width - round(charater.width / 2))
            obstacle_list.append(obstacle)

        # 메모리를 위해 화면 밖으로 나간 도넛 삭제 코드
        death = []
        for i in range(len(obstacle_list)):
            o = obstacle_list[i]
            o.y += o.v
            if o.y >= size[1]:
                death.append(i)
        death.reverse()
        for o in death:
            del obstacle_list[o]

    elif 10 < eat:
        if random.randint(1, 300) > 280:  # 방해물 도넛 나오는 확률 업그레이드
            obstacle = Character(40, 40, 3)
            obstacle.put_img("감점 도넛.png")
            obstacle.change_size()
            obstacle.x = random.randrange(
                0, size[0] - obstacle.width - round(charater.width / 2))
            obstacle_list.append(obstacle)

        death = []
        for i in range(len(obstacle_list)):
            o = obstacle_list[i]
            o.y += o.v
            if o.y >= size[1]:
                death.append(i)
        death.reverse()
        for o in death:
            del obstacle_list[o]

    # 충돌감지
    # 그냥 도넛 먹었을 때
    del_list_1 = []
    for i in range(len(donut_list)):
        dd = donut_list[i]
        if space_go == True and crash(charater, dd) == True:
            del_list_1.append(i)

    del_list_1.reverse()
    for i in del_list_1:
        eat += 1
        del donut_list[i]

    # 방해물 도넛 먹었을 때
    del_list_2 = []
    for i in range(len(obstacle_list)):
        oo = obstacle_list[i]
        if space_go == True and crash(charater, oo) == True:
            del_list_2.append(i)

    del_list_2.reverse()
    for i in del_list_2:
        eat -= 3
        del obstacle_list[i]

    # 점수가 올라갈 수록 도넛 속도 증가
    if eat > 5:
        donut.v = 2
    elif eat > 10:
        donut.v = 3
    elif eat > 15:
        donut.v = 4
    elif eat < 0:
        running = False

    # win 게임 종료
    if eat >= 30:
        end = True
        running = False

    # 그리기
    screen.blit(background, (0, 0))
    charater.show()

    for d in donut_list:
        d.show()
    for o in obstacle_list:
        o.show()

    font = pygame.font.Font("ImcreSoojin OTF.otf", 20)
    text = font.render(
        f"eated: {eat}                                                    life: {life}",
        True, (255, 255, 0))  # True 글자깨지지않게 해주는 역할
    screen.blit(text, (10, 5))

    # 업데이트
    pygame.display.flip()

# 게임 종료

game_over = True
while end and game_over:
    clock.tick(2)
    font = pygame.font.Font("ImcreSoojin OTF.otf", 80)
    text = font.render("WIN!", True, (255, 0, 0))
    screen.blit(text, (140, size[1] / 2 - 50))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False

while game_over and end == False:
    clock.tick(60)
    font = pygame.font.Font("ImcreSoojin OTF.otf", 40)
    text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (120, size[1] / 2 - 50))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False

pygame.quit()
