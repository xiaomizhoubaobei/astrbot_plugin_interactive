from astrbot.api.event import AstrMessageEvent, MessageEventResult

from ..utils.logger_manager import PluginLogger, UserActionLogger


from ..config import ACHIEVEMENTS


class ProfileCommand:
    """查看个人资料命令"""

    def __init__(self, user_manager, logger: PluginLogger):
        self.logger = logger
        self.plugin_name = "astrbot_plugin_interactive"
        self.action_logger = UserActionLogger(logger)
        self.user_manager = user_manager

    async def handle(self, event: AstrMessageEvent) -> None:
        """处理查看个人资料命令"""
        if not event.session_id:
            event.set_result(MessageEventResult().message("无法获取用户ID"))
            return

        user_id = event.get_sender_id()
        platform = event.get_platform_id()

        user = await self.user_manager.get_user_data(user_id, platform)

        # 构建物品列表字符串
        items_list = "无"
        if user["inventory"]:
            items_list = "\n   ".join(
                [f"{item['name']} x{item['count']}" for item in user["inventory"]]
            )

        result = (
            f"📊 {user_id} 的个人资料 📊\n"
            f"💰 积分: {user['points']}\n"
            f"📅 连续签到: {user['consecutive_days']} 天 (总签到: {user['total_sign_days']}天)\n"
            f"🎮 游戏: {user['games_won']} 胜 / {user['games_played']} 场\n"
            f"🎯 成就: {len(user['achievements'])}/{len(ACHIEVEMENTS)} 个\n"
            f"🎰 抽中SSR: {user['ssr_count']} 次\n"
            f"🎯 幸运转盘: {user.get('total_spins', 0)} 次 (免费: {user.get('free_spin_count', 0)})\n"
            f"🛒 商店消费: {user['total_spent']} 积分\n"
            f"🧾 今日使用: {user['daily_command_count']}/50 次\n"
            f"🎁 道具:\n"
            f"  双倍卡: {'1' if user['has_double_card'] else '0'} 张\n"
            f"  免费券: {user['free_lottery_count']} 张\n"
            f"  提示牌: {user['hint_tokens']} 枚\n"
            f"  幸运符: {user['lucky_charm_count']} 个\n"
            f"🎒 物品栏:\n   {items_list}\n\n"
            f"输入 'achievements' 查看成就详情 | 'leaderboard' 查看排名 | 'inventory' 查看物品"
        )

        event.set_result(MessageEventResult().message(result))
