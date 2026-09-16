# astrbot_plugin_interactive

![GitHub Repo stars](https://img.shields.io/github/stars/xiaomizhoubaobei/astrbot_plugin_interactive)
![GitHub forks](https://img.shields.io/github/forks/xiaomizhoubaobei/astrbot_plugin_interactive)
![GitHub watchers](https://img.shields.io/github/watchers/xiaomizhoubaobei/astrbot_plugin_interactive)
[![GitHub issues](https://img.shields.io/github/issues/xiaomizhoubaobei/astrbot_plugin_interactive)](https://github.com/xiaomizhoubaobei/astrbot_plugin_interactive/issues)
[![GitHub license](https://img.shields.io/github/license/xiaomizhoubaobei/astrbot_plugin_interactive)](https://github.com/xiaomizhoubaobei/astrbot_plugin_interactive/blob/main/LICENSE)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/xiaomizhoubaobei/astrbot_plugin_interactive)](https://github.com/xiaomizhoubaobei/astrbot_plugin_interactive/releases)
[![Commit Activity](https://img.shields.io/github/commit-activity/w/xiaomizhoubaobei/astrbot_plugin_interactive)](https://github.com/xiaomizhoubaobei/astrbot_plugin_interactive)
![GitHub last commit](https://img.shields.io/github/last-commit/xiaomizhoubaobei/astrbot_plugin_interactive)
![GitHub contributors](https://img.shields.io/github/contributors/xiaomizhoubaobei/astrbot_plugin_interactive)
![Python Version](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Repo Size](https://img.shields.io/github/repo-size/xiaomizhoubaobei/astrbot_plugin_interactive.svg)

一个功能丰富的AsrBot互动游戏插件，包含猜数字、签到、抽奖、商店、成就系统和牛牛系统等功能。

## 功能特性

### 🎲 猜数字游戏 (`/guess`)
- 有趣的猜数字游戏
- 时间奖励机制
- 积分奖励系统

### ✅ 每日签到 (`/sign`)
- 每日签到获取积分
- 连续签到奖励
- 周奖励机制

### 🎰 抽奖系统 (`/lottery`)
- 消耗积分进行抽奖
- SSR/SR/R稀有度设定
- 不同等级对应不同奖励

### 🛒 积分商店 (`/shop`)
- 多样化商品
- 使用积分购买道具
- 包含双倍卡、抽奖券、提示令牌等道具

### 📦 物品系统 (`/inventory`)
- 个人物品栏管理
- 物品使用功能 (`/use`)

### 🏆 成就系统 (`/achievements`)
- 丰富的成就解锁
- 用户进度追踪

### 👤 个人资料 (`/profile`)
- 查看个人统计数据
- 展示用户游戏历史

### 🐄 牛牛系统 (`/cow`)
- 有趣的宠物养成玩法
- 喂养、玩耍互动
- 等级与好感度系统

### 🎡 幸运转盘 (`/spin`)
- 多种奖励机制
- 可自定义的奖品池
- 激动人心的转盘体验

## 安装

1. 确保已安装并运行 AstrBot
2. 将此插件放入 AstrBot 的 plugins 目录
3. 重启 AstrBot 使插件生效

## 配置

插件具有详细的配置选项，涵盖：

- 积分系统配置（初始积分、命令限制、冷却时间）
- 签到奖励配置（基础奖励、连续签到奖励）
- 抽奖系统配置（费用、各稀有度概率、奖励金额）
- 猜数字游戏配置（最大数字、基础奖励、时间奖励）
- 牛牛系统配置（喂养成本、亲密度恢复等）
- 商店配置（商品价格）

## 命令列表

- `/guess [number]` - 参与猜数字游戏
- `/sign` - 每日签到
- `/lottery` - 进行抽奖
- `/shop [action] [item_id]` - 访问积分商店
- `/use [item_id]` - 使用物品
- `/inventory` - 查看背包
- `/achievements` - 查看成就
- `/profile` - 查看个人资料
- `/cow [action] [nickname]` - 牛牛系统交互
- `/spin [options]` - 幸运转盘
- `/interactive` - 插件帮助

## 项目结构

```
.
├── main.py                 # 插件主入口
├── commands/               # 各功能命令实现
│   ├── achievements.py     # 成就系统
│   ├── cow.py             # 牛牛系统
│   ├── guess.py           # 猜数字游戏
│   ├── inventory.py       # 物品栏管理
│   ├── lottery.py         # 抽奖系统
│   ├── profile.py         # 个人资料
│   ├── shop.py            # 商店系统
│   ├── sign.py            # 签到系统
│   └── use.py             # 物品使用
├── data/                   # 数据存储
│   ├── UserManager.py     # 用户数据管理
│   └── GameManager.py     # 游戏数据管理
├── utils/                  # 工具函数
│   └── logger_manager.py  # 日志管理
├── docs/                   # 文档
├── config/                 # 配置文件（如存在）
├── metadata.yaml           # 插件元数据
├── CONTRIBUTING.md        # 贡献指南
├── FEATURE_ROADMAP.md     # 功能路线图
└── README.md              # 项目说明
```

## 🔗 链上存证

本插件的**创建记录**与**全部版本（v0.0.1 / v0.0.2 / v0.0.3）**均已通过蚂蚁链开放联盟链完成**链上存证**，
可公开核验、不可篡改。存证编号 `#5`（创建）、`#6`~`#8`（版本发布），
合约 `AstrBotPluginDeposit`（`0x377e1ffe…28e03`，链 `a00e36c5`）。

| 编号 | 类别 | 版本 | 交易 hash |
|------|------|------|-----------|
| `#5` | 插件创建 | — | `ed09f218…d6534b` |
| `#6` | 版本发布 | `v0.0.1` | `b0551201…6f50f1c` |
| `#7` | 版本发布 | `v0.0.2` | `b4539979…9ec1a10` |
| `#8` | 版本发布 | `v0.0.3` | `2f795a8a…a4852ba` |

> 完整明细（commit / 产物 SHA256 指纹 / 区块高度 / gasUsed）与核验命令见 [DEPOSIT.md](./DEPOSIT.md)。

## 贡献

我们欢迎各种形式的贡献！请参阅 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解如何开始。

## 许可证

本项目遵循 [LICENSE](./LICENSE) 文件中指定的许可证协议。

## 支持

如果您在使用过程中遇到问题，请查看以下资源：

- 查看 [Issues](https://github.com/xiaomizhoubaobei/astrbot_plugin_interactive/issues) 页面是否已有类似问题
- 提交新的 Issue 以报告 Bug 或请求新功能
- 参考相关文档获取更多信息