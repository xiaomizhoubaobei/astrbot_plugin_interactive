"""
幸运转盘配置
"""

# 转盘基础配置
SPIN_CONFIG = {
    "daily_free": 1,  # 每日免费次数
    "paid_limit": 3,  # 付费次数上限
    "cost": 20,  # 每次付费价格（积分）
    "cooldown_seconds": 3,  # 转动冷却时间（秒）
}

# 转盘奖励配置
# probability: 概率（0-1）
# rewards: 奖励内容
SPIN_REWARDS = [
    {
        "tier": 1,
        "name": "🏆 特等奖",
        "probability": 0.005,  # 0.5%
        "rewards": {
            "points": 500,
            "items": [
                {
                    "id": "title_lucky",
                    "name": "🍀 天选之人",
                    "description": "幸运转盘特等奖获得者专属称号",
                }
            ],
        },
        "message": "🎉🎉🎉 天选之人！你获得了特等奖！",
    },
    {
        "tier": 2,
        "name": "🥇 一等奖",
        "probability": 0.02,  # 2%
        "rewards": {
            "points": 200,
            "items": [
                {
                    "id": "exp_card",
                    "name": "📚 经验卡",
                    "description": "使用后获得额外20%经验加成",
                }
            ],
        },
        "message": "🎊 太棒了！你获得了一等奖！",
    },
    {
        "tier": 3,
        "name": "🥈 二等奖",
        "probability": 0.075,  # 7.5%
        "rewards": {
            "points": 100,
            "items": [
                {
                    "id": "lottery_ticket",
                    "name": "🎫 抽奖券",
                    "description": "可用于免费抽奖一次",
                }
            ],
        },
        "message": "✨ 恭喜！你获得了二等奖！",
    },
    {
        "tier": 4,
        "name": "🥉 三等奖",
        "probability": 0.20,  # 20%
        "rewards": {"points": 50, "items": []},
        "message": "🎈 不错哦！你获得了三等奖！",
    },
    {
        "tier": 5,
        "name": "🏅 四等奖",
        "probability": 0.30,  # 30%
        "rewards": {
            "points": 20,
            "items": [
                {
                    "id": "fish_bait",
                    "name": "🐟 小鱼干",
                    "description": "钓鱼时恢复20点体力",
                }
            ],
        },
        "message": "🎁 运气不错！你获得了四等奖！",
    },
    {
        "tier": 6,
        "name": "🎀 参与奖",
        "probability": 0.40,  # 40%
        "rewards": {
            "points": 10,
            "items": [
                {
                    "id": "comfort_cookie",
                    "name": "🍪 安慰饼干",
                    "description": "甜甜的小饼干，吃了心情会变好",
                }
            ],
        },
        "message": "💝 谢谢参与！送你一份小小心意~",
    },
]


# 验证概率总和为1
def validate_spin_config():
    """验证转盘配置是否正确"""
    total_prob = sum(r["probability"] for r in SPIN_REWARDS)
    if abs(total_prob - 1.0) > 0.0001:
        raise ValueError(f"转盘概率总和必须为1，当前为: {total_prob}")
    return True


# 运行验证
validate_spin_config()

__all__ = ["SPIN_CONFIG", "SPIN_REWARDS", "validate_spin_config"]
