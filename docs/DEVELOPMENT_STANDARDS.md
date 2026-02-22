# AstrBot 互动游戏插件 - 开发规范

## 代码规范

### Python代码规范
- 遵循 PEP 8 编码规范
- 使用 4 空格缩进
- 最大行长度：88字符（使用 Black 默认值）
- 使用有意义的变量和函数名
- 添加类型注解（Type Hints）

### 代码示例
```python
from typing import Dict, List, Optional

class UserManager:
    """用户管理器
    
    负责用户数据的创建、更新和查询
    """
    
    def __init__(self, star_instance: Any) -> None:
        self.star = star_instance
        self.plugin_name = "astrbot_plugin_interactive"
    
    async def get_user_data(
        self, 
        user_id: str, 
        platform: str
    ) -> Dict[str, Any]:
        """获取用户数据
        
        Args:
            user_id: 用户ID
            platform: 平台ID
            
        Returns:
            用户数据字典
        """
        # 实现代码
        pass
```

### 文档字符串
- 使用 Google 风格的文档字符串
- 包含参数说明、返回值说明、异常说明
- 为公共API添加文档

---

## 测试规范

### 单元测试
- 使用 pytest 框架
- 测试覆盖率目标：≥80%
- 每个功能模块都有对应的测试

### 测试示例
```python
import pytest
from data.user_manager import UserManager

@pytest.mark.asyncio
async def test_get_user_data():
    """测试获取用户数据"""
    manager = UserManager(mock_star)
    user_data = await manager.get_user_data("test_user", "test_platform")
    
    assert user_data is not None
    assert user_data["id"] == "test_user"
    assert user_data["points"] >= 0

@pytest.mark.asyncio
async def test_add_points():
    """测试添加积分"""
    manager = UserManager(mock_star)
    await manager.add_points("test_user", "test_platform", 50)
    
    user_data = await manager.get_user_data("test_user", "test_platform")
    assert user_data["points"] >= 50
```

### 集成测试
- 测试模块间交互
- 测试数据库操作
- 测试API接口

---

## 文档规范

### API文档
- 使用 Swagger/OpenAPI 规范
- 包含请求参数、响应格式
- 添加使用示例

### README文档
- 项目简介
- 安装指南
- 使用说明
- 常见问题

### 代码注释
- 复杂逻辑添加注释
- 解释"为什么"而不是"是什么"
- 保持注释与代码同步

---

## 版本管理

### 语义化版本
- 格式：主版本号.次版本号.修订号
- 主版本号：不兼容的API修改
- 次版本号：向下兼容的功能性新增
- 修订号：向下兼容的问题修正

### Git分支策略
- `main`: 主分支，用于生产环境
- `develop`: 开发分支，用于集成新功能
- `feature/*`: 功能分支
- `bugfix/*`: 修复分支
- `release/*`: 发布分支
- `hotfix/*`: 紧急修复分支

### 提交信息规范
使用 Conventional Commits 格式：
```
<type>(<scope>): <subject>

<body>

<footer>
```

类型说明：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具链相关

示例：
```
feat(cow): 添加牛牛自动衰减机制

实现了牛牛状态随时间自动下降的功能：
- 健康度每小时下降5%
- 心情每小时下降3%
- 饱食度每小时下降8%

Closes #123
```

---

## 代码审查

### 审查清单
- [ ] 代码符合PEP 8规范
- [ ] 添加了类型注解
- [ ] 添加了文档字符串
- [ ] 添加了单元测试
- [ ] 测试覆盖率达标
- [ ] 没有引入新的安全漏洞
- [ ] 没有引入性能问题

### 审查流程
1. 创建 Pull Request
2. 至少一人审查通过
3. CI/CD 检查通过
4. 合并到目标分支

---

## 配置管理

### 配置文件
- 使用 YAML 格式
- 分环境配置（dev, test, prod）
- 敏感信息使用环境变量

### 配置示例
```yaml
# config/development.yaml
points:
  initial_points: 100
  daily_command_limit: 50
  command_cooldown: 5

sign:
  base_reward: 10
  consecutive_bonus: 2
  max_consecutive_bonus: 100
  week_bonus: 50
```

---

## 错误处理

### 异常处理原则
- 不要吞掉异常
- 记录异常日志
- 提供友好的错误信息
- 使用自定义异常类

### 错误处理示例
```python
class PluginError(Exception):
    """插件基础异常"""
    pass

class UserNotFoundError(PluginError):
    """用户未找到异常"""
    pass

class InsufficientPointsError(PluginError):
    """积分不足异常"""
    pass

async def consume_points(
    self, 
    user_id: str, 
    platform: str, 
    points: int
) -> bool:
    """消耗积分
    
    Args:
        user_id: 用户ID
        platform: 平台ID
        points: 要消耗的积分
        
    Returns:
        是否成功消耗
        
    Raises:
        InsufficientPointsError: 积分不足时抛出
    """
    if points <= 0:
        logger.warning(f"尝试消耗非正积分: {points}")
        return False
    
    user = await self.get_user_data(user_id, platform)
    if user["points"] < points:
        raise InsufficientPointsError(
            f"积分不足: 需要 {points}, 拥有 {user['points']}"
        )
    
    # 扣除积分
    user["points"] -= points
    await self.update_user_data(user_id, platform, user)
    return True
```

---

## 性能优化

### 优化原则
- 避免N+1查询
- 使用缓存
- 异步IO操作
- 批量操作

### 性能监控
- 使用性能分析工具
- 监控关键路径
- 定期性能测试

---

**文档版本**: v1.0  
**最后更新**: 2026-02-22