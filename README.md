<div align="center">

# 🏰 astrbot_plugin_rocom
### *WeGame 洛克王国数据查询 AstrBot 版*

[![GitHub stars](https://img.shields.io/github/stars/Entropy-Increase-Team/astrbot_plugin_rocom?style=for-the-badge&color=FFc65f)](https://github.com/Entropy-Increase-Team/astrbot_plugin_rocom/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Entropy-Increase-Team/astrbot_plugin_rocom?style=for-the-badge&color=d88124)](https://github.com/Entropy-Increase-Team/astrbot_plugin_rocom/network)
[![GitHub issues](https://img.shields.io/github/issues/Entropy-Increase-Team/astrbot_plugin_rocom?style=for-the-badge&color=45B7D1)](https://github.com/Entropy-Increase-Team/astrbot_plugin_rocom/issues)
[![AstrBot](https://img.shields.io/badge/AstrBot-Plugin-FFc65f?style=for-the-badge&logo=python)](https://github.com/Soulter/AstrBot)

### 🚀 基于 WeGame API & 洛克王国数据 的查询工具
### 扫码绑定 · 个人档案 · 最近战绩 · 精灵背包

**如果这个插件对你有帮助，请点亮⭐支持一下！**

</div>

---

## 📑 目录

- [✨ 特性一览](#-特性一览)
- [🔧 安装与配置](#-安装与配置)
- [📁 项目结构](#-项目结构)
- [🎮 功能详解](#-功能详解)
- [🎨 自定义美化](#-自定义美化)
- [📋 TODO](#-todo)
- [❓ 常见问题](#-常见问题)
- [🙏 鸣谢](#-鸣谢)

---

## ✨ 特性一览

✅ **账号管理** - 扫码登录(QQ/微信)/凭证导入/多账号切换/删除绑定，主账号快速切换  

✅ **数据查询** - 个人档案可视化渲染、近期对战详情、背包精灵图鉴检索

✅ **图片展示** - 深度还原 WeGame 各级视觉效果的排版与艺术风格字体字形重绘，自带自适应宽度渲染

---

## 🔧 安装与配置

### 快速安装

在AstrBot插件管理器中搜索 `astrbot_plugin_rocom` 安装，或通过 Git 克隆：

```bash
cd AstrBot/data/plugins
git clone https://github.com/Entropy-Increase-Team/astrbot_plugin_rocom.git
```

### 环境依赖

确保已安装Playwright浏览器内核：

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
├── _conf_schema.json       # WebUI配置schema
├── core/                   # 核心逻辑
│   ├── client.py           # API异步客户端
│   ├── user.py             # 用户数据中心
│   └── render.py           # HTML渲染助手
├── data/                   # 持久化存储
│   └── users.json          # 用户绑定数据
├── img/                    # 各项渲染所需依赖底图
├── ttf/                    # 无衬线免税字体库
└── render/                 # 网页模板资源
    ├── bind-list/          # 绑定列表与多账号面板模板
    ├── menu/               # 帮助菜单模板
    ├── package/            # 背包图鉴汇总模板
    ├── personal-card/      # 洛克档案面板模板
    └── record/             # 对战回放数据模板
```

---

## 🎮 功能详解

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
| `洛克背包 [分类] [页码]` | 展示对应条件精选收藏情况，支持 分类如 `了不起` 等 |

> 💡 发送 `洛克` 可查看插件完整且精美的图片图解版内置帮助。

---

## 🎨 自定义美化

你可以通过替换内部图片的方式实现基础的背景个性化：

**路径：** `AstrBot/data/plugins/astrbot_plugin_rocom/img/`

---

## ❓ 常见问题

### Q1: 安装后无法渲染图片？

✅ 检查是否已执行 `playwright install chromium`。如果在 AstrBot 下通过源形式管理请确保面板依赖中成功拉取了底层渲染工具，或调整系统超时配置。

### Q2: 提示 API Key 存在或无权限？

✅ 由于更新了统一鉴权协议架构，旧的分别申请的方法不再适用。请确保开发者只使用了单一具有对应子能力映射申请权限的 WeGame API Key 填入配置页面。

---

## 🙏 鸣谢

特别赞助与感谢：
- **Astrbot**：[Soulter/AstrBot](https://github.com/Soulter/AstrBot) 提供强大的机器人开发与部署平台支撑
- **熵增项目组** - 对各类抓取代理转发能力的构筑

本插件界面UI由原平台页面自研拆解逆向还原成微网页模板。全部图表美术素材著作及归属权属于腾讯科技 WeGame 及《洛克王国》项目组官方主体。
