"""
幸运转盘命令
提供幸运转盘抽奖功能
"""

from astrbot.api.event import AstrMessageEvent, MessageEventResult
from ..utils.logger_manager import PluginLogger, UserActionLogger
import random


class SpinCommand:
    """幸运转盘命令"""

    def __init__(self, star_instance, user_manager, achievement_manager, logger: PluginLogger):
        self.star = star_instance
        self.user_manager = user_manager
        self.achievement_manager = achievement_manager
        self.logger = logger
        self.action_logger = UserActionLogger(logger)
        self.plugin_name = "astrbot_plugin_interactive"

        # 幸运转盘配置
        self.prizes = [
            {"name": "特等奖", "probability": 0.01, "points": 500, "description": "500积分大奖"},
            {"name": "一等奖", "probability": 0.05, "points": 200, "description": "200积分"},
            {"name": "二等奖", "probability": 0.10, "points": 100, "description": "100积分"},
            {"name": "三等奖", "probability": 0.15, "points": 50, "description": "50积分"},
            {"name": "四等奖", "probability": 0.20, "points": 20, "description": "20积分"},
            {"name": "五等奖", "probability": 0.25, "points": 10, "description": "10积分"},
            {"name": "谢谢参与", "probability": 0.24, "points": 0, "description": "下次好运"},
        ]

        # 转盘消耗
        self.spin_cost = 50

    async def handle(self, event: AstrMessageEvent, message: str = "") -> None:
        """处理幸运转盘命令"""
        if not event.session_id:
            event.set_result(MessageEventResult().message("无法获取用户ID"))
            return

        user_id = event.get_sender_id()
        platform = event.get_platform_id()
        msg = message.strip().lower()

        self.logger.debug(f"[{self.plugin_name}] 用户 {user_id}@{platform} 尝试幸运转盘: {msg}")

        # 处理子命令
        if msg == "info":
            event.set_result(MessageEventResult().message(self.get_prizes_info()))
            return
        elif msg == "help":
            help_text = (
                "🎰 幸运转盘帮助 🎰\n\n"
                "可用命令：\n"
                "• spin - 免费转动一次（每日免费）\n"
                "• spin pay - 付费转动（50积分）\n"
                "• spin info - 查看奖品详情\n"
                "• spin help - 显示此帮助"
            )
            event.set_result(MessageEventResult().message(help_text))
            return
        elif msg == "pay":
            cost = self.spin_cost
        else:
            # 默认使用免费次数
            user = await self.user_manager.get_user_data(user_id, platform)
            
            # 检查是否有免费次数
            free_spins = user.get("free_spin_count", 0)
            if free_spins > 0 and msg != "pay":
                cost = 0
                user["free_spin_count"] = free_spins - 1
                await self.user_manager.update_user_data(user_id, platform, user)
            else:
                cost = self.spin_cost

        # 检查用户积分
        user = await self.user_manager.get_user_data(user_id, platform)
        if user["points"] < cost:
            self.logger.debug(f"[{self.plugin_name}] 用户 {user_id}@{platform} 积分不足")
            event.set_result(
                MessageEventResult().message(
                    f"💰 积分不足！幸运转盘需要 {cost} 积分，你当前只有 {user['points']} 积分"
                )
            )
            return

        # 扣除积分
        user["points"] -= cost
        user["total_spent"] += cost
        await self.user_manager.update_user_data(user_id, platform, user)

        # 发送转盘动画
        await self.star.context.send_message(event, "🎰 幸运转盘启动中...")

        # 随机抽奖
        prize = self._spin_wheel()

        # 记录抽奖结果
        self.action_logger.log_lottery(user_id, platform, prize["name"])

        # 发放奖励
        if prize["points"] > 0:
            user["points"] += prize["points"]
            await self.user_manager.update_user_data(user_id, platform, user)

        # 检查成就
        await self.achievement_manager.check(user_id, platform, user, event)

        # 返回结果
        if prize["points"] > 0:
            result_msg = (
                f"🎉 恭喜！你抽中了 {prize['name']}！\n"
                f"🎁 {prize['description']}\n"
                f"💰 当前积分：{user['points']}"
            )
        else:
            result_msg = (
                f"😢 很遗憾，{prize['name']}！\n"
                f"💸 消耗 {cost} 积分\n"
                f"💰 当前积分：{user['points']}\n"
                f"💡 下次好运！"
            )

        event.set_result(MessageEventResult().message(result_msg))

    def _spin_wheel(self) -> dict:
        """执行转盘抽奖"""
        rand = random.random()
        cumulative_prob = 0

        for prize in self.prizes:
            cumulative_prob += prize["probability"]
            if rand < cumulative_prob:
                return prize

        # 如果概率计算有误，返回最低奖励
        return self.prizes[-1]

    def get_prizes_info(self) -> str:
        """获取奖品信息"""
        info = "🎰 幸运转盘奖品 🎰\n\n"
        for prize in reversed(self.prizes):
            emoji = "🌟" if prize["points"] > 0 else "💔"
            prob_percent = int(prize["probability"] * 100)
            info += f"{emoji} {prize['name']}: {prize['description']} ({prob_percent}%)\n"
        info += f"\n💰 消耗：{self.spin_cost} 积分/次"
        return info