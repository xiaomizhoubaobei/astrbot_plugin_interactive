from datetime import datetime
from typing import Dict, Optional
import random

from astrbot.api import logger


class GameManager:
    """游戏状态管理器"""

    def __init__(self):
        self.games: Dict[str, Dict] = {}  # 存储游戏状态
        self.plugin_name = "astrbot_plugin_interactive"

    def create_guess_game(self, game_key: str, max_number: int = 100) -> Dict:
        """创建猜数字游戏"""
        game = {
            "target_number": random.randint(1, max_number),
            "attempts": 0,
            "start_time": int(datetime.now().timestamp() * 1000),
            "max_number": max_number
        }
        self.games[game_key] = game
        logger.info(f"[{self.plugin_name}] 创建新游戏: {game_key}, 目标数字: {game['target_number']}")
        return game

    def get_game(self, game_key: str) -> Optional[Dict]:
        """获取游戏状态"""
        return self.games.get(game_key)

    def delete_game(self, game_key: str) -> bool:
        """删除游戏状态"""
        if game_key in self.games:
            del self.games[game_key]
            logger.debug(f"[{self.plugin_name}] 游戏已删除: {game_key}")
            return True
        return False

    def update_game_attempts(self, game_key: str) -> None:
        """增加游戏尝试次数"""
        if game_key in self.games:
            self.games[game_key]["attempts"] += 1
            logger.debug(f"[{self.plugin_name}] 游戏尝试次数更新: {game_key}, 当前次数: {self.games[game_key]['attempts']}")

    def calculate_game_score(self, game: Dict) -> tuple[int, int]:
        """计算游戏得分"""
        time_used = int((int(datetime.now().timestamp() * 1000) - game["start_time"]) / 1000)
        base_points = max(1, 10 - game["attempts"]) * 5
        time_bonus = max(1, 60 - time_used) * 2
        logger.debug(f"[{self.plugin_name}] 计算得分: 基础分={base_points}, 时间奖励={time_bonus}, 用时={time_used}秒")
        return base_points, time_bonus

    def get_hint_range(self, game: Dict) -> tuple[int, int]:
        """获取提示范围"""
        range_val = game["max_number"] // 10
        lower = max(1, game["target_number"] - range_val)
        upper = min(game["max_number"], game["target_number"] + range_val)
        logger.debug(f"[{self.plugin_name}] 生成提示范围: {lower} ~ {upper}")
        return lower, upper