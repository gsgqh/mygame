import pygame
import sys
from tile import *
from score import *

WHITE = (255, 255, 255)
DARK_WHITE = (240, 240, 240)
MORE_DARK_WHITE = (220, 220, 220)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (170, 170, 170)
DARK_GRAY = (100, 100, 100)


#定义难度，AI占0%
class Mode:
    def __init__(self, WIDTH, diff = "easy"):
        if(diff == 'easy'):
            self.diff = diff
            self.x = [8,4,8]
            self.y = [6,3,6]
            self.type = 6
            self.TILE_SIZE = int(WIDTH//8)
            self.layer = 3
            self.time_limit = 180
            self.score_rate = 1
        elif(diff == 'normal'):
            self.diff = diff
            self.x = [12,6,12,6,12]
            self.y = [8,4,8,4,8]
            self.type = 8
            self.TILE_SIZE = int(WIDTH//10)
            self.layer = 5
            self.time_limit = 300
            self.score_rate = 1.5
        elif(diff == 'hard'):
            self.diff = diff
            self.x = [12,6,12,6,12]
            self.y = [8,4,8,4,8]
            self.type = 10
            self.TILE_SIZE = int(WIDTH//10)
            self.layer = 5
            self.time_limit = 500
            self.score_rate = 2
        elif (diff == 'fast mode'):
            self.diff = diff
            self.x = [9]
            self.y = [7]
            self.type = 7
            self.TILE_SIZE = int(WIDTH//9)
            self.layer = 1
            self.time_limit = 35
            self.score_rate = 3

#定义胜利条件，AI占0%
def win_condition(tiles,bar):
    if tiles.__len__() == 0 and bar.__len__() == 0:
        return True
    
#定义失败条件，AI占0%
def lose_condition(bar):
    if bar.__len__() > 6:
        return True

# 创建开始界面，AI占40%
def draw_start(screen, WIDTH, HEIGHT):
    draw_background(screen,WIDTH,HEIGHT)
    font = pygame.font.SysFont('Microsoft YaHei', 50)
    text1 = font.render("选择难度", True, BLACK)
    text1_rect = text1.get_rect(center=(WIDTH / 2, HEIGHT / 2.5))
    screen.blit(text1, text1_rect)

    CHINESE_font = pygame.font.SysFont('Microsoft YaHei', 80)
    text2 = CHINESE_font.render("我嘞个豆", True, BLACK)
    text2_rect = text2.get_rect(center=(WIDTH / 2, HEIGHT / 5))
    screen.blit(text2, text2_rect)

    button_font = pygame.font.SysFont('Microsoft YaHei', 40)
    leaderboard_button_font = pygame.font.SysFont('Microsoft YaHei', 40)

    pygame.display.flip()

    while True:
        pos = pygame.mouse.get_pos()
        easy_rect = draw_button(screen, "简单", button_font, WIDTH / 2, HEIGHT / 2, WIDTH / 3, HEIGHT / 13, pos,MORE_DARK_WHITE)
        normal_rect = draw_button(screen, "一般", button_font, WIDTH / 2, HEIGHT / 2 + HEIGHT / 10, WIDTH / 3, HEIGHT / 13, pos,MORE_DARK_WHITE)
        hard_rect = draw_button(screen, "困难", button_font, WIDTH / 2, HEIGHT / 2 + HEIGHT  / 5, WIDTH / 3, HEIGHT / 13, pos,MORE_DARK_WHITE)
        fast_rect = draw_button(screen, "快速模式", button_font, WIDTH / 2, HEIGHT / 2 + HEIGHT* 3 / 10, WIDTH / 3, HEIGHT / 13, pos,MORE_DARK_WHITE)
        leaderboard_rect = draw_button(screen, "排行榜", leaderboard_button_font, WIDTH * 4 / 5, HEIGHT / 10, WIDTH / 4, HEIGHT / 20, pos, MORE_DARK_WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(pos):
                    return "easy"
                elif normal_rect.collidepoint(pos):
                    return "normal"
                elif hard_rect.collidepoint(pos):
                    return "hard"
                elif fast_rect.collidepoint(pos):
                    return "fast mode"
                elif leaderboard_rect.collidepoint(pos):
                    show_leaderboard(screen, WIDTH, HEIGHT)
                    return "show_leaderboard"
        pygame.display.flip()

# 创建弹窗按钮，AI占80%
def draw_button(screen, text, font, x, y, width, height,mouse_pos,color = DARK_WHITE):
    button_rect = pygame.Rect(x, y, width, height)
    button_rect.center = (x,y)
    pygame.draw.rect(screen, color, button_rect)
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, LIGHT_GRAY, button_rect, 3)  # 边框
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(x, y))
    screen.blit(text_surf, text_rect)
    return button_rect

# 绘制结束弹窗，AI占50%
def draw_end(screen, WIDTH, HEIGHT,timer,rate,score,difficulty ,end = "win"):
    # 绘制半透明背景
    s = pygame.Surface((WIDTH, HEIGHT))  
    s.set_alpha(180)  # 半透明
    s.fill(WHITE)
    screen.blit(s, (0, 0))

    font = pygame.font.SysFont('Microsoft YaHei', 80)
    if end == "win":
        text = font.render("You Win!", True, BLACK)
        score.add(int(timer.time_left()*rate))
    elif end == "lose":
        text = font.render("Game Over!", True, BLACK)
    elif end == "timeup":
        text = font.render("Time's Up!", True, BLACK)

    print(f"Saving score: {score.score}")  # 调试信息
    save_leaderboard(score, difficulty)
    

    # 获取文本图像的 Rect 对象
    text_rect = text.get_rect()

    # 将文本的中心位置设置为屏幕的中心
    text_rect.center = (WIDTH / 2, HEIGHT / 4 )

    screen.blit(text, text_rect)

    score_text = font.render(f"Score: {score.score}", True, BLACK)
    score_rect = score_text.get_rect(center=(WIDTH / 2, HEIGHT / 3))
    screen.blit(score_text, score_rect)

    # 创建按钮
    button_font = pygame.font.SysFont('Microsoft YaHei', 60)
    
    while True:
        pos = pygame.mouse.get_pos()
        quit_rect = draw_button(screen, "QUIT", button_font, WIDTH/2, HEIGHT/2 + HEIGHT*3/10, WIDTH / 3, HEIGHT / 10, pos, MORE_DARK_WHITE)
        retry_rect = draw_button(screen, "RETRY", button_font, WIDTH/2, HEIGHT/2 + HEIGHT/10, WIDTH / 3, HEIGHT / 10, pos, MORE_DARK_WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if quit_rect.collidepoint(pos):
                    pygame.quit()
                    sys.exit()
                    return 'quit'
                elif retry_rect.collidepoint(pos):
                    return 'retry'
        pygame.display.flip()

#显示背景图片，AI占0%
def draw_background(screen,WIDTH,HEIGHT):
    background = pygame.image.load("./photo/background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))

# 绘制返回按钮，AI占0%
def draw_back_button(screen, HEIGHT, pos, mouse_pos):
    back_button_image = pygame.image.load("./photo/back_button.png")
    back_button_image = pygame.transform.scale(back_button_image, (HEIGHT/20, HEIGHT/20))
    back_button_image2 = pygame.image.load("./photo/back_button_mouse.png")
    back_button_image2 = pygame.transform.scale(back_button_image2, (HEIGHT/20, HEIGHT/20))
    
    button_rect = back_button_image.get_rect(topleft=pos)
    if button_rect.collidepoint(mouse_pos):
        screen.blit(back_button_image2, pos)
    else:
        screen.blit(back_button_image, pos)
    return button_rect

#绘制撤回按钮，AI占0%
def draw_undo_button(screen, font, x, y, width, height,mouse_pos,tiles,last_tiles):
    undo_button_rect = pygame.Rect(x, y, width, height)
    undo_button_rect.center = (x,y)
    if len(tiles) == len(last_tiles):
        pygame.draw.rect(screen,LIGHT_GRAY , undo_button_rect)
    else:
        pygame.draw.rect(screen, DARK_WHITE, undo_button_rect)
        if undo_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, LIGHT_GRAY, undo_button_rect, 3)  # 边框
    text_surf = font.render("撤回", True, BLACK)
    text_rect = text_surf.get_rect(center=(x, y))
    screen.blit(text_surf, text_rect)
    return undo_button_rect