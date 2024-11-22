import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """管理游戏资源和行为的总类。"""

    def __init__(self):
        """初始化游戏并创建游戏资源。"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # 创建一个实例来存储游戏统计信息。
        # 并创建一个计分板。
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # 在非活动状态下开始外星入侵游戏。
        self.game_active = False

        # 创建“开始”按钮。
        self.play_button = Button(self, "Play")

    def run_game(self):
        """启动游戏的主循环。"""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """响应按键和鼠标事件。"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """当玩家点击“开始”按钮时启动新游戏。"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # 重新进行游戏设置
            self.settings.initialize_dynamic_settings()

            # 重置游戏统计信息。
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            # 清除所有剩余的子弹和外星人。
            self.bullets.empty()
            self.aliens.empty()

            # 创建新的一队外星人并将飞船置于中心。
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏鼠标光标。
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """响应按键按下事件。"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应按键松开事件。"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗新子弹并将其添加到子弹组中。"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并清除已消失的子弹。"""
        # 更新子弹位置。
        self.bullets.update()

        # 删除已消失的子弹。
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹与外星人的碰撞。"""
        # 删除任何与外星人碰撞的子弹和外星人。
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # 销毁现有子弹并创建新的一队外星人。
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 提升等级。
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        """响应飞船被外星人击中。"""
        if self.stats.ships_left > 0:
            # 减少剩余飞船数量。
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # 清除所有剩余的子弹和外星人。
            self.bullets.empty()
            self.aliens.empty()

            # 创建新的一队外星人并将飞船置于中心。
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """更新外星人队伍中所有外星人的位置，检查外星人队伍是否到达边缘，然后更新位置。"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检查外星人与飞船是否碰撞。
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查外星人是否碰到屏幕底部。
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕底部。"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # 将此处理为飞船被击中的情况。
                self._ship_hit()
                break

    def _create_fleet(self):
        """创建外星人队伍。"""
        # 创建一个外星人并不断添加外星人，直到没有足够空间为止。
        # 外星人之间的间距是一个外星人宽度和一个外星人高度。
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # 完成一行；重置x值，增加y值
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """创建一个外星人并将其放入队伍中。"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """如果任何外星人到达边缘，做出相应反应。"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """整个队伍下移并改变方向。"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕。"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # 显示出得分信息
        self.sb.show_score()

        # 如果游戏处于非活动状态，则绘制“开始”按钮。
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # 开始游戏
    ai = AlienInvasion()
    ai.run_game()