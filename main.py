from astrbot.api import star
from astrbot.api.event import AstrMessageEvent, filter

from .utils.logger_manager import PluginLogger, UserActionLogger
from .data import UserManager, GameManager
from .commands.achievements import AchievementManager, AchievementsCommand
from .commands.guess import GuessCommand
from .commands.sign import SignCommand
from .commands.lottery import LotteryCommand
from .commands.shop import ShopCommand
from .commands.use import UseCommand
from .commands.inventory import InventoryCommand
from .commands.profile import ProfileCommand
from .commands.help import HelpCommand
from .commands.cow import CowCommand
from .commands.spin import SpinCommand


class Main(star.Star):
    """互动游戏插件入口类 - 负责命令注册和初始化"""

    author = "祁筱欣"
    name = "astrbot_plugin_interactive"

    def __init__(self, context: star.Context, config: dict | None = None) -> None:
        super().__init__(context, config)
        self.plugin_id = "astrbot_plugin_interactive"

        # 初始化配置
        self.config = config if config else {}
        self._init_config()

        # 初始化日志系统
        self.logger = PluginLogger(
            self.name,
            enable_debug=self.config.get("debug_mode", False)
        )
        self.action_logger = UserActionLogger(self.logger)

        # 初始化管理器
        self.user_manager = UserManager(self)
        self.game_manager = GameManager(self.logger)
        self.achievement_manager = AchievementManager(self.user_manager, self.logger)

        # 初始化命令处理器
        self.guess_command = GuessCommand(self, self.user_manager, self.game_manager, self.achievement_manager, self.logger)
        self.sign_command = SignCommand(self, self.user_manager, self.achievement_manager, self.logger)
        self.lottery_command = LotteryCommand(self, self.user_manager, self.achievement_manager, self.logger)
        self.shop_command = ShopCommand(self, self.user_manager, self.achievement_manager, self.logger)
        self.use_command = UseCommand(self, self.user_manager, self.logger)
        self.inventory_command = InventoryCommand(self.user_manager, self.logger)
        self.achievements_command = AchievementsCommand(self.user_manager, self.logger)
        self.profile_command = ProfileCommand(self.user_manager, self.logger)
        self.help_command = HelpCommand()
        self.cow_command = CowCommand(self, self.user_manager, self.logger)
        self.spin_command = SpinCommand(self, self.user_manager, self.achievement_manager, self.logger)

        self.logger.info("插件组件初始化完成")

    def _init_config(self) -> None:
        """初始化配置，确保所有配置项都有默认值"""
        defaults = {
            "points": {
                "initial_points": 100,
                "daily_command_limit": 50,
                "command_cooldown": 5,
            },
            "sign": {
                "base_reward": 10,
                "consecutive_bonus": 2,
                "max_consecutive_bonus": 100,
                "week_bonus": 50,
            },
            "lottery": {
                "cost": 10,
                "ssr_rate": 5.0,
                "sr_rate": 10.0,
                "r_rate": 25.0,
                "ssr_reward": 100,
                "sr_reward": 30,
                "r_reward": 10,
                "lucky_charm_boost": 20.0,
            },
            "guess_game": {
                "max_number": 100,
                "base_points": 5,
                "time_bonus_rate": 2.0,
                "attempt_penalty": 1,
            },
            "cow_system": {
                "feed_cost": 10,
                "play_cost": 5,
                "feed_restore": 30,
                "play_restore": 30,
                "level_up_exp_mult": 1.0,
                "level_up_favor_mult": 1.0,
            },
            "shop": {
                "enable_custom_prices": False,
                "double_card_price": 50,
                "lottery_ticket_price": 40,
                "hint_token_price": 30,
                "lucky_charm_price": 100,
                "coffee_price": 80,
                "exp_card_price": 120,
            },
        }

        # 合并默认值到配置
        for key, value in defaults.items():
            if key not in self.config:
                self.config[key] = value
            else:
                # 确保嵌套对象也有默认值
                if isinstance(value, dict) and isinstance(self.config[key], dict):
                    for sub_key, sub_value in value.items():
                        if sub_key not in self.config[key]:
                            self.config[key][sub_key] = sub_value

    def get_config(self, *keys) -> any:
        """获取配置值"""
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        return value

    async def initialize(self) -> None:
        """插件初始化"""
        self.logger.info("互动游戏插件已加载")

    async def terminate(self) -> None:
        """插件卸载"""
        self.logger.info("互动游戏插件已卸载，当前活跃游戏数: {len(self.game_manager.games)}")

    # ========== 命令注册 ==========
    @filter.command("guess")
    async def guess(self, event: AstrMessageEvent, message: str = "") -> None:
        """猜数字游戏"""
        user_id = event.get_sender_id()
        self.logger.debug("用户 {user_id} 执行 guess 命令: {message}")
        await self.guess_command.handle(event, message)

    @filter.command("sign")
    async def sign(self, event: AstrMessageEvent) -> None:
        """每日签到"""
        user_id = event.get_sender_id()
        self.logger.debug("用户 {user_id} 执行 sign 命令")
        await self.sign_command.handle(event)

    @filter.command("lottery")
    async def lottery(self, event: AstrMessageEvent) -> None:
        """消耗10积分抽奖"""
        user_id = event.get_sender_id()
        self.logger.debug("用户 {user_id} 执行 lottery 命令")
        await self.lottery_command.handle(event)

    @filter.command("shop")
    async def shop(self, event: AstrMessageEvent, action: str = "", item_id: str = "") -> None:
        """积分商店"""
        user_id = event.get_sender_id()
        self.logger.debug("用户 {user_id} 执行 shop 命令: action={action}, item_id={item_id}")
        await self.shop_command.handle(event, action, item_id)

    @filter.command("use")
    async def use_item(self, event: AstrMessageEvent, item_id: str = "") -> None:
        """使用物品"""
        user_id = event.get_sender_id()
        self.logger.debug("用户 {user_id} 执行 use 命令: item_id={item_id}")
        await self.use_command.handle(event, item_id)

    @filter.command("inventory")
    async def inventory(self, event: AstrMessageEvent) -> None:
        """查看物品栏"""
        user_id = event.get_sender_id()
        self.logger.debug("用户 {user_id} 执行 inventory 命令")
        await self.inventory_command.handle(event)

    @filter.command("achievements")
    async def achievements(self, event: AstrMessageEvent) -> None:
        """查看成就"""
        user_id = event.get_sender_id()
        self.logger.debug("用户 {user_id} 执行 achievements 命令")
        await self.achievements_command.handle(event)

    @filter.command("profile")
    async def profile(self, event: AstrMessageEvent) -> None:
        """查看个人资料"""
        user_id = event.get_sender_id()
        self.logger.debug("用户 {user_id} 执行 profile 命令")
        await self.profile_command.handle(event)

    @filter.command("interactive")
    async def interactive_help(self, event: AstrMessageEvent) -> None:
        """互动功能帮助"""
        self.logger.debug("执行 interactive_help 命令")
        await self.help_command.handle(event)

    @filter.command("cow")
    async def cow(self, event: AstrMessageEvent, action: str = "", nickname: str = "") -> None:
        """牛牛系统"""
        user_id = event.get_sender_id()
        self.logger.debug("用户 {user_id} 执行 cow 命令: action={action}, nickname={nickname}")
        await self.cow_command.handle(event, action, nickname)

    @filter.command("spin")
    async def spin(self, event: AstrMessageEvent, message: str = "") -> None:
        """幸运转盘"""
        user_id = event.get_sender_id()
        self.logger.debug("用户 {user_id} 执行 spin 命令: {message}")
        await self.spin_command.handle(event, message.strip())