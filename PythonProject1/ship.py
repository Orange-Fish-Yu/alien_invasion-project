import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """管理飞船的类。"""

    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置。"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获取其 rect。
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 每艘新飞船都位于屏幕底部中央。
        self.rect.midbottom = self.screen_rect.midbottom

        # 以浮点数存储飞船的精确水平位置。
        self.x = float(self.rect.x)

        # 移动标志；飞船初始状态为静止。
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        """让飞船居中在屏幕底部。"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        """根据移动标志更新飞船的位置。"""
        # 更新飞船的 x 值，而不是 rect。
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # 根据 self.x 更新 rect 对象。
        self.rect.x = self.x

    def blitme(self):
        """在当前位置绘制飞船。"""
        self.screen.blit(self.image, self.rect)



