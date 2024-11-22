class GameStats:
    """跟踪《外星人入侵》的统计信息。"""

    def __init__(self, ai_game):
        """初始化统计信息。"""
        self.settings = ai_game.settings
        self.reset_stats()

        # 最高分不被重置
        self.high_score = 0

    def reset_stats(self):
        """初始化游戏中可能会变化的统计信息。"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
