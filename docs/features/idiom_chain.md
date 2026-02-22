# 成语接龙 - 开发文档

## 功能概述

成语接龙是一个经典的中国文化游戏，玩家需要说出以前一个成语最后一个字开头的成语。该功能支持单人（与AI对战）和双人（轮流接龙）两种模式。

## 需求分析

### 功能需求

#### 核心功能
- 单人模式：玩家与AI轮流接龙
- 双人模式：两名玩家轮流接龙
- 超时机制：超过时间未回复自动判负
- 成语验证：检查成语是否合法
- 语音匹配：支持同音字匹配

#### 游戏规则
- 必须使用四字成语
- 后一个成语首字必须与前一个成语尾字相同
- 支持同音字（拼音相同）
- 不能重复使用相同成语
- 超时时间：60秒

#### 奖励机制
- 获胜奖励：20-30积分
- 连胜奖励：连续获胜额外奖励
- 首字奖励：率先达到10个成语
- 参与奖励：完成对局5积分

### 非功能需求
- 响应时间：<1秒
- 成语库：≥3000个常用成语
- 支持多平台

## 技术设计

### 数据结构

```python
# 成语数据结构
{
    "id": "str",              # 成语ID
    "text": "str",            # 成语文本
    "pinyin": "str",          # 拼音（带声调）
    "first_char": "str",      # 首字
    "last_char": "str",       # 尾字
    "first_pinyin": "str",    # 首字拼音
    "last_pinyin": "str",     # 尾字拼音
    "difficulty": "int",      # 难度（1-5）
    "usage": "int"            # 使用频率
}

# 游戏状态
{
    "game_id": "str",
    "mode": "single|multi",
    "player1_id": "str",
    "player2_id": "str",      # AI模式为"ai"
    "current_turn": "int",    # 当前回合
    "last_idiom": "str",      # 上一个成语
    "last_char": "str",       # 最后一个字
    "last_pinyin": "str",     # 最后一个字拼音
    "used_idioms": "list",    # 已使用的成语
    "start_time": "int",
    "last_action_time": "int",
    "status": "playing|finished"
}
```

### 模块设计

```
idiom_chain/
├── __init__.py
├── data/
│   ├── idiom_database.py      # 成语数据库
│   └── idiom_validator.py     # 成语验证
├── game/
│   ├── idiom_game.py          # 游戏逻辑
│   ├── ai_player.py           # AI玩家
│   └── game_manager.py        # 游戏管理
└── command/
    └── idiom_command.py       # 命令处理
```

### 接口设计

#### 命令接口
```
idiom start [mode]           # 开始游戏
idiom <成语>                  # 接龙
idiom giveup                 # 放弃
idiom hint                   # 提示
idiom status                 # 查看状态
```

#### API接口
```python
class IdiomGame:
    def __init__(self, game_id: str, mode: str, players: list)
    
    async def play_idiom(self, user_id: str, idiom: str) -> dict
        """玩家出成语"""
        
    async def check_timeout(self) -> bool
        """检查超时"""
        
    async def get_hint(self, user_id: str) -> str
        """获取提示"""
        
    async def get_valid_idioms(self, last_char: str) -> list
        """获取可用成语列表"""
```

### 配置项

```yaml
idiom_chain:
  timeout: 60              # 超时时间（秒）
  ai_difficulty: 3         # AI难度（1-5）
  max_turns: 20            # 最大回合数
  rewards:
    win: 25                # 获胜奖励
    lose: 5                # 失败奖励
    consecutive_bonus: 5   # 连胜奖励
    first_to_10: 20        # 首先达到10个成语
  allow_tone_match: true   # 允许同音字
  allow_same_char: false   # 允许同字
```

## 实现步骤

### 阶段一：数据准备（2天）
1. 收集成语数据（3000+常用成语）
2. 添加拼音标注
3. 创建成语数据库
4. 编写验证逻辑

### 阶段二：核心逻辑（3天）
1. 实现成语匹配算法
2. 实现游戏状态管理
3. 实现超时检查
4. 实现AI玩家逻辑

### 阶段三：命令处理（2天）
1. 实现命令解析
2. 实现用户交互
3. 实现奖励发放
4. 集成成就系统

### 阶段四：测试优化（2天）
1. 单元测试
2. 集成测试
3. 性能优化
4. 用户测试

## 成就系统

```python
ACHIEVEMENTS = [
    {
        "id": "idiom_master",
        "name": "成语大师",
        "description": "成语接龙获胜10次",
        "reward": 100
    },
    {
        "id": "consecutive_winner",
        "name": "连胜王者",
        "description": "成语接龙连胜5次",
        "reward": 150
    },
    {
        "id": "speed_demon",
        "name": "接龙快手",
        "description": "在30秒内完成一局",
        "reward": 80
    }
]
```

## 测试计划

### 单元测试
- 成语验证测试
- 拼音匹配测试
- AI决策测试
- 超时检查测试

### 集成测试
- 单人对战流程
- 双人对战流程
- 奖励发放测试
- 异常处理测试

### 用户测试
- 可用性测试
- 性能测试
- 兼容性测试

## 预期效果

- 用户活跃度：+20%
- 平均游戏时长：3-5分钟
- 完成率：≥80%
- 用户满意度：≥90%

## 风险与挑战

### 技术风险
- 成语数据质量
- 拼音匹配准确性
- AI智能程度

### 解决方案
- 使用高质量成语数据源
- 多层验证机制
- 可配置AI难度

---

**文档版本**: v1.0  
**创建日期**: 2026-02-22