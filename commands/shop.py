from astrbot.api.event import AstrMessageEvent, MessageEventResult

from ..utils.logger_manager import PluginLogger, UserActionLogger


from ..config import DEFAULT_SHOP_ITEMS


class ShopCommand:
    """商店命令"""

    def __init__(
        self, star_instance, user_manager, achievement_manager, logger: PluginLogger
    ):
        self.logger = logger
        self.plugin_name = "astrbot_plugin_interactive"
        self.action_logger = UserActionLogger(logger)
        self.star = star_instance
        self.user_manager = user_manager
        self.achievement_manager = achievement_manager

    async def handle(
        self, event: AstrMessageEvent, action: str = "", item_id: str = ""
    ) -> None:
        """处理商店命令"""
        if not event.session_id:
            event.set_result(MessageEventResult().message("❌ 无法获取用户ID"))
            return

        user_id = event.get_sender_id()
        platform = event.get_platform_id()

        if not action:
            event.set_result(
                MessageEventResult().message('❌ 请输入 "shop list" 查看商品列表')
            )
            return

        if action == "list":
            await self._show_shop_list(event)
        elif action == "buy":
            await self._buy_item(event, user_id, platform, item_id)
        else:
            event.set_result(
                MessageEventResult().message(
                    '❌ 无效操作，请输入 "shop list" 或 "shop buy <商品ID>"'
                )
            )

    async def _show_shop_list(self, event: AstrMessageEvent) -> None:
        """显示商店列表"""
        self.logger.debug(f"[{self.logger}] 显示商店列表")
        shop_list = "🛍️ 商店商品列表 🛍️\n"
        for item in DEFAULT_SHOP_ITEMS:
            shop_list += f"[{item['id']}] {item['name']} - {item['description']}\n"
            shop_list += f"💰 价格: {item['price']} 积分 | "
            shop_list += (
                f"类型: {'可存储物品' if item['storable'] else '立即生效道具'}\n\n"
            )
        shop_list += '💡 提示: 输入 "shop buy <商品ID>" 购买商品'
        event.set_result(MessageEventResult().message(shop_list))

    async def _buy_item(
        self, event: AstrMessageEvent, user_id: str, platform: str, item_id: str
    ) -> None:
        """购买物品"""
        if not item_id:
            event.set_result(MessageEventResult().message("❌ 请输入要购买的商品ID"))
            return

        item = next((i for i in DEFAULT_SHOP_ITEMS if i["id"] == item_id), None)
        if not item:
            self.logger.debug(
                f"[{self.logger}] 用户 {user_id}@{platform} 尝试购买不存在的商品: {item_id}"
            )
            event.set_result(
                MessageEventResult().message("❌ 找不到该商品，请检查商品ID")
            )
            return

        user = await self.user_manager.get_user_data(user_id, platform)
        if user["points"] < item["price"]:
            self.logger.debug(
                f"[{self.logger}] 用户 {user_id}@{platform} 积分不足购买 {item['name']}"
            )
            event.set_result(
                MessageEventResult().message(
                    f"❌ 积分不足！需要 {item['price']} 积分，你当前只有 {user['points']} 积分"
                )
            )
            return

        user["points"] -= item["price"]
        user["total_spent"] += item["price"]

        self.logger.info(
            f"[{self.logger}] 用户 {user_id}@{platform} 购买商品: {item['name']} ({item['price']} 积分)"
        )

        if item["storable"]:
            await self.user_manager.add_item_to_inventory(user_id, platform, item)
            effect_msg = f"🛍️ 成功购买 {item['name']}！已添加到物品栏，使用 'use {item['id']}' 来使用它"
        else:
            effect_msg = self._apply_item_effect(user, item_id)

        await self.user_manager.update_user_data(user_id, platform, user)

        await self.achievement_manager.check(user_id, platform, user, event)

        event.set_result(
            MessageEventResult().message(f"{effect_msg}\n💰 剩余积分: {user['points']}")
        )

    def _apply_item_effect(self, user: dict, item_id: str) -> str:
        """应用立即生效物品效果"""
        if item_id == "double_card":
            user["has_double_card"] = True
            self.logger.debug(f"[{self.logger}] 应用效果: 双倍积分卡")
            return "✅ 购买成功！下次签到将获得双倍积分！"
        elif item_id == "lottery_ticket":
            user["free_lottery_count"] += 1
            self.logger.debug(f"[{self.logger}] 应用效果: 免费抽奖券")
            return "✅ 购买成功！获得一张免费抽奖券！"
        elif item_id == "hint_token":
            user["hint_tokens"] += 1
            self.logger.debug(f"[{self.logger}] 应用效果: 提示令牌")
            return "✅ 购买成功！获得一枚提示令牌！"
        elif item_id == "lucky_charm":
            user["lucky_charm_count"] += 1
            self.logger.debug(f"[{self.logger}] 应用效果: 幸运护符")
            return "✅ 购买成功！获得幸运护符，下次抽奖时生效！"
        return "✅ 购买成功！"
