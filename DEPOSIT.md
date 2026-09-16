# 链上存证说明（Blockchain Attestation）

本插件的**创建记录**与**全部版本（git tag）**均已通过蚂蚁链开放联盟链（myevm）的
**AstrBot 插件存证合约（`AstrBotPluginDeposit`）** 完成链上存证，可公开核验、不可篡改。

- **合约地址**：`0x377e1ffe880072164581de8258864c2df95820e187fbfc84eeb476e966c28e03`
- **链 ID**：`a00e36c5`（蚂蚁链开放联盟链）
- **存证组织路径**：`XMZZUZHI/Astrbot`
- **合约版本**：`1.1.0`

> 说明：本仓库（CNB 侧，`cnb.cool/XMZZUZHI/Astrbot/astrbot_plugin_interactive`）未打 git tag；
> **git tag 仅存在于 GitHub 镜像仓库**（`metadata.yaml` 的 `repo` 字段所指
> `github.com/xiaomizhoubaobei/astrbot_plugin_interactive`）。因此版本存证以
> **GitHub 镜像的 tag 为真源**，读取 tag → commit → 产物指纹。

## 插件创建存证

| 项目 | 值 |
|------|-----|
| 存证编号 | `#5` |
| 类别 | 插件创建 `PluginCreation` |
| 仓库 | `XMZZUZHI/Astrbot/astrbot_plugin_interactive` |
| 插件名 | `astrbot_plugin_interactive` |
| 创建 commit | `3735f8519062da113a14f030061bd94da1ccd2c2`（Initial commit） |
| 产物摘要 (SHA256) | 创建时为空串（`""`） |
| **交易 hash** | `ed09f2189f485512092878cf390c1ad5b37d2fffe0c5eb8db13efa8e09d6534b` |
| 区块高度 | `182778143` |
| gasUsed | `416,445` |
| 上链结果 | `result=0`（成功） |

## 版本（tag）存证

本插件共有 **3 个 tag**，全部已存证：

### tag `v0.0.1`

| 项目 | 值 |
|------|-----|
| 存证编号 | `#6` |
| 类别 | 版本发布 `ReleasePublish` |
| 版本号 | `v0.0.1` |
| 来源 | **GitHub 镜像 tag**（真源） |
| commit | `0f2dce831245173995e779981cc7414eedced5c2` |
| 产物摘要 (SHA256) | `f57ad782b3472b6f5d79cc004e8463fe73a2180207778eee8ce8bcc6da5ecb80` |
| **交易 hash** | `b05512019b75cb90621364d42617bbbf47f43e66e3fef6c0a4c6a7e836f50f1c` |
| 区块高度 | `182778149` |
| gasUsed | `546,825` |
| 上链结果 | `result=0`（成功） |

### tag `v0.0.2`

| 项目 | 值 |
|------|-----|
| 存证编号 | `#7` |
| 类别 | 版本发布 `ReleasePublish` |
| 版本号 | `v0.0.2` |
| 来源 | **GitHub 镜像 tag**（真源） |
| commit | `7cb3c766d41a3040cbe24656b6ec4f3a29bed499` |
| 产物摘要 (SHA256) | `8ec2d49d44549a989c7e5658df042cc93b637f32b399da1522520228c021e1f8` |
| **交易 hash** | `b4539979fc07daeec19083b9f0eabfbea35162765dc8e777eb7e55a009ec1a10` |
| 区块高度 | `182778151` |
| gasUsed | `546,825` |
| 上链结果 | `result=0`（成功） |

### tag `v0.0.3`（当前 `metadata.yaml.version`）

| 项目 | 值 |
|------|-----|
| 存证编号 | `#8` |
| 类别 | 版本发布 `ReleasePublish` |
| 版本号 | `v0.0.3` |
| 来源 | **GitHub 镜像 tag**（真源） |
| commit | `30fada91866c092b852069bb3000f31fb293a8b8` |
| 产物摘要 (SHA256) | `33f88df6af8ba5c45b83098f9776669da03a440cbedf8946c392798ca06c45e5` |
| **交易 hash** | `2f795a8a64c50e93908592d4505df1500952e381ab080bd4a35053121a4852ba` |
| 区块高度 | `182778153` |
| gasUsed | `546,825` |
| 上链结果 | `result=0`（成功） |

## 产物摘要（digest）如何计算

摘要取自 **确定性 tar 归档**，任何环境均可复现同一指纹：

```bash
git archive --format=tar <tag-or-commit> | sha256sum
```

> `zip` / `tar.gz` 含时间戳等非确定性字段，同一源码在不同环境会产生不同指纹，故不采用。

## 如何核验

在「蚂蚁链开放联盟链浏览器」按合约地址搜索，或用配套脚本
`chain-contracts`（`scripts/contract_astrbot_plugin.py`）查询：

```bash
# 凭交易 hash 一步还原「本次存证了啥」（推荐）
python3 scripts/contract_astrbot_plugin.py verify-tx \
  --hash 2f795a8a64c50e93908592d4505df1500952e381ab080bd4a35053121a4852ba --name AstrBotPluginDeposit

# 按插件名查询全部存证编号 → 应为 [5,6,7,8]
python3 scripts/contract_astrbot_plugin.py query-by-plugin \
  --plugin astrbot_plugin_interactive --name AstrBotPluginDeposit

# 按版本号查询
python3 scripts/contract_astrbot_plugin.py query-by-release \
  --plugin astrbot_plugin_interactive --tag v0.0.3 --name AstrBotPluginDeposit

# 按 commit 查询（创建）
python3 scripts/contract_astrbot_plugin.py query-by-commit \
  --commit 3735f8519062da113a14f030061bd94da1ccd2c2 --name AstrBotPluginDeposit

# 按 commit 查询（tag v0.0.3 真源）
python3 scripts/contract_astrbot_plugin.py query-by-commit \
  --commit 30fada91866c092b852069bb3000f31fb293a8b8 --name AstrBotPluginDeposit

# 查看完整存证记录
python3 scripts/contract_astrbot_plugin.py get-evidence-detail \
  --id 8 --name AstrBotPluginDeposit
```

## 存证一览（速查）

| 编号 | 类别 | 版本 | 交易 hash |
|------|------|------|-----------|
| `#5` | 插件创建 | — | `ed09f2189f485512092878cf390c1ad5b37d2fffe0c5eb8db13efa8e09d6534b` |
| `#6` | 版本发布 | `v0.0.1` | `b05512019b75cb90621364d42617bbbf47f43e66e3fef6c0a4c6a7e836f50f1c` |
| `#7` | 版本发布 | `v0.0.2` | `b4539979fc07daeec19083b9f0eabfbea35162765dc8e777eb7e55a009ec1a10` |
| `#8` | 版本发布 | `v0.0.3` | `2f795a8a64c50e93908592d4505df1500952e381ab080bd4a35053121a4852ba` |

> 后续发布新 tag 时，可由流水线自动完成版本发布存证，无需人工补录。

---

*存证由 [XMZZUZHI/chain-contracts](https://cnb.cool/XMZZUZHI/chain-contracts) 的
`AstrBotPluginDeposit` 合约与 `scripts/contract_astrbot_plugin.py` 脚本完成。*
