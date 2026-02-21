from astrbot.api.event import AstrMessageEvent, MessageEventResult
from astrbot.api import logger


class GuessCommand:
    """猜数字游戏命令"""

    def __init__(self, star_instance, user_manager, game_manager, achievement_manager):
        self.star = star_instance
        self.user_manager = user_manager
        self.game_manager = game_manager
        self.achievement_manager = achievement_manager
        self.plugin_name = "astrbot_plugin_interactive"

    async def handle(self, event: AstrMessageEvent, message: str = "") -> None:
        """处理猜数字命令"""
        if not event.session_id:
            event.set_result(MessageEventResult().message("无法获取用户ID"))
            return

        user_id = event.get_sender_id()
        platform = event.get_platform_id()

        if not message:
            event.set_result(MessageEventResult().message('输入 "guess start" 开始猜数字游戏！'))
            return

        game_key = f"{platform}:{user_id}"

        if message == "start":
            await self._start_game(event, user_id, platform)
        elif message == "hint":
            await self._use_hint(event, user_id, platform, game_key)
        elif message == "giveup":
            await self._give_up(event, user_id, platform, game_key)
        else:
            await self._make_guess(event, user_id, platform, game_key, message)

    async def _start_game(self, event: AstrMessageEvent, user_id: str, platform: str) -> None:
        """开始游戏"""
        logger.info(f"[{self.plugin_name}] 用户 {user_id}@{platform} 开始猜数字游戏")
        if not await self.user_manager.check_command_limits(user_id, platform, event):
            return

        user = await self.user_manager.get_user_data(user_id, platform)
        user["games_played"] += 1
        await self.user_manager.update_user_data(user_id, platform, user)

        game = self.game_manager.create_guess_game(f"{platform}:{user_id}", 100)

        event.set_result(
            MessageEventResult().message(
                f"🎮 游戏开始！我已经想好了一个 1~100 之间的数字，猜猜看是多少？\n"
                f"提示：输入 'hint' 可以使用提示令牌（当前持有: {user['hint_tokens']} 枚）"
            )
        )

    async def _use_hint(self, event: AstrMessageEvent, user_id: str, platform: str, game_key: str) -> None:
        """使用提示"""
        game = self.game_manager.get_game(game_key)
        if not game:
            event.set_result(MessageEventResult().message("你还没有开始游戏！"))
            return

        user = await self.user_manager.get_user_data(user_id, platform)
        if user["hint_tokens"] <= 0:
            logger.debug(f"[{self.plugin_name}] 用户 {user_id}@{platform} 提示令牌不足")
            event.set_result(MessageEventResult().message("你没有提示令牌了！去商店购买吧~"))
            return

        user["hint_tokens"] -= 1
        await self.user_manager.update_user_data(user_id, platform, user)

        lower, upper = self.game_manager.get_hint_range(game)

        event.set_result(
            MessageEventResult().message(
                f"🔍 提示：数字在 {lower} ~ {upper} 之间（当前持有: {user['hint_tokens']} 枚）"
            )
        )

    async def _give_up(self, event: AstrMessageEvent, user_id: str, platform: str, game_key: str) -> None:
        """放弃游戏"""
        game = self.game_manager.get_game(game_key)
        if not game:
            event.set_result(MessageEventResult().message("你还没有开始游戏！"))
            return

        logger.info(f"[{self.plugin_name}] 用户 {user_id}@{platform} 放弃游戏，答案: {game['target_number']}")
        self.game_manager.delete_game(game_key)

        event.set_result(
            MessageEventResult().message(
                f"😢 你放弃了游戏！正确答案是 {game['target_number']}，下次加油哦！"
            )
        )

    async def _make_guess(self, event: AstrMessageEvent, user_id: str, platform: str, game_key: str, message: str) -> None:
        """进行猜测"""
        game = self.game_manager.get_game(game_key)
        if not game:
            event.set_result(MessageEventResult().message("你还没有开始游戏，输入 'guess start' 开始吧！"))
            return

        try:
            guess = int(message)
        except ValueError:
            logger.debug(f"[{self.plugin_name}] 用户 {user_id}@{platform} 输入无效数字: {message}")
            event.set_result(MessageEventResult().message("请输入有效的数字！"))
            return

        if guess < 1 or guess > 100:
            logger.debug(f"[{self.plugin_name}] 用户 {user_id}@{platform} 输入超出范围: {guess}")
            event.set_result(MessageEventResult().message("请输入 1~100 之间的数字！"))
            return

        self.game_manager.update_game_attempts(game_key)

        if guess == game["target_number"]:
            await self._game_won(event, user_id, platform, game_key, game)
        else:
            await self._guess_feedback(event, game_key, game, guess)

    async def _game_won(self, event: AstrMessageEvent, user_id: str, platform: str, game_key: str, game: dict) -> None:
        """游戏胜利"""
        from ..config import LOTTERY_ITEMS
        from datetime import datetime

        base_points, time_bonus = self.game_manager.calculate_game_score(game)

        # 检查经验卡加成
        user = await self.user_manager.get_user_data(user_id, platform)
        exp_card_bonus = 0
        exp_card_msg = ""
        for item in user["inventory"]:
            if item["id"] == "exp_card" and item["count"] > 0:
                exp_card_bonus = int((base_points + time_bonus) * 0.2)
                exp_card_msg = f"（经验卡加成 +{exp_card_bonus}）"
                logger.info(f"[{self.plugin_name}] 用户 {user_id}@{platform} 使用经验卡，获得额外 {exp_card_bonus} 积分")
                break

        total_points = base_points + time_bonus + exp_card_bonus

        user["points"] += total_points
        user["games_won"] += 1
        await self.user_manager.update_user_data(user_id, platform, user)

        await self.achievement_manager.check(user_id, platform, user, event)

        self.game_manager.delete_game(game_key)

        logger.info(f"[{self.plugin_name}] 用户 {user_id}@{platform} 赢得游戏！总积分: {total_points}")

        if game["attempts"] <= 3:
            comment = "🎯 太厉害了！你是天才吗？"
        elif game["attempts"] <= 7:
            comment = "👍 很棒的表现！"
        else:
            comment = "💪 再接再厉！"

        event.set_result(
            MessageEventResult().message(
                f"{comment}\n🎉 恭喜你猜对了！答案就是 {game['target_number']}！\n"
                f"尝试次数: {game['attempts']} ({base_points}分) | "
                f"用时: {(int(datetime.now().timestamp() * 1000) - game['start_time']) // 1000}秒 ({time_bonus}分){exp_card_msg}\n"
                f"总计获得 {total_points} 积分！"
            )
        )

    async def _guess_feedback(self, event: AstrMessageEvent, game_key: str, game: dict, guess: int) -> None:
        """猜测反馈"""
        diff = abs(guess - game["target_number"])
        if diff > 30:
            hint = "差得远呢~"
        elif diff > 10:
            hint = "接近了，但还不够~"
        else:
            hint = "非常接近了！"

        if guess < game["target_number"]:
            msg = f"⬇️ 猜小了！{hint}（已尝试 {game['attempts']} 次）"
        else:
            msg = f"⬆️ 猜大了！{hint}（已尝试 {game['attempts']} 次）"

        event.set_result(MessageEventResult().message(msg))
