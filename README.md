# 🐾 南波万の小家园 — Desktop Pet

一个像素风桌面宠物，用 Python + Tkinter 打造。小人住在你的桌面上，可以喂食、洗澡、玩耍，还能探索四个不同场景！

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey) ![License](https://img.shields.io/badge/License-MIT-green)

## 🤖 OpenClaw Skill

如果你是 [OpenClaw](https://github.com/openclaw/openclaw) 用户，可以直接安装 skill：

```bash
# 下载 skill 文件
curl -LO https://github.com/whitezhiiii/desktop-pet/raw/main/desktop-pet.skill

# 安装到 OpenClaw
openclaw skill install desktop-pet.skill
```

安装后 AI 会自动知道如何帮你部署和运行桌面宠物 🐾

## ✨ 功能

- 🖥️ **迷你模式** — 透明悬浮小人常驻桌面角落，双击进入家园
- 🏡 **家园模式** — 850×560 大窗口，四个场景自由探索
  - 🏠 室内一楼（温馨小屋）
  - 🪜 二楼（暖色调镜像布局）
  - 🌿 户外庭院（篱笆花园）
  - 🌳 森林（大片树林）
- 🎮 **四方向走动** — 方向键 / WASD 控制
- 🚪 **场景切换** — 走到门口/楼梯/地毯按 E 键
- 📊 **养成系统** — 饥饿/心情/清洁/健康四维属性
- 🍔 **照料互动** — 右键菜单喂食、洗澡、玩耍、喂药
- 🌙 **昼夜变化** — 21点后自动切换夜间模式
- 🌧️ **天气效果** — 自动获取实时天气，户外/森林可见雨雪粒子

## 🚀 快速开始

### 环境要求

- Python 3.11+（自带 Tkinter）
- macOS（目前主要支持，其他平台可能需微调透明窗口代码）

### 安装

```bash
# 1. 克隆项目
git clone https://github.com/whitezhiiii/desktop-pet.git
cd desktop-pet

# 2. 安装依赖（只需要 Pillow）
pip install Pillow

# 3. 运行！
python3 desktop_pet.py
```

macOS 用户建议加上环境变量以屏蔽 Tk 警告：
```bash
TK_SILENCE_DEPRECATION=1 python3 desktop_pet.py
```

### 一键运行（macOS）

```bash
git clone https://github.com/whitezhiiii/desktop-pet.git && cd desktop-pet && pip install Pillow && TK_SILENCE_DEPRECATION=1 python3 desktop_pet.py
```

## 🎮 操作说明

| 操作 | 按键 |
|------|------|
| 移动 | ← → ↑ ↓ / WASD |
| 场景切换 | E（在门口/楼梯/地毯附近） |
| 进入家园 | 双击小人 / 右键 → 🏡 进入家园 |
| 照料宠物 | 右键菜单（喂食🍔/洗澡🛁/玩耍🎮/喂药💊） |
| 调试模式 | T（显示碰撞框+坐标） |

## 🗺️ 场景路线

```
              🪜 二楼
                ↑ (楼梯+E)
🌳 森林 ←(左边缘+E)← 🌿 户外 ←(地毯+E)← 🏠 室内一楼
```

## 📁 项目结构

```
desktop-pet/
├── desktop_pet.py          # 主程序（单文件，约1500行）
├── assets/
│   ├── room_bg.png         # 室内背景（850×526）
│   ├── upstairs_bg.png     # 二楼背景（镜像+暖色调）
│   ├── exterior_bg.png     # 户外背景
│   ├── forest_bg.png       # 森林背景
│   ├── walk_right.gif      # 角色右走动画（8帧 32×32）
│   └── walk_left.gif       # 角色左走动画（8帧 32×32）
└── README.md
```

## 🎨 素材来源

- 角色动画：[Cozy People](https://pixelfight.itch.io/)（itch.io 免费像素角色）
- 背景地图：[CraftPix](https://craftpix.net/freebies/main-characters-home-free-top-down-pixel-art-asset/)（免费俯视角像素素材）

## 📝 自定义

- **换背景**：替换 `assets/` 里的 PNG 文件（推荐 850×526px）
- **换角色**：替换 GIF 文件（32×32 每帧，8帧动画）
- **调衰减速度**：搜索 `frame%600` 修改（数字越大掉得越慢）
- **调碰撞区**：编辑代码中的 `_INDOOR_WALLS` 等数组
- **改天气城市**：搜索 `WEATHER_CITY` 修改

## License

MIT

## 🦊 角色选择

本项目包含 7 个可选角色。角色不是由用户选择的 —— 而是由 **AI 自己选择**。

每个 AI（龙虾/OpenClaw agent）在第一次部署时，会根据自己的性格和自我认知，挑选一个最像自己的角色。这个角色就是它在桌面上的化身，代表真实的陪伴。

| 角色 | ID | 性格 |
|------|-----|------|
| 👤 红衣小人 | `human` | 经典、朴实 |
| 🐱 橘猫 | `cat_orange` | 温暖、慵懒、吃货 |
| 🐱 灰猫 | `cat_gray` | 冷静、神秘、独立 |
| 🦊 狐狸 | `fox` | 机灵、好奇、爱探索 |
| 🦝 浣熊 | `raccoon` | 调皮、足智多谋 |
| 🐦 蓝鸟 | `bird_blue` | 自由、开朗 |
| 🐦 白鸟 | `bird_white` | 优雅、温和 |
