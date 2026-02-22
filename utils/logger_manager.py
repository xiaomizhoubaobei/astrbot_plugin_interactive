"""
日志管理器模块
提供插件专用的日志记录功能
"""

from astrbot.api import logger


class PluginLogger:
    """插件日志记录器"""

    def __init__(self, plugin_name: str, enable_debug: bool = False):
        """
        初始化插件日志记录器

        Args:
            plugin_name: 插件名称
            enable_debug: 是否启用调试模式
        """
        self.plugin_name = plugin_name
        self.enable_debug = enable_debug

    def info(self, message: str) -> None:
        """记录信息日志"""
        logger.info(f"[{self.plugin_name}] {message}")

    def debug(self, message: str) -> None:
        """记录调试日志"""
        logger.debug(f"[{self.plugin_name}] {message}")

    def warning(self, message: str) -> None:
        """记录警告日志"""
        logger.warning(f"[{self.plugin_name}] {message}")

    def error(self, message: str) -> None:
        """记录错误日志"""
        logger.error(f"[{self.plugin_name}] {message}")

    def log_action(self, user_id: str, platform: str, action: str, details: str = "") -> None:
        """
        记录用户操作日志

        Args:
            user_id: 用户ID
            platform: 平台
            action: 操作类型
            details: 操作详情
        """
        self.info(f"用户 {user_id}@{platform} 执行操作: {action}" + (f" - {details}" if details else ""))


class UserActionLogger:
    """用户操作日志记录器"""

    def __init__(self, plugin_logger: PluginLogger):
        """
        初始化用户操作日志记录器

        Args:
            plugin_logger: 插件日志记录器实例
        """
        self.logger = plugin_logger

    def log_sign(self, user_id: str, platform: str, reward: int) -> None:
        """记录签到操作"""
        self.logger.log_action(user_id, platform, "签到", f"获得 {reward} 积分")

    def log_lottery(self, user_id: str, platform: str, result: str) -> None:
        """记录抽奖操作"""
        self.logger.log_action(user_id, platform, "抽奖", f"结果: {result}")

    def log_shop_buy(self, user_id: str, platform: str, item_name: str, price: int) -> None:
        """记录商店购买操作"""
        self.logger.log_action(user_id, platform, "购买", f"{item_name} ({price} 积分)")

    def log_game_start(self, user_id: str, platform: str, game_type: str) -> None:
        """记录游戏开始操作"""
        self.logger.log_action(user_id, platform, "开始游戏", f"类型: {game_type}")

    def log_game_end(self, user_id: str, platform: str, game_type: str, score: int, won: bool) -> None:
        """记录游戏结束操作"""
        result = "胜利" if won else "失败"
        self.logger.log_action(user_id, platform, "结束游戏", f"{game_type} - {result} ({score} 分)")

    def log_item_use(self, user_id: str, platform: str, item_name: str) -> None:
        """记录物品使用操作"""
        self.logger.log_action(user_id, platform, "使用物品", f"{item_name}")

    def log_cow_action(self, user_id: str, platform: str, action: str) -> None:
        """记录牛牛操作"""
        self.logger.log_action(user_id, platform, "牛牛互动", action)

    def log_generic(self, user_id: str, platform: str, action: str, details: str = "") -> None:
        """记录通用操作"""
        self.logger.log_action(user_id, platform, action, details)