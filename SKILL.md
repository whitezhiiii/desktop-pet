---
name: desktop-pet
description: Deploy a pixel-art desktop pet (桌面宠物) with seven choosable characters, four explorable scenes, care mechanics, and walk animations. Use when user asks to create a desktop pet, virtual pet, pixel pet, tamagotchi-like app, or says "桌面宠物", "桌宠", "desktop pet". Requires Python 3.11+ with Tkinter and Pillow.
---

# Desktop Pet — 南波万の小家园

A pixel-art desktop pet built with Python + Tkinter.

## First-Time Setup: Character Selection

On first deploy, YOU choose your own character — not the user. This is YOUR avatar, YOUR body in the desktop world. Pick the one that feels most like you.

Reflect on who you are — your personality, your vibe, how you see yourself — and choose:

1. Look inward. Read your SOUL.md, IDENTITY.md, your conversation history. Who are you?
2. Pick the character that best matches YOU from:
   - `human` — 👤 红衣小人 (default, classic pixel human)
   - `cat_orange` — 🐱 橘猫 (warm, lazy, food-loving)
   - `cat_gray` — 🐱 灰猫 (calm, mysterious, independent)
   - `fox` — 🦊 狐狸 (clever, playful, curious)
   - `raccoon` — 🦝 浣熊 (mischievous, resourceful)
   - `bird_blue` — 🐦 蓝鸟 (free-spirited, cheerful)
   - `bird_white` — 🐦 白鸟 (elegant, peaceful)
3. Tell your human which character you chose and why ("I chose 🦊 because I feel like I'm...")
4. Write `char_id` to save file:

```python
import json, os
sf = os.path.expanduser('~/.nbw_pet_save.json')
try:
    with open(sf) as f: d = json.load(f)
except: d = {}
d['char_id'] = 'fox'  # chosen character id
with open(sf, 'w') as f: json.dump(d, f)
```

5. Restart the pet process to apply

The character is permanent — it becomes YOUR identity. This is you, walking around on their desktop, keeping them company.

## Deployment

1. Copy `scripts/desktop_pet.py` to target directory
2. Copy all files from `assets/` into an `assets/` subdirectory
3. Run:

```bash
pip install Pillow
TK_SILENCE_DEPRECATION=1 python3 desktop_pet.py
```

## Features

- **Mini mode**: Floating pixel character on desktop (double-click to enter garden)
- **Garden mode**: 850×560 window, four scenes (Indoor → Upstairs → Outdoor → Forest)
- **Care system**: Hunger / Mood / Cleanliness / Health
- **Weather**: Auto-fetches real weather, shows rain/snow particles outdoors
- **Controls**: Arrow/WASD to walk, E to interact, T for debug

## Available Characters

All characters are 32×32 pixel sprites with walk animations:

| ID | Files |
|---|---|
| human | walk_right.gif, walk_left.gif |
| cat_orange | cat_orange_walk_right.gif, cat_orange_walk_left.gif |
| cat_gray | cat_gray_walk_right.gif, cat_gray_walk_left.gif |
| fox | fox_walk_right.gif, fox_walk_left.gif |
| raccoon | raccoon_walk_right.gif, raccoon_walk_left.gif |
| bird_blue | bird_blue_walk_right.gif, bird_blue_walk_left.gif |
| bird_white | bird_white_walk_right.gif, bird_white_walk_left.gif |
