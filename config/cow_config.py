# 牛牛系统配置

# 牛牛等级配置
COW_LEVELS = [
    {"level": 1, "name": "小牛犊", "exp_needed": 0, "favor_needed": 0},
    {"level": 2, "name": "成长牛", "exp_needed": 100, "favor_needed": 50},
    {"level": 3, "name": "健壮牛", "exp_needed": 300, "favor_needed": 150},
    {"level": 4, "name": "成年牛", "exp_needed": 600, "favor_needed": 300},
    {"level": 5, "name": "精英牛", "exp_needed": 1000, "favor_needed": 500},
    {"level": 6, "name": "传说牛", "exp_needed": 1500, "favor_needed": 800},
    {"level": 7, "name": "神牛", "exp_needed": 2500, "favor_needed": 1200},
    {"level": 8, "name": "牛魔王", "exp_needed": 4000, "favor_needed": 1800},
]

# 牛牛默认状态
DEFAULT_COW = {
    "name": "",
    "level": 1,
    "exp": 0,
    "favor": 0,
    "health": 100,
    "mood": 100,
    "hunger": 100,
    "last_feed_time": 0,
    "last_play_time": 0,
    "created_at": 0,
}

# 互动配置
COW_INTERACTIONS = {
    "feed": {"hunger_restore": 30, "favor_gain": 5, "exp_gain": 10, "points_cost": 10},
    "play": {"mood_restore": 30, "favor_gain": 8, "exp_gain": 15, "points_cost": 5},
    "pet": {"favor_gain": 3, "exp_gain": 5, "points_cost": 0},
}

# 牛牛昵称库
COW_NICKNAMES = [
    "小奶牛",
    "花花",
    "黑白",
    "斑点",
    "哞哞",
    "大壮",
    "小乖",
    "妞妞",
    "阿牛",
    "牛牛",
    "毛毛",
    "可可",
]