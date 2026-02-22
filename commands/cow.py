import random
from datetime import datetime
from typing import Any
from astrbot.api.event import AstrMessageEvent, MessageEventResult

from ..utils.logger_manager import PluginLogger, UserActionLogger




from ..config import COW_LEVELS, DEFAULT_COW, COW_INTERACTIONS, COW_NICKNAMES


class CowCommand:
    """牛牛系统命令"""

    def __init__(self, star_instance, user_manager, logger: PluginLogger):
        self.logger = logger
        self.plugin_name = "astrbot_plugin_interactive"
        self.action_logger = UserActionLogger(logger)
        self.star = star_instance
        self.user_manager = user_manager

    async def handle(self, event: AstrMessageEvent, action: str = "", nickname: str = "") -> None:
        """处理牛牛命令"""
        if not event.session_id:
            event.set_result(MessageEventResult().message("无法获取用户 ID"))
            return

        user_id = event.get_sender_id()
        platform = event.get_platform_id()

        if not action:
            await self._show_cow_info(event, user_id, platform)
        elif action == "adopt":
            await self._adopt_cow(event, user_id, platform, nickname)
        elif action == "feed":
            await self._feed_cow(event, user_id, platform)
        elif action == "play":
            await self._play_with_cow(event, user_id, platform)
        elif action == "pet":
            await self._pet_cow(event, user_id, platform)
        elif action == "rename":
            await self._rename_cow(event, user_id, platform, nickname)
        else:
            event.set_result(MessageEventResult().message(
                '❌ 无效操作！请输入 "cow" 查看帮助\n'
                '可用操作: adopt(领养), feed(喂食), play(玩耍), pet(抚摸), rename(改名)'
            ))

    async def _show_cow_info(self, event: AstrMessageEvent, user_id: str, platform: str) -> None:
        """显示牛牛信息"""
        user = await self.user_manager.get_user_data(user_id, platform)
        
        if not user.get("cow"):
            event.set_result(MessageEventResult().message(
                "🐄 你还没有领养牛牛哦！\n"
                '输入 "cow adopt <昵称>" 领养一只属于你的牛牛吧！'
            ))
            return

        cow = user["cow"]
        level_info = self._get_level_info(cow["level"])
        
        # 计算升级进度
        next_level = self._get_next_level(cow["level"])
        if next_level:
            exp_progress = f"{cow['exp']}/{next_level['exp_needed']}"
            favor_progress = f"{cow['favor']}/{next_level['favor_needed']}"
        else:
            exp_progress = "已满级"
            favor_progress = "已满级"

        # 状态条
        health_bar = self._get_status_bar(cow["health"])
        mood_bar = self._get_status_bar(cow["mood"])
        hunger_bar = self._get_status_bar(cow["hunger"])

        result = (
            f"🐄 {cow['name']} 的信息 🐄\n"
            f"等级: Lv.{cow['level']} {level_info['name']}\n"
            f"经验: {exp_progress}\n"
            f"好感度: {favor_progress}\n\n"
            f"状态:\n"
            f"  ❤️ 健康: {health_bar} {cow['health']}%\n"
            f"  😊 心情: {mood_bar} {cow['mood']}%\n"
            f"  🍽️ 饱食: {hunger_bar} {cow['hunger']}%\n\n"
            f"📝 指令:\n"
            f"  cow feed (10 积分) - 喂食牛牛\n"
            f"  cow play (5 积分) - 和牛牛玩耍\n"
            f"  cow pet (免费) - 抚摸牛牛\n"
            f"  cow rename <昵称> - 给牛牛改名"
        )
        
        event.set_result(MessageEventResult().message(result))

    async def _adopt_cow(self, event: AstrMessageEvent, user_id: str, platform: str, nickname: str) -> None:
        """领养牛牛"""
        user = await self.user_manager.get_user_data(user_id, platform)
        
        if user.get("cow"):
            event.set_result(MessageEventResult().message(f"❌ 你已经领养了牛牛 {user['cow']['name']}，不能再领养了！"))
            return

        if not nickname:
            event.set_result(MessageEventResult().message('❌ 请输入牛牛的昵称！格式: cow adopt <昵称>'))
            return

        # 创建新牛牛
        cow = DEFAULT_COW.copy()
        cow["name"] = nickname
        cow["created_at"] = int(datetime.now().timestamp() * 1000)
        
        user["cow"] = cow
        await self.user_manager.update_user_data(user_id, platform, user)

        self.logger.info(f"[{self.logger}] 用户 {user_id}@{platform} 领养了牛牛: {nickname}")

        event.set_result(MessageEventResult().message(
            f"🎉 恭喜！你成功领养了牛牛「{nickname}」！\n"
            f"好好照顾它吧，输入 'cow' 查看它的状态~"
        ))

    async def _feed_cow(self, event: AstrMessageEvent, user_id: str, platform: str) -> None:
        """喂食牛牛"""
        user = await self.user_manager.get_user_data(user_id, platform)
        
        if not user.get("cow"):
            event.set_result(MessageEventResult().message("❌ 你还没有领养牛牛！"))
            return

        cow = user["cow"]
        config = COW_INTERACTIONS["feed"]

        # 检查积分
        if user["points"] < config["points_cost"]:
            event.set_result(MessageEventResult().message(
                f"❌ 积分不足！喂食需要 {config['points_cost']} 积分"
            ))
            return

        # 检查是否太饱了
        if cow["hunger"] >= 100:
            event.set_result(MessageEventResult().message(f"💕 {cow['name']} 已经吃饱啦，吃不下更多了！"))
            return

        # 执行喂食
        user["points"] -= config["points_cost"]
        user["total_spent"] += config["points_cost"]
        
        cow["hunger"] = min(100, cow["hunger"] + config["hunger_restore"])
        cow["favor"] += config["favor_gain"]
        cow["exp"] += config["exp_gain"]
        cow["last_feed_time"] = int(datetime.now().timestamp() * 1000)

        # 检查升级
        leveled_up = self._check_level_up(cow)
        
        await self.user_manager.update_user_data(user_id, platform, user)

        result = f"🍽️ 你喂了 {cow['name']} 一顿美味的食物！\n"
        result += f"饱食度 +{config['hunger_restore']} | 好感度 +{config['favor_gain']} | 经验 +{config['exp_gain']}"
        
        if leveled_up:
            level_info = self._get_level_info(cow["level"])
            result += f"\n🎉 升级啦！{cow['name']} 升到了 Lv.{cow['level']} {level_info['name']}！"

        event.set_result(MessageEventResult().message(result))

    async def _play_with_cow(self, event: AstrMessageEvent, user_id: str, platform: str) -> None:
        """和牛牛玩耍"""
        user = await self.user_manager.get_user_data(user_id, platform)
        
        if not user.get("cow"):
            event.set_result(MessageEventResult().message("❌ 你还没有领养牛牛！"))
            return

        cow = user["cow"]
        config = COW_INTERACTIONS["play"]

        # 检查积分
        if user["points"] < config["points_cost"]:
            event.set_result(MessageEventResult().message(
                f"❌ 积分不足！玩耍需要 {config['points_cost']} 积分"
            ))
            return

        # 检查心情
        if cow["mood"] >= 100:
            event.set_result(MessageEventResult().message(f"💕 {cow['name']} 心情很好，暂时不想玩~"))
            return

        # 执行玩耍
        user["points"] -= config["points_cost"]
        user["total_spent"] += config["points_cost"]
        
        cow["mood"] = min(100, cow["mood"] + config["mood_restore"])
        cow["favor"] += config["favor_gain"]
        cow["exp"] += config["exp_gain"]
        cow["last_play_time"] = int(datetime.now().timestamp() * 1000)

        # 检查升级
        leveled_up = self._check_level_up(cow)
        
        await self.user_manager.update_user_data(user_id, platform, user)

        result = f"🎮 你和 {cow['name']} 玩得很开心！\n"
        result += f"心情 +{config['mood_restore']} | 好感度 +{config['favor_gain']} | 经验 +{config['exp_gain']}"
        
        if leveled_up:
            level_info = self._get_level_info(cow["level"])
            result += f"\n🎉 升级啦！{cow['name']} 升到了 Lv.{cow['level']} {level_info['name']}！"

        event.set_result(MessageEventResult().message(result))

    async def _pet_cow(self, event: AstrMessageEvent, user_id: str, platform: str) -> None:
        """抚摸牛牛"""
        user = await self.user_manager.get_user_data(user_id, platform)
        
        if not user.get("cow"):
            event.set_result(MessageEventResult().message("❌ 你还没有领养牛牛！"))
            return

        cow = user["cow"]
        config = COW_INTERACTIONS["pet"]

        # 执行抚摸
        cow["favor"] += config["favor_gain"]
        cow["exp"] += config["exp_gain"]

        # 检查升级
        leveled_up = self._check_level_up(cow)
        
        await self.user_manager.update_user_data(user_id, platform, user)

        # 随机回应
        responses = [
            f"💕 {cow['name']} 享受地蹭了蹭你的手~",
            f"😊 {cow['name']} 很喜欢你的抚摸~",
            f"🥰 {cow['name']} 开心地叫了一声~",
            f"🤗 {cow['name']} 温顺地靠在你身边~",
        ]
        
        result = random.choice(responses)
        result += f"\n好感度 +{config['favor_gain']} | 经验 +{config['exp_gain']}"
        
        if leveled_up:
            level_info = self._get_level_info(cow["level"])
            result += f"\n🎉 升级啦！{cow['name']} 升到了 Lv.{cow['level']} {level_info['name']}！"

        event.set_result(MessageEventResult().message(result))

    async def _rename_cow(self, event: AstrMessageEvent, user_id: str, platform: str, new_name: str) -> None:
        """给牛牛改名"""
        user = await self.user_manager.get_user_data(user_id, platform)
        
        if not user.get("cow"):
            event.set_result(MessageEventResult().message("❌ 你还没有领养牛牛！"))
            return

        if not new_name:
            event.set_result(MessageEventResult().message('❌ 请输入新的昵称！格式: cow rename <新昵称>'))
            return

        old_name = user["cow"]["name"]
        user["cow"]["name"] = new_name
        await self.user_manager.update_user_data(user_id, platform, user)

        event.set_result(MessageEventResult().message(
            f"✅ 你的牛牛已经改名为「{new_name}」啦！(原名: {old_name})"
        ))

    def _get_level_info(self, level: int) -> dict:
        """获取等级信息"""
        for level_config in COW_LEVELS:
            if level_config["level"] == level:
                return level_config
        return COW_LEVELS[-1]

    def _get_next_level(self, current_level: int) -> dict | None:
        """获取下一等级信息"""
        for level_config in COW_LEVELS:
            if level_config["level"] == current_level + 1:
                return level_config
        return None

    def _check_level_up(self, cow: dict) -> bool:
        """检查是否升级"""
        next_level = self._get_next_level(cow["level"])
        if not next_level:
            return False

        if cow["exp"] >= next_level["exp_needed"] and cow["favor"] >= next_level["favor_needed"]:
            cow["level"] += 1
            self.logger.debug(f"[{self.logger}] 牛牛升级到 Lv.{cow['level']}")
            return True
        return False

    def _get_status_bar(self, value: int) -> str:
        """获取状态条"""
        filled = value // 10
        bar = "█" * filled + "░" * (10 - filled)
        return f"[{bar}]"
