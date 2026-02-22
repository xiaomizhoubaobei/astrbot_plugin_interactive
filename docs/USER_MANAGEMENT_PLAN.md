# AstrBot 互动游戏插件 - 用户管理系统完善计划

## 📋 文档概述

本文档详细规划用户管理系统的完善方案，旨在提升系统的稳定性、可扩展性和用户体验。

**版本**: v1.0  
**创建日期**: 2026-02-22  
**维护者**: 开发团队

---

## 🔍 当前状态分析

### 1. 现有功能

#### 1.1 核心功能
- ✅ 用户数据持久化存储（基于 KV 存储）
- ✅ 跨平台用户支持（多平台用户隔离）
- ✅ 积分管理系统（增减、查询）
- ✅ 物品栏系统（添加、移除、查询）
- ✅ 每日命令限制（默认50次）
- ✅ 命令冷却时间（默认5秒）
- ✅ 签到系统（连续签到、累计签到）
- ✅ 成就系统追踪

#### 1.2 数据结构
```json
{
    "id": "用户ID",
    "platform": "平台标识",
    "points": 100,                    # 积分
    "last_sign": "",                  # 最后签到日期
    "consecutive_days": 0,            # 连续签到天数
    "total_sign_days": 0,             # 累计签到天数
    "games_played": 0,                # 游戏次数
    "games_won": 0,                   # 获胜次数
    "achievements": [],               # 成就列表
    "has_double_card": "False",         # 双倍积分卡状态
    "free_lottery_count": 0,          # 免费抽奖次数
    "hint_tokens": 0,                 # 提示令牌
    "lucky_charm_count": 0,           # 幸运护符
    "last_command_time": 0,           # 最后命令时间
    "daily_command_count": 0,         # 每日命令次数
    "last_command_date": "",          # 最后命令日期
    "total_spent": 0,                 # 累计消费
    "ssr_count": 0,                   # SSR次数
    "inventory": []                   # 物品栏
}
```

### 2. 已识别的问题

#### 2.1 数据验证问题
- ❌ 缺少输入参数验证
- ❌ 缺少数据边界检查（积分、物品数量等）
- ❌ 缺少数据完整性验证
- ❌ 异常数据可能导致系统不稳定

#### 2.2 性能问题
- ❌ 每次操作都需要读写 KV 存储
- ❌ 缺少缓存机制
- ❌ 频繁的数据库操作可能影响性能

#### 2.3 功能缺失
- ❌ 缺少用户数据备份机制
- ❌ 缺少用户数据恢复功能
- ❌ 缺少用户行为分析
- ❌ 缺少用户等级/成长系统
- ❌ 缺少用户黑名单/封禁机制
- ❌ 缺少数据导出功能

#### 2.4 配置管理问题
- ❌ 部分配置硬编码（如每日命令限制50次、冷却5秒）
- ❌ 缺少配置热更新机制
- ❌ 不同平台无法差异化配置

#### 2.5 安全问题
- ❌ 缺少敏感操作审计日志
- ❌ 缺少用户数据加密（如果需要）
- ❌ 缺少防刷机制（除了基本的冷却）

---

## 🎯 完善计划

### 阶段一：稳定性增强（优先级：高）

#### 1.1 数据验证层

**目标**: 确保所有用户数据的有效性和完整性

**实施内容**:

```python
# 新增数据验证模块
# data/user_validator.py

class UserValidator:
    """用户数据验证器"""

    @staticmethod
    def validate_user_id(user_id: str) -> bool:
        """验证用户ID格式"""
        if not user_id or not isinstance(user_id, str):
            return False
        if len(user_id) > 128:
            return False
        return True

    @staticmethod
    def validate_platform(platform: str) -> bool:
        """验证平台标识"""
        valid_platforms = ["qq", "telegram", "discord", "kook"]
        return platform in valid_platforms

    @staticmethod
    def validate_points(points: int) -> bool:
        """验证积分范围"""
        return 0 <= points <= 1_000_000_000

    @staticmethod
    def validate_item_count(count: int) -> bool:
        """验证物品数量"""
        return 0 <= count <= 999

    @staticmethod
    def validate_user_data(data: Dict[str, Any]) -> bool:
        """验证完整用户数据结构"""
        required_fields = [
            "id", "platform", "points", "last_sign",
            "consecutive_days", "total_sign_days",
            "games_played", "games_won", "achievements",
            "has_double_card", "free_lottery_count",
            "hint_tokens", "lucky_charm_count",
            "last_command_time", "daily_command_count",
            "last_command_date", "total_spent",
            "ssr_count", "inventory"
        ]
        # 验证必填字段
        # 验证数据类型
        # 验证数据范围
        return True
```

**集成点**:
- `get_user_data()` 后验证
- `update_user_data()` 前验证
- 所有公共方法的入口验证

**预期收益**:
- 减少90%的数据异常问题
- 提高系统稳定性
- 便于问题排查

---

#### 1.2 错误处理增强

**目标**: 统一错误处理机制，提供友好的错误提示

**实施内容**:

```python
# 新增自定义异常类
# data/exceptions.py

class UserManagementError(Exception):
    """用户管理基础异常"""
    pass

class UserNotFoundError(UserManagementError):
    """用户不存在异常"""
    pass

class InvalidUserDataError(UserManagementError):
    """无效用户数据异常"""
    pass

class InsufficientPointsError(UserManagementError):
    """积分不足异常"""
    pass

class ItemNotFoundError(UserManagementError):
    """物品不存在异常"""
    pass

class RateLimitExceededError(UserManagementError):
    """超出限制异常"""
    pass
```

**改进点**:
- 所有方法添加 try-except
- 统一日志记录格式
- 用户友好的错误消息
- 详细的调试信息

---

#### 1.3 数据边界检查

**目标**: 防止数据溢出和异常值

**实施内容**:

| 字段 | 最小值 | 最大值 | 默认值 | 处理策略 |
|------|--------|--------|--------|----------|
| points | 0 | 1,000,000,000 | 100 | 超出截断 |
| daily_command_count | 0 | 1000 | 0 | 超出限制 |
| consecutive_days | 0 | 3650 | 0 | 超出截断 |
| total_sign_days | 0 | 3650 | 0 | 超出截断 |
| games_played | 0 | 1,000,000 | 0 | 超出截断 |
| games_won | 0 | 1,000,000 | 0 | 超出截断 |
| item.count | 0 | 999 | 0 | 超出截断 |
| ssr_count | 0 | 10,000 | 0 | 超出截断 |
| total_spent | 0 | 1,000,000,000 | 0 | 超出截断 |

---

### 阶段二：性能优化（优先级：中）

#### 2.1 缓存机制

**目标**: 减少 KV 存储访问频率，提升响应速度

**实施内容**:

```python
# 新增缓存管理器
# data/cache_manager.py

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from astrbot.api import logger

class UserCache:
    """用户数据缓存"""

    def __init__(self, ttl: int = 300):
        """初始化缓存
        
        Args:
            ttl: 缓存过期时间（秒），默认5分钟
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.timestamps: Dict[str, datetime] = {}
        self.ttl = ttl

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """从缓存获取数据"""
        if key not in self.cache:
            return None
        
        # 检查是否过期
        if datetime.now() - self.timestamps[key] > timedelta(seconds=self.ttl):
            self.invalidate(key)
            return None
        
        logger.debug(f"[UserCache] 命中缓存: {key}")
        return self.cache[key].copy()

    def set(self, key: str, data: Dict[str, Any]) -> None:
        """设置缓存"""
        self.cache[key] = data.copy()
        self.timestamps[key] = datetime.now()
        logger.debug(f"[UserCache] 设置缓存: {key}")

    def invalidate(self, key: str) -> None:
        """使缓存失效"""
        self.cache.pop(key, None)
        self.timestamps.pop(key, None)
        logger.debug(f"[UserCache] 缓存失效: {key}")

    def clear(self) -> None:
        """清空所有缓存"""
        self.cache.clear()
        self.timestamps.clear()
        logger.info("[UserCache] 清空所有缓存")
```

**集成策略**:
- 读操作优先使用缓存
- 写操作更新缓存
- 定期清理过期缓存
- 提供手动刷新接口

**预期收益**:
- 减少70%的 KV 存储读取
- 响应时间提升50%
- 降低服务器负载

---

#### 2.2 批量操作优化

**目标**: 支持批量用户数据操作

**实施内容**:

```python
async def batch_get_users(self, user_ids: List[Tuple[str, str]]) -> Dict[str, Dict[str, Any]]:
    """批量获取用户数据
    
    Args:
        user_ids: [(user_id, platform), ...]
    
    Returns:
        {user_key: user_data, ...}
    """
    results = {}
    for user_id, platform in user_ids:
        key = self._get_user_key(user_id, platform)
        results[key] = await self.get_user_data(user_id, platform)
    return results

async def batch_update_users(self, updates: List[Tuple[str, str, Dict[str, Any]]]) -> None:
    """批量更新用户数据
    
    Args:
        updates: [(user_id, platform, data), ...]
    """
    for user_id, platform, data in updates:
        await self.update_user_data(user_id, platform, data)
```

**使用场景**:
- 排行榜查询
- 批量奖励发放
- 数据统计分析

---

### 阶段三：功能扩展（优先级：中）

#### 3.1 用户成长系统

**目标**: 添加用户等级和经验系统

**实施内容**:

**新增字段**:
```python
{
    "level": 1,                # 用户等级
    "exp": 0,                  # 当前经验
    "exp_to_next": 100,        # 升级所需经验
    "title": "新手",           # 称号
    "level_up_rewards": []     # 已领取的升级奖励
}
```

**等级经验表**:
| 等级 | 升级所需经验 | 称号 | 奖励 |
|------|--------------|------|------|
| 1 | 100 | 新手 | - |
| 2 | 200 | 游戏初学者 | 50积分 |
| 3 | 300 | 游戏爱好者 | 100积分 |
| 4 | 500 | 游戏达人 | 200积分 |
| 5 | 800 | 游戏专家 | 双倍积分卡×1 |
| 6 | 1200 | 游戏大师 | 500积分 |
| 7 | 1800 | 游戏宗师 | 免费抽奖券×2 |
| 8 | 2800 | 游戏王者 | 幸运护符×1 |
| 9 | 4200 | 游戏传说 | 1000积分 |
| 10 | 6000 | 游戏之神 | 稀有称号 |

**获得经验的方式**:
- 签到: +10 EXP
- 完成游戏: +5 EXP
- 获得胜利: +10 EXP
- 完成任务: +20 EXP
- 解锁成就: +50 EXP
- 消费积分: 每100积分+1 EXP

---

#### 3.2 用户行为分析

**目标**: 记录用户行为数据，支持后续分析

**实施内容**:

**新增字段**:
```python
{
    "behavior_logs": [],       # 行为日志（最多保留100条）
    "last_active_date": "",    # 最后活跃日期
    "total_online_days": 0,    # 累计活跃天数
    "favorite_activities": []  # 喜好活动统计
}
```

**行为日志格式**:
```python
{
    "timestamp": 1708569600000,
    "action": "sign",
    "details": {"type": "daily"},
    "reward": {"points": 10}
}
```

**统计分析**:
- 日活跃用户数 (DAU)
- 用户留存率
- 功能使用频率
- 平均游戏时长

---

#### 3.3 用户管理工具

**目标**: 提供管理员管理用户的工具

**实施内容**:

```python
async def ban_user(self, user_id: str, platform: str, reason: str, duration: int) -> bool:
    """封禁用户
    
    Args:
        user_id: 用户ID
        platform: 平台
        reason: 封禁原因
        duration: 封禁时长（小时），0表示永久
    
    Returns:
        是否成功
    """
    pass

async def unban_user(self, user_id: str, platform: str) -> bool:
    """解封用户
    
    Args:
        user_id: 用户ID
        platform: 平台
    
    Returns:
        是否成功
    """
    pass

async def reset_user_data(self, user_id: str, platform: str) -> bool:
    """重置用户数据
    
    Args:
        user_id: 用户ID
        platform: 平台
    
    Returns:
        是否成功
    """
    pass

async def get_user_statistics(self, user_id: str, platform: str) -> Dict[str, Any]:
    """获取用户统计数据
    
    Returns:
        统计数据字典
    """
    pass

async def export_user_data(self, user_id: str, platform: str) -> Dict[str, Any]:
    """导出用户数据
    
    Returns:
        用户数据字典
    """
    pass

async def import_user_data(self, user_id: str, platform: str, data: Dict[str, Any]) -> bool:
    """导入用户数据
    
    Args:
        user_id: 用户ID
        platform: 平台
        data: 用户数据
    
    Returns:
        是否成功
    """
    pass
```

---

### 阶段四：配置管理（优先级：中）

#### 4.1 配置化改造

**目标**: 将硬编码配置移至配置文件

**新增配置文件**:
```yaml
# config/user_management.yaml

# 用户管理配置
user_management:
  # 积分配置
  points:
    initial: 100
    max: 1_000_000_000
    min: 0
  
  # 命令限制
  command_limits:
    daily: 50
    cooldown_ms: 5000
    max_daily: 1000
  
  # 签到配置
  sign_in:
    base_reward: 10
    consecutive_bonus: 2
    max_consecutive_bonus: 100
    weekly_reward: 50
  
  # 物品栏配置
  inventory:
    max_slots: 100
    max_item_count: 999
  
  # 等级配置
  level:
    max_level: 10
    exp_table:
      1: 100
      2: 200
      3: 300
      4: 500
      5: 800
      6: 1200
      7: 1800
      8: 2800
      9: 4200
      10: 6000
  
  # 缓存配置
  cache:
    enabled: true
    ttl: 300
    max_size: 1000
```

**加载配置**:
```python
# data/user_config.py
import yaml
from pathlib import Path
from typing import Dict, Any

class UserConfig:
    """用户管理配置加载器"""
    
    _instance = None
    _config: Dict[str, Any] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if self._config is not None:
            return self._config
        
        config_path = Path(__file__).parent.parent / "config" / "user_management.yaml"
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)
        return self._config
    
    def get(self, key: str, default=None) -> Any:
        """获取配置项"""
        config = self.load_config()
        keys = key.split('.')
        value = config
        for k in keys:
            value = value.get(k, {})
            if not isinstance(value, dict) and k != keys[-1]:
                return default
        return value if key in str(config) else default
```

---

#### 4.2 平台差异化配置

**目标**: 支持不同平台的差异化配置

**配置结构**:
```yaml
platform_configs:
  qq:
    command_limits:
      daily: 50
      cooldown_ms: 5000
  telegram:
    command_limits:
      daily: 100
      cooldown_ms: 3000
  discord:
    command_limits:
      daily: 75
      cooldown_ms: 4000
```

---

### 阶段五：安全性增强（优先级：中）

#### 5.1 审计日志

**目标**: 记录敏感操作，便于追踪和审计

**实施内容**:

```python
# 新增审计日志模块
# data/audit_logger.py

from datetime import datetime
from typing import Dict, Any

class AuditLogger:
    """审计日志记录器"""
    
    async def log_action(
        self,
        user_id: str,
        platform: str,
        action: str,
        details: Dict[str, Any],
        status: str = "success"
    ) -> None:
        """记录操作日志
        
        Args:
            user_id: 用户ID
            platform: 平台
            action: 操作类型
            details: 操作详情
            status: 操作状态
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "platform": platform,
            "action": action,
            "details": details,
            "status": status
        }
        # 写入审计日志
        logger.info(f"[AUDIT] {log_entry}")
```

**需要审计的操作**:
- 用户数据修改
- 积分变动
- 物品获得/消耗
- 管理员操作（封禁、解封等）
- 异常操作

---

#### 5.2 防刷机制增强

**目标**: 加强防刷机制，防止恶意刷积分

**实施内容**:

1. **IP 限制**:（如果平台支持）
   - 同IP每分钟请求限制
   - 同IP每小时请求限制

2. **行为模式检测**:
   - 检测异常高频操作
   - 检测异常时间模式
   - 自动触发警报

3. **验证码机制**:
   - 可疑操作要求验证
   - 管理员操作二次验证

---

### 阶段六：数据备份与恢复（优先级：低）

#### 6.1 自动备份

**目标**: 定期备份用户数据，防止数据丢失

**实施内容**:

```python
# 新增备份管理器
# data/backup_manager.py

from datetime import datetime
import json
from pathlib import Path

class BackupManager:
    """数据备份管理器"""
    
    def __init__(self, backup_dir: str = "backups"):
        """初始化备份管理器
        
        Args:
            backup_dir: 备份目录
        """
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
    
    async def create_backup(self, user_data: Dict[str, Any]) -> str:
        """创建备份
        
        Args:
            user_data: 用户数据
        
        Returns:
            备份文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"user_backup_{timestamp}.json"
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)
        
        return str(backup_file)
    
    async def restore_backup(self, backup_file: str) -> Dict[str, Any]:
        """恢复备份
        
        Args:
            backup_file: 备份文件路径
        
        Returns:
            用户数据
        """
        with open(backup_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    async def list_backups(self) -> list:
        """列出所有备份
        
        Returns:
            备份文件列表
        """
        return sorted(self.backup_dir.glob("user_backup_*.json"))
    
    async def clean_old_backups(self, keep_days: int = 30) -> None:
        """清理旧备份
        
        Args:
            keep_days: 保留天数
        """
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        for backup_file in self.list_backups():
            file_date = datetime.strptime(
                backup_file.stem.split("_")[2],
                "%Y%m%d%H%M%S"
            )
            if file_date < cutoff_date:
                backup_file.unlink()
```

---

#### 6.2 数据迁移工具

**目标**: 支持数据格式升级和迁移

**实施内容**:

```python
async def migrate_user_data(self, old_data: Dict[str, Any], version: str) -> Dict[str, Any]:
    """迁移用户数据
    
    Args:
        old_data: 旧版本数据
        version: 旧数据版本
    
    Returns:
        新版本数据
    """
    migrations = {
        "0.1.0": self._migrate_v010_to_v020,
        "0.2.0": self._migrate_v020_to_v030,
    }
    
    if version in migrations:
        return await migrations[version](old_data)
    
    return old_data

async def _migrate_v010_to_v020(self, data: Dict[str, Any]) -> Dict[str, Any]:
    """从 v0.1.0 迁移到 v0.2.0"""
    # 添加新字段
    if "level" not in data:
        data["level"] = 1
        data["exp"] = 0
        data["exp_to_next"] = 100
        data["title"] = "新手"
        data["level_up_rewards"] = []
    return data
```

---

## 📅 实施时间表

| 阶段 | 任务 | 优先级 | 预计时间 | 负责人 |
|------|------|--------|----------|--------|
| 阶段一 | 数据验证层 | 高 | 3天 | - |
| 阶段一 | 错误处理增强 | 高 | 2天 | - |
| 阶段一 | 数据边界检查 | 高 | 2天 | - |
| 阶段二 | 缓存机制 | 中 | 4天 | - |
| 阶段二 | 批量操作优化 | 中 | 3天 | - |
| 阶段三 | 用户成长系统 | 中 | 5天 | - |
| 阶段三 | 用户行为分析 | 中 | 4天 | - |
| 阶段三 | 用户管理工具 | 中 | 5天 | - |
| 阶段四 | 配置化改造 | 中 | 3天 | - |
| 阶段四 | 平台差异化配置 | 中 | 2天 | - |
| 阶段五 | 审计日志 | 中 | 3天 | - |
| 阶段五 | 防刷机制增强 | 中 | 4天 | - |
| 阶段六 | 自动备份 | 低 | 3天 | - |
| 阶段六 | 数据迁移工具 | 低 | 3天 | - |

**总计**: 约 46 天（约 1.5 个月）

---

## 📊 预期收益

### 稳定性提升
- ✅ 减少 90% 的数据异常问题
- ✅ 提升 95% 的错误处理覆盖率
- ✅ 实现零数据丢失

### 性能提升
- ✅ 响应时间提升 50%
- ✅ KV 存储读取减少 70%
- ✅ 支持更高并发用户

### 功能完善
- ✅ 用户等级系统提升用户粘性
- ✅ 行为分析支持运营决策
- ✅ 管理工具提升运维效率

### 安全性增强
- ✅ 完整的审计日志
- ✅ 更强的防刷机制
- ✅ 数据备份保障

---

## 🧪 测试计划

### 单元测试
- 数据验证函数测试
- 错误处理测试
- 边界条件测试
- 缓存机制测试

### 集成测试
- 用户完整生命周期测试
- 多平台用户隔离测试
- 并发操作测试
- 数据备份恢复测试

### 性能测试
- 缓存命中率测试
- 批量操作性能测试
- 高并发压力测试
- 长期运行稳定性测试

### 安全测试
- 异常数据注入测试
- 刷积分防护测试
- 权限控制测试

---

## 📝 注意事项

1. **向后兼容**: 所有改动需要保证向后兼容，旧数据需要自动迁移
2. **渐进式实施**: 优先实施高优先级任务，低优先级任务可延后
3. **充分测试**: 每个阶段完成后需要充分测试再进入下一阶段
4. **文档更新**: 实施过程中同步更新相关文档
5. **性能监控**: 实施过程中持续监控性能指标

---

## 🔗 相关文档

- [当前功能清单](./CURRENT_FEATURES.md)
- [问题与改进空间](./ISSUES_IMPROVEMENTS.md)
- [短期迭代计划](./ROADMAP_SHORT_TERM.md)
- [开发规范](./DEVELOPMENT_STANDARDS.md)
- [技术优化建议](./TECHNICAL_OPTIMIZATION.md)

---

**文档版本**: v1.0  
**最后更新**: 2026-02-22  
**下次审查**: 2026-03-22