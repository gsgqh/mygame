import pygame
import random
from tile import * 
from setup import *
from gametime import *
from score import *
# 初始化 Pygame
pygame.init()

# 设置屏幕尺寸

# 根据屏幕分辨率设置尺寸
infoObject = pygame.display.Info()
HEIGHT = infoObject.current_h - 100
WIDTH = HEIGHT/3*2
#WIDTH, HEIGHT = 800, 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("我了个豆小游戏")

# 设置颜色和字体
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# TILE_COLORS = [
#     (255, 0, 0),     # 红色 (Red)
#     (0, 255, 0),     # 绿色 (Green)
#     (0, 0, 255),     # 蓝色 (Blue)
#     (255, 165, 0),   # 橙色 (Orange)
#     (128, 0, 128),   # 紫色 (Purple)
#     (255, 255, 0),   # 黄色 (Yellow)
#     (0, 255, 255)    # 青色 (Cyan)
# ]
FONT = pygame.font.SysFont('Microsoft YaHei', 40)

#主游戏循环,AI占50%
def game_loop():
    running = True

    diff = draw_start(screen,WIDTH,HEIGHT)
    if diff == "show_leaderboard":
        running = False
        return 

    m = Mode(WIDTH,diff);
    BAR_HEIGHT = 2 * m.TILE_SIZE
    TILE_COLORS = [ (f"./photo/{i}.png") for i in range(1, m.type + 1) ]
    game_timer = GameTimer(m.time_limit)
    score = Score()

    font = pygame.font.SysFont('None', 40)
    undo_font = pygame.font.SysFont('Microsoft YaHei', 30)

    tiles = []
    bar = []
    last_tiles = []
    last_bar = []
    tiles = create_tiles(m,m.TILE_SIZE,TILE_COLORS)
    last_tiles = tiles.copy()

    while running:
        draw_background(screen,WIDTH,HEIGHT)
        pos = pygame.mouse.get_pos()
        back_button_rect = draw_back_button(screen, HEIGHT, (WIDTH*1/20, HEIGHT/40), pos)
        undo_button_rect = draw_undo_button(screen, undo_font, WIDTH*1/2, HEIGHT* 1 /30, WIDTH / 10, HEIGHT / 20, pos, tiles, last_tiles)  
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for tile in tiles:
                    if tile.rect.collidepoint(pos) and tile.isactive:
                        last_bar = bar.copy()
                        last_tiles = tiles.copy()
                        bar.append(tile)
                        tiles.remove(tile)
                        score,bar = check_bar(bar,score)
                        break
                if back_button_rect.collidepoint(pos):
                    running = False
                if undo_button_rect.collidepoint(pos):
                    score, tiles, bar = undo_last_move(score,last_tiles,last_bar)
                
        # 绘制方块
        for tile in tiles:
            tile.active(tiles)
            tile.draw(screen,pos)

        # 绘制栏中的方块
        draw_bar(screen, bar, WIDTH, HEIGHT, BAR_HEIGHT, m.TILE_SIZE)
        
        # 显示时间分数
        game_timer.display_time(screen, font, WIDTH, HEIGHT)
        score.display_score(screen, font, WIDTH, HEIGHT)

        pygame.display.flip()
        if win_condition(tiles,bar):
            draw_end(screen,WIDTH,HEIGHT,game_timer,m.score_rate,score,diff,'win')
            running = False
        elif lose_condition(bar):
            draw_end(screen,WIDTH,HEIGHT,game_timer,m.score_rate,score,diff,'lose')
            running = False
        elif game_timer.is_time_up():
            draw_end(screen,WIDTH,HEIGHT,game_timer,m.score_rate,score,diff,'timeup')
            running = False

# 主游戏循环
def main():
    while True:
        game_loop()

    
        

if __name__ == "__main__":
    main()
