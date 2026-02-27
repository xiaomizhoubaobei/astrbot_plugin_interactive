# 配置模块
from .achievements import ACHIEVEMENTS
from .shop_items import DEFAULT_SHOP_ITEMS
from .lottery_items import LOTTERY_ITEMS
from .cow_config import COW_LEVELS, DEFAULT_COW, COW_INTERACTIONS, COW_NICKNAMES
from .spin_config import SPIN_CONFIG, SPIN_REWARDS

__all__ = [
    "ACHIEVEMENTS",
    "DEFAULT_SHOP_ITEMS",
    "LOTTERY_ITEMS",
    "COW_LEVELS",
    "DEFAULT_COW",
    "COW_INTERACTIONS",
    "COW_NICKNAMES",
    "SPIN_CONFIG",
    "SPIN_REWARDS",
]