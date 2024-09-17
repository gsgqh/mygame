import pygame
import random

GRAY = (128, 128, 128)
BLACK = (0,0,0)
LIGHT_YELLOW = (255, 255, 204)

#让颜色更暗,弃用
def darken_color(color, amount=30):
    r = max(color[0] - amount, 0)  # 减少红色通道值
    g = max(color[1] - amount, 0)  # 减少绿色通道值
    b = max(color[2] - amount, 0)  # 减少蓝色通道值
    return (r, g, b)

#让图像变暗，AI占100%
def darken_image(image, amount=50):
    """ 
    将图像变暗，通过和半透明的黑色层叠加。
    amount 参数控制变暗的程度，范围是 0 到 255。
    """
    dark_overlay = pygame.Surface(image.get_size()).convert_alpha()  # 创建和图片相同大小的表面
    dark_overlay.fill((0, 0, 0, amount))  # 用黑色填充，并设置透明度
    image_copy = image.copy()  # 复制原始图片，避免直接修改
    image_copy.blit(dark_overlay, (0, 0))  # 将黑色叠加到图片上
    return image_copy

#生成灰色,弃用
def to_grayscale_mix(color, mix_ratio=0.5):
    # 通过将 RGB 通道平均值生成灰色调
    gray_value = sum(color) // 3
    # 计算每个通道的新值，按照 mix_ratio 比例混合原始颜色和灰度值
    r = int(color[0] * (1 - mix_ratio) + gray_value * mix_ratio)
    g = int(color[1] * (1 - mix_ratio) + gray_value * mix_ratio)
    b = int(color[2] * (1 - mix_ratio) + gray_value * mix_ratio)
    return (r, g, b)

# 定义方块类，AI占75%
class Tile:
    def __init__(self, image_path, x, y, TILE_SIZE,layer):
        self.TILE_SIZE = TILE_SIZE
        # self.color = color
        self.image_path = image_path
        self.image = pygame.image.load(image_path)  # 加载图片
        self.image = pygame.transform.scale(self.image, (self.TILE_SIZE, self.TILE_SIZE))  # 缩放图片到合适大小
        self.dark_image = darken_image(self.image)  # 变暗的图片
        self.rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
        self.layer = layer
        self.isactive = False

    def is_overlapping(self, tile):
    # 检查是否有相交的区域
        if self.rect.colliderect(tile.rect):
            # 确定相交的矩形区域
            overlap_rect = self.rect.clip(tile.rect)
            # 检查相交区域的宽度和高度是否都大于0
            if overlap_rect.width > 0 and overlap_rect.height > 0:
                return True
        return False
    
    #遍历所有上层方块，如果没有位置在其之上的方块，则激活
    def active(self,tiles):
        if self.layer == 0:
            self.isactive = True
            return
        self.isactive = True
        for tile in tiles:
            if tile.layer < self.layer and self.is_overlapping(tile):
                self.isactive = False
                break

    def draw(self,screen,mouse_pos):
        # if self.isactive and self.rect.collidepoint(mouse_pos):
        #     #pygame.draw.rect(screen, (lighten_color(self.color)), (self.rect.x-2, self.rect.y-2, self.TILE_SIZE+4, self.TILE_SIZE+4))
        #     pygame.draw.rect(screen, BLACK, (self.rect.x-2, self.rect.y-2, self.TILE_SIZE+4, self.TILE_SIZE+4),2)
        #     pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, self.TILE_SIZE, self.TILE_SIZE))
        # elif self.isactive:
        #     pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, self.TILE_SIZE, self.TILE_SIZE))
        # else:
        #     pygame.draw.rect(screen, to_grayscale_mix(self.color), (self.rect.x, self.rect.y, self.TILE_SIZE, self.TILE_SIZE))


        if self.isactive and self.rect.collidepoint(mouse_pos):
            #pygame.draw.rect(screen, (lighten_color(self.color)), (self.rect.x-2, self.rect.y-2, self.TILE_SIZE+4, self.TILE_SIZE+4))
            screen.blit(self.image, (self.rect.x, self.rect.y))
            pygame.draw.rect(screen, LIGHT_YELLOW, (self.rect.x, self.rect.y, self.TILE_SIZE, self.TILE_SIZE),self.TILE_SIZE//25)
        elif self.isactive:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.dark_image, (self.rect.x, self.rect.y))

#伪随机，AI占0%
def random_value(last):
    if last == 3:
        return (0,-3)
    elif last == -3:
        return (0,3)
    value = random.random()
    if value > 0.75:
        return (3,3)
    elif value < 0.25:
        return (-3,-3)
    else:
        return (0,0)

# 绘制方块栏
def draw_bar(screen, bar, WIDTH, HEIGHT, BAR_HEIGHT,TILE_SIZE):
    start_x = (WIDTH - TILE_SIZE * 7)/2
    pygame.draw.rect(screen, GRAY, (start_x, HEIGHT - BAR_HEIGHT, TILE_SIZE * 7, TILE_SIZE))
    for i, tile in enumerate(bar):
        #pygame.draw.rect(screen, tile.color, (start_x + i * TILE_SIZE, HEIGHT - BAR_HEIGHT, TILE_SIZE, TILE_SIZE))
        screen.blit(tile.image, (start_x + i * TILE_SIZE, HEIGHT - BAR_HEIGHT))

# 检查方块栏是否有相同颜色的方块并消除
def check_bar(bar, score):
    if len(bar) >= 3:
        counts = {}
        for tile in bar:
            image_path = tile.image_path  # 改为检测图片路径
            if image_path in counts:
                counts[image_path] += 1
            else:
                counts[image_path] = 1
        for image_path, count in counts.items():
            if count >= 3:
                # 如果有 3 个或更多相同的图案，将这些图案移除
                bar = [t for t in bar if t.image_path != image_path]
                score.add(1)
                break
    return score, bar

# 撤回功能，AI占5%
def undo_last_move(score,last_tiles,last_bar):
    tiles = last_tiles.copy()
    bar = last_bar.copy()
    if score.score > 0:
        score.subtract(1)  # 分数减1
    return score, tiles, bar

# # 创建堆叠模板
# def create_stack_template(m):
#     template = []
#     for layer in range(m.layers):
#         layer_template = []
#         for i in range(m.x):
#             row = []
#             for j in range(m.y):
#                 row.append((j, i, layer))
#             layer_template.append(row)
#         template.append(layer_template)
#     return template


# 初始化一组随机方块并按照堆叠模板摆放，AI占30%
def create_tiles(m, TILE_SIZE, TILE_COLORS):
    tiles = []
    tiles_num = []
    colors = []
    count = 0
    for i in range(len(m.x)):
        count += m.x[i] * m.y[i]
    base_count = count // len(TILE_COLORS)
    last = 0
    for i in range(len(TILE_COLORS) - 1):
        last, random_val = random_value(last)
        tiles_num.append(min(base_count + random_val, count))
        count -= tiles_num[-1]
    tiles_num.append(count)
    print(tiles_num)
    for i, num in enumerate(tiles_num):
        for j in range(num):
            colors.append(TILE_COLORS[i])
    print(TILE_COLORS[-1])
    random.shuffle(colors)

    layer = m.layer

    for i in range(layer-1,-1,-1):
        for j in range(m.x[i]):
            for k in range(m.y[i]):
                
                if i % 2 == 1:
                    color = colors.pop()
                    tile = Tile(color, k * (2 * TILE_SIZE) + TILE_SIZE*3/2, j * (2 * TILE_SIZE) + TILE_SIZE*3/2, TILE_SIZE, i)
                    tiles.append(tile)
                else:
                    color = colors.pop()
                    tile = Tile(color, k * (TILE_SIZE) + TILE_SIZE, j * (TILE_SIZE) + TILE_SIZE, TILE_SIZE, i)
                    tiles.append(tile)
    return tiles
