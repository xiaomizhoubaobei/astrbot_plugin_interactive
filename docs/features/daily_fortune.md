# 每日一签 - 开发文档

## 功能概述

每日一签是一个基于运势系统的每日互动功能，用户每天可以抽取当天的运势，获得诗句、格言等文化内容。该功能增加用户登录动机，具有社交传播性。

## 需求分析

### 功能需求

#### 核心功能
- 每日限抽：每天1次免费抽取
- 运势系统：5种运势（大吉、吉、平、凶、大凶）
- 诗词格言：文化内容展示
- 解签系统：运势解读
- 分享功能：生成分享文本

#### 运势类型
1. **大吉**：运势极佳，幸运值高
2. **吉**：运势良好，事事顺利
3. **平**：运势平稳，平平淡淡
4. **凶**：运势不佳，需谨慎
5. **大凶**：运势很差，注意避凶

#### 奖励机制
- 大吉：20积分
- 吉：15积分
- 平：10积分
- 凶：5积分
- 大凶：0积分（安慰分）

### 非功能需求
- 每日0点重置
- 响应时间：<1秒
- 支持多平台

## 技术设计

### 数据结构

```python
# 运势数据
{
    "id": "str",              # 运势ID
    "type": "str",            # 运势类型
    "emoji": "str",           # 显示emoji
    "title": "str",           # 标题
    "description": "str",     # 描述
    "poem": "str",            # 诗词/格言
    "poet": "str",            # 作者
    "advice": "str",          # 建议
    "lucky_items": "list",    # 幸运物品
    "avoid_items": "list",    # 避忌物品
    "probability": "float",   # 概率
    "reward": "int"           # 积分奖励
}

# 用户数据扩展
{
    "fortune_last_date": "str",     # 上次抽签日期
    "fortune_history": "list",      # 历史记录
    "fortune_streak": "int",        # 连续抽签天数
    "total_fortune_count": "int"    # 总抽签次数
}
```

### 运势配置

```yaml
fortune_types:
  - id: "great_luck"
    type: "大吉"
    emoji: "🌟"
    probability: 0.10
    reward: 20
    title: "鸿运当头"
    description: "今日运势极佳，诸事顺遂"
    advice: "适合做重要决定，把握机会"
    lucky_items: ["红色", "数字8", "东方"]
    avoid_items: ["黑色", "数字4", "西方"]
    
  - id: "good_luck"
    type: "吉"
    emoji: "✨"
    probability: 0.25
    reward: 15
    title: "吉星高照"
    description: "今日运势良好，顺利无碍"
    advice: "积极行动，会有好结果"
    lucky_items: ["黄色", "数字3", "南方"]
    avoid_items: ["白色", "数字7", "北方"]
    
  - id: "neutral"
    type: "平"
    emoji: "😊"
    probability: 0.40
    reward: 10
    title: "平平淡淡"
    description: "今日运势平稳，一切如常"
    advice: "保持平常心，稳步前行"
    lucky_items: ["绿色", "数字5", "中心"]
    avoid_items: ["无"]
    
  - id: "bad_luck"
    type: "凶"
    emoji: "😟"
    probability: 0.20
    reward: 5
    title: "运势不佳"
    description: "今日运势不佳，需谨慎行事"
    advice: "避免冒险，保持低调"
    lucky_items: ["蓝色", "数字2", "休息"]
    avoid_items: ["冲动", "急躁"]
    
  - id: "great_bad"
    type: "大凶"
    emoji: "😰"
    probability: 0.05
    reward: 0
    title: "运势很差"
    description: "今日运势很差，需格外小心"
    advice: "避免做重要决定，多休息"
    lucky_items: ["白色", "数字1", "静养"]
    avoid_items: ["所有决策", "外出"]
```

### 诗词库

```python
POEMS = [
    {
        "text": "春风得意马蹄疾，一日看尽长安花",
        "poet": "孟郊",
        "dynasty": "唐",
        "type": "励志"
    },
    {
        "text": "长风破浪会有时，直挂云帆济沧海",
        "poet": "李白",
        "dynasty": "唐",
        "type": "励志"
    },
    # ... 更多诗词
]
```

### 模块设计

```
fortune/
├── __init__.py
├── data/
│   ├── fortune_database.py   # 运势数据库
│   └── poem_library.py       # 诗词库
├── logic/
│   ├── fortune_system.py     # 运势系统
│   └── draw_fortune.py       # 抽签逻辑
└── command/
    └── fortune_command.py    # 命令处理
```

### 接口设计

#### 命令接口
```
fortune draw                 # 抽取运势
fortune history              # 查看历史
fortune share                # 分享运势
fortune status               # 查看状态
```

#### API接口
```python
class FortuneSystem:
    def __init__(self, user_manager, fortune_database)
    
    async def draw_fortune(self, user_id: str, platform: str) -> dict
        """抽取运势"""
        
    async def get_history(self, user_id: str, platform: str) -> list
        """获取历史记录"""
        
    async def get_share_text(self, user_id: str, platform: str) -> str
        """获取分享文本"""
        
    def calculate_fortune(self, user_id: str) -> dict
        """计算运势（可加入用户因素）"""
```

### 配置项

```yaml
fortune:
  daily_limit: 1              # 每日限制次数
  reset_time: "00:00"         # 重置时间
  show_streak: true           # 显示连续天数
  consecutive_bonus: 5        # 连续奖励
  share_reward: 10            # 分享奖励
```

## 实现步骤

### 阶段一：数据准备（1天）
1. 收集运势描述
2. 收集诗词格言
3. 创建运势数据库
4. 添加概率配置

### 阶段二：核心逻辑（2天）
1. 实现抽签逻辑
2. 实现运势计算
3. 实现重置机制
4. 集成奖励系统

### 阶段三：用户功能（1天）
1. 实现历史记录
2. 实现连续天数
3. 实现分享功能
4. 优化显示效果

### 阶段四：测试优化（1天）
1. 概率测试
2. 重置测试
3. 用户测试
4. 效果优化

## 分享文本生成

```python
def generate_share_text(fortune: dict, user_name: str) -> str:
    """生成分享文本"""
    text = f"""
🌟 {user_name}的今日运势 🌟

{fortune['emoji']} {fortune['type']} - {fortune['title']}

📝 {fortune['description']}

💡 建议：{fortune['advice']}

🍀 幸运物品：{', '.join(fortune['lucky_items'])}
⚠️ 避忌：{', '.join(fortune['avoid_items'])}

📜 今日诗词：
{fortune['poem']}
— {fortune['poet']}

✨ 积分奖励：+{fortune['reward']}

#AstrBot #每日运势
    """
    return text.strip()
```

## 成就系统

```python
ACHIEVEMENTS = [
    {
        "id": "fortune_seeker",
        "name": "运势追寻者",
        "description": "连续抽签7天",
        "reward": 100
    },
    {
        "id": "lucky_star",
        "name": "幸运之星",
        "description": "抽中3次大吉",
        "reward": 150
    },
    {
        "id": "poetry_lover",
        "name": "诗词爱好者",
        "description": "收集到50首不同诗词",
        "reward": 80
    }
]
```

## 测试计划

### 功能测试
- 抽签流程
- 重置机制
- 奖励发放
- 历史记录

### 概率测试
- 运势分布验证
- 长期统计测试
- 边界情况测试

### 用户测试
- 可用性测试
- 显示效果测试
- 分享功能测试

## 预期效果

- 日活跃度：+25%
- 完成率：≥95%
- 分享率：≥20%
- 用户满意度：≥90%

## 风险与挑战

### 技术风险
- 运势概率不平衡
- 重置机制问题
- 内容重复问题

### 解决方案
- 数据统计调整
- 时区处理
- 内容去重

---

**文档版本**: v1.0  
**创建日期**: 2026-02-22