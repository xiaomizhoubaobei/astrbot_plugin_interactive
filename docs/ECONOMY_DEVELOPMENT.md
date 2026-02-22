# AstrBot 互动游戏插件 - 经济系统开发文档

## 📋 文档概述

本文档详细规划经济系统的完善方案，旨在建立健康稳定的经济体系、平衡积分产出与消耗、提供多样化的经济互动。

**版本**: v1.0  
**创建日期**: 2026-02-22  
**维护者**: 开发团队

---

## 🔍 当前状态分析

### 1. 现有功能

#### 1.1 积分系统
- **初始积分**: 新用户100积分
- **积分上限**: 无明确上限（理论上限1,000,000,000）
- **积分下限**: 0积分（不可为负）
- **积分获取**:
  - 签到: 10-110积分（基础+连续+周奖励）
  - 游戏: 1-100+积分（基于表现）
  - 抽奖: 0-100积分（SSR奖励）
- **积分消耗**:
  - 抽奖: 10积分/次
  - 商店: 30-120积分/商品
  - 物品使用: 部分消耗积分

#### 1.2 商店定价
| 商品 | 价格 | 类型 |
|------|------|------|
| 双倍积分卡 | 50 | 立即生效 |
| 免费抽奖券 | 40 | 立即生效 |
| 提示令牌 | 30 | 立即生效 |
| 幸运护符 | 100 | 立即生效 |
| 提神咖啡 | 80 | 可存储 |
| 经验卡 | 120 | 可存储 |

#### 1.3 抽奖系统
- **消耗**: 10积分/次
- **奖励**:
  - SSR: 100积分（概率5%）
  - SR: 30积分（概率10%）
  - R: 10积分（概率25%）
  - N: 0积分（概率60%）
- **期望收益**: 10积分 × (0.05×10 + 0.10×3 + 0.25×1 + 0.60×0) = 10 × 1.05 = 10.5积分
- **期望收益比**: 105%（略高于成本）

#### 1.4 游戏奖励
- **猜数字游戏**:
  - 基础分: (10 - 尝试次数) × 5，最低1分
  - 时间奖励: (60 - 用时) × 2，最低1分
  - 经验卡加成: +20%
- **典型收益**: 20-60积分/局

#### 1.5 签到奖励
- **基础奖励**: 10积分
- **连续奖励**: 每天递增2积分，最高100积分
- **周奖励**: 每7天额外50积分
- **双倍卡**: 双倍基础奖励

### 2. 已识别的问题

#### 2.1 通胀风险
- ❌ 积分产出高于消耗（抽奖期望收益105%）
- ❌ 长期玩家积分积累过多
- ❌ 缺少积分回收机制
- ❌ 缺少通胀控制措施

#### 2.2 平衡性问题
- ❌ 游戏奖励差距过大（1-100+积分）
- ❌ 新老玩家差距扩大
- ❌ 早期游戏奖励过低
- ❌ 缺少动态平衡调整

#### 2.3 经济系统单一
- ❌ 只有积分一种货币
- ❌ 缺少代币系统
- ❌ 缺少虚拟货币
- ❌ 缺少交易系统

#### 2.4 缺少经济监管
- ❌ 缺少经济数据统计
- ❌ 缺少通胀率监控
- ❌ 缺少异常交易检测
- ❌ 缺少经济分析工具

#### 2.5 功能缺失
- ❌ 缺少税务系统
- ❌ 缺少银行系统
- ❌ 缺少投资系统
- ❌ 缺少交易市场
- ❌ 缺少汇率系统

---

## 🎯 完善计划

### 阶段一：经济平衡调整（优先级：高）

#### 1.1 积分产出控制

**目标**: 控制积分产出速率，防止通胀

**实施内容**:

**签到奖励调整**:
```yaml
# config/economy.yaml

sign_in:
  base_reward: 10                  # 基础奖励
  consecutive_bonus: 2             # 连续奖励（每天递增）
  max_consecutive_bonus: 50        # 最大连续奖励（从100降至50）
  weekly_reward: 30                # 周奖励（从50降至30）
  double_card_multiplier: 1.5      # 双倍卡倍率（从2降至1.5）
```

**游戏奖励调整**:
```yaml
games:
  guess:
    base_points_formula: "max(5, (10 - attempts) * 5)"  # 最低5分
    time_bonus_formula: "max(5, (60 - time_used) * 2)"  # 最低5分
    max_total_points: 60           # 最高60分（从无限制）
    exp_card_multiplier: 1.15      # 经验卡加成（从0.2降至0.15）
```

**抽奖期望调整**:
```yaml
lottery:
  cost: 10
  rewards:
    ssr:
      probability: 0.05
      points: 80                   # 从100降至80
    sr:
      probability: 0.10
      points: 25                   # 从30降至25
    r:
      probability: 0.25
      points: 8                    # 从10降至8
    n:
      probability: 0.60
      points: 0
  
  # 新期望收益: 10 × (0.05×8 + 0.10×2.5 + 0.25×0.8) = 10 × 0.9 = 9积分
  # 期望收益比: 90%（略低于成本，控制通胀）
```

---

#### 1.2 积分回收机制

**目标**: 增加积分消耗渠道，回收过剩积分

**实施内容**:

**新增消耗方式**:

1. **税收系统**:
   - 交易税: 赠予物品收取10%税收
   - 市场税: 市场交易收取5%税收
   - 兑换税: 货币兑换收取2%税收

2. **维护费用**:
   - 牛牛维护: 每天消耗5积分
   - 房间维护: 创建房间消耗10积分
   - 公会维护: 公会每日消耗积分

3. **增值服务**:
   - 个性化称号: 1000积分
   - 自定义头像: 500积分
   - 特殊表情包: 200积分

4. **奢侈品**:
   - 限定称号: 5000积分
   - 稀有皮肤: 3000积分
   - 特殊道具: 1000积分

**税收配置**:
```yaml
tax:
  gift: 0.10                       # 赠予税10%
  market: 0.05                     # 市场税5%
  exchange: 0.02                   # 兑换税2%
  
  # 税收池
  tax_pool:
    enabled: true
    distribution:
      lottery_bonus: 0.30          # 30%用于抽奖奖池
      community_reward: 0.40       # 40%用于社区奖励
      charity: 0.30                # 30%用于慈善活动
```

---

#### 1.3 动态平衡系统

**目标**: 根据经济数据自动调整平衡

**实施内容**:

**监控指标**:
- 全网总积分
- 平均每人积分
- 积分产出率（积分/天）
- 积分消耗率（积分/天）
- 通胀率

**调整策略**:
```python
def adjust_economy(self, metrics: Dict) -> None:
    """根据经济指标调整平衡
    
    Args:
        metrics: 经济指标
    """
    inflation_rate = metrics["inflation_rate"]
    
    if inflation_rate > 0.1:  # 通胀率超过10%
        # 降低产出
        self.config["sign_in"]["base_reward"] *= 0.9
        self.config["games"]["guess"]["max_total_points"] *= 0.9
        # 提高消耗
        self.config["lottery"]["cost"] *= 1.1
        self.config["tax"]["gift"] *= 1.1
        
    elif inflation_rate < -0.05:  # 通缩率超过5%
        # 提高产出
        self.config["sign_in"]["base_reward"] *= 1.1
        self.config["games"]["guess"]["max_total_points"] *= 1.1
        # 降低消耗
        self.config["lottery"]["cost"] *= 0.9
        self.config["tax"]["gift"] *= 0.9
```

---

### 阶段二：多货币系统（优先级：高）

#### 2.1 货币体系设计

**目标**: 建立多层次的货币体系

**实施内容**:

**货币类型**:

| 货币 | 名称 | 用途 | 获取方式 | 兑换比例 |
|------|------|------|----------|----------|
| 积分 | Points | 通用货币 | 签到、游戏、任务 | 基准 |
| 金币 | Coins | 稀有货币 | 充值、活动 | 1金币 = 100积分 |
| 钻石 | Diamonds | 高级货币 | 充值、成就 | 1钻石 = 10金币 |
| 代币 | Tokens | 特殊货币 | 交易、活动 | 1代币 = 50积分 |

**数据结构**:
```python
{
    "currencies": {
        "points": 1000,              # 积分
        "coins": 10,                 # 金币
        "diamonds": 2,               # 钻石
        "tokens": 20                 # 代币
    }
}
```

**货币用途**:

1. **积分（Points）**:
   - 抽奖
   - 商店购买
   - 游戏投注
   - 日常消费

2. **金币（Coins）**:
   - 高级商品
   - 限定物品
   - 特殊服务
   - 奢侈品

3. **钻石（Diamonds）**:
   - 顶级商品
   - 专属称号
   - 特殊功能
   - VIP服务

4. **代币（Tokens）**:
   - 市场交易
   - 玩家间交易
   - 兑换服务
   - 特殊活动

---

#### 2.2 货币兑换系统

**目标**: 支持货币间兑换

**实施内容**:

**兑换规则**:
```yaml
exchange:
  # 兑换比例
  rates:
    points_to_coins: 100            # 100积分 = 1金币
    coins_to_diamonds: 10           # 10金币 = 1钻石
    points_to_tokens: 50            # 50积分 = 1代币
  
  # 兑换手续费
  fee:
    points_to_coins: 0.05           # 5%手续费
    coins_to_diamonds: 0.02         # 2%手续费
    points_to_tokens: 0.10          # 10%手续费
  
  # 兑换限制
  limits:
    daily_exchange: 1000            # 每日最大兑换1000积分
    min_exchange: 100               # 最小兑换100积分
```

**命令**:
- `exchange <目标货币> <数量>` - 兑换货币
- `exchange rates` - 查看汇率
- `exchange history` - 查看兑换历史

---

#### 2.3 充值系统

**目标**: 支持虚拟货币充值

**实施内容**:

**充值套餐**:
```yaml
# config/recharge_packages.yaml

packages:
  - id: "starter"
    name: "新手礼包"
    points: 1000
    price: "¥1.00"
    bonus: 0.0                      # 无额外赠送
  
  - id: "standard"
    name: "标准套餐"
    points: 5000
    price: "¥5.00"
    bonus: 0.10                     # 额外赠送10%
  
  - id: "premium"
    name: "高级套餐"
    points: 10000
    price: "¥10.00"
    bonus: 0.20                     # 额外赠送20%
  
  - id: "vip"
    name: "VIP套餐"
    points: 50000
    price: "¥50.00"
    bonus: 0.50                     # 额外赠送50%
    includes_diamonds: 10           # 赠送10钻石
```

**充值功能**:
- 充值记录
- 充值奖励
- 充值活动
- 充值排行榜

---

### 阶段三：银行系统（优先级：中）

#### 3.1 存款功能

**目标**: 提供积分存储和利息

**实施内容**:

**存款类型**:
1. **活期存款**:
   - 随时可存取
   - 年利率: 5%
   - 无最低存款

2. **定期存款**:
   - 锁定期限
   - 年利率: 10%
   - 到期自动转存

3. **大额存单**:
   - 大额存款
   - 年利率: 15%
   - 最低1000积分

**存款配置**:
```yaml
bank:
  savings:
    type: "demand"                  # 活期
    interest_rate: 0.05             # 年利率5%
    min_deposit: 0                  # 无最低
    max_deposit: 1000000            # 最高100万积分
  
  fixed_deposit:
    type: "fixed"                   # 定期
    interest_rate: 0.10             # 年利率10%
    periods: [7, 30, 90, 180, 365]  # 存款期限（天）
    min_deposit: 100                # 最低100积分
  
  large_deposit:
    type: "large"                   # 大额
    interest_rate: 0.15             # 年利率15%
    min_deposit: 1000               # 最低1000积分
    periods: [30, 90, 180, 365]     # 存款期限（天）
```

**命令**:
- `bank deposit <金额> [类型]` - 存款
- `bank withdraw <金额>` - 取款
- `bank balance` - 查看余额
- `bank history` - 查看交易记录

**数据结构**:
```python
{
    "bank_accounts": {
        "savings": {
            "balance": 1000,
            "last_interest_time": 1708569600000
        },
        "fixed_deposits": [
            {
                "id": "fd_1",
                "amount": 500,
                "period": 30,
                "interest_rate": 0.10,
                "start_time": 1708569600000,
                "end_time": 1711161600000,
                "status": "active"
            }
        ]
    }
}
```

---

#### 3.2 贷款功能

**目标**: 提供短期贷款服务

**实施内容**:

**贷款规则**:
- 贷款额度: 根据信用等级
- 贷款期限: 7-30天
- 贷款利率: 日利率0.5%
- 逾期惩罚: 日利率2%

**信用系统**:
```python
def calculate_credit_limit(self, user_data: Dict) -> int:
    """计算贷款额度
    
    Args:
        user_data: 用户数据
    
    Returns:
        贷款额度
    """
    base_limit = 100
    level = user_data.get("level", 1)
    history_score = user_data.get("credit_score", 100)
    
    return base_limit * level * (history_score / 100)
```

**命令**:
- `bank loan <金额> [期限]` - 申请贷款
- `bank repay <金额>` - 还款
- `bank loan status` - 查看贷款状态

---

### 阶段四：交易市场（优先级：中）

#### 4.1 玩家交易市场

**目标**: 允许玩家间交易

**实施内容**:

**市场功能**:
1. **物品交易**:
   - 发布出售
   - 购买物品
   - 拍卖功能

2. **积分交易**:
   - 积分兑换
   - 充值转让
   - 礼包交易

3. **服务交易**:
   - 代练服务
   - 任务代做
   - 带飞服务

**市场配置**:
```yaml
market:
  # 手续费
  fee: 0.05                        # 5%手续费
  
  # 上架限制
  listing_fee: 10                  # 上架费10积分
  max_listings: 10                 # 最多上架10个
  max_price: 10000                 # 最高价格10000积分
  
  # 交易保护
  escrow_enabled: true             # 启用托管
  escrow_period: 3600              # 托管期1小时
  
  # 争议处理
  dispute_timeout: 7200            # 争议处理时限2小时
```

**命令**:
- `market sell <物品ID> <价格>` - 上架出售
- `market buy <交易ID>` - 购买物品
- `market list` - 查看市场列表
- `market my` - 查看我的交易

---

#### 4.2 拍卖系统

**目标**: 支持物品拍卖

**实施内容**:

**拍卖类型**:
1. **普通拍卖**:
   - 起拍价设定
   - 加价幅度
   - 拍卖时长

2. **一口价**:
   - 固定价格
   - 先到先得
   - 无竞价

3. **荷兰拍卖**:
   - 价格递减
   - 越早越便宜
   - 卖完即止

**拍卖数据**:
```python
{
    "id": "auction_1",
    "item_id": "legendary_crystal",
    "item_name": "传说水晶",
    "seller": "user1",
    "start_price": 500,
    "current_price": 800,
    "min_increment": 50,           # 最小加价
    "buyout_price": 2000,          # 一口价
    "start_time": 1708569600000,
    "end_time": 1708656000000,
    "bids": [
        {"bidder": "user2", "price": 600, "time": 1708570000000},
        {"bidder": "user3", "price": 800, "time": 1708570500000}
    ],
    "status": "active"
}
```

**命令**:
- `auction create <物品ID> <起拍价>` - 创建拍卖
- `auction bid <拍卖ID> <出价>` - 竞价
- `auction list` - 查看拍卖列表
- `auction buyout <拍卖ID>` - 一口价购买

---

### 阶段五：投资系统（优先级：低）

#### 5.1 投资基金

**目标**: 提供投资理财功能

**实施内容**:

**基金类型**:
1. **保守型基金**:
   - 低风险
   - 年收益率: 5-10%
   - 适合稳健投资

2. **平衡型基金**:
   - 中风险
   - 年收益率: 10-20%
   - 适合平衡投资

3. **进取型基金**:
   - 高风险
   - 年收益率: 20-50%
   - 适合激进投资

**基金配置**:
```yaml
funds:
  conservative:
    name: "稳健基金"
    risk_level: "low"
    expected_return: 0.08          # 期望年收益8%
    volatility: 0.05               # 波动率5%
    min_investment: 100
    lock_period: 30                # 锁定期30天
  
  balanced:
    name: "平衡基金"
    risk_level: "medium"
    expected_return: 0.15          # 期望年收益15%
    volatility: 0.15               # 波动率15%
    min_investment: 500
    lock_period: 90
  
  aggressive:
    name: "进取基金"
    risk_level: "high"
    expected_return: 0.30          # 期望年收益30%
    volatility: 0.30               # 波动率30%
    min_investment: 1000
    lock_period: 180
```

**命令**:
- `invest <基金ID> <金额>` - 投资
- `invest withdraw <基金ID> <金额>` - 赎回
- `invest balance` - 查看投资组合
- `invest performance` - 查看收益

---

#### 5.2 股票系统

**目标**: 模拟股票交易

**实施内容**:

**股票类型**:
- **成长股**: 高成长性，高波动
- **价值股**: 稳定分红，低波动
- **科技股**: 创新驱动，中高波动

**股票交易**:
- 买入/卖出
- 持仓管理
- 收益统计
- 涨跌幅排行

**股票数据**:
```python
{
    "id": "stock_1",
    "name": "科技股A",
    "sector": "technology",
    "price": 100.0,
    "change": 5.2,                 # 涨跌幅
    "volume": 10000,               # 成交量
    "market_cap": 1000000,         # 市值
    "pe_ratio": 20.0,              # 市盈率
    "dividend_yield": 0.02         # 股息率
}
```

---

### 阶段六：经济监管系统（优先级：高）

#### 6.1 经济数据统计

**目标**: 收集和分析经济数据

**实施内容**:

**统计指标**:
```python
{
    "total_points": 10000000,      # 全网总积分
    "total_users": 1000,           # 总用户数
    "avg_points_per_user": 10000,  # 平均每人积分
    "points_inflow_today": 50000,  # 今日积分流入
    "points_outflow_today": 45000, # 今日积分流出
    "inflation_rate": 0.02,        # 通胀率2%
    "gini_coefficient": 0.35,      # 基尼系数
    "transaction_volume": 100000,  # 交易量
    "market_cap": 10000000         # 市场总值
}
```

**统计维度**:
- 时间维度: 日/周/月/年
- 用户维度: 新老用户/VIP/等级
- 功能维度: 签到/游戏/抽奖/商店
- 地域维度: 平台/群组

**命令**:
- `economy stats` - 查看经济统计
- `economy inflation` - 查看通胀率
- `economy distribution` - 查看财富分布

---

#### 6.2 异常检测

**目标**: 检测异常经济行为

**实施内容**:

**异常类型**:
1. **积分异常**:
   - 短时间内大量积分变动
   - 异常积分增长
   - 负积分

2. **交易异常**:
   - 频繁交易
   - 异常价格交易
   - 可疑交易模式

3. **行为异常**:
   - 刷积分
   - 多号作弊
   - 利用漏洞

**检测规则**:
```python
def detect_anomalies(self, user_id: str, platform: str) -> List[Dict]:
    """检测异常行为
    
    Args:
        user_id: 用户ID
        platform: 平台
    
    Returns:
        异常列表
    """
    anomalies = []
    user = self.get_user_data(user_id, platform)
    
    # 检测积分增长异常
    if user["points"] > 100000:
        anomalies.append({
            "type": "excessive_points",
            "severity": "high",
            "value": user["points"]
        })
    
    # 检测交易异常
    recent_transactions = self.get_recent_transactions(user_id, platform, hours=1)
    if len(recent_transactions) > 50:
        anomalies.append({
            "type": "excessive_transactions",
            "severity": "medium",
            "value": len(recent_transactions)
        })
    
    return anomalies
```

---

#### 6.3 自动调节系统

**目标**: 自动调整经济参数

**实施内容**:

**调节机制**:
```python
async def auto_adjust_economy(self) -> None:
    """自动调整经济参数"""
    metrics = self.get_economy_metrics()
    
    # 通胀控制
    if metrics["inflation_rate"] > 0.1:
        await self.apply_deflationary_measures()
    elif metrics["inflation_rate"] < -0.05:
        await self.apply_inflationary_measures()
    
    # 流动性管理
    if metrics["liquidity"] < 0.5:
        await self.increase_liquidity()
    elif metrics["liquidity"] > 0.8:
        await self.decrease_liquidity()
    
    # 收入分配
    gini = metrics["gini_coefficient"]
    if gini > 0.4:
        await self.redistribute_wealth()
```

---

## 📅 实施时间表

| 阶段 | 任务 | 优先级 | 预计时间 | 负责人 |
|------|------|--------|----------|--------|
| 阶段一 | 积分产出控制 | 高 | 5天 | - |
| 阶段一 | 积分回收机制 | 高 | 4天 | - |
| 阶段一 | 动态平衡系统 | 高 | 6天 | - |
| 阶段二 | 货币体系设计 | 高 | 4天 | - |
| 阶段二 | 货币兑换系统 | 高 | 5天 | - |
| 阶段二 | 充值系统 | 中 | 6天 | - |
| 阶段三 | 存款功能 | 中 | 6天 | - |
| 阶段三 | 贷款功能 | 中 | 5天 | - |
| 阶段四 | 玩家交易市场 | 中 | 8天 | - |
| 阶段四 | 拍卖系统 | 中 | 6天 | - |
| 阶段五 | 投资基金 | 低 | 8天 | - |
| 阶段五 | 股票系统 | 低 | 10天 | - |
| 阶段六 | 经济数据统计 | 高 | 5天 | - |
| 阶段六 | 异常检测 | 高 | 4天 | - |
| 阶段六 | 自动调节系统 | 高 | 6天 | - |

**总计**: 约 88 天（约 2.9 个月）

---

## 📊 预期收益

### 经济稳定
- ✅ 控制通胀率在5%以内
- ✅ 保持积分供需平衡
- ✅ 建立健康的经济循环

### 系统完善
- ✅ 多货币体系增加灵活性
- ✅ 银行系统提供金融服务
- ✅ 交易市场增加互动

### 用户价值
- ✅ 更多投资理财选择
- ✅ 更公平的经济环境
- ✅ 更丰富的经济玩法

### 运营价值
- ✅ 经济数据支持决策
- ✅ 异常检测保障安全
- ✅ 自动调节降低运维成本

---

## 🧪 测试计划

### 经济平衡测试
- 积分产出率测试
- 积分消耗率测试
- 通胀率模拟测试
- 长期经济运行测试

### 货币系统测试
- 货币兑换测试
- 汇率波动测试
- 多货币交易测试
- 充值流程测试

### 银行系统测试
- 存款利息计算测试
- 贷款审批测试
- 逾期惩罚测试
- 银行账户管理测试

### 交易市场测试
- 交易流程测试
- 手续费计算测试
- 拍卖竞价测试
- 争议处理测试

### 投资系统测试
- 基金收益计算测试
- 股票价格波动测试
- 投资组合测试
- 风险评估测试

### 监管系统测试
- 数据统计准确性测试
- 异常检测灵敏度测试
- 自动调节效果测试
- 误报率测试

---

## 📝 注意事项

1. **经济平衡**: 需要持续监控和调整
2. **风险控制**: 高风险功能需要限制
3. **用户教育**: 提供清晰的经济规则说明
4. **数据安全**: 经济数据需要加密存储
5. **合规要求**: 遵守相关法律法规

---

## 🔗 相关文档

- [当前功能清单](./CURRENT_FEATURES.md)
- [问题与改进空间](./ISSUES_IMPROVEMENTS.md)
- [短期迭代计划](./ROADMAP_SHORT_TERM.md)
- [中期迭代计划](./ROADMAP_MID_TERM.md)
- [用户管理系统完善计划](./USER_MANAGEMENT_PLAN.md)
- [游戏管理系统完善计划](./GAME_MANAGEMENT_PLAN.md)
- [娱乐功能开发文档](./ENTERTAINMENT_DEVELOPMENT.md)
- [开发规范](./DEVELOPMENT_STANDARDS.md)
- [技术优化建议](./TECHNICAL_OPTIMIZATION.md)

---

**文档版本**: v1.0  
**最后更新**: 2026-02-22  
**下次审查**: 2026-03-22