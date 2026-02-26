from astrbot.api.event import AstrMessageEvent, MessageEventResult

from ..utils.logger_manager import PluginLogger, UserActionLogger


class InventoryCommand:
    """查看物品栏命令"""

    def __init__(self, user_manager, logger: PluginLogger):
        self.logger = logger
        self.plugin_name = "astrbot_plugin_interactive"
        self.action_logger = UserActionLogger(logger)
        self.user_manager = user_manager

    async def handle(self, event: AstrMessageEvent) -> None:
        """处理查看物品栏命令"""
        if not event.session_id:
            event.set_result(MessageEventResult().message("无法获取用户ID"))
            return

        user_id = event.get_sender_id()
        platform = event.get_platform_id()

        user = await self.user_manager.get_user_data(user_id, platform)

        if not user["inventory"]:
            event.set_result(
                MessageEventResult().message("你的物品栏空空如也，快去商店购买物品吧！")
            )
            return

        result = "🎒 你的物品栏 🎒\n"
        for item in user["inventory"]:
            result += f"[{item['id']}] {item['name']} x{item['count']}\n"
            result += f"📝 {item['description']}\n\n"
        result += "使用'use <物品ID>'来使用物品"

        event.set_result(MessageEventResult().message(result))
