# 表情包猜词 - 开发文档

## 功能概述

表情包猜词是一个趣味性强的游戏，用emoji组合表示词汇，用户猜测emoji代表的词汇。该功能年轻用户喜爱，纯emoji无需图像处理，可自定义题目。

## 需求分析

### 功能需求

#### 核心功能
- Emoji词库：预设emoji词汇组合
- 提示机制：使用提示令牌
- 分类系统：动物、食物、成语、日常等
- 难度分级：根据emoji数量和常见度
- 用户贡献：允许用户提交新题目

#### 游戏类型
1. **动物**：🐶🐱 = 猫狗
2. **食物**：🍔🍟 = 汉堡薯条
3. **成语**：🎂🎂 = 生日（双喜）
4. **日常**：🌧️☔ = 雨伞
5. **影视**：⚔️👑 = 皇帝

#### 游戏规则
- 无限次猜测
- 可使用提示令牌
- 答案支持多种表达
- 猜对获得积分奖励
- 猜错不扣积分

### 非功能需求
- 响应时间：<1秒
- Emoji词库：≥200个
- 答案匹配准确

## 技术设计

### 数据结构

```python
# Emoji词汇数据
{
    "id": "str",              # 题目ID
    "category": "str",        # 分类
    "difficulty": "int",      # 难度（1-5）
    "emojis": "str",          # emoji组合
    "answer": "str",          # 答案
    "aliases": "list",        # 答案别名
    "hint": "str",            # 提示
    "creator": "str",         # 创建者（用户ID或system）
    "usage_count": "int",     # 使用次数
    "correct_rate": "float"   # 正确率
}

# 游戏状态
{
    "game_id": "str",
    "user_id": "str",
    "question_id": "str",
    "attempts": "int",
    "hints_used": "int",
    "start_time": "int",
    "status": "playing|finished"
}
```

### Emoji词库配置

```yaml
emoji_puzzles:
  - id: "e001"
    category: "动物"
    difficulty: 1
    emojis: "🐶🐱"
    answer: "猫狗"
    aliases: ["猫和狗", "猫与狗"]
    hint: "两种常见的宠物"
    creator: "system"
    
  - id: "e002"
    category: "食物"
    difficulty: 2
    emojis: "🍔🍟"
    answer: "汉堡薯条"
    aliases: ["快餐", "麦当劳"]
    hint: "西式快餐组合"
    creator: "system"
    
  - id: "e003"
    category: "成语"
    difficulty: 3
    emojis: "🐉🎃"
    answer: "龙飞凤舞"
    aliases: []
    hint: "四个字，与龙凤有关"
    creator: "system"
    
  - id: "e004"
    category: "影视"
    difficulty: 4
    emojis: "🎬🦸"
    answer: "超级英雄"
    aliases: ["超人", "英雄"]
    hint: "电影里的英雄角色"
    creator: "system"
```

### 模块设计

```
emoji_guess/
├── __init__.py
├── data/
│   ├── emoji_database.py     # Emoji词库
│   └── answer_matcher.py    # 答案匹配
├── logic/
│   ├── emoji_game.py         # 游戏逻辑
│   └── user_submission.py    # 用户提交
└── command/
    └── emoji_command.py      # 命令处理
```

### 接口设计

#### 命令接口
```
emoji start [category]       # 开始游戏
emoji <答案>                 # 猜答案
emoji hint                   # 使用提示
emoji submit <emojis> <答案> # 提交新题目
emoji list                   # 查看可用分类
emoji giveup                 # 放弃
```

#### API接口
```python
class EmojiGame:
    def __init__(self, game_manager, emoji_database)
    
    async def start_game(self, user_id: str, platform: str, 
                        category: str) -> dict
        """开始游戏"""
        
    async def guess_answer(self, user_id: str, platform: str, 
                          answer: str) -> dict
        """猜测答案"""
        
    async def submit_puzzle(self, user_id: str, platform: str,
                           emojis: str, answer: str) -> dict
        """提交新题目"""
        
    async def get_categories(self) -> list
        """获取可用分类"""
```

### 配置项

```yaml
emoji_game:
  base_points: 15             # 基础积分
  difficulty_bonus: 5         # 难度加成
  hint_cost: 1                # 提示令牌消耗
  submission_reward: 20       # 提交题目奖励
  review_required: true       # 需要审核
  max_attempts: 10            # 最大尝试次数
```

## 实现步骤

### 阶段一：数据准备（2天）
1. 收集emoji词汇（200+）
2. 分类整理
3. 添加答案别名
4. 编写匹配逻辑

### 阶段二：核心逻辑（2天）
1. 实现答案匹配算法
2. 实现游戏状态管理
3. 实现提示系统
4. 实现积分奖励

### 阶段三：用户贡献（1天）
1. 实现题目提交功能
2. 实现审核机制
3. 实现奖励发放
4. 管理后台

### 阶段四：测试优化（1天）
1. 答案匹配测试
2. emoji显示测试
3. 用户测试
4. 效果优化

## 题目审核流程

```python
class PuzzleReviewer:
    """题目审核器"""
    
    def __init__(self):
        self.pending_submissions = []
        self.approved_puzzles = []
        
    async def submit(self, user_id: str, emojis: str, answer: str):
        """提交题目待审核"""
        submission = {
            "id": f"sub_{int(time.time())}",
            "user_id": user_id,
            "emojis": emojis,
            "answer": answer,
            "status": "pending",
            "submit_time": int(time.time())
        }
        self.pending_submissions.append(submission)
        return submission
        
    async def approve(self, submission_id: str):
        """通过审核"""
        for sub in self.pending_submissions:
            if sub["id"] == submission_id:
                puzzle = {
                    "id": f"e{len(self.approved_puzzles) + 1}",
                    "emojis": sub["emojis"],
                    "answer": sub["answer"],
                    "creator": sub["user_id"],
                    "category": "user",
                    "difficulty": self.calculate_difficulty(sub["emojis"])
                }
                self.approved_puzzles.append(puzzle)
                return puzzle
        return None
```

## 成就系统

```python
ACHIEVEMENTS = [
    {
        "id": "emoji_master",
        "name": "Emoji大师",
        "description": "猜对50个Emoji词汇",
        "reward": 150
    },
    {
        "id": "creative_user",
        "name": "创意达人",
        "description": "提交10个通过的题目",
        "reward": 120
    },
    {
        "id": "quick_guesser",
        "name": "闪电猜谜",
        "description": "在15秒内猜对Emoji词汇",
        "reward": 80
    }
]
```

## 测试计划

### 功能测试
- 答案匹配测试
- emoji显示测试
- 分类筛选测试
- 提交审核测试

### 用户测试
- 可用性测试
- 趣味性测试
- 创意性测试

### 性能测试
- 响应时间测试
- 数据库查询测试

## 预期效果

- 用户参与度：+20%
- 平均完成率：≥80%
- 用户贡献率：≥15%
- 用户满意度：≥88%

## 风险与挑战

### 技术风险
- Emoji兼容性问题
- 答案匹配准确性
- 审核工作量

### 解决方案
- 使用Unicode标准Emoji
- 多层匹配机制
- 社区审核机制

---

**文档版本**: v1.0  
**创建日期**: 2026-02-22