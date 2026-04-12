<div align="center">

# 🏰 astrbot_plugin_rocom
### *WeGame 洛克王国数据查询*

[![GitHub stars](https://img.shields.io/github/stars/Entropy-Increase-Team/astrbot_plugin_rocom?style=for-the-badge&color=FFc65f)](https://github.com/Entropy-Increase-Team/astrbot_plugin_rocom/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Entropy-Increase-Team/astrbot_plugin_rocom?style=for-the-badge&color=d88124)](https://github.com/Entropy-Increase-Team/astrbot_plugin_rocom/network)
[![GitHub issues](https://img.shields.io/github/issues/Entropy-Increase-Team/astrbot_plugin_rocom?style=for-the-badge&color=45B7D1)](https://github.com/Entropy-Increase-Team/astrbot_plugin_rocom/issues)
[![AstrBot](https://img.shields.io/badge/AstrBot-Plugin-FFc65f?style=for-the-badge&logo=python)](https://github.com/Soulter/AstrBot)

### 🚀 基于 WeGame API & 洛克王国数据 的查询工具
### 扫码绑定 · 个人档案 · 最近战绩 · 精灵背包 · 阵容助手

**如果这个插件对你有帮助，请点亮⭐支持一下！**

</div>

---

## 📑 目录

- [✨ 特性一览](#-特性一览)
- [🔧 安装与配置](#-安装与配置)
- [📁 项目结构](#-项目结构)
- [🎮 功能详解](#-功能详解)
- [📸 功能预览](#-功能预览)
- [🎨 自定义美化](#-自定义美化)
- [📋 TODO](#-todo)
- [📜 更新日志](#-更新日志)
- [❓ 常见问题](#-常见问题)
- [🙏 鸣谢](#-鸣谢)

---

## ✨ 特性一览

✅ **账号管理** - 扫码登录 (QQ/微信)/凭证导入/多账号切换/删除绑定，主账号快速切换  

✅ **消息撤回** - 登录链接与二维码超时、完成或被拒时自动撤回，保护账号安全

✅ **数据查询** - 个人档案可视化渲染、近期对战详情、背包精灵图鉴检索、交换大厅、阵容推荐

✅ **图片展示** - 深度还原 WeGame 各级视觉效果的排版与艺术风格字体字形重绘，自带自适应宽度渲染

✅ **阵容助手** - 热门阵容推荐、2x3 网格布局展示、阵容码查询、详细技能配置

---

## 🔧 安装与配置

### 快速安装

在 AstrBot 插件管理器中搜索 `astrbot_plugin_rocom` 安装，或通过 Git 克隆：

```bash
cd AstrBot/data/plugins
git clone https://github.com/Entropy-Increase-Team/astrbot_plugin_rocom.git
```

### 环境依赖

确保已安装 Playwright 浏览器内核：

```bash
playwright install chromium
```

### 配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|:-------|:-----|:-------|:-----|
| `api_base_url` | string | `https://wegame.shallow.ink` | API 服务后端地址 |
| `wegame_api_key` | string | 无 | ⚠️ 必填，拥有 wegame 作用域的 API Key，统一用于各项查询获取 |
| `render_timeout` | number | `30000` | 图片渲染超时时间（毫秒） |

---

## 📁 项目结构

```
astrbot_plugin_rocom/
├── main.py                 # 插件入口，指令路由
├── metadata.yaml           # 插件元数据
├── _conf_schema.json       # WebUI 配置 schema
├── core/                   # 核心逻辑
│   ├── client.py           # API 异步客户端
│   ├── user.py             # 用户数据中心
│   └── render.py           # HTML 渲染助手
├── data/                   # 持久化存储
│   └── users.json          # 用户绑定数据
├── img/                    # 各项渲染所需依赖底图
├── ttf/                    # 无衬线免税字体库
└── render/                 # 网页模板资源
    ├── bind-list/          # 绑定列表与多账号面板模板
    ├── menu/               # 帮助菜单模板
    ├── package/            # 背包图鉴汇总模板
    ├── personal-card/      # 洛克档案面板模板
    ├── record/             # 对战回放数据模板
    ├── exchange-hall/      # 洛克交换大厅模板
    ├── lineup/             # 洛克阵容助手模板
    └── lineup-detail/      # 阵容详情模板
```

---

## 🎮 功能详解

> 💡 **指令前缀**：默认为 `/`，在 AstrBot 配置中自定义

### 🔐 账号与绑定

| 指令 | 说明 |
|:-----|:-----|
| `洛克QQ登录` | 使用 QQ 扫码快捷登录及绑定 |
| `洛克微信登录` | 使用微信扫码快捷登录及绑定 |
| `洛克导入 [ID] [Ticket]` | 通过客户端扫尾凭证手动导入登录 |
| `洛克刷新` | 刷新当前有效主账号 QQ 凭证生存期 |
| `洛克绑定列表` | 查看所有已扫描绑定的账号记录 |
| `洛克切换 [序号]` | 一键切换当前群聊激活的前置主查询账号 |
| `洛克解绑 [序号]` | 移除不再需要的冗余账号绑定内容 |

### 📊 数据查询

| 指令 | 说明 |
|:-----|:-----|
| `洛克档案` | 生成全盘概览的个人数据雷达星级名片 |
| `洛克战绩 [页码]` | 查询并展示指定历史对战记录的对手及结果 |
| `洛克背包 [分类] [页码]` | 展示对应条件精选收藏情况，支持分类如 `了不起`、`异色`、`炫彩` 等 |
| `洛克交换大厅 [页码]` | 浏览其他玩家的精灵交换请求列表 |
| `洛克阵容 <分类> <页码>` | 查看热门阵容推荐及组成，2x3 网格布局展示 |
| `查看阵容 <阵容码>` | 查看指定阵容的详细信息，包含精灵技能配置 |

> 💡 发送 `洛克` 可查看插件完整且精美的图片图解版内置帮助。

---

## 📸 功能预览

<details open>
<summary>点击展开预览图</summary>

| `洛克档案` | `洛克战绩` |
|:---:|:---:|
| 个人数据雷达星级名片 | 近期对战记录详情 |

| `洛克背包` | `洛克交换大厅` |
|:---:|:---:|
| 精灵背包图鉴检索 | 玩家交换请求列表 |

| `洛克阵容` | `查看阵容` |
|:---:|:---:|
| 2x3 网格布局展示 | 阵容详细信息 |

</details>

---

## 🎨 自定义美化

你可以通过替换内部图片的方式实现基础的背景个性化：

**路径：** `AstrBot/data/plugins/astrbot_plugin_rocom/img/`

| 功能 | 文件 |
|:-----|:-----|
| 背景图 | `bg.C8CUoi7I.jpg` |
| 战绩背景 | `record-bg.C1mPRb4R.png` |

---

## 📋 TODO

- [x] **基础查询** (个人档案/战绩/背包)
- [x] **交换大厅** (精灵交换请求列表)
- [x] **阵容助手** (阵容列表/详情查询)
- [ ] **更多功能** (敬请期待)

---

## 📜 更新日志

<details>
<summary>点击展开版本历史</summary>

### v1.1.0 (2026-04-12)

**新增功能**
- 新增洛克交换大厅指令：`/洛克交换大厅` / `/洛克大厅` / `/交换大厅`
- 新增洛克阵容助手指令：`/洛克阵容 <分类> <页码>`
- 新增查看阵容详情指令：`/查看阵容 <阵容码>`
- 新增精灵背包分类筛选：`全部`、`异色`、`了不起`、`炫彩`

**优化改进**
- 重构阵容列表页面样式：采用 2x3 网格布局、方形精灵头像、卡片式设计
- 优化阵容详情页面渲染效果，精灵头像采用圆形展示
- 修复页脚提示不显示问题
- 修复页脚过大占据半个屏幕问题
- 优化渲染器截图逻辑，确保完整包含页脚内容
- 标准化页脚样式，统一字体大小和间距

**指令优化**
- 洛克背包：支持参数交换位置，如 `/洛克背包 2 异色` 或 `/洛克背包 异色 2`
- 默认值：全部第 1 页，支持 `背包 <页码>` 或 `背包 <分类>` 格式
- 洛克战绩：修复页脚样式不匹配问题

### v1.0.0 (2026-04-11)

- ✨ 初始版本发布
- ✅ 支持 QQ/微信扫码登录
- ✅ 个人档案、战绩、背包查询
- ✅ 图片渲染输出

</details>

---

## 🙏 鸣谢


- **Astrbot**：[Soulter/AstrBot](https://github.com/Soulter/AstrBot) 提供强大的机器人开发与部署平台支撑

特别感谢：
- **熵增项目组** - 对各类抓取代理转发能力的构筑

本插件界面 UI 由原平台页面自研拆解逆向还原成微网页模板。全部图表美术素材著作及归属权属于腾讯科技 WeGame 及《洛克王国》项目组官方主体。

---

<div align="center">

### 💬 加入交流群

| AstrBot 洛克王国插件交流群 |
|:---:|
| [870543663](https://qm.qq.com/q/kPxQZy5gg8) |

</div>

---

<div align="center">
    
# 如果喜欢这个插件，别忘了给仓库点个⭐！

# [⬆ 返回顶部](#-astrbot_plugin_rocom)

</div>
