import pygame

# 计时器类，AI占100%
class GameTimer:
    def __init__(self, time_limit):
        self.time_limit = time_limit  # 总时间，单位为秒
        self.start_ticks = pygame.time.get_ticks()  # 获取游戏开始时的时间戳

    def time_left(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) / 1000  # 计算已过时间，单位为秒
        return max(self.time_limit - elapsed_time, 0)  # 返回剩余时间，确保不为负

    def is_time_up(self):
        return self.time_left() <= 0  # 检查是否时间到了

    def display_time(self, screen, font, width, height):
        time_left = int(self.time_left())
        text = font.render(f"Time left: {time_left}", True, (0, 0, 0))  # 黑色字体显示时间
        screen.blit(text, (width*7/10, height/40))  # 显示在屏幕右上角
