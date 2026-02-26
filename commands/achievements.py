from astrbot.api.event import AstrMessageEvent, MessageEventResult

from ..utils.logger_manager import PluginLogger, UserActionLogger


from ..config import ACHIEVEMENTS


class AchievementManager:
    """成就管理器"""

    def __init__(self, user_manager, logger: PluginLogger):
        self.logger = logger
        self.plugin_name = "astrbot_plugin_interactive"
        self.action_logger = UserActionLogger(logger)
        self.user_manager = user_manager

    async def check(
        self, user_id: str, platform: str, user_data: dict, event: AstrMessageEvent
    ) -> None:
        """检查并解锁成就"""
        unlocked = []

        for achievement in ACHIEVEMENTS:
            if achievement["id"] not in user_data["achievements"]:
                if self._check_condition(achievement, user_data):
                    user_data["achievements"].append(achievement["id"])
                    user_data["points"] += achievement["reward"]
                    unlocked.append(
                        f"🎖️ {achievement['name']} - {achievement['description']} (+{achievement['reward']}积分)"
                    )
                    self.logger.info(
                        f"[{self.logger}] 用户 {user_id}@{platform} 解锁成就: {achievement['name']}"
                    )

        if unlocked:
            await self.user_manager.update_user_data(user_id, platform, user_data)
            event.set_result(
                MessageEventResult().message(f"🎉 解锁成就！\n" + "\n".join(unlocked))
            )

    def _check_condition(self, achievement: dict, user_data: dict) -> bool:
        """检查成就条件"""
        if achievement["id"] == "first_blood":
            return user_data["games_won"] >= 1
        elif achievement["id"] == "sign_master":
            return user_data["consecutive_days"] >= 7
        elif achievement["id"] == "millionaire":
            return user_data["points"] >= 500
        elif achievement["id"] == "game_addict":
            return user_data["games_played"] >= 20
        elif achievement["id"] == "lottery_king":
            return user_data["ssr_count"] >= 5
        elif achievement["id"] == "shopper":
            return user_data["total_spent"] >= 1000
        # 转盘相关成就
        elif achievement["id"] == "spin_beginner":
            spin_data = user_data.get("spin", {})
            return spin_data.get("total_spins", 0) >= 1
        elif achievement["id"] == "spin_regular":
            spin_data = user_data.get("spin", {})
            return spin_data.get("total_spins", 0) >= 10
        elif achievement["id"] == "spin_master":
            spin_data = user_data.get("spin", {})
            # 检查连续7天参与（简化版：检查最近7天是否都有记录）
            history = spin_data.get("history", [])
            if len(history) < 7:
                return False
            from datetime import datetime, timedelta

            today = datetime.now().date()
            dates = set()
            for entry in history[:20]:  # 检查最近20条记录
                try:
                    entry_date = datetime.strptime(entry["date"], "%Y-%m-%d").date()
                    dates.add(entry_date)
                except:
                    continue
            # 检查今天和前6天是否都有记录
            for i in range(7):
                check_date = today - timedelta(days=i)
                if check_date not in dates:
                    return False
            return True
        elif achievement["id"] == "lucky_star":
            spin_data = user_data.get("spin", {})
            history = spin_data.get("history", [])
            # 检查是否获得过特等奖（tier=1）
            return any(entry.get("tier") == 1 for entry in history)
        return False


class AchievementsCommand:
    """查看成就命令"""

    def __init__(self, user_manager, logger: PluginLogger):
        self.user_manager = user_manager

    async def handle(self, event: AstrMessageEvent) -> None:
        """处理查看成就命令"""
        if not event.session_id:
            event.set_result(MessageEventResult().message("无法获取用户ID"))
            return

        user_id = event.get_sender_id()
        platform = event.get_platform_id()

        self.logger.debug(f"[{self.logger}] 用户 {user_id}@{platform} 查看成就列表")

        user = await self.user_manager.get_user_data(user_id, platform)

        result = "🏆 成就系统 🏆\n"

        if not user["achievements"]:
            result += "你还没有解锁任何成就，继续努力吧！\n\n"
        else:
            result += "🎖️ 已解锁成就 🎖️\n"
            for ach_id in user["achievements"]:
                achievement = next((a for a in ACHIEVEMENTS if a["id"] == ach_id), None)
                if achievement:
                    result += (
                        f"✅ {achievement['name']}: {achievement['description']}\n"
                    )
            result += "\n"

        result += "🔒 未解锁成就 🔒\n"
        for achievement in ACHIEVEMENTS:
            if achievement["id"] not in user["achievements"]:
                result += f"❌ {achievement['name']}: {achievement['description']}\n"

        event.set_result(MessageEventResult().message(result))
