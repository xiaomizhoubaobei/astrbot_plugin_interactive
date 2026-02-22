# AstrBot 互动游戏插件 - 游戏管理系统完善计划

## 📋 文档概述

本文档详细规划游戏管理系统的完善方案，旨在丰富游戏类型、提升游戏体验、增强系统稳定性。

**版本**: v1.0  
**创建日期**: 2026-02-22  
**维护者**: 开发团队

---

## 🔍 当前状态分析

### 1. 现有功能

#### 1.1 核心功能
- ✅ 游戏状态管理（内存存储）
- ✅ 猜数字游戏（1-100范围）
- ✅ 实时计分系统（基于尝试次数和时间）
- ✅ 游戏提示功能（消耗提示令牌）
- ✅ 游戏放弃功能
- ✅ 成就系统集成

#### 1.2 猜数字游戏特性
- **游戏类型**: 单人猜数字
- **范围**: 1-100（可配置）
- **评分规则**:
  - 基础分: (10 - 尝试次数) × 5，最低1分
  - 时间奖励: (60 - 用时秒数) × 2，最低1分
- **提示系统**: 显示目标数字 ±10% 的范围
- **反馈机制**: 根据差距提供不同程度的提示

#### 1.3 数据结构
```python
{
    "target_number": 42,              # 目标数字
    "attempts": 3,                    # 尝试次数
    "start_time": 1708569600000,      # 开始时间（毫秒）
    "max_number": 100                 # 最大数字
}
```

### 2. 已识别的问题

#### 2.1 游戏类型单一
- ❌ 只有猜数字一种游戏
- ❌ 缺少不同类型的游戏
- ❌ 无法满足不同用户偏好
- ❌ 长期游玩缺乏新鲜感

#### 2.2 游戏体验问题
- ❌ 缺少游戏难度系统
- ❌ 缺少游戏教程和帮助
- ❌ 缺少游戏历史记录
- ❌ 缺少游戏统计数据分析
- ❌ 缺少游戏存档功能（重启后丢失）

#### 2.3 功能缺失
- ❌ 缺少多人游戏支持
- ❌ 缺少游戏排行榜
- ❌ 缺少游戏成就独立系统
- ❌ 缺少游戏任务系统
- ❌ 缺少游戏赛季系统
- ❌ 缺少游戏锦标赛功能

#### 2.4 技术问题
- ❌ 游戏状态存储在内存（重启丢失）
- ❌ 缺少游戏配置化（难度、奖励等）
- ❌ 缺少游戏数据持久化
- ❌ 缺少游戏缓存机制
- ❌ 缺少游戏超时自动结束

#### 2.5 安全问题
- ❌ 缺少防作弊机制
- ❌ 缺少游戏操作审计日志
- ❌ 缺少异常行为检测
- ❌ 缺少游戏频率限制

---

## 🎯 完善计划

### 阶段一：游戏状态持久化（优先级：高）

#### 1.1 游戏数据持久化

**目标**: 解决游戏状态重启丢失问题

**实施内容**:

```python
# 改进 game_manager.py
from datetime import datetime, timedelta
from typing import Dict, Optional
import random
import json
from pathlib import Path

class GameManager:
    """游戏状态管理器"""

    def __init__(self):
        self.games: Dict[str, Dict] = {}  # 内存缓存
        self.game_storage_path = Path("data/games")
        self.game_storage_path.mkdir(exist_ok=True)
        self.plugin_name = "astrbot_plugin_interactive"
        self._load_games()

    def _get_game_file_path(self, game_key: str) -> Path:
        """获取游戏文件路径"""
        return self.game_storage_path / f"{game_key}.json"

    def _load_games(self) -> None:
        """从文件加载游戏状态"""
        try:
            for game_file in self.game_storage_path.glob("*.json"):
                with open(game_file, 'r', encoding='utf-8') as f:
                    game_data = json.load(f)
                    game_key = game_file.stem
                    self.games[game_key] = game_data
            logger.info(f"[{self.plugin_name}] 加载了 {len(self.games)} 个游戏状态")
        except Exception as e:
            logger.error(f"[{self.plugin_name}] 加载游戏状态失败: {e}")

    def _save_game(self, game_key: str) -> None:
        """保存游戏状态到文件"""
        if game_key not in self.games:
            return
        
        try:
            game_file = self._get_game_file_path(game_key)
            with open(game_file, 'w', encoding='utf-8') as f:
                json.dump(self.games[game_key], f, ensure_ascii=False, indent=2)
            logger.debug(f"[{self.plugin_name}] 保存游戏状态: {game_key}")
        except Exception as e:
            logger.error(f"[{self.plugin_name}] 保存游戏状态失败: {e}")

    def delete_game(self, game_key: str) -> bool:
        """删除游戏状态"""
        if game_key in self.games:
            del self.games[game_key]
            game_file = self._get_game_file_path(game_key)
            if game_file.exists():
                game_file.unlink()
            logger.debug(f"[{self.plugin_name}] 游戏已删除: {game_key}")
            return True
        return False
```

**集成点**:
- 创建游戏时保存
- 更新游戏状态时保存
- 删除游戏时清理文件
- 服务启动时自动加载

**预期收益**:
- 游戏状态不丢失
- 支持服务重启
- 便于数据备份

---

#### 1.2 游戏超时机制

**目标**: 自动清理超时游戏

**实施内容**:

```python
async def cleanup_expired_games(self, timeout_minutes: int = 60) -> int:
    """清理超时游戏
    
    Args:
        timeout_minutes: 超时时间（分钟）
    
    Returns:
        清理的游戏数量
    """
    from datetime import timedelta
    
    now = datetime.now()
    timeout = timedelta(minutes=timeout_minutes)
    expired_games = []
    
    for game_key, game in self.games.items():
        start_time = datetime.fromtimestamp(game["start_time"] / 1000)
        if now - start_time > timeout:
            expired_games.append(game_key)
    
    for game_key in expired_games:
        self.delete_game(game_key)
        logger.info(f"[{self.plugin_name}] 清理超时游戏: {game_key}")
    
    return len(expired_games)
```

**定时任务**:
- 每10分钟检查一次
- 自动清理超时游戏
- 记录清理日志

---

### 阶段二：游戏类型扩展（优先级：高）

#### 2.1 石头剪刀布游戏

**目标**: 添加经典猜拳游戏

**实施内容**:

**游戏特性**:
- 单人对战AI
- 三局两胜制
- 记录连胜次数
- 连胜奖励加成

**数据结构**:
```python
{
    "game_type": "rps",              # 游戏类型
    "round": 1,                       # 当前回合
    "max_rounds": 3,                  # 总回合数
    "player_wins": 0,                 # 玩家胜利次数
    "ai_wins": 0,                     # AI胜利次数
    "player_streak": 0,               # 连胜次数
    "history": [],                    # 历史记录
    "start_time": 1708569600000
}
```

**评分规则**:
- 胜利: 20分
- 连胜奖励: +5分/连胜
- 完美胜利: +10分（3-0获胜）

**命令**:
- `rps start` - 开始游戏
- `rps <石头/剪刀/布>` - 出拳
- `rps giveup` - 放弃

---

#### 2.2 幸运数字游戏

**目标**: 添加概率类小游戏

**实施内容**:

**游戏特性**:
- 从1-36中选择数字
- 系统随机抽取中奖号码
- 支持单注和复式投注
- 消耗积分参与

**数据结构**:
```python
{
    "game_type": "lucky_number",      # 游戏类型
    "bet_numbers": [7, 18, 25],       # 投注号码
    "bet_cost": 30,                   # 投注消耗
    "winning_number": 0,              # 中奖号码
    "result": "",                     # 结果
    "reward": 0,                      # 奖励
    "start_time": 1708569600000
}
```

**规则**:
- 单注消耗10积分
- 猜中单个号码: 5倍奖励
- 猜中多个号码: 累计奖励

**命令**:
- `lucky <数字>` - 单注投注
- `lucky <数字1> <数字2> ...` - 复式投注

---

#### 2.3 猜词游戏

**目标**: 添加文字类游戏

**实施内容**:

**游戏特性**:
- 系统随机选择词语
- 显示词语的长度和部分字母
- 最多10次猜测机会
- 支持提示功能

**数据结构**:
```python
{
    "game_type": "word_guess",        # 游戏类型
    "target_word": "APPLE",           # 目标词语
    "guessed_letters": [],            # 已猜字母
    "wrong_guesses": 0,               # 错误次数
    "max_wrong": 10,                  # 最大错误次数
    "hints_used": 0,                  # 使用提示次数
    "start_time": 1708569600000
}
```

**评分规则**:
- 基础分: (10 - 错误次数) × 10
- 时间奖励: 每30秒+10分
- 提示惩罚: 每次使用-20分

**命令**:
- `word start` - 开始游戏
- `word <字母>` - 猜字母
- `word hint` - 使用提示

---

#### 2.4 记忆游戏

**目标**: 添加记忆力挑战游戏

**实施内容**:

**游戏特性**:
- 显示一串数字（5-10位）
- 几秒后隐藏
- 玩家需要回忆并输入
- 支持多个难度等级

**数据结构**:
```python
{
    "game_type": "memory",            # 游戏类型
    "sequence": [3, 7, 2, 8, 5],      # 数字序列
    "difficulty": "medium",           # 难度
    "attempts": 0,                    # 尝试次数
    "best_score": 0,                  # 最佳成绩
    "start_time": 1708569600000
}
```

**难度设置**:
- 简单: 5位数字，显示5秒
- 中等: 7位数字，显示3秒
- 困难: 10位数字，显示2秒

**评分规则**:
- 一次正确: 100分
- 二次正确: 70分
- 三次正确: 40分

**命令**:
- `memory start [难度]` - 开始游戏
- `memory <数字>` - 输入答案

---

### 阶段三：游戏难度系统（优先级：中）

#### 3.1 猜数字游戏难度扩展

**目标**: 添加多难度选择

**实施内容**:

**难度设置**:

| 难度 | 数字范围 | 基础分 | 时间限制 | 提示范围 |
|------|----------|--------|----------|----------|
| 简单 | 1-50 | 50 | 90秒 | ±20% |
| 中等 | 1-100 | 100 | 60秒 | ±10% |
| 困难 | 1-200 | 200 | 45秒 | ±5% |
| 专家 | 1-500 | 500 | 30秒 | ±2% |

**命令**:
- `guess start [难度]` - 指定难度开始
- `guess start` - 默认中等难度

---

#### 3.2 动态难度调整

**目标**: 根据玩家水平自动调整难度

**实施内容**:

```python
def calculate_recommended_difficulty(self, user_data: Dict) -> str:
    """根据玩家数据推荐难度
    
    Args:
        user_data: 用户数据
    
    Returns:
        推荐难度
    """
    win_rate = 0
    if user_data["games_played"] > 0:
        win_rate = user_data["games_won"] / user_data["games_played"]
    
    avg_attempts = 0
    # 计算平均尝试次数（需要从游戏历史获取）
    
    if win_rate > 0.8 and avg_attempts < 5:
        return "expert"
    elif win_rate > 0.6 and avg_attempts < 7:
        return "hard"
    elif win_rate > 0.4:
        return "medium"
    else:
        return "easy"
```

---

### 阶段四：游戏统计系统（优先级：中）

#### 4.1 游戏历史记录

**目标**: 记录玩家游戏历史

**实施内容**:

**新增字段**:
```python
{
    "game_history": [                # 游戏历史（最多保留100条）
        {
            "game_type": "guess",
            "difficulty": "medium",
            "result": "win",
            "score": 50,
            "timestamp": 1708569600000,
            "details": {
                "attempts": 3,
                "time_used": 25
            }
        }
    ],
    "game_stats": {                  # 游戏统计
        "total_games": 100,
        "total_wins": 60,
        "win_rate": 0.6,
        "total_score": 5000,
        "best_score": 150,
        "favorite_game": "guess",
        "games_by_type": {
            "guess": 80,
            "rps": 15,
            "lucky_number": 5
        }
    }
}
```

---

#### 4.2 游戏排行榜

**目标**: 添加竞技元素

**实施内容**:

**排行榜类型**:
1. **积分排行榜** - 按游戏总积分排名
2. **胜率排行榜** - 按游戏胜率排名
3. **连胜排行榜** - 按最长连胜排名
4. **游戏场次排行榜** - 按游戏场次排名

**排行榜功能**:
- 实时更新
- 周/月/全服排行
- 查看个人排名
- 排行榜奖励

**命令**:
- `rank [类型]` - 查看排行榜
- `rank my` - 查看个人排名

---

### 阶段五：多人游戏支持（优先级：中）

#### 5.1 挑战系统

**目标**: 允许玩家互相挑战

**实施内容**:

**挑战模式**:
- 猜数字对战（谁先猜中）
- 石头剪刀布对战
- 成绩比拼（同一游戏）

**数据结构**:
```python
{
    "game_type": "challenge",        # 游戏类型
    "challenge_type": "guess_race",  # 挑战类型
    "challenger": "user1",           # 挑战者
    "challenged": "user2",           # 被挑战者
    "status": "pending",             # 状态: pending/active/finished
    "game_data": {},                 # 游戏数据
    "winner": "",                    # 胜者
    "reward": 50,                    # 奖励
    "created_time": 1708569600000
}
```

**命令**:
- `challenge <用户ID> <游戏>` - 发起挑战
- `challenge accept` - 接受挑战
- `challenge decline` - 拒绝挑战
- `challenge status` - 查看挑战状态

---

#### 5.2 房间系统

**目标**: 支持多人游戏房间

**实施内容**:

**房间功能**:
- 创建房间
- 加入房间
- 房间聊天
- 开始游戏
- 观战功能

**数据结构**:
```python
{
    "room_id": "room_123",           # 房间ID
    "room_name": "快乐游戏房",        # 房间名称
    "host": "user1",                 # 房主
    "players": ["user1", "user2"],   # 玩家列表
    "max_players": 4,                # 最大人数
    "game_type": "guess",            # 游戏类型
    "status": "waiting",             # 状态: waiting/playing/finished
    "game_data": {},                 # 游戏数据
    "created_time": 1708569600000
}
```

**命令**:
- `room create <名称>` - 创建房间
- `room join <房间ID>` - 加入房间
- `room leave` - 离开房间
- `room start` - 开始游戏
- `room list` - 查看房间列表

---

### 阶段六：游戏任务系统（优先级：中）

#### 6.1 每日游戏任务

**目标**: 增加玩家每日参与动力

**实施内容**:

**任务类型**:
1. **完成3场游戏** - 奖励50积分
2. **获得2次胜利** - 奖励30积分
3. **游玩2种不同游戏** - 奖励40积分
4. **单局获得100+积分** - 奖励60积分
5. **使用1次提示** - 奖励20积分

**任务数据结构**:
```python
{
    "daily_tasks": [
        {
            "id": "play_3_games",
            "name": "游戏达人",
            "description": "完成3场游戏",
            "target": 3,
            "current": 1,
            "reward": {"points": 50, "items": []},
            "completed": false
        }
    ],
    "last_task_refresh": "2026-02-22"
}
```

**命令**:
- `tasks` - 查看任务列表
- `tasks claim <任务ID>` - 领取奖励

---

#### 6.2 成就系统扩展

**目标**: 添加游戏专属成就

**实施内容**:

**新增成就**:

| 成就ID | 名称 | 描述 | 奖励 |
|--------|------|------|------|
| guess_master | 猜数字大师 | 猜数字游戏胜利50次 | 500积分 |
| perfect_guess | 完美一击 | 3次内猜中数字 | 200积分 |
| rps_champion | 拳皇 | 石头剪刀布连胜10次 | 300积分 |
| memory_king | 记忆之王 | 记忆游戏获得满分10次 | 400积分 |
| all_games | 博学家 | 玩过所有类型游戏 | 600积分 |
| high_roller | 大玩家 | 单局游戏获得500+积分 | 800积分 |

---

### 阶段七：游戏配置化（优先级：中）

#### 7.1 游戏配置文件

**目标**: 支持游戏参数配置

**实施内容**:

```yaml
# config/games.yaml

games:
  # 猜数字游戏配置
  guess:
    difficulties:
      easy:
        max_number: 50
        base_points: 50
        time_limit: 90
        hint_range: 0.2
      medium:
        max_number: 100
        base_points: 100
        time_limit: 60
        hint_range: 0.1
      hard:
        max_number: 200
        base_points: 200
        time_limit: 45
        hint_range: 0.05
      expert:
        max_number: 500
        base_points: 500
        time_limit: 30
        hint_range: 0.02
    timeout_minutes: 60
  
  # 石头剪刀布游戏配置
  rps:
    rounds: 3
    win_points: 20
    streak_bonus: 5
    perfect_bonus: 10
    timeout_minutes: 30
  
  # 记忆游戏配置
  memory:
    difficulties:
      easy:
        sequence_length: 5
        display_time: 5
        max_attempts: 5
      medium:
        sequence_length: 7
        display_time: 3
        max_attempts: 3
      hard:
        sequence_length: 10
        display_time: 2
        max_attempts: 1
    timeout_minutes: 20
```

---

### 阶段八：安全性与防作弊（优先级：中）

#### 8.1 防作弊机制

**目标**: 防止玩家作弊

**实施内容**:

1. **游戏频率限制**:
   - 每小时最多开始10场游戏
   - 每天最多开始50场游戏

2. **异常行为检测**:
   - 检测超短时间完成（<5秒）
   - 检测100%胜率（多场游戏）
   - 检测异常高分

3. **验证码机制**:
   - 可疑行为要求验证
   - 高分游戏需要验证

4. **游戏数据签名**:
   - 游戏状态签名
   - 防止篡改

---

#### 8.2 游戏审计日志

**目标**: 记录游戏操作

**实施内容**:

```python
async def log_game_action(
    self,
    user_id: str,
    platform: str,
    game_key: str,
    action: str,
    details: Dict[str, Any]
) -> None:
    """记录游戏操作日志"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "platform": platform,
        "game_key": game_key,
        "action": action,
        "details": details
    }
    logger.info(f"[GAME_AUDIT] {log_entry}")
```

**记录的操作**:
- 游戏开始/结束
- 游戏暂停/继续
- 猜测/操作
- 获得奖励
- 异常行为

---

## 📅 实施时间表

| 阶段 | 任务 | 优先级 | 预计时间 | 负责人 |
|------|------|--------|----------|--------|
| 阶段一 | 游戏数据持久化 | 高 | 4天 | - |
| 阶段一 | 游戏超时机制 | 高 | 2天 | - |
| 阶段二 | 石头剪刀布游戏 | 高 | 5天 | - |
| 阶段二 | 幸运数字游戏 | 高 | 4天 | - |
| 阶段二 | 猜词游戏 | 中 | 5天 | - |
| 阶段二 | 记忆游戏 | 中 | 4天 | - |
| 阶段三 | 猜数字难度扩展 | 中 | 3天 | - |
| 阶段三 | 动态难度调整 | 中 | 3天 | - |
| 阶段四 | 游戏历史记录 | 中 | 4天 | - |
| 阶段四 | 游戏排行榜 | 中 | 6天 | - |
| 阶段五 | 挑战系统 | 中 | 5天 | - |
| 阶段五 | 房间系统 | 低 | 8天 | - |
| 阶段六 | 每日游戏任务 | 中 | 4天 | - |
| 阶段六 | 成就系统扩展 | 中 | 3天 | - |
| 阶段七 | 游戏配置文件 | 中 | 3天 | - |
| 阶段八 | 防作弊机制 | 中 | 4天 | - |
| 阶段八 | 游戏审计日志 | 中 | 3天 | - |

**总计**: 约 70 天（约 2.3 个月）

---

## 📊 预期收益

### 游戏内容丰富
- ✅ 从1种游戏扩展到5种游戏
- ✅ 多难度选择适合不同玩家
- ✅ 多人游戏增加社交性

### 用户体验提升
- ✅ 游戏状态持久化不丢失
- ✅ 游戏统计满足成就感
- ✅ 排行榜增加竞争乐趣
- ✅ 任务系统增加上线动力

### 系统稳定性
- ✅ 游戏数据安全可靠
- ✅ 防作弊机制公平性
- ✅ 审计日志可追溯
- ✅ 配置化易于维护

### 社区活跃度
- ✅ 多人游戏增加互动
- ✅ 排行榜激发竞争
- ✅ 挑战系统增加话题

---

## 🧪 测试计划

### 单元测试
- 游戏创建和销毁
- 游戏状态更新
- 评分算法验证
- 难度计算

### 集成测试
- 游戏完整流程
- 多人游戏交互
- 排行榜实时更新
- 任务完成检测

### 性能测试
- 并发游戏性能
- 排行榜查询性能
- 历史记录存储性能

### 安全测试
- 防作弊机制
- 异常行为检测
- 数据篡改防护

---

## 📝 注意事项

1. **向后兼容**: 旧版本游戏数据需要迁移
2. **渐进式发布**: 优先发布核心功能，高级功能逐步开放
3. **平衡性调整**: 需要持续调整游戏平衡性
4. **用户反馈**: 收集用户反馈，及时优化
5. **性能监控**: 监控游戏系统性能指标

---

## 🔗 相关文档

- [当前功能清单](./CURRENT_FEATURES.md)
- [问题与改进空间](./ISSUES_IMPROVEMENTS.md)
- [短期迭代计划](./ROADMAP_SHORT_TERM.md)
- [用户管理系统完善计划](./USER_MANAGEMENT_PLAN.md)
- [开发规范](./DEVELOPMENT_STANDARDS.md)
- [技术优化建议](./TECHNICAL_OPTIMIZATION.md)

---

**文档版本**: v1.0  
**最后更新**: 2026-02-22  
**下次审查**: 2026-03-22