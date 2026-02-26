from astrbot.api.event import AstrMessageEvent, MessageEventResult

from ..utils.logger_manager import PluginLogger, UserActionLogger


class HelpCommand:
    """帮助命令"""

    async def handle(self, event: AstrMessageEvent) -> None:
        """处理帮助命令"""
        help_text = (
            "🎮 互动功能菜单 🎮\n\n"
            "1. 🎲 猜数字游戏\n"
            "   - 输入 'guess start' 开始游戏\n"
            "   - 游戏中输入数字进行猜测\n"
            "   - 输入 'hint' 使用提示令牌\n"
            "   - 输入 'giveup' 放弃游戏\n\n"
            "2. 📅 每日签到\n"
            "   - 输入 'sign' 领取积分\n"
            "   - 连续签到有额外奖励\n\n"
            "3. 🎰 幸运抽奖\n"
            "   - 输入 'lottery' 消耗10积分抽奖\n"
            "   - 有几率获得稀有奖励\n\n"
            "4. 🎯 幸运转盘 🆕\n"
            "   - 输入 'spin' 免费转动（每日免费）\n"
            "   - 输入 'spin pay' 付费转动（50积分）\n"
            "   - 输入 'spin info' 查看奖品详情\n"
            "   - 输入 'spin help' 显示帮助\n\n"
            "5. 🛒 积分商店\n"
            "   - 输入 'shop list' 查看商品\n"
            "   - 输入 'shop buy <商品ID>' 购买\n\n"
            "6. 🎒 使用物品\n"
            "   - 输入 'use <物品ID>' 使用物品\n"
            "   - 输入 'inventory' 查看物品栏\n\n"
            "7. 🐄 牛牛系统\n"
            "   - 输入 'cow adopt <昵称>' 领养牛牛\n"
            "   - 输入 'cow feed' 喂食 (10 积分)\n"
            "   - 输入 'cow play' 玩耍 (5 积分)\n"
            "   - 输入 'cow pet' 抚摸 (免费)\n"
            "   - 输入 'cow rename <昵称>' 改名\n"
            "   - 输入 'cow' 查看牛牛状态\n\n"
            "8. 🏆 成就系统\n"
            "   - 输入 'achievements' 查看成就\n"
            "   - 完成条件解锁奖励\n\n"
            "9. 👤 个人资料\n"
            "   - 输入 'profile' 查看数据\n"
            "   - 查看积分、成就等信息\n\n"
            "💡 提示: 每天都有新的挑战和奖励，快来体验吧！"
        )
        event.set_result(MessageEventResult().message(help_text))
