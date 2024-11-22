import pygame.font


class Button:
    """为游戏创建按钮的类。"""

    def __init__(self, ai_game, msg):
        """初始化按钮属性。"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮的尺寸和属性。
        self.width, self.height = 200, 50
        self.button_color = (100, 27, 133)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # 创建按钮的 rect 对象并使其居中。
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的消息只需要准备一次。
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """将消息转换为渲染图像，并使文本在按钮上居中。"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制空按钮，然后绘制消息。"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)