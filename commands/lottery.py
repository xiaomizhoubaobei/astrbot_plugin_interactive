import random
from astrbot.api.event import AstrMessageEvent, MessageEventResult
from astrbot.api import logger
from ..config import LOTTERY_ITEMS


class LotteryCommand:
    """抽奖命令"""

    def __init__(self, star_instance, user_manager, achievement_manager):
        self.star = star_instance
        self.user_manager = user_manager
        self.achievement_manager = achievement_manager
        self.plugin_name = "astrbot_plugin_interactive"

    async def handle(self, event: AstrMessageEvent) -> None:
        """处理抽奖命令"""
        if not event.session_id:
            event.set_result(MessageEventResult().message("无法获取用户ID"))
            return

        user_id = event.get_sender_id()
        platform = event.get_platform_id()

        logger.info(f"[{self.plugin_name}] 用户 {user_id}@{platform} 开始抽奖")

        if not await self.user_manager.check_command_limits(user_id, platform, event):
            return

        user = await self.user_manager.get_user_data(user_id, platform)

        # 检查免费抽奖券
        use_free_ticket = False
        if user["free_lottery_count"] > 0:
            user["free_lottery_count"] -= 1
            use_free_ticket = True
            logger.debug(f"[{self.plugin_name}] 用户 {user_id}@{platform} 使用免费抽奖券")
        else:
            if user["points"] < 10:
                logger.debug(f"[{self.plugin_name}] 用户 {user_id}@{platform} 积分不足抽奖")
                event.set_result(
                    MessageEventResult().message(
                        f"积分不足！抽奖需要10积分，你当前只有 {user['points']} 积分"
                    )
                )
                return
            user["points"] -= 10
            user["total_spent"] += 10

        # 抽奖动画
        await self.star.context.send_message(event, "抽奖中...")

        # 按概率抽奖
        # 基础概率：SSR 5%, SR 10%, R 25%, N 60%
        ssr_threshold = 0.05
        sr_threshold = 0.15
        r_threshold = 0.4
        
        # 幸运护符效果：增加高级奖品概率 20%
        charm_effect = ""
        if user["lucky_charm_count"] > 0:
            ssr_threshold *= 1.2  # SSR: 5% -> 6%
            sr_threshold *= 1.2   # SR: 10% -> 12%
            r_threshold *= 1.2    # R: 25% -> 30%
            user["lucky_charm_count"] -= 1
            charm_effect = "（幸运护符生效）"
            logger.debug(f"[{self.plugin_name}] 用户 {user_id}@{platform} 幸运护符生效，概率提升 20%")
            await self.user_manager.update_user_data(user_id, platform, user)
        
        rand = random.random()

        if rand < ssr_threshold:
            index = 0  # SSR
        elif rand < sr_threshold:
            index = 1  # SR
        elif rand < r_threshold:
            index = 2  # R
        else:
            index = 3  # N

        prize = LOTTERY_ITEMS[index]
        result = f"🎰 抽奖结果：{prize}！{charm_effect}"

        logger.info(f"[{self.plugin_name}] 用户 {user_id}@{platform} 抽奖结果: {prize} (rand={rand:.3f})")

        # 特殊奖励处理
        if index == 0:
            user["points"] += 100
            user["ssr_count"] += 1
            result += " ✨ 额外获得 100 积分！"
            logger.info(f"[{self.plugin_name}] 用户 {user_id}@{platform} 抽中SSR！累计 {user['ssr_count']} 次")
        elif index == 1:
            user["points"] += 30
            result += " ✨ 额外获得 30 积分！"
        elif index == 2:
            user["points"] += 10
            result += " ✨ 额外获得 10 积分！"

        result += f"\n当前积分：{user['points']}"

        if use_free_ticket:
            result = f"(使用免费券) {result}"

        await self.user_manager.update_user_data(user_id, platform, user)

        await self.achievement_manager.check(user_id, platform, user, event)

        event.set_result(MessageEventResult().message(result))