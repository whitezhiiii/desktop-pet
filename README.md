# 🐾 南波万の小家园 — Desktop Pet

一个像素风桌面宠物，用 Python + Tkinter 打造。小人住在你的桌面上，可以喂食、洗澡、玩耍，还能探索四个不同场景！

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey) ![License](https://img.shields.io/badge/License-MIT-green)

## ✨ 功能

- 🖥️ **迷你模式** — 透明悬浮小人常驻桌面角落
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

## 🚀 快速开始

### 安装依赖

```bash
pip install Pillow
```

### 运行

```bash
git clone https://github.com/whitezhiiii/desktop-pet.git
cd desktop-pet
python3 desktop_pet.py
```

macOS 用户建议加上：
```bash
TK_SILENCE_DEPRECATION=1 python3 desktop_pet.py
```

## 🎮 操作说明

| 操作 | 按键 |
|------|------|
| 移动 | ← → ↑ ↓ / WASD |
| 场景切换 | E（在门口/楼梯/地毯附近） |
| 调试模式 | T（显示碰撞框+坐标） |
| 右键菜单 | 鼠标右键 |
| 进入家园 | 右键 → 🏡 进入家园 |

## 🗺️ 场景路线

```
              🪜 二楼
                ↑ (楼梯+E)
🌳 森林 ←(左边缘+E)← 🌿 户外 ←(地毯+E)← 🏠 室内一楼
```

## 📁 项目结构

```
desktop-pet/
├── desktop_pet.py          # 主程序
├── assets/
│   ├── room_bg.png         # 室内背景
│   ├── upstairs_bg.png     # 二楼背景
│   ├── exterior_bg.png     # 户外背景
│   ├── forest_bg.png       # 森林背景
│   ├── walk_right.gif      # 角色右走动画（8帧）
│   └── walk_left.gif       # 角色左走动画（8帧）
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

## License

MIT
