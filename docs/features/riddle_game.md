# 猜谜语 - 开发文档

## 功能概述

猜谜语是一个智力挑战游戏，用户通过文字描述猜测谜底。支持多种类型谜语（字谜、物谜、脑筋急转弯），可使用提示令牌获取提示，复用现有猜数字架构。

## 需求分析

### 功能需求

#### 核心功能
- 谜语分类：字谜、物谜、成语谜、脑筋急转弯
- 难度分级：简单、中等、困难
- 提示机制：使用提示令牌获取提示
- 答案验证：支持多种表达方式
- 积分奖励：难度决定奖励

#### 谜语类型
1. **字谜**：通过描述猜汉字
2. **物谜**：通过描述猜物品
3. **成语谜**：通过描述猜成语
4. **脑筋急转弯**：趣味问答

#### 游戏规则
- 无限次猜测机会
- 可使用提示令牌（每次消耗1枚）
- 谜语有难度分级
- 猜对获得积分奖励
- 猜错不扣积分

### 非功能需求
- 响应时间：<1秒
- 谜语库：≥500个谜语
- 答案匹配准确

## 技术设计

### 数据结构

```python
# 谜语数据结构
{
    "id": "str",              # 谜语ID
    "type": "str",            # 类型（char/object/idiom/brain）
    "difficulty": "int",      # 难度（1-5）
    "question": "str",        # 谜面
    "answer": "str",          # 答案
    "aliases": "list",        # 答案别名
    "hint": "str",            # 提示
    "explanation": "str",     # 解释
    "emoji": "str"            # 显示emoji
}

# 游戏状态
{
    "game_id": "str",
    "user_id": "str",
    "riddle_id": "str",
    "attempts": "int",        # 尝试次数
    "hints_used": "int",      # 已使用提示次数
    "start_time": "int",
    "status": "playing|finished"
}
```

### 谜语库配置

```yaml
riddle_database:
  - id: "r001"
    type: "char"
    difficulty: 2
    question: "一口咬掉牛尾巴"
    answer: "告"
    aliases: []
    hint: "牛字去掉尾巴"
    explanation: "牛字下面去掉尾巴就是告"
    emoji: "🔤"
    
  - id: "r002"
    type: "object"
    difficulty: 3
    question: "有面没有口，有脚没有手，虽有四只脚，自己不会走"
    answer: "桌子"
    aliases: ["台", "桌"]
    hint: "放在屋里用的"
    explanation: "桌子有面四只脚但不会走"
    emoji: "🪑"
    
  - id: "r003"
    type: "brain"
    difficulty: 2
    question: "什么东西越洗越脏？"
    answer: "水"
    aliases: []
    hint: "清洁用品"
    explanation: "水洗东西会变脏"
    emoji: "💧"
```

### 模块设计

```
riddle/
├── __init__.py
├── data/
│   ├── riddle_database.py    # 谜语数据库
│   └── riddle_matcher.py     # 答案匹配
├── logic/
│   ├── riddle_game.py        # 游戏逻辑
│   └── hint_system.py        # 提示系统
└── command/
    └── riddle_command.py     # 命令处理
```

### 接口设计

#### 命令接口
```
riddle start [type] [difficulty]  # 开始猜谜
riddle <答案>                     # 猜答案
riddle hint                       # 使用提示
riddle giveup                     # 放弃
riddle status                     # 查看状态
```

#### API接口
```python
class RiddleGame:
    def __init__(self, game_manager, riddle_database)
    
    async def start_game(self, user_id: str, platform: str, 
                        riddle_type: str, difficulty: int) -> dict
        """开始游戏"""
        
    async def guess_answer(self, user_id: str, platform: str, 
                          answer: str) -> dict
        """猜测答案"""
        
    async def use_hint(self, user_id: str, platform: str) -> dict
        """使用提示"""
        
    def match_answer(self, user_answer: str, correct_answer: str, 
                     aliases: list) -> bool
        """匹配答案"""
```

### 配置项

```yaml
riddle_game:
  base_points: 10             # 基础积分
  difficulty_bonus: 5         # 难度加成
  time_bonus: 2               # 时间加成
  max_attempts: 10            # 最大尝试次数
  hint_cost: 1                # 提示令牌消耗
  rewards:
    difficulty_1: 10          # 简单难度奖励
    difficulty_2: 15          # 中等难度奖励
    difficulty_3: 20          # 困难难度奖励
    difficulty_4: 30          # 专家难度奖励
    difficulty_5: 50          # 大师难度奖励
```

## 实现步骤

### 阶段一：数据准备（2天）
1. 收集谜语数据（500+）
2. 分类整理
3. 添加答案别名
4. 编写匹配逻辑

### 阶段二：核心逻辑（2天）
1. 实现答案匹配算法
2. 实现游戏状态管理
3. 实现提示系统
4. 集成积分奖励

### 阶段三：命令处理（1天）
1. 实现命令解析
2. 实现用户交互
3. 实现难度选择
4. 集成成就系统

### 阶段四：测试优化（1天）
1. 答案匹配测试
2. 难度平衡测试
3. 性能优化
4. 用户测试

## 答案匹配算法

```python
def match_answer(user_answer: str, correct_answer: str, 
                 aliases: list) -> bool:
    """匹配答案
    
    Args:
        user_answer: 用户答案
        correct_answer: 正确答案
        aliases: 答案别名
        
    Returns:
        是否匹配
    """
    # 标准化处理
    user_answer = user_answer.strip().lower()
    correct_answer = correct_answer.strip().lower()
    
    # 直接匹配
    if user_answer == correct_answer:
        return True
    
    # 别名匹配
    for alias in aliases:
        alias = alias.strip().lower()
        if user_answer == alias:
            return True
    
    # 模糊匹配（去除标点）
    import re
    user_clean = re.sub(r'[^\w]', '', user_answer)
    correct_clean = re.sub(r'[^\w]', '', correct_answer)
    
    if user_clean == correct_clean:
        return True
    
    return False
```

## 成就系统

```python
ACHIEVEMENTS = [
    {
        "id": "riddle_master",
        "name": "谜语大师",
        "description": "猜对20个谜语",
        "reward": 100
    },
    {
        "id": "hard_core",
        "name": "硬核玩家",
        "description": "猜对5个困难谜语",
        "reward": 120
    },
    {
        "id": "quick_solver",
        "name": "闪电解谜",
        "description": "在10秒内猜对谜语",
        "reward": 80
    }
]
```

## 测试计划

### 单元测试
- 答案匹配测试
- 难度分级测试
- 提示系统测试
- 积分计算测试

### 集成测试
- 游戏流程测试
- 多种类型测试
- 异常处理测试

### 用户测试
- 可用性测试
- 谜语质量测试
- 难度平衡测试

## 预期效果

- 用户参与度：+15%
- 平均完成率：≥75%
- 用户满意度：≥88%
- 提示令牌使用率：+30%

## 风险与挑战

### 技术风险
- 答案匹配准确性
- 谜语质量参差不齐
- 难度平衡问题

### 解决方案
- 多层匹配机制
- 用户反馈机制
- 动态难度调整

---

**文档版本**: v1.0  
**创建日期**: 2026-02-22