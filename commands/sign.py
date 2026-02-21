from datetime import datetime, timedelta
from astrbot.api.event import AstrMessageEvent, MessageEventResult


class SignCommand:
    """签到命令"""

    def __init__(self, star_instance, user_manager, achievement_manager):
        self.star = star_instance
        self.user_manager = user_manager
        self.achievement_manager = achievement_manager

    async def handle(self, event: AstrMessageEvent) -> None:
        """处理签到命令"""
        if not event.session_id:
            event.set_result(MessageEventResult().message("无法获取用户ID"))
            return

        user_id = event.get_sender_id()
        platform = event.get_platform_id()

        if not await self.user_manager.check_command_limits(user_id, platform, event):
            return

        user = await self.user_manager.get_user_data(user_id, platform)
        today = self._get_today()

        if user["last_sign"] == today:
            event.set_result(MessageEventResult().message("你今天已经签到过了哦，明天再来吧！"))
            return

        # 计算连续签到
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_str = f"{yesterday.year}-{yesterday.month}-{yesterday.day}"

        if user["last_sign"] == yesterday_str:
            user["consecutive_days"] += 1
        else:
            user["consecutive_days"] = 1

        user["total_sign_days"] += 1

        # 计算奖励
        base_reward = 10
        bonus = min(100, user["consecutive_days"] * 2)

        # 双倍卡效果
        double_effect = ""
        if user["has_double_card"]:
            base_reward *= 2
            user["has_double_card"] = False
            double_effect = "（双倍卡生效）"

        total = base_reward + bonus

        user["points"] += total
        user["last_sign"] = today

        await self.user_manager.update_user_data(user_id, platform, user)

        await self.achievement_manager.check(user_id, platform, user, event)

        # 特殊签到奖励
        special_bonus = ""
        if user["consecutive_days"] % 7 == 0:
            week_bonus = 50
            user["points"] += week_bonus
            special_bonus = f"\n✨ 连续签到满 {user['consecutive_days']} 天，额外奖励 {week_bonus} 积分！"
            await self.user_manager.update_user_data(user_id, platform, user)

        event.set_result(
            MessageEventResult().message(
                f"✅ 签到成功！🎉\n"
                f"连续签到：{user['consecutive_days']} 天 (总签到: {user['total_sign_days']} 天)\n"
                f"获得积分：{base_reward}{double_effect} + {bonus} = {total} 积分{special_bonus}\n"
                f"当前积分：{user['points']}"
            )
        )

    def _get_today(self) -> str:
        """获取今天的日期字符串"""
        now = datetime.now()
        return f"{now.year}-{now.month}-{now.day}"
