# 幸运转盘 - 开发文档

## 功能概述

幸运转盘是一个每日限时的抽奖游戏，用户可以通过转盘获得积分、物品或特殊奖励。该功能设计简单、反馈即时，能够有效提升用户日活跃度。

## 需求分析

### 功能需求

#### 核心功能
- 每日免费次数：1次免费旋转
- 积分消费：额外旋转消耗5积分
- 奖励池：积分、物品、特殊奖励
- 旋转动画：文字版旋转效果
- 概率配置：可调整各项奖励概率

#### 奖励类型
1. 积分奖励（10-100积分）
2. 免费物品（双倍积分卡、抽奖券等）
3. 特殊奖励（限定称号、额外次数等）
4. 空奖（保持概率平衡）

#### 游戏规则
- 每日1次免费机会
- 额外旋转消耗5积分
- 奖励即时发放
- 可连续旋转
- 奖励记录可查询

### 非功能需求
- 响应时间：<1秒
- 并发支持：支持多人同时旋转
- 概率准确：确保概率配置准确

## 技术设计

### 数据结构

```python
# 奖励项配置
{
    "id": "str",              # 奖励ID
    "name": "str",            # 奖励名称
    "type": "points|item|special|none",
    "emoji": "str",           # 显示emoji
    "probability": "float",   # 概率（0-1）
    "value": "int|dict",      # 奖励值
    "description": "str"      # 描述
}

# 用户数据扩展
{
    "wheel_free_count": "int",      # 今日免费次数
    "wheel_last_spin": "int",       # 上次旋转时间
    "wheel_total_spins": "int",     # 总旋转次数
    "wheel_history": "list"         # 旋转历史
}
```

### 奖励池配置

```yaml
wheel_rewards:
  - id: "points_100"
    name: "100积分"
    type: "points"
    emoji: "💰"
    probability: 0.05
    value: 100
    description: "获得100积分"
    
  - id: "points_50"
    name: "50积分"
    type: "points"
    emoji: "💵"
    probability: 0.10
    value: 50
    description: "获得50积分"
    
  - id: "points_20"
    name: "20积分"
    type: "points"
    emoji: "💎"
    probability: 0.20
    value: 20
    description: "获得20积分"
    
  - id: "points_10"
    name: "10积分"
    type: "points"
    emoji: "🪙"
    probability: 0.25
    value: 10
    description: "获得10积分"
    
  - id: "item_double_card"
    name: "双倍积分卡"
    type: "item"
    emoji: "🃏"
    probability: 0.08
    value: {"item_id": "double_card", "count": 1}
    description: "获得双倍积分卡x1"
    
  - id: "item_lottery_ticket"
    name: "免费抽奖券"
    type: "item"
    emoji: "🎫"
    probability: 0.08
    value: {"item_id": "lottery_ticket", "count": 1}
    description: "获得免费抽奖券x1"
    
  - id: "special_extra_spin"
    name: "额外一次"
    type: "special"
    emoji: "🎁"
    probability: 0.02
    value: {"extra_spin": 1}
    description: "获得额外一次旋转机会"
    
  - id: "none"
    name: "再接再厉"
    type: "none"
    emoji: "😅"
    probability: 0.22
    value: null
    description: "很遗憾，这次没有中奖"
```

### 模块设计

```
lucky_wheel/
├── __init__.py
├── config/
│   └── wheel_config.py        # 转盘配置
├── logic/
│   ├── wheel_spinner.py       # 旋转逻辑
│   ├── reward_calculator.py   # 奖励计算
│   └── probability.py         # 概率计算
└── command/
    └── wheel_command.py       # 命令处理
```

### 接口设计

#### 命令接口
```
wheel spin                   # 旋转转盘
wheel history                # 查看历史
wheel status                 # 查看状态
```

#### API接口
```python
class LuckyWheel:
    def __init__(self, user_manager, config)
    
    async def spin(self, user_id: str, platform: str) -> dict
        """旋转转盘"""
        
    async def get_status(self, user_id: str, platform: str) -> dict
        """获取转盘状态"""
        
    async def get_history(self, user_id: str, platform: str) -> list
        """获取旋转历史"""
        
    def calculate_reward(self) -> dict
        """计算奖励（概率）"""
```

### 配置项

```yaml
lucky_wheel:
  daily_free_spins: 1        # 每日免费次数
  spin_cost: 5               # 额外旋转积分消耗
  max_history: 10            # 保留历史记录数
  spin_duration: 3           # 旋转动画时长（秒）
  reset_time: "00:00"        # 每日重置时间
```

## 实现步骤

### 阶段一：基础功能（1天）
1. 创建奖励池配置
2. 实现概率计算逻辑
3. 实现基础旋转功能
4. 集成用户数据

### 阶段二：用户体验（1天）
1. 实现旋转动画
2. 添加历史记录
3. 实现状态查询
4. 优化反馈效果

### 阶段三：测试优化（1天）
1. 概率测试
2. 边界测试
3. 性能测试
4. 用户测试

## 旋转效果设计

```python
# 文字版旋转动画
def get_spin_animation():
    stages = [
        "🎡 转盘开始旋转...",
        "🎡 旋转中... 💰",
        "🎡 旋转中... 💰💵",
        "🎡 旋转中... 💰💵💎",
        "🎡 旋转中... 💰💵💎🪙",
        "🎡 旋转中... 💰💵💎🪙🃏",
        "🎡 旋转中... 💰💵💎🪙🃏🎫",
        "🎡 最终结果..."
    ]
    return stages
```

## 成就系统

```python
ACHIEVEMENTS = [
    {
        "id": "lucky_winner",
        "name": "幸运之星",
        "description": "转盘抽中100积分",
        "reward": 50
    },
    {
        "id": "daily_spinner",
        "name": "每日转盘",
        "description": "连续7天使用转盘",
        "reward": 80
    },
    {
        "id": "jackpot_winner",
        "name": "大奖得主",
        "description": "抽中特殊奖励",
        "reward": 120
    }
]
```

## 测试计划

### 概率测试
- 各项奖励概率验证
- 长期统计验证
- 边界情况测试

### 功能测试
- 免费次数重置
- 积分扣除
- 奖励发放
- 历史记录

### 性能测试
- 并发旋转测试
- 响应时间测试
- 数据一致性测试

## 预期效果

- 日活跃度：+30%
- 平均使用次数：1.5次/人/天
- 完成率：≥95%
- 用户满意度：≥85%

## 风险与挑战

### 技术风险
- 概率准确性
- 并发问题
- 数据一致性

### 解决方案
- 使用高质量随机数生成器
- 添加分布式锁
- 事务处理

---

**文档版本**: v1.0  
**创建日期**: 2026-02-22