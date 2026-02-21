from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from astrbot.api import logger


class UserManager:
    """用户数据管理器"""

    def __init__(self, star_instance):
        self.star = star_instance
        self.plugin_name = "astrbot_plugin_interactive"

    def _get_user_key(self, user_id: str, platform: str) -> str:
        """生成用户数据存储的键"""
        return f"{platform}:{user_id}"

    def _get_today(self) -> str:
        """获取今天的日期字符串"""
        now = datetime.now()
        return f"{now.year}-{now.month}-{now.day}"

    async def get_user_data(self, user_id: str, platform: str) -> Dict[str, Any]:
        """获取用户数据"""
        key = self._get_user_key(user_id, platform)
        data = await self.star.get_kv_data(key, None)

        if data is None:
            # 新用户初始化
            logger.info(f"[{self.plugin_name}] 创建新用户: {user_id}@{platform}")
            data = {
                "id": user_id,
                "platform": platform,
                "points": 100,
                "last_sign": "",
                "consecutive_days": 0,
                "total_sign_days": 0,
                "games_played": 0,
                "games_won": 0,
                "achievements": [],
                "has_double_card": False,
                "free_lottery_count": 0,
                "hint_tokens": 0,
                "lucky_charm_count": 0,
                "last_command_time": 0,
                "daily_command_count": 0,
                "last_command_date": self._get_today(),
                "total_spent": 0,
                "ssr_count": 0,
                "inventory": []
            }
            await self.star.put_kv_data(key, data)

        return data

    async def update_user_data(self, user_id: str, platform: str, data: Dict[str, Any]) -> None:
        """更新用户数据"""
        key = self._get_user_key(user_id, platform)
        await self.star.put_kv_data(key, data)

    async def check_command_limits(self, user_id: str, platform: str, event) -> bool:
        """检查冷却时间和每日限制"""
        from astrbot.api.event import MessageEventResult

        user = await self.get_user_data(user_id, platform)
        now = int(datetime.now().timestamp() * 1000)
        today = self._get_today()

        # 重置每日计数器
        if user["last_command_date"] != today:
            user["daily_command_count"] = 0
            user["last_command_date"] = today

        # 检查每日限制 (默认50次)
        daily_limit = 50
        if user["daily_command_count"] >= daily_limit:
            logger.debug(f"[{self.plugin_name}] 用户 {user_id}@{platform} 今日使用次数已达上限")
            event.set_result(
                MessageEventResult().message(f"今日使用次数已达上限（{daily_limit}次），请明天再来吧！")
            )
            return False

        # 检查冷却时间 (默认5000ms)
        cool_down = 5000
        if now - user["last_command_time"] < cool_down:
            remaining = (cool_down - (now - user["last_command_time"])) // 1000 + 1
            logger.debug(f"[{self.plugin_name}] 用户 {user_id}@{platform} 操作过于频繁，需等待 {remaining} 秒")
            event.set_result(
                MessageEventResult().message(f"操作太频繁啦，请 {remaining} 秒后再试~")
            )
            return False

        # 更新计数器
        user["daily_command_count"] += 1
        user["last_command_time"] = now
        await self.update_user_data(user_id, platform, user)
        return True

    async def add_points(self, user_id: str, platform: str, points: int) -> None:
        """增加积分"""
        if points <= 0:
            logger.warning(f"[{self.plugin_name}] 尝试增加非正积分: {points}，忽略")
            return
        user = await self.get_user_data(user_id, platform)
        user["points"] += points
        await self.update_user_data(user_id, platform, user)
        logger.debug(f"[{self.plugin_name}] 用户 {user_id}@{platform} 积分 +{points}, 当前: {user['points']}")

    async def consume_points(self, user_id: str, platform: str, points: int) -> bool:
        """消耗积分"""
        if points <= 0:
            logger.warning(f"[{self.plugin_name}] 尝试消耗非正积分: {points}，忽略")
            return False
        user = await self.get_user_data(user_id, platform)
        if user["points"] < points:
            logger.debug(f"[{self.plugin_name}] 用户 {user_id}@{platform} 积分不足: 需要 {points}, 拥有 {user['points']}")
            return False
        user["points"] -= points
        # 确保积分不会变成负数
        if user["points"] < 0:
            user["points"] = 0
            logger.warning(f"[{self.plugin_name}] 用户 {user_id}@{platform} 积分修正为0")
        await self.update_user_data(user_id, platform, user)
        logger.debug(f"[{self.plugin_name}] 用户 {user_id}@{platform} 积分 -{points}, 当前: {user['points']}")
        return True

    async def add_item_to_inventory(self, user_id: str, platform: str, item: Dict[str, Any]) -> None:
        """添加物品到物品栏"""
        user = await self.get_user_data(user_id, platform)
        existing_item = next((i for i in user["inventory"] if i["id"] == item["id"]), None)

        if existing_item:
            existing_item["count"] += 1
            # 限制物品数量上限，防止溢出
            if existing_item["count"] > 999:
                existing_item["count"] = 999
                logger.warning(f"[{self.plugin_name}] 用户 {user_id}@{platform} 物品 {item['name']} 数量已达上限")
            logger.debug(f"[{self.plugin_name}] 用户 {user_id}@{platform} 物品 {item['name']} 数量 +1, 当前: {existing_item['count']}")
        else:
            user["inventory"].append({
                "id": item["id"],
                "name": item["name"],
                "description": item["description"],
                "count": 1
            })
            logger.info(f"[{self.plugin_name}] 用户 {user_id}@{platform} 获得新物品: {item['name']}")
        await self.update_user_data(user_id, platform, user)

    async def remove_item_from_inventory(self, user_id: str, platform: str, item_id: str) -> bool:
        """从物品栏移除物品"""
        user = await self.get_user_data(user_id, platform)
        for i, item in enumerate(user["inventory"]):
            if item["id"] == item_id:
                if item["count"] > 1:
                    item["count"] -= 1
                    # 确保数量不会变成负数
                    if item["count"] < 0:
                        item["count"] = 0
                        logger.warning(f"[{self.plugin_name}] 用户 {user_id}@{platform} 物品 {item['name']} 数量异常，修正为0")
                    logger.debug(f"[{self.plugin_name}] 用户 {user_id}@{platform} 物品 {item['name']} 数量 -1, 当前: {item['count']}")
                else:
                    user["inventory"].pop(i)
                    logger.debug(f"[{self.plugin_name}] 用户 {user_id}@{platform} 物品 {item['name']} 已用完")
                await self.update_user_data(user_id, platform, user)
                return True
        logger.debug(f"[{self.plugin_name}] 用户 {user_id}@{platform} 物品栏中未找到物品: {item_id}")
        return False

    async def get_inventory_item(self, user_id: str, platform: str, item_id: str) -> Optional[Dict[str, Any]]:
        """获取物品栏中的物品"""
        user = await self.get_user_data(user_id, platform)
        for item in user["inventory"]:
            if item["id"] == item_id or item["name"] == item_id:
                return item
        return None