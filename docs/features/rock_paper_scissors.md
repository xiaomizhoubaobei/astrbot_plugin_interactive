# 石头剪刀布 - 开发文档

## 功能概述

石头剪刀布是一个经典的猜拳游戏，支持与AI对战，可以加入积分对赌机制，简单快速，适合碎片时间娱乐。

## 需求分析

### 功能需求

#### 核心功能
- 基础对战：石头、剪刀、布
- AI对战：与AI进行猜拳
- 积分对赌：下注积分
- 连胜奖励：连续获胜额外奖励
- 特殊技能：预判技能（消耗道具）

#### 游戏规则
- 石头胜剪刀，剪刀胜布，布胜石头
- 相同为平局
- 支持积分下注（5-50积分）
- 5局3胜制
- 连胜记录

#### 奖励机制
- 胜利：获得下注积分
- 平局：返还下注积分
- 失败：扣除下注积分
- 连胜奖励：连胜2次以上额外奖励
- 特殊技能：预判对手出拳

### 非功能需求
- 响应时间：<0.5秒
- 支持多平台
- AI智能可配置

## 技术设计

### 数据结构

```python
# 游戏状态
{
    "game_id": "str",
    "user_id": "str",
    "bet_points": "int",       # 下注积分
    "wins": "int",             # 用户获胜局数
    "ai_wins": "int",          # AI获胜局数
    "round": "int",            # 当前回合
    "consecutive_wins": "int", # 连胜次数
    "history": "list",         # 历史记录
    "start_time": "int",
    "status": "playing|finished"
}

# 历史记录
{
    "round": "int",
    "user_choice": "str",      # 用户选择
    "ai_choice": "str",        # AI选择
    "result": "win|lose|draw" # 结果
}
```

### AI策略

```python
class AIPlayer:
    def __init__(self, difficulty: int = 3)
    
    def get_choice(self, user_history: list) -> str
        """AI选择出拳
        
        策略：
        - 随机选择（低难度）
        - 统计分析（中难度）
        - 预测模式（高难度）
        """
```

### 模块设计

```
rps/
├── __init__.py
├── logic/
│   ├── rps_game.py          # 游戏逻辑
│   ├── ai_player.py         # AI玩家
│   └── skill_system.py      # 技能系统
└── command/
    └── rps_command.py       # 命令处理
```

### 接口设计

#### 命令接口
```
rps start [积分]             # 开始游戏
rps <选择>                   # 出拳（石头/剪刀/布）
rps predict                  # 使用预判技能
rps giveup                   # 放弃
rps status                   # 查看状态
```

#### API接口
```python
class RPSGame:
    def __init__(self, user_manager, ai_player)
    
    async def start_game(self, user_id: str, platform: str, 
                        bet_points: int) -> dict
        """开始游戏"""
        
    async def play_round(self, user_id: str, platform: str, 
                        choice: str) -> dict
        """进行一局"""
        
    async def use_predict_skill(self, user_id: str, platform: str) -> dict
        """使用预判技能"""
        
    def calculate_result(self, user_choice: str, ai_choice: str) -> str
        """计算结果"""
```

### 配置项

```yaml
rps_game:
  min_bet: 5                 # 最小下注
  max_bet: 50                # 最大下注
  rounds_to_win: 3           # 获胜局数
  ai_difficulty: 3           # AI难度（1-5）
  consecutive_bonus: 10      # 连胜奖励
  skill_cost: 20             # 预判技能积分消耗
  choices:
    rock:
      emoji: "🪨"
      beats: "scissors"
      loses_to: "paper"
    scissors:
      emoji: "✂️"
      beats: "paper"
      loses_to: "rock"
    paper:
      emoji: "📄"
      beats: "rock"
      loses_to: "scissors"
```

## 实现步骤

### 阶段一：基础逻辑（1天）
1. 实现基础游戏逻辑
2. 实现胜负判断
3. 实现积分对赌
4. 实现AI基础策略

### 阶段二：高级功能（1天）
1. 实现连胜奖励
2. 实现技能系统
3. 实现历史记录
4. 优化AI策略

### 阶段三：命令处理（1天）
1. 实现命令解析
2. 实现用户交互
3. 集成成就系统
4. 优化用户体验

### 阶段四：测试优化（1天）
1. 功能测试
2. AI平衡测试
3. 性能测试
4. 用户测试

## 游戏效果展示

```python
def get_round_result_display(user_choice: str, ai_choice: str, 
                             result: str, bet_points: int):
    """获取回合结果显示"""
    emojis = {
        "rock": "🪨",
        "scissors": "✂️",
        "paper": "📄"
    }
    
    result_text = {
        "win": "你赢了！",
        "lose": "你输了！",
        "draw": "平局"
    }
    
    display = f"""
    你出拳：{emojis[user_choice]}
    AI出拳：{emojis[ai_choice]}
    
    {result_text[result]}
    """
    
    if result != "draw":
        points = bet_points if result == "win" else -bet_points
        display += f"\n积分变化：{'+' if points > 0 else ''}{points}"
    
    return display
```

## 成就系统

```python
ACHIEVEMENTS = [
    {
        "id": "rps_master",
        "name": "猜拳大师",
        "description": "赢得20局猜拳",
        "reward": 100
    },
    {
        "id": "consecutive_winner",
        "name": "连胜王者",
        "description": "连续猜拳获胜10次",
        "reward": 150
    },
    {
        "id": "high_roller",
        "name": "豪赌客",
        "description": "单次下注50积分并获胜",
        "reward": 80
    }
]
```

## 测试计划

### 功能测试
- 基础对战流程
- 积分下赌
- 连胜奖励
- 技能使用

### AI测试
- 随机性测试
- 策略测试
- 平衡性测试

### 性能测试
- 响应时间测试
- 并发测试
- 数据一致性测试

## 预期效果

- 用户参与度：+10%
- 平均游戏时长：1-2分钟
- 完成率：≥90%
- 用户满意度：≥85%

## 风险与挑战

### 技术风险
- AI策略过于简单
- 随机性不足
- 平衡性问题

### 解决方案
- 多种AI策略组合
- 真随机数生成
- 数据统计调整

---

**文档版本**: v1.0  
**创建日期**: 2026-02-22