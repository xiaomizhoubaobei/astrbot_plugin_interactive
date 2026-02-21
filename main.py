from astrbot.api import star, logger
from astrbot.api.event import AstrMessageEvent, filter

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


class Main(star.Star):
    """互动游戏插件入口类 - 负责命令注册和初始化"""

    author = "XMZZUZHI"
    name = "astrbot_plugin_interactive"

    def __init__(self, context: star.Context, config: dict | None = None) -> None:
        super().__init__(context, config)
        self.plugin_id = "astrbot_plugin_interactive"

        # 初始化管理器
        self.user_manager = UserManager(self)
        self.game_manager = GameManager()
        self.achievement_manager = AchievementManager(self.user_manager)

        # 初始化命令处理器
        self.guess_command = GuessCommand(self, self.user_manager, self.game_manager, self.achievement_manager)
        self.sign_command = SignCommand(self, self.user_manager, self.achievement_manager)
        self.lottery_command = LotteryCommand(self, self.user_manager, self.achievement_manager)
        self.shop_command = ShopCommand(self, self.user_manager, self.achievement_manager)
        self.use_command = UseCommand(self, self.user_manager)
        self.inventory_command = InventoryCommand(self.user_manager)
        self.achievements_command = AchievementsCommand(self.user_manager)
        self.profile_command = ProfileCommand(self.user_manager)
        self.help_command = HelpCommand()

        logger.info(f"[{self.name}] 插件组件初始化完成")

    async def initialize(self) -> None:
        """插件初始化"""
        logger.info(f"[{self.name}] 互动游戏插件已加载")

    async def terminate(self) -> None:
        """插件卸载"""
        logger.info(f"[{self.name}] 互动游戏插件已卸载，当前活跃游戏数: {len(self.game_manager.games)}")

    # ========== 命令注册 ==========
    @filter.command("guess")
    async def guess(self, event: AstrMessageEvent, message: str = "") -> None:
        """猜数字游戏"""
        user_id = event.get_sender_id()
        logger.debug(f"[{self.name}] 用户 {user_id} 执行 guess 命令: {message}")
        await self.guess_command.handle(event, message)

    @filter.command("sign")
    async def sign(self, event: AstrMessageEvent) -> None:
        """每日签到"""
        user_id = event.get_sender_id()
        logger.debug(f"[{self.name}] 用户 {user_id} 执行 sign 命令")
        await self.sign_command.handle(event)

    @filter.command("lottery")
    async def lottery(self, event: AstrMessageEvent) -> None:
        """消耗10积分抽奖"""
        user_id = event.get_sender_id()
        logger.debug(f"[{self.name}] 用户 {user_id} 执行 lottery 命令")
        await self.lottery_command.handle(event)

    @filter.command("shop")
    async def shop(self, event: AstrMessageEvent, action: str = "", item_id: str = "") -> None:
        """积分商店"""
        user_id = event.get_sender_id()
        logger.debug(f"[{self.name}] 用户 {user_id} 执行 shop 命令: action={action}, item_id={item_id}")
        await self.shop_command.handle(event, action, item_id)

    @filter.command("use")
    async def use_item(self, event: AstrMessageEvent, item_id: str = "") -> None:
        """使用物品"""
        user_id = event.get_sender_id()
        logger.debug(f"[{self.name}] 用户 {user_id} 执行 use 命令: item_id={item_id}")
        await self.use_command.handle(event, item_id)

    @filter.command("inventory")
    async def inventory(self, event: AstrMessageEvent) -> None:
        """查看物品栏"""
        user_id = event.get_sender_id()
        logger.debug(f"[{self.name}] 用户 {user_id} 执行 inventory 命令")
        await self.inventory_command.handle(event)

    @filter.command("achievements")
    async def achievements(self, event: AstrMessageEvent) -> None:
        """查看成就"""
        user_id = event.get_sender_id()
        logger.debug(f"[{self.name}] 用户 {user_id} 执行 achievements 命令")
        await self.achievements_command.handle(event)

    @filter.command("profile")
    async def profile(self, event: AstrMessageEvent) -> None:
        """查看个人资料"""
        user_id = event.get_sender_id()
        logger.debug(f"[{self.name}] 用户 {user_id} 执行 profile 命令")
        await self.profile_command.handle(event)

    @filter.command("interactive")
    async def interactive_help(self, event: AstrMessageEvent) -> None:
        """互动功能帮助"""
        logger.debug(f"[{self.name}] 执行 interactive_help 命令")
        await self.help_command.handle(event)