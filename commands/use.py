from astrbot.api.event import AstrMessageEvent, MessageEventResult

from ..utils.logger_manager import PluginLogger, UserActionLogger


class UseCommand:
    """使用物品命令"""

    def __init__(self, star_instance, user_manager, logger: PluginLogger):
        self.logger = logger
        self.plugin_name = "astrbot_plugin_interactive"
        self.action_logger = UserActionLogger(logger)
        self.star = star_instance
        self.user_manager = user_manager

    async def handle(self, event: AstrMessageEvent, item_id: str = "") -> None:
        """处理使用物品命令"""
        if not event.session_id:
            event.set_result(MessageEventResult().message("❌ 无法获取用户ID"))
            return

        user_id = event.get_sender_id()
        platform = event.get_platform_id()

        if not item_id:
            event.set_result(
                MessageEventResult().message(
                    "❌ 请输入要使用的物品ID，使用 'shop list' 查看可购买物品"
                )
            )
            return

        if not await self.user_manager.check_command_limits(user_id, platform, event):
            return

        user = await self.user_manager.get_user_data(user_id, platform)
        item = await self.user_manager.get_inventory_item(user_id, platform, item_id)

        if not item:
            event.set_result(
                MessageEventResult().message(
                    "❌ 你没有该物品或物品不存在，请检查物品ID是否正确"
                )
            )
            return

        result = self._apply_item_effect(user, item)

        await self.user_manager.remove_item_from_inventory(user_id, platform, item_id)
        await self.user_manager.update_user_data(user_id, platform, user)

        event.set_result(MessageEventResult().message(result))

    def _apply_item_effect(self, user: dict, item: dict) -> str:
        """应用物品效果"""
        if item["id"] == "coffee":
            if user["daily_command_count"] >= 5:
                user["daily_command_count"] -= 5
            else:
                user["daily_command_count"] = 0
            return "☕ 你喝了一杯提神咖啡，恢复了 5 次每日使用次数！"
        elif item["id"] == "exp_card":
            return "✨ 经验卡已激活！下次猜数字游戏将获得额外 20% 积分奖励！"
        else:
            return f"✅ 使用了 {item['name']}：{item['description']}"
