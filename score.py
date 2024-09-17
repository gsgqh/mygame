import json
import os
import pygame
import setup

from datetime import datetime

BLACK = (0, 0, 0)

#计分类，AI占15%
class Score:
    def __init__(self):
        self.score = 0 

    def add(self,num):
        self.score += num

    def subtract(self,num):
        self.score -= num

    def display_score(self, screen, font, width, height):
        text = font.render(f"SCORE:   {self.score}", True, (0, 0, 0)) 
        screen.blit(text, (width*3/4, height/20))  # 显示在屏幕右上角


# 保存排行榜到文件，AI占100%
def save_leaderboard(score, difficulty):
    leaderboard_file = "leaderboard.json"
    
    # 检查文件是否存在，不存在则创建
    if not os.path.exists(leaderboard_file):
        leaderboard = []
    else:
        with open(leaderboard_file, 'r') as file:
            leaderboard = json.load(file)

    # 添加新记录
    leaderboard.append({
        "score": score.score,
        "difficulty": difficulty,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    # 按分数排序
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)

    # 保存到文件
    with open(leaderboard_file, 'w') as file:
        json.dump(leaderboard, file, indent=4)

# 加载排行榜，AI占100%
def load_leaderboard():
    leaderboard_file = "leaderboard.json"
    
    if not os.path.exists(leaderboard_file):
        return []

    with open(leaderboard_file, 'r') as file:
        leaderboard = json.load(file)

    return leaderboard

#显示排行榜，AI占90%
def show_leaderboard(screen, WIDTH, HEIGHT):
    leaderboard = load_leaderboard()

    # Define colors
    RED = (255, 0, 0)
    ORANGE = (255, 165, 0)
    YELLOW = (255, 255, 0)
    BROWN = (165,42,42)
    GRAY = (90,90,90)
    BLACK = (0, 0, 0)

    # Initialize pygame font
    pygame.font.init()
    font = pygame.font.SysFont('Microsoft YaHei', 70)
    title = font.render("排行榜", True, BLACK)
    title_rect = title.get_rect(center = (WIDTH / 2, HEIGHT / 8))
    running = True
    while running:
        # Draw background
        setup.draw_background(screen, WIDTH, HEIGHT)

        # Draw title
        screen.blit(title, title_rect)

        # Draw headers
        header_font = pygame.font.SysFont(None, 45)
        headers = ["RANK", "Score", "Difficulty", "Time"]
        header_x_positions = [WIDTH / 10, WIDTH / 4, WIDTH / 2, WIDTH * 3 / 4]

        for i, header in enumerate(headers):
            header_text = header_font.render(header, True, BLACK)
            screen.blit(header_text, (header_x_positions[i], HEIGHT / 4))

        y_offset = HEIGHT / 4 + HEIGHT / 15  # Move to the next line

        # Draw leaderboard entries
        for idx, entry in enumerate(leaderboard[:10], start=1):  # Show top 10 entries
            entry_font = pygame.font.SysFont(None, 40)

            # Extract date without year
            try:
                date_str = entry['time']
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                date_display = date_obj.strftime("%m-%d %H:%M:%S")
            except ValueError:
                date_display = entry['time']  # Fallback if date parsing fails

            entry_data = [str(idx), str(entry['score']), entry['difficulty'], date_display]

            # Determine color for the entry
            if idx == 1:
                color = RED
            elif idx == 2:
                color = ORANGE
            elif idx == 3:
                color = BROWN
            else:
                color = GRAY

            for i, data in enumerate(entry_data):
                entry_text = entry_font.render(data, True, color)
                screen.blit(entry_text, (header_x_positions[i], y_offset))

            y_offset += HEIGHT / 15  # Move to the next line

        # Draw back button
        pos = pygame.mouse.get_pos()
        back_button_rect = setup.draw_back_button(screen, HEIGHT, (WIDTH * 1/20, HEIGHT / 40), pos)

        # Refresh display
        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and back_button_rect.collidepoint(pos):
                running = False

