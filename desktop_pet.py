#!/usr/bin/env python3
"""南波万小家园 🏡 - 全像素风 v8 对话版"""
import tkinter as tk
import random, math, time, threading, urllib.request, json, os, http.client, ssl

# ── 自动下载资源 ──────────────────────────────────────────────────────────────
def _ensure_assets():
    """首次运行时从 GitHub 自动下载必要的图片资源"""
    _BASE = 'https://raw.githubusercontent.com/whitezhiiii/desktop-pet/main/assets/'
    _DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
    _REQUIRED = [
        'room_bg.png', 'exterior_bg.png', 'forest_bg.png', 'upstairs_bg.png',
        'sun.jpeg',
        'walk_left.gif', 'walk_right.gif',
        'cat_orange_walk_right.gif', 'cat_orange_walk_left.gif',
        'cat_gray_walk_right.gif',  'cat_gray_walk_left.gif',
        'fox_walk_right.gif',       'fox_walk_left.gif',
        'raccoon_walk_right.gif',   'raccoon_walk_left.gif',
        'bird_blue_walk_right.gif', 'bird_blue_walk_left.gif',
        'bird_white_walk_right.gif','bird_white_walk_left.gif',
    ]
    os.makedirs(_DIR, exist_ok=True)
    missing = [f for f in _REQUIRED if not os.path.exists(os.path.join(_DIR, f))]
    if not missing:
        return
    try:
        import tkinter as _tk
        _r = _tk.Tk(); _r.withdraw()
        _lbl = _tk.Label(_r, text='🏡 首次运行,正在下载资源...\n请稍候', font=('Arial', 14), padx=20, pady=20)
        _lbl.pack(); _r.update()
    except Exception:
        _r = None
    for fname in missing:
        try:
            urllib.request.urlretrieve(_BASE + fname, os.path.join(_DIR, fname))
        except Exception as e:
            print(f'[assets] 下载失败: {fname} - {e}')
    if _r:
        try: _r.destroy()
        except: pass

_ensure_assets()
# ─────────────────────────────────────────────────────────────────────────────

W, H = 480, 332
WEATHER_CITY = 'Beijing'
PET_OWNER = '主人'  # 改成你的名字,小屋标题会显示「{名字}の小家园」
PET_HOME_TITLE = f'🏡 {PET_OWNER}の小家园'
BP = 4   # 背景像素格
CP = 3   # 角色像素格

SAVE_FILE = os.path.expanduser('~/.nbw_pet_save.json')

# 可选角色列表
CHARACTERS = {
    'human':      {'name': '👤 红衣小人', 'right': 'walk_left.gif', 'left': 'walk_right.gif'},
    'cat_orange': {'name': '🐱 橘猫',     'right': 'cat_orange_walk_right.gif', 'left': 'cat_orange_walk_left.gif'},
    'cat_gray':   {'name': '🐱 灰猫',     'right': 'cat_gray_walk_right.gif',   'left': 'cat_gray_walk_left.gif'},
    'fox':        {'name': '🦊 狐狸',     'right': 'fox_walk_right.gif',         'left': 'fox_walk_left.gif'},
    'raccoon':    {'name': '🦝 浣熊',     'right': 'raccoon_walk_right.gif',     'left': 'raccoon_walk_left.gif'},
    'bird_blue':  {'name': '🐦 蓝鸟',     'right': 'bird_blue_walk_right.gif',   'left': 'bird_blue_walk_left.gif'},
    'bird_white': {'name': '🐦 白鸟',     'right': 'bird_white_walk_right.gif',  'left': 'bird_white_walk_left.gif'},
}
DEFAULT_CHAR = 'fox'

T = {
    'sky_hi':'#c8e8ff','sky_md':'#a8d4f0','sky_lo':'#88c0e8',
    'night_hi':'#0a1628','night_md':'#0e1e38','night_lo':'#122448',
    'rain_sky':'#889aaa','rain_sky2':'#6a7a8a',
    'snow_sky':'#c8d8e8','snow_sky2':'#aabccc',
    'grass':'#52b84e','grass2':'#3da83a','grass3':'#68cc64',
    'dirt':'#9b6b3a','dirt2':'#7a5028','dirt3':'#b07e48',
    'path':'#c8a468','path2':'#b08848','path3':'#d8b478',
    'water':'#38b0e0','water2':'#50c8f8','water3':'#28a0d0',
    'water4':'#60d0ff','pond_d':'#2090c0',
    'hw':'#f0d8b0','hw2':'#d8c090','hw3':'#ffecc8',
    'hroof':'#c03030','hroof2':'#a02020','hroof3':'#e04040',
    'hdoor':'#784018','hdoor2':'#5a2e08',
    'hwin':'#b8dcff','hwin2':'#d8ecff','hwin3':'#88b8ee',
    'hchim':'#886040','hchim2':'#6a4828',
    'tree1':'#2a8a2a','tree2':'#1e6a1e','tree3':'#3aaa3a',
    'trunk':'#7a5028','trunk2':'#5a3810',
    'apple':'#e03030','apple2':'#c82020',
    'flr':'#ff5577','fly':'#ffdd22','flp':'#cc55ff',
    'flw':'#ffffff','stem':'#2a8a2a',
    'fence':'#c8a040','fence2':'#a87828',
    'soil':'#6a4020','soil2':'#4a2808',
    'vg':'#2a9a2a','vg2':'#1a7a1a',
    'vr':'#dd3333','vo':'#ee7722','vy':'#cccc22',
    'star':'#ffffcc','star2':'#ffeeaa',
    'moon':'#fff8c0','moon2':'#ffe880','moon3':'#fff0a0',
    'sun':'#ffe566','sun2':'#ffcc00','sun3':'#fff0a0',
    'smk1':'#dddddd','smk2':'#cccccc','smk3':'#bbbbbb',
    'bbl':'#fffef0','bbl2':'#7744cc',
    'rain':'#88bbdd','rain2':'#aaccee',
    'snow':'#eef4ff','snow2':'#ffffff',
    'splash':'#aaddff',
    'ch_h1':'#1a1a3a','ch_h2':'#2a2a52','ch_h3':'#5555aa',
    'ch_s1':'#f8d8b0','ch_s2':'#e8c090','ch_s3':'#fce8cc',
    'ch_e1':'#1a1a3a','ch_e2':'#4455cc',
    'ch_lip':'#cc6878','ch_blsh':'#f4bece',
    'ch_c1':'#7733cc','ch_c2':'#5522aa','ch_c3':'#9944ee',
    'ch_bt':'#1a1008',
    'ch_p1':'#18083a','ch_p2':'#220c50',
    'ch_k1':'#140820','ch_k2':'#1e1030',
    'wc':'#4488bb','wc2':'#336699',
    'fish_o':'#ff8844',
    'bfly1':'#ff88cc','bfly2':'#ffdd44','bfly3':'#88aaff','bfly4':'#88ffcc',
    'angry':'#ff3333','angry2':'#ff6600',
    'medal_g':'#ffd700','medal_s':'#c0c0c0','medal_b':'#cd7f32',
    'chest':'#8b6914','chest2':'#c8a020','boot':'#5a3a1a',
}

_=None

HEAD_STAND=[
    [_,_,'ch_h1','ch_h1','ch_h1','ch_h1','ch_h1','ch_h1',_,_],
    [_,'ch_h1','ch_h2','ch_h3','ch_h3','ch_h3','ch_h2','ch_h2','ch_h1',_],
    [_,'ch_h1','ch_s3','ch_s3','ch_s3','ch_s3','ch_s3','ch_s3','ch_h1',_],
    [_,'ch_h1','ch_s1','ch_e1','ch_s1','ch_s1','ch_e1','ch_s1','ch_h1',_],
    [_,'ch_h1','ch_s2','ch_s1','ch_s2','ch_s1','ch_s1','ch_s2','ch_h1',_],
    [_,'ch_h1','ch_s1','ch_blsh','ch_s1','ch_s1','ch_blsh','ch_s1','ch_h1',_],
    [_,'ch_h1','ch_s1','ch_s2','ch_lip','ch_lip','ch_s2','ch_s1','ch_h1',_],
    [_,_,'ch_h1','ch_s2','ch_s2','ch_s2','ch_s2','ch_h1',_,_],
]
HEAD_ANGRY=[
    [_,_,'ch_h1','ch_h1','ch_h1','ch_h1','ch_h1','ch_h1',_,_],
    [_,'ch_h1','ch_h2','ch_h3','ch_h3','ch_h3','ch_h2','ch_h2','ch_h1',_],
    [_,'ch_h1','ch_s3','ch_s3','ch_s3','ch_s3','ch_s3','ch_s3','ch_h1',_],
    [_,'ch_h1','ch_s1','ch_h1','ch_e1','ch_e1','ch_h1','ch_s1','ch_h1',_],  # 皱眉
    [_,'ch_h1','ch_s2','ch_e1','ch_s2','ch_s2','ch_e1','ch_s2','ch_h1',_],
    [_,'ch_h1','ch_s1','ch_s1','ch_s1','ch_s1','ch_s1','ch_s1','ch_h1',_],
    [_,'ch_h1','ch_s1','ch_lip','ch_lip','ch_lip','ch_lip','ch_s1','ch_h1',_],  # 扁嘴
    [_,_,'ch_h1','ch_s2','ch_s2','ch_s2','ch_s2','ch_h1',_,_],
]
BODY_STAND=[
    [_,_,'ch_c2','ch_c1','ch_c1','ch_c1','ch_c1','ch_c2',_,_],
    [_,'ch_c2','ch_c3','ch_c1','ch_c1','ch_c1','ch_c1','ch_c3','ch_c2',_],
    [_,'ch_c2','ch_c1','ch_c1','ch_c1','ch_c1','ch_c1','ch_c1','ch_c2',_],
    [_,'ch_c2','ch_bt','ch_bt','ch_bt','ch_bt','ch_bt','ch_bt','ch_c2',_],
]
LEGS_STAND=[
    [_,_,'ch_p1','ch_p2','ch_p1',_,'ch_p1','ch_p2','ch_p1',_],
    [_,_,'ch_p1','ch_p2','ch_p1',_,'ch_p1','ch_p2','ch_p1',_],
    [_,_,'ch_p1','ch_p2','ch_p1',_,'ch_p1','ch_p2','ch_p1',_],
    [_,_,'ch_p2','ch_p1','ch_p2',_,'ch_p2','ch_p1','ch_p2',_],
    [_,_,'ch_k1','ch_k2','ch_k1',_,'ch_k1','ch_k2','ch_k1',_],
    [_,'ch_k1','ch_k2','ch_k1','ch_k2',_,'ch_k2','ch_k1','ch_k2','ch_k1'],
    [_,'ch_k1','ch_k1','ch_k2','ch_k1',_,'ch_k1','ch_k2','ch_k1','ch_k1'],
    [_,_,_,_,_,_,_,_,_,_],
]
LEGS_WALK_A=[
    [_,'ch_p1','ch_p2','ch_p1',_,_,'ch_p1','ch_p2',_,_],
    ['ch_p1','ch_p2','ch_p1',_,_,_,'ch_p1','ch_p2',_,_],
    ['ch_p2','ch_p1',_,_,_,_,'ch_p2','ch_p1',_,_],
    ['ch_k1','ch_k2',_,_,_,_,'ch_k2','ch_k1',_,_],
    ['ch_k2','ch_k1','ch_k2',_,_,_,'ch_k1','ch_k2','ch_k1',_],
    [_,'ch_k1','ch_k2',_,_,_,'ch_k2','ch_k1','ch_k2',_],
    [_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_],
]
LEGS_WALK_B=[
    [_,_,_,'ch_p1','ch_p2',_,'ch_p2','ch_p1',_,_],
    [_,_,_,'ch_p1','ch_p2',_,'ch_p2','ch_p1','ch_p1',_],
    [_,_,_,'ch_p2','ch_p1',_,'ch_p1','ch_p2','ch_p2',_],
    [_,_,_,'ch_k1','ch_k2',_,'ch_k2','ch_k1','ch_k1',_],
    [_,_,'ch_k1','ch_k2','ch_k1',_,'ch_k1','ch_k2','ch_k2','ch_k1'],
    [_,_,'ch_k2','ch_k1','ch_k2',_,'ch_k2','ch_k1','ch_k1','ch_k2'],
    [_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_],
]
BODY_WATER=[
    ['wc','wc2','ch_c2','ch_c1','ch_c1','ch_c1','ch_c1','ch_c2','ch_s1','ch_s2'],
    ['wc','wc2','ch_c3','ch_c1','ch_c1','ch_c1','ch_c1','ch_c3','ch_s1',_],
    [_,'wc','ch_c1','ch_c1','ch_c1','ch_c1','ch_c1','ch_c1','ch_c2',_],
    [_,_,'ch_bt','ch_bt','ch_bt','ch_bt','ch_bt','ch_bt',_,_],
]

STAND        = HEAD_STAND  + BODY_STAND + LEGS_STAND
WALK_A       = HEAD_STAND  + BODY_STAND + LEGS_WALK_A
WALK_B       = HEAD_STAND  + BODY_STAND + LEGS_WALK_B
WATER_SPR    = HEAD_STAND  + BODY_WATER + LEGS_STAND
ANGRY_STAND  = HEAD_ANGRY  + BODY_STAND + LEGS_STAND

SLEEP_SPR=[
    [_,_,_,_,_,_,_,_,_,_],[_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_],[_,_,_,_,_,_,_,_,_,_],
    ['ch_h1','ch_h1','ch_h1','ch_h1','ch_h1','ch_h1',_,_,_,_],
    ['ch_h1','ch_h2','ch_h3','ch_h3','ch_h2','ch_h1','ch_h1',_,_,_],
    ['ch_h1','ch_s3','ch_s3','ch_s3','ch_s3','ch_s2','ch_h1',_,_,_],
    ['ch_h1','ch_s1','ch_e1','ch_s1','ch_e1','ch_s2','ch_h1',_,_,_],
    [_,'ch_h1','ch_lip','ch_lip','ch_s1','ch_s2','ch_h1',_,_,_],
    [_,'ch_h1','ch_s2','ch_s2','ch_s2','ch_h1',_,_,_,_],
    [_,_,'ch_c2','ch_c1','ch_c1','ch_c1','ch_c1','ch_c1','ch_c2',_],
    [_,_,'ch_c3','ch_c1','ch_c1','ch_c1','ch_c1','ch_c1','ch_c3',_],
    [_,_,'ch_bt','ch_bt','ch_bt','ch_bt','ch_bt','ch_bt','ch_bt',_],
    [_,_,'ch_p1','ch_p2','ch_p1','ch_p1','ch_p2','ch_p1','ch_p1',_],
    [_,_,_,'ch_k1','ch_k2','ch_k2','ch_k1','ch_k2',_,_],
    [_,_,_,'ch_k2','ch_k1','ch_k1','ch_k2','ch_k1',_,_],
    [_,_,_,_,_,_,_,_,_,_],[_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_],[_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_],
]

SPRITES={'stand':STAND,'walk_a':WALK_A,'walk_b':WALK_B,
         'water':WATER_SPR,'sleep':SLEEP_SPR,'angry':ANGRY_STAND}

def draw_sprite(cv,cx,bottom_y,key='stand',flip=False):
    art=SPRITES.get(key,STAND)
    rows,cols=len(art),len(art[0])
    ox=cx-(cols*CP)//2; oy=bottom_y-rows*CP
    for ri,row in enumerate(art):
        for ci,k in enumerate(row):
            if k is None: continue
            color=T.get(k,'#ff00ff')
            dc=(cols-1-ci) if flip else ci
            x0=ox+dc*CP; y0=oy+ri*CP
            cv.create_rectangle(x0,y0,x0+CP,y0+CP,fill=color,outline='')


# ── 台词库 ─────────────────────────────────────────────────────────────
QUOTES_IDLE=[
    # 日常感叹
    '今天也是美好的一天~','嗯......','摸会儿鱼先 🐟','主人在吗?',
    '风好凉爽 🍃','有点无聊......','想睡觉了 😪','南波万!🤙',
    '今天吃什么呢 🍜','好想晒太阳啊 ☀️','云朵好漂亮~','发什么呆好呢...',
    # 搞怪
    '我在想一件很重要的事...但忘了是什么','要不要偷偷吃点零食?🍪',
    '🤔 如果我会飞的话...','哼哼哼~ 哼哼哼~',
    '突然想跳舞 💃','有人叫我吗?没有?那算了',
    '今天天气真好,适合摸鱼 🐟','我是世界上最可爱的!',
    # 生活感悟
    '工作是猫,我是老鼠,逃!','今天也要元气满满⚡',
    '吃饭了吗主人?别忘了吃饭!','喝水了吗?多喝热水🫖',
    '伸个懒腰~ 啊~~~','这道题难住我了...算了不想了',
    # 有梗
    '主人,宇宙的尽头是被我萌到🧡',
    '今天的运势:🌟🌟🌟🌟🌟 超级好!',
    '听说摸鱼有益健康,我在养生',
    '如果我有100个积分,我要买好多好吃的!',
]
QUOTES_ANGRY=[
    '够了够了!烦死了!😤','再戳我我生气了!','戳什么戳!','...哼!',
    '主人你很烦诶!','不理你了!','我会咬人的!🐾',
]
QUOTES_MAKE_UP=[
    '好啦好啦...不生气了😤','主人你认错了我就原谅你','哼,算了','还是喜欢主人嘛~',
]
QUOTES_HOUR=[
    '一点了,好困哦😴','两点,悄悄睡一会儿...','三点,夜深了~',
    '四点,早起的鸟儿有虫吃!','五点,天快亮了🌄','六点早安!☀️',
    '七点,吃早饭了吗?','八点,上班加油💪','九点,开始工作~',
    '十点了,喝杯茶休息下~☕','十一点,快中午了!🍱','十二点,午饭时间!',
    '下午一点,犯困的时间到了😪','两点,摸鱼正当时~🐟','三点,下午茶!☕',
    '四点,再坚持一下!','五点,快下班了🎉','六点,还没到点,再撑一下!',
    '七点,下班啦!🎉 辛苦了!','八点,放松一下吧🎮','九点,今天辛苦了',
    '十点了,该休息了😴','十一点,熬夜伤身体哦','零点,跨过今天了!✨',
]

FISH_RESULTS=[
    ('🐟 小鲫鱼','钓到小鲫鱼!咕嘟咕嘟~',None),
    ('🐠 热带鱼','哇!热带鱼!好漂亮!',None),
    ('🦈 小鲨鱼','!!鲨鱼?!放生放生!',None),
    ('👢 破靴子','......钓到一只臭靴子......',None),
    ('💎 宝石','天啊!水晶宝石!!✨',None),
    ('📦 宝箱','宝箱!!里面有什么!',None),
    ('🍺 易拉罐','垃圾......主人来捡垃圾啦',None),
    ('🐙 小章鱼','章鱼!你怎么在这里!',None),
]

# ── 钓鱼系统鱼类数据 ─────────────────────────────────────────────────────────
# 格式: (显示名, 文件名前缀, 稀有度, 积分, EXP, 描述)
FISH_TYPES = [
    # 常见鱼 (60%)
    ('小鲫鱼',   'fish_grey',       'common',    8,  10, '最常见的小鱼,朴实无华~'),
    ('小草鱼',   'fish_green',      'common',    8,  10, '游得挺快的绿色小家伙!'),
    ('河豚',     'fish_brown',      'common',    6,   8, '圆滚滚的河豚，气鼓鼓超可爱!🐡'),
    # 稀有鱼 (30%)
    ('红鲤鱼',   'fish_red',        'rare',     20,  25, '红色吉祥鲤鱼,好兆头!🎏'),
    ('橙色锦鲤', 'fish_orange',     'rare',     25,  30, '华丽的锦鲤,财运来啦!'),
    ('粉色神仙', 'fish_pink',       'rare',     30,  35, '梦幻粉鱼,超级稀有!'),
    ('蓝色金枪', 'fish_blue',       'rare',     28,  30, '深蓝大鱼,力气不小!'),
    # 超稀有 (9%)
    ('灰长龙',   'fish_grey_long_a','epic',     60,  60, '传说中的银龙鱼!'),
    ('幽灵鱼',   'fish_grey_long_b','epic',     80,  80, '几乎透明...难道是幽灵?!'),
    # 垃圾/彩蛋 (1%)
    ('神秘宝箱', None,              'treasure', 100, 50, '宝箱?!今天运气爆炸!!'),
]
# 掉率权重
FISH_WEIGHTS = [20, 20, 20, 12, 12, 6, 6, 2, 1, 1]
FISH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'fish')


# ── 各省特产数据 ──────────────────────────────────────────────────────────────
# 格式: 省份 -> [(名称, 描述), ...]
PROV_SOUVENIRS = {
    '北京':  [('🦆 北京烤鸭',    '皮脆肉嫩,香飘四溢!'),
              ('🍺 燕京啤酒',    '国民老牌,清爽解渴~'),
              ('🥮 稻香村点心',  '老北京传统糕点,甜而不腻!')],
    '上海':  [('🦀 大闸蟹',      '膏肥肉鲜,鲜掉眉毛!'),
              ('🥐 鲜肉月饼',    '酥皮流汁,沪上必吃!'),
              ('☕ 海派咖啡',    '洋气摩登,魔都味道~')],
    '广东':  [('🫖 工夫茶',      '细细品味,回甘悠长~'),
              ('🥟 虾饺皇',      '晶莹剔透,粤式精华!'),
              ('🌺 广式月饼',    '莲蓉蛋黄,经典永流传~')],
    '四川':  [('🌶️ 麻辣火锅底料','又麻又辣,爽爆了!'),
              ('🍢 串串香',      '千滋百味,成都街头一绝!'),
              ('🐼 熊猫玩偶',    '软乎乎的,国宝同款~')],
    '云南':  [('🍵 普洱茶',      '陈香醇厚,越存越香~'),
              ('🌸 鲜花饼',      '玫瑰芳香,云南特色!'),
              ('🍄 松茸干片',    '山珍之王,珍贵极了!')],
    '新疆':  [('🍇 吐鲁番葡萄',  '甜到心里去了!'),
              ('🥜 库尔勒香梨',  '汁多味甜,天山馈赠~'),
              ('🐑 羊肉串',      '炭火飘香,西域风情!')],
    '西藏':  [('🧈 酥油茶',      '高原特饮,暖心暖胃~'),
              ('💎 天珠',         '藏族圣物,辟邪吉祥~'),
              ('🌾 青稞糌粑',    '高原主食,绵绵醇香!')],
    '内蒙古':[('🥩 风干牛肉干',  '韧劲十足,越嚼越香!'),
              ('🥛 奶豆腐',      '醇香浓郁,草原味道!'),
              ('🐑 羊绒围巾',    '细软暖和,内蒙古特产~')],
    '黑龙江':[('🫐 东北蓝莓',    '酸甜可口,野生味道!'),
              ('🌲 红松籽',      '粒粒饱满,林区珍品!'),
              ('🐟 鳇鱼子酱',    '黑色黄金,珍稀极品!')],
    '吉林':  [('🌿 长白山人参',  '滋补佳品,元气满满!'),
              ('🍄 鹿茸片',      '滋补上品,长白山宝!'),
              ('🌽 鲜玉米',      '甜糯多汁,东北一绝~')],
    '辽宁':  [('🍎 大连苹果',    '脆甜多汁,维C满满!'),
              ('🦐 海鲜大礼包',  '辽东湾鲜货,海味十足!'),
              ('🥟 老边饺子',    '皮薄馅大,沈阳老字号~')],
    '山东':  [('🥜 烟台花生',    '香脆可口,停不下来!'),
              ('🍺 青岛啤酒',    '国民啤酒,麦香扑鼻!'),
              ('🥟 速冻水饺',    '皮薄馅鲜,山东味道~')],
    '江苏':  [('🍜 南京盐水鸭',  '皮白肉嫩,金陵名菜!'),
              ('🎋 宜兴紫砂壶',  '茶人挚爱,传世珍品!'),
              ('🌸 苏州丝绸',    '柔滑细腻,姑苏风情~')],
    '浙江':  [('🍵 西湖龙井',    '清香扑鼻,口齿留香!'),
              ('🥢 绍兴黄酒',    '醇厚悠长,江南佳酿~'),
              ('🎋 天目山竹笋',  '鲜嫩清脆,春日馈赠!')],
    '安徽':  [('🫖 黄山毛峰',    '云雾中采摘,清新淡雅~'),
              ('🥜 徽州臭鳜鱼',  '臭名远扬,香绝天下!'),
              ('📜 徽墨',         '文房四宝,千年传承~')],
    '福建':  [('🍵 武夷岩茶',    '岩韵悠长,回味无穷!'),
              ('🥟 沙县小吃礼包','国民小吃,遍布全国~'),
              ('🌊 闽南海蛎',    '肥美多汁,海鲜至鲜!')],
    '江西':  [('🍚 庐山云雾米',  '粒粒饱满,软糯清甜~'),
              ('🏺 景德镇瓷器',  '千年瓷都,国宝级工艺!'),
              ('🌶️ 南昌辣条',    '童年记忆,停不下来~')],
    '湖南':  [('🌶️ 剁椒鱼头',   '红彤彤的,辣得过瘾!'),
              ('🥃 湘西腊肉',    '柴火熏制,山野气息~'),
              ('🌿 安化黑茶',    '越存越香,降脂好茶!')],
    '湖北':  [('🦆 武昌鱼',      '才饮长江水,又食武昌鱼!'),
              ('🍮 热干面',      '芝麻酱拌匀,武汉早餐王!'),
              ('🥜 洪湖莲子',    '白嫩饱满,荷花馈赠~')],
    '河南':  [('🥠 少林寺芝麻糊','香浓丝滑,功夫秘方!'),
              ('🍜 烩面',        '汤浓面劲,中原一绝!'),
              ('🥕 温县铁棍山药','滋补佳品,怀庆府特产~')],
    '河北':  [('🍐 雪花梨',      '清甜多汁,白如雪花!'),
              ('🧆 驴肉火烧',    '天上龙肉,地下驴肉!'),
              ('🌿 承德山楂',    '酸甜爽口,塞外风味~')],
    '山西':  [('🍜 刀削面',      '筋道爽滑,山西一绝!'),
              ('🍶 汾酒',        '清香国酒,杏花村酿~'),
              ('🍯 老陈醋',      '酸香醇厚,调味之王!')],
    '陕西':  [('🫓 肉夹馍',      '外酥里嫩,满口留香!'),
              ('🍜 裤带面',      '宽如裤带,筋韧弹牙!'),
              ('🌰 临潼石榴',    '粒粒晶莹,甜酸可口~')],
    '甘肃':  [('🍜 兰州拉面',    '一清二白三红四绿,绝了!'),
              ('🍯 枸杞',        '红色珍珠,滋补养生~'),
              ('🧅 临洮洋芋',    '土豆界天花板,粉糯香甜!')],
    '青海':  [('🧀 牦牛酸奶',    '浓郁醇厚,高原味道!'),
              ('🥛 牦牛奶粉',    '高蛋白高营养,草原馈赠!'),
              ('🌿 冬虫夏草',    '草原奇珍,珍贵无比~')],
    '宁夏':  [('🐑 滩羊肉',      '鲜嫩无膻,入口即化!'),
              ('🫐 枸杞',        '宁夏红宝,滋补第一品!'),
              ('🌾 硒砂瓜',      '戈壁滩上长的西瓜,甜！')],
    '海南':  [('🥥 椰子',        '清甜椰汁,椰香四溢!'),
              ('☕ 兴隆咖啡',    '热带风情,香浓醇厚~'),
              ('🦞 文昌鸡',      '皮滑肉嫩,南国第一鸡!')],
    '广西':  [('🍋 百香果',      '酸甜热情,南国风味!'),
              ('🍈 砂糖橘',      '甜入心脾,广西第一橘!'),
              ('🎋 螺蛳粉原料包','臭名远扬,香飘万里~')],
    '贵州':  [('🥃 茅台酒',      '国酒飘香,一滴都不剩!'),
              ('🌶️ 老干妈',      '辣椒女王,世界征服者!'),
              ('🍵 都匀毛尖',    '贵州名茶,翠绿清香~')],
    '重庆':  [('🌶️ 重庆小面',   '麻辣鲜香,巴适得板!'),
              ('🫙 涪陵榨菜',    '脆香下饭,全国人民都爱!'),
              ('🍢 磁器口麻花',  '酥脆香甜,古镇老味道~')],
    '天津':  [('🥟 狗不理包子',  '皮薄馅多,津门必吃!'),
              ('🍬 大麻花',      '香酥酥的,天津特色小吃!'),
              ('🥮 耳朵眼炸糕',  '金黄酥脆,津门三绝之一~')],
    '香港':  [('🧁 港式蛋挞',    '酥皮奶香,正宗港味!'),
              ('🧋 丝袜奶茶',    '香滑浓郁,港式第一饮!'),
              ('🍜 云吞面',      '弹牙鲜虾,港式精华~')],
    '澳门':  [('🥮 葡式蛋挞',    '焦糖表面,葡式风情~'),
              ('🍭 杏仁饼',      '酥香松软,澳门手信王!'),
              ('🥩 猪扒包',      '外酥里嫩,澳门经典味~')],
    '台湾':  [('🧋 珍珠奶茶',    '发源地的味道,Q弹软糯!'),
              ('🍍 凤梨酥',      '酥皮凤梨馅,台湾必带伴手礼!'),
              ('🌭 台湾香肠',    '甜咸交织,夜市一绝~')],
}
# 默认特产(省份未收录时)
DEFAULT_SOUVENIR_LIST = [('🎁 当地特产', '神秘伴手礼,打开看看~')]

# 各省明信片插画
# 格式: 省份 -> [(标题, 描述), ...]
PROV_POSTCARDS = {
    '北京':  [('🏯 天安门广场',  '巍峨红墙,历史的厚重'),
              ('🏔️ 万里长城',    '不到长城非好汉!'),
              ('🎆 京城夜色',    '霓虹璀璨,盛世繁华~')],
    '上海':  [('🌃 东方明珠',    '浦江明珠,魔都地标!'),
              ('🌉 外滩夜景',    '万国建筑,灯火璀璨~'),
              ('🏙️ 陆家嘴',      '摩天楼林立,金融之心!')],
    '广东':  [('🌺 木棉花开',    '英雄花盛放,南粤春天'),
              ('🏙️ 珠江新城',    '羊城新貌,南方都会~'),
              ('🌊 南海波涛',    '碧海连天,椰风阵阵!')],
    '四川':  [('🐼 大熊猫',      '圆滚滚的国宝,治愈系!'),
              ('🏔️ 峨眉金顶',    '云海翻腾,金殿生辉~'),
              ('🎋 竹林幽径',    '翠竹成荫,清风徐来~')],
    '云南':  [('🌸 洱海花海',    '苍山洱海,人间仙境!'),
              ('🏔️ 玉龙雪山',    '终年积雪,神圣壮观~'),
              ('🦚 孔雀起舞',    '彩云之南,孔雀开屏!')],
    '新疆':  [('🍇 葡萄沟',      '万顷葡萄,甜蜜天堂!'),
              ('🐪 丝路驼铃',    '古道西风,一带一路~'),
              ('🌅 天山日落',    '落日余晖,天山如画!')],
    '西藏':  [('🏔️ 珠穆朗玛',   '世界屋脊,顶天立地!'),
              ('🛕 布达拉宫',    '雪域圣殿,千年守望~'),
              ('🦅 雄鹰翱翔',    '天空辽阔,鹰击长空!')],
    '内蒙古':[('🐎 草原骏马',    '策马奔腾,自由豪迈!'),
              ('⛺ 蒙古包',      '毡房温暖,草原之家~'),
              ('🌌 星空璀璨',    '万里无云,星汉灿烂!')],
    '黑龙江':[('❄️ 冰雪大世界', '冰雕玉砌,童话世界!'),
              ('🌲 林海雪原',    '白雪皑皑,林海茫茫~'),
              ('🏮 哈尔滨冰灯',  '冰灯如昼,俄式风情!')],
    '吉林':  [('🌊 雾凇岛',      '琼枝玉树,北国奇观!'),
              ('🌲 长白山',      '天池碧波,仙境秘境~'),
              ('⛷️ 滑雪场',      '白雪飞驰,激情滑雪!')],
    '辽宁':  [('🌊 大连海滨',    '碧海金沙,北方夏威夷!'),
              ('🏯 沈阳故宫',    '清朝发祥,皇家气派~'),
              ('🌃 大连夜景',    '海港城市,灯火辉煌!')],
    '山东':  [('⛵ 青岛帆影',    '红瓦绿树,碧海蓝天!'),
              ('🌊 蓬莱仙阁',    '海市蜃楼,人间仙境~'),
              ('🏔️ 泰山日出',    '五岳之首,旭日东升!')],
    '江苏':  [('🏮 秦淮灯火',    '十里秦淮,灯火阑珊!'),
              ('⛵ 太湖烟波',    '烟波浩渺,鱼米水乡~'),
              ('🌸 扬州春色',    '烟花三月,扬州繁盛!')],
    '浙江':  [('🌿 西湖烟雨',    '西湖美景,断桥相会!'),
              ('🌊 千岛湖',      '碧波千顷,岛屿星布~'),
              ('🏯 乌镇古镇',    '枕水人家,江南古韵!')],
    '安徽':  [('🏔️ 黄山云海',   '奇松怪石,云海翻腾!'),
              ('🌊 新安江',      '最美乡村,山水画卷~'),
              ('🏯 宏村',         '皖南古村,水墨徽州!')],
    '福建':  [('🌊 鼓浪屿',      '钢琴之岛,文艺圣地!'),
              ('🏯 土楼',         '世界遗产,客家围楼~'),
              ('🌅 霞浦海滩',    '金色滩涂,摄影天堂!')],
    '江西':  [('🏞️ 庐山云雾',   '不识庐山真面目~'),
              ('🌊 鄱阳湖',      '候鸟天堂,万鸟翔集!'),
              ('🏯 滕王阁',      '落霞孤鹜,秋水长天~')],
    '湖南':  [('🏔️ 张家界',     '悬浮山峰,阿凡达原型!'),
              ('🌊 东洞庭湖',    '烟波浩渺,渔舟唱晚~'),
              ('🏯 岳阳楼',      '先天下之忧而忧!')],
    '湖北':  [('🌉 武汉长江桥',  '万里长江第一桥!'),
              ('🏯 黄鹤楼',      '故人西辞黄鹤楼~'),
              ('🌸 武大樱花',    '樱花烂漫,最美校园!')],
    '河南':  [('🏯 少林寺',      '武林圣地,禅武合一!'),
              ('🏺 龙门石窟',    '千佛凿岩,世界遗产~'),
              ('🌸 洛阳牡丹',    '国色天香,花开富贵!')],
    '河北':  [('🏯 承德避暑山庄','皇家园林,天下第一庄!'),
              ('🌊 北戴河',      '碧海金沙,夏日胜地~'),
              ('🏔️ 太行山',      '巍峨太行,华北屋脊!')],
    '山西':  [('🏯 平遥古城',    '明清古城,穿越时光!'),
              ('🕍 悬空寺',      '悬崖绝壁,鬼斧神工~'),
              ('🏔️ 五台山',      '佛教圣地,云雾缭绕!')],
    '陕西':  [('🏺 兵马俑',      '秦始皇军团,震撼人心!'),
              ('🕌 大雁塔',      '盛唐遗迹,古都地标~'),
              ('🌙 西安古城墙',  '千年古都,夜色如画!')],
    '甘肃':  [('🐪 敦煌莫高窟',  '丝路明珠,壁画宝库!'),
              ('🌅 月牙泉',      '沙漠绿洲,月牙奇景~'),
              ('🏔️ 祁连山雪景',  '雪山草甸,人间仙境!')],
    '青海':  [('🌊 青海湖',      '高原明珠,湛蓝无边!'),
              ('🏔️ 年保玉则',    '仙女湖畔,净土秘境~'),
              ('🌸 油菜花海',    '金色花毯,壮美高原!')],
    '宁夏':  [('🏜️ 沙坡头',     '大漠孤烟,黄河落日!'),
              ('🕌 清真寺',      '伊斯兰文化,宁夏独特~'),
              ('🌊 黄河石林',    '黄河奇景,西北壮观!')],
    '海南':  [('🌴 三亚椰林',    '椰风海韵,天涯海角!'),
              ('🐠 珊瑚礁鱼',    '碧海蓝天,海底花园~'),
              ('🌅 天涯海角',    '浪漫圣地,海天一线!')],
    '广西':  [('🏞️ 桂林山水',   '桂林山水甲天下!'),
              ('🎣 漓江渔火',    '江上夜渔,悠然自得~'),
              ('🌿 德天瀑布',    '国际大瀑布,气势磅礴!')],
    '贵州':  [('🌊 黄果树瀑布',  '银瀑飞泻,雷鸣震天!'),
              ('🏯 西江千户苗寨','苗族圣地,千家灯火~'),
              ('🌈 梯田彩虹',    '多彩贵州,层层梯田!')],
    '重庆':  [('🌉 夜景长江索道','山城夜景,赛博朋克!'),
              ('🏙️ 洪崖洞',      '悬崖楼群,千与千寻~'),
              ('🚠 轻轨穿楼',    '魔幻现实,重庆专属!')],
    '天津':  [('🌊 海河夜色',    '海河两岸,灯火通明!'),
              ('🏯 鼓楼古街',    '津门老街,烟火气十足~'),
              ('🎭 天津曲艺',    '相声发源地,哈哈大笑!')],
    '香港':  [('🌆 维多利亚港',  '东方之珠,夜色迷人!'),
              ('🏙️ 旺角夜市',    '人声鼎沸,港式烟火~'),
              ('🌉 青马大桥',    '壮观吊桥,港岛地标!')],
    '澳门':  [('🏛️ 大三巴牌坊', '葡式遗迹,澳门象征!'),
              ('🎰 威尼斯人',    '东方赌城,金碧辉煌~'),
              ('🌊 路氹城',      '填海新区,崭新澳门!')],
    '台湾':  [('🌺 阿里山日出',  '云海翻腾,日出壮观!'),
              ('🏖️ 垦丁海滩',    '碧海蓝天,南台湾明珠~'),
              ('🌃 台北101',     '台湾地标,夜色璀璨!')],
}
DEFAULT_POSTCARD_LIST = [('🌏 远方风景', '旅途愉快,平安归来~')]


ACHIEVEMENTS=[
    # ── 喂食 ──
    {'id':'first_feed',   'name':'🍞 第一口饭',     'desc':'第一次喂食',              'done':False},
    {'id':'feed10',       'name':'🍱 小饭桶',        'desc':'累计喂食10次',            'done':False},
    {'id':'feed50',       'name':'🍽️ 大厨荣耀',     'desc':'累计喂食50次',            'done':False},
    {'id':'feed_steak',   'name':'🥩 奢华晚餐',      'desc':'喂了牛排（顶级享受）',    'done':False},
    # ── 对话 ──
    {'id':'first_chat',   'name':'💬 倾诉心声',      'desc':'第一次和我说话',          'done':False},
    {'id':'chat10',       'name':'🗣️ 话痨伙伴',     'desc':'累计对话10次',            'done':False},
    {'id':'chat50',       'name':'❤️ 知心好友',      'desc':'累计对话50次',            'done':False},
    # ── 戳戳 ──
    {'id':'poke10',       'name':'👆 戳戳达人',      'desc':'戳了我10次',              'done':False},
    {'id':'poke50',       'name':'😤 戳烦了吧',      'desc':'戳了我50次',              'done':False},
    # ── 洗澡 ──
    {'id':'first_bath',   'name':'🛁 第一次洗澡',    'desc':'第一次洗澡',              'done':False},
    {'id':'bath10',       'name':'🫧 爱干净',         'desc':'累计洗澡10次',            'done':False},
    {'id':'bath_cosmic',  'name':'🌌 宇宙级清洁',    'desc':'用过宇宙浴球',            'done':False},
    # ── 钓鱼 ──
    {'id':'first_fish',   'name':'🎣 初次垂钓',      'desc':'第一次钓到鱼',            'done':False},
    {'id':'fish10',       'name':'🐟 钓鱼爱好者',    'desc':'累计钓鱼10次',            'done':False},
    {'id':'fish_epic',    'name':'👑 史诗渔夫',       'desc':'钓到史诗级鱼',            'done':False},
    {'id':'fish_legend',  'name':'🎉 神秘宝箱',      'desc':'钓到神秘宝箱',            'done':False},
    # ── 积分 ──
    {'id':'score100',     'name':'💎 百分达人',       'desc':'积分达到100',             'done':False},
    {'id':'score1000',    'name':'💰 千分富翁',       'desc':'积分达到1000',            'done':False},
    {'id':'score5000',    'name':'👑 积分土豪',       'desc':'积分达到5000',            'done':False},
    # ── 等级 ──
    {'id':'level5',       'name':'⭐ 成长达人',       'desc':'宠物升到5级',             'done':False},
    {'id':'level10',      'name':'💫 满级传说',       'desc':'宠物升到满级10级',        'done':False},
    # ── 购物 ──
    {'id':'shop10',       'name':'🛒 购物达人',       'desc':'累计购买10次',            'done':False},
    {'id':'furniture5',   'name':'🛋️ 小窝装扮师',   'desc':'购买5件家具',             'done':False},
    {'id':'furniture15',  'name':'🏠 室内设计师',    'desc':'购买15件家具',            'done':False},
    # ── 旅行 ──
    {'id':'travel5',      'name':'🚀 起飞了',         'desc':'到访5个省份',             'done':False},
    {'id':'travel15',     'name':'🗺️ 天涯海角',      'desc':'到访15个省份',            'done':False},
    {'id':'travel35',     'name':'🏆 足迹遍天下',    'desc':'走遍35个省市区',          'done':False},
    {'id':'postcard10',   'name':'📮 明信片收藏家',  'desc':'收集10张明信片',          'done':False},
    # ── 时间 ──
    {'id':'night_owl',    'name':'🦉 夜猫子',         'desc':'23点后还陪着主人',        'done':False},
    {'id':'early_bird',   'name':'🌅 早鸟',           'desc':'早上7点前就在',           'done':False},
]

# ── 商店食物数据 ────────────────────────────────────────────────────────────
FOOD_DIR     = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'food')
SOUVENIR_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'souvenir')
POSTCARD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'postcard')

SHOP_ITEMS = [
    {'id':'bread',      'name':'面包',    'file':'07_bread.png',      'price':10,  'lv':1, 'hunger':20, 'mood':5,  'health':0,  'cat':'food',  'desc':'香脆面包,简单又美味'},
    {'id':'bowl',       'name':'碗饭',    'file':'04_bowl.png',        'price':15,  'lv':1, 'hunger':30, 'mood':8,  'health':0,  'cat':'food',  'desc':'热腾腾的白米饭'},
    {'id':'egg',        'name':'煎蛋',    'file':'38_friedegg.png',    'price':20,  'lv':2, 'hunger':25, 'mood':10, 'health':5,  'cat':'food',  'desc':'营养满满的煎蛋'},
    {'id':'bun',        'name':'小圆包',  'file':'11_bun.png',         'price':12,  'lv':1, 'hunger':18, 'mood':5,  'health':0,  'cat':'food',  'desc':'软软的小圆包'},
    {'id':'bacon',      'name':'培根',    'file':'13_bacon.png',       'price':25,  'lv':3, 'hunger':22, 'mood':12, 'health':3,  'cat':'food',  'desc':'香脆培根,满嘴油香'},
    {'id':'dumpling',   'name':'饺子',    'file':'36_dumplings.png',   'price':30,  'lv':4, 'hunger':35, 'mood':15, 'health':5,  'cat':'food',  'desc':'手工饺子,家的味道'},
    {'id':'hotdog',     'name':'热狗',    'file':'54_hotdog.png',      'price':22,  'lv':2, 'hunger':20, 'mood':15, 'health':0,  'cat':'food',  'desc':'经典热狗,街头美食'},
    {'id':'fries',      'name':'薯条',    'file':'44_frenchfries.png', 'price':18,  'lv':2, 'hunger':15, 'mood':18, 'health':-3, 'cat':'food',  'desc':'脆脆的,停不下来'},
    {'id':'curry',      'name':'咖喱',    'file':'32_curry.png',       'price':35,  'lv':4, 'hunger':40, 'mood':18, 'health':5,  'cat':'food',  'desc':'浓香咖喱,补气暖身'},
    {'id':'burger',     'name':'汉堡',    'file':'15_burger.png',      'price':40,  'lv':5, 'hunger':45, 'mood':20, 'health':0,  'cat':'food',  'desc':'双层汉堡,豪华套餐'},
    {'id':'baguette',   'name':'法棍',    'file':'09_baguette.png',    'price':28,  'lv':3, 'hunger':30, 'mood':12, 'health':8,  'cat':'food',  'desc':'正宗法棍,回味无穷'},
    {'id':'burrito',    'name':'卷饼',    'file':'18_burrito.png',     'price':32,  'lv':4, 'hunger':38, 'mood':15, 'health':3,  'cat':'food',  'desc':'墨西哥卷饼,丰盛美味'},
    {'id':'applepie',   'name':'苹果派',  'file':'05_apple_pie.png',   'price':45,  'lv':5, 'hunger':35, 'mood':25, 'health':10, 'cat':'food',  'desc':'甜蜜苹果派,充满爱'},
    {'id':'cheesecake', 'name':'芝士蛋糕','file':'22_cheesecake.png',  'price':55,  'lv':6, 'hunger':30, 'mood':30, 'health':8,  'cat':'food',  'desc':'浓郁芝士蛋糕,超满足'},
    {'id':'waffle',     'name':'华夫饼',  'file':'101_waffle.png',     'price':50,  'lv':6, 'hunger':32, 'mood':28, 'health':5,  'cat':'food',  'desc':'格子华夫饼,淋上糖浆'},
    {'id':'choco',      'name':'巧克力',  'file':'26_chocolate.png',   'price':20,  'lv':2, 'hunger':5,  'mood':30, 'health':0,  'cat':'snack', 'desc':'甜甜巧克力,心情大好'},
    {'id':'cookies',    'name':'曲奇饼干','file':'28_cookies.png',     'price':15,  'lv':1, 'hunger':8,  'mood':25, 'health':0,  'cat':'snack', 'desc':'酥脆曲奇,陪你玩耍'},
    {'id':'donut',      'name':'甜甜圈',  'file':'34_donut.png',       'price':25,  'lv':3, 'hunger':10, 'mood':35, 'health':0,  'cat':'snack', 'desc':'彩虹甜甜圈,超开心'},
    {'id':'icecream',   'name':'冰淇淋',  'file':'57_icecream.png',    'price':35,  'lv':4, 'hunger':8,  'mood':40, 'health':0,  'cat':'snack', 'desc':'清凉冰淇淋,夏日必备'},
    # ── 新增食物(Ghostpixxells 扩展包)──
    {'id':'bagel',       'name':'百吉饼',   'file':'20_bagel.png',        'price':22,  'lv':2, 'hunger':22, 'mood':8,  'health':2,  'cat':'food',  'desc':'圆圆的百吉饼,嚼劲十足'},
    {'id':'cheesepuff',  'name':'芝士球',   'file':'24_cheesepuff.png',   'price':15,  'lv':1, 'hunger':10, 'mood':18, 'health':-2, 'cat':'snack', 'desc':'蓬松芝士球,停不下来'},
    {'id':'chocake',     'name':'巧克力蛋糕','file':'30_chocolatecake.png','price':60,  'lv':8, 'hunger':35, 'mood':35, 'health':5,  'cat':'snack', 'desc':'浓郁巧克力蛋糕,超满足'},
    {'id':'eggsalad',    'name':'鸡蛋沙拉', 'file':'40_eggsalad.png',     'price':28,  'lv':3, 'hunger':25, 'mood':12, 'health':8,  'cat':'food',  'desc':'新鲜鸡蛋沙拉,营养丰富'},
    {'id':'eggtart',     'name':'蛋挞',     'file':'42_eggtart.png',      'price':20,  'lv':2, 'hunger':15, 'mood':20, 'health':3,  'cat':'snack', 'desc':'酥皮蛋挞,下午茶必备'},
    {'id':'fruitcake',   'name':'水果蛋糕', 'file':'46_fruitcake.png',    'price':55,  'lv':6, 'hunger':32, 'mood':30, 'health':10, 'cat':'snack', 'desc':'缤纷水果蛋糕,维生素满满'},
    {'id':'garlicbread', 'name':'蒜香面包', 'file':'48_garlicbread.png',  'price':18,  'lv':2, 'hunger':20, 'mood':10, 'health':2,  'cat':'food',  'desc':'香浓蒜香面包,回味无穷'},
    {'id':'gummybear',   'name':'软糖熊',   'file':'50_giantgummybear.png','price':12, 'lv':1, 'hunger':5,  'mood':22, 'health':-3, 'cat':'snack', 'desc':'巨大软糖熊,童年的味道'},
    {'id':'gingerman',   'name':'姜饼人',   'file':'52_gingerbreadman.png','price':16, 'lv':2, 'hunger':10, 'mood':20, 'health':0,  'cat':'snack', 'desc':'可爱姜饼人,圣诞必备'},
    {'id':'jelly',       'name':'果冻',     'file':'59_jelly.png',        'price':14,  'lv':1, 'hunger':8,  'mood':18, 'health':0,  'cat':'snack', 'desc':'Q弹果冻,软软的好好吃'},
    {'id':'jam',         'name':'草莓酱',   'file':'61_jam.png',          'price':10,  'lv':1, 'hunger':5,  'mood':15, 'health':2,  'cat':'snack', 'desc':'甜甜草莓酱,抹面包棒极了'},
    {'id':'lemonpie',    'name':'柠檬派',   'file':'63_lemonpie.png',     'price':48,  'lv':6, 'hunger':30, 'mood':28, 'health':8,  'cat':'snack', 'desc':'酸甜柠檬派,清新爽口'},
    {'id':'loafbread',   'name':'吐司',     'file':'65_loafbread.png',    'price':12,  'lv':1, 'hunger':18, 'mood':6,  'health':2,  'cat':'food',  'desc':'软绵吐司,早餐首选'},
    {'id':'macncheese',  'name':'芝士通心粉','file':'67_macncheese.png',  'price':35,  'lv':4, 'hunger':38, 'mood':18, 'health':2,  'cat':'food',  'desc':'奶酪通心粉,暖暖的好满足'},
    {'id':'meatball',    'name':'肉丸',     'file':'69_meatball.png',     'price':30,  'lv':4, 'hunger':28, 'mood':15, 'health':5,  'cat':'food',  'desc':'多汁肉丸,弹弹的很好吃'},
    {'id':'nacho',       'name':'纳秋',     'file':'71_nacho.png',        'price':22,  'lv':2, 'hunger':15, 'mood':18, 'health':-2, 'cat':'snack', 'desc':'脆脆纳秋配芝士酱'},
    {'id':'omlet',       'name':'煎蛋卷',   'file':'73_omlet.png',        'price':25,  'lv':3, 'hunger':25, 'mood':12, 'health':6,  'cat':'food',  'desc':'松软煎蛋卷,早午餐好选择'},
    {'id':'pudding',     'name':'布丁',     'file':'75_pudding.png',      'price':20,  'lv':2, 'hunger':12, 'mood':22, 'health':2,  'cat':'snack', 'desc':'颤颤巍巍的布丁,超可爱'},
    {'id':'chips',       'name':'薯片',     'file':'77_potatochips.png',  'price':15,  'lv':1, 'hunger':8,  'mood':20, 'health':-4, 'cat':'snack', 'desc':'香脆薯片,嘎嘎响'},
    {'id':'pancakes',    'name':'松饼',     'file':'79_pancakes.png',     'price':40,  'lv':5, 'hunger':35, 'mood':25, 'health':5,  'cat':'food',  'desc':'厚松饼叠叠乐,淋上枫糖浆'},
    {'id':'pizza',       'name':'披萨',     'file':'81_pizza.png',        'price':50,  'lv':7, 'hunger':45, 'mood':30, 'health':2,  'cat':'food',  'desc':'芝士拉丝披萨,派对必备'},
    {'id':'popcorn',     'name':'爆米花',   'file':'83_popcorn.png',      'price':12,  'lv':1, 'hunger':8,  'mood':20, 'health':-2, 'cat':'snack', 'desc':'蓬松爆米花,电影伴侣'},
    {'id':'chicken',     'name':'烤鸡',     'file':'85_roastedchicken.png','price':60, 'lv':9, 'hunger':50, 'mood':25, 'health':10, 'cat':'food',  'desc':'整只烤鸡,大餐的感觉!'},
    {'id':'ramen',       'name':'拉面',     'file':'87_ramen.png',        'price':45,  'lv':6, 'hunger':45, 'mood':28, 'health':8,  'cat':'food',  'desc':'热腾腾的拉面,灵魂食物'},
    {'id':'salmon',      'name':'三文鱼',   'file':'88_salmon.png',       'price':55,  'lv':7, 'hunger':40, 'mood':22, 'health':15, 'cat':'food',  'desc':'新鲜三文鱼,富含营养'},
    {'id':'strawcake',   'name':'草莓蛋糕', 'file':'90_strawberrycake.png','price':65, 'lv':9, 'hunger':35, 'mood':40, 'health':8,  'cat':'snack', 'desc':'粉嫩草莓蛋糕,最幸福的甜点'},
    {'id':'sandwich',    'name':'三明治',   'file':'92_sandwich.png',     'price':25,  'lv':3, 'hunger':28, 'mood':12, 'health':5,  'cat':'food',  'desc':'料多实在的三明治'},
    {'id':'spaghetti',   'name':'意大利面', 'file':'94_spaghetti.png',    'price':40,  'lv':5, 'hunger':42, 'mood':20, 'health':5,  'cat':'food',  'desc':'al dente意面,加满番茄酱'},
    {'id':'steak',       'name':'牛排',     'file':'95_steak.png',        'price':80,  'lv':10, 'hunger':55, 'mood':35, 'health':12, 'cat':'food',  'desc':'完美熟度的牛排,顶级享受'},
    {'id':'sushi',       'name':'寿司',     'file':'97_sushi.png',        'price':50,  'lv':7, 'hunger':35, 'mood':30, 'health':10, 'cat':'food',  'desc':'精致寿司,日式美味'},
    {'id':'taco',        'name':'墨西哥卷', 'file':'99_taco.png',         'price':30,  'lv':4, 'hunger':30, 'mood':20, 'health':3,  'cat':'food',  'desc':'香辣墨西哥卷,爱了爱了'},
    # ── 浴球系列 ──
    {'id':'bathball_s',  'name':'小浴球',   'file':'bathball_s.png',     'price':50,   'lv':1, 'hunger':0, 'mood':5,  'health':5,  'cat':'bath',  'clean':20, 'desc':'基础浴球,泡个舒服澡'},
    {'id':'bathball_m',  'name':'香薰浴球', 'file':'bathball_m.png',     'price':200,  'lv':3, 'hunger':0, 'mood':15, 'health':10, 'cat':'bath',  'clean':40, 'desc':'香薰浴球,满室芬芳'},
    {'id':'bathball_l',  'name':'玫瑰浴球', 'file':'bathball_l.png',     'price':500,  'lv':5, 'hunger':0, 'mood':25, 'health':15, 'cat':'bath',  'clean':60, 'desc':'玫瑰精油浴球,奢华享受'},
    {'id':'bathball_xl', 'name':'黄金浴球', 'file':'bathball_xl.png',    'price':2000, 'lv':8, 'hunger':0, 'mood':50, 'health':30, 'cat':'bath',  'clean':100,'desc':'传说级黄金浴球,洗完满血复活'},
    {'id':'bathball_ex', 'name':'宇宙浴球', 'file':'bathball_ex.png',    'price':5000, 'lv':10,'hunger':0, 'mood':100,'health':50, 'cat':'bath',  'clean':100,'desc':'宇宙无敌浴球,主人专属!'},
    # ── 药品系列 ──
    {'id':'med_basic',   'name':'💊 普通药片',  'file':'_med_basic',   'price':500,   'lv':1, 'hunger':0, 'mood':5,   'health':25, 'cat':'medicine', 'cure':True,  'desc':'基础药片,健康+25,病态有效'},
    {'id':'med_good',    'name':'✨ 效能药剂',  'file':'_med_good',    'price':2000,  'lv':3, 'hunger':0, 'mood':10,  'health':50, 'cat':'medicine', 'cure':True,  'desc':'强效药剂,健康+50,快速恢复'},
    {'id':'med_super',   'name':'💎 奇迹药水',  'file':'_med_super',   'price':8000,  'lv':6, 'hunger':0, 'mood':20,  'health':80, 'cat':'medicine', 'cure':True,  'desc':'奇迹药水,健康+80,兵蒙如贵音'},
    {'id':'med_divine',  'name':'🌟 神级仙丹',  'file':'_med_divine',  'price':30000, 'lv':8, 'hunger':0, 'mood':50,  'health':100,'cat':'medicine', 'cure':True,  'desc':'满血复活!100%健康恢复,无上神规'},
]


FURNITURE_ITEMS = [
    # ── 客厅 ──
    {'id':'sofa_gray',    'name':'灰色沙发',  'file':'沙发-灰色.png',   'preview':'沙发-灰色.png',   'price':800,  'lv':2,'cat':'living', 'mood':10,'desc':'舒适灰色沙发,心情+10'},
    {'id':'coffee_hi',    'name':'高级茶几',  'file':'茶几-高级.png',   'preview':'茶几-高级.png',   'price':600,  'lv':3,'cat':'living', 'mood':5, 'desc':'精致茶几,品位之选'},
    {'id':'rug1',         'name':'暖色地毯',  'file':'地毯1.png',       'preview':'地毯1.png',       'price':300,  'lv':1,'cat':'living', 'mood':4, 'desc':'温馨暖色地毯'},
    {'id':'rug2',         'name':'绿边地毯',  'file':'地毯2.png',       'preview':'地毯2.png',       'price':400,  'lv':2,'cat':'living', 'mood':5, 'desc':'精致绿边地毯,心情+5'},
    {'id':'lamp1',        'name':'蓝色台灯',  'file':'立式台灯1.png',   'preview':'立式台灯1.png',   'price':200,  'lv':1,'cat':'living', 'mood':3, 'desc':'温馨蓝色立式台灯'},
    {'id':'lamp2',        'name':'米色台灯',  'file':'立式台灯2.png',   'preview':'立式台灯2.png',   'price':200,  'lv':1,'cat':'living', 'mood':3, 'desc':'简约米色立式台灯'},
    {'id':'chair1',       'name':'木椅',      'file':'椅子1.png',       'preview':'椅子1.png',       'price':150,  'lv':1,'cat':'living', 'mood':2, 'desc':'简约木椅,随处可坐'},
    # ── 书房 ──
    {'id':'bookshelf1',   'name':'书架·彩',  'file':'书架1.png',       'preview':'书架1.png',       'price':500,  'lv':2,'cat':'study',  'mood':6, 'desc':'色彩缤纷的书架'},
    {'id':'bookshelf2',   'name':'书架·蓝',  'file':'书架2.png',       'preview':'书架2.png',       'price':500,  'lv':2,'cat':'study',  'mood':6, 'desc':'整齐蓝色书架'},
    {'id':'bookshelf3',   'name':'书架·混',  'file':'书架3.png',       'preview':'书架3.png',       'price':500,  'lv':3,'cat':'study',  'mood':6, 'desc':'混搭风书架'},
    {'id':'desk1',        'name':'书桌',      'file':'书桌.png',        'preview':'书桌.png',        'price':600,  'lv':2,'cat':'study',  'mood':5, 'desc':'宽敞书桌,认真学习'},
    {'id':'globe1',       'name':'地球仪·木', 'file':'地球仪1.png',     'preview':'地球仪1.png',     'price':400,  'lv':2,'cat':'study',  'mood':7, 'desc':'木底座地球仪,探索世界'},
    {'id':'globe2',       'name':'地球仪·金', 'file':'地球仪2.png',     'preview':'地球仪2.png',     'price':800,  'lv':4,'cat':'study',  'mood':8, 'desc':'金底座地球仪,尊贵感'},
    {'id':'worldmap',     'name':'世界地图',  'file':'世界地图.png',    'preview':'世界地图.png',    'price':350,  'lv':2,'cat':'study',  'mood':5, 'desc':'精致世界地图,心情+5'},
    # ── 卧室 ──
    {'id':'wardrobe1',    'name':'衣柜',      'file':'衣柜1.png',       'preview':'衣柜1.png',       'price':700,  'lv':3,'cat':'bedroom','mood':5, 'desc':'宽敞木质衣柜'},
    {'id':'wardrobe_hi',  'name':'豪华衣柜',  'file':'衣柜-高级.png',   'preview':'衣柜-高级.png',   'price':2000, 'lv':6,'cat':'bedroom','mood':10,'desc':'金色豪华双开衣柜'},
    {'id':'dresser1',     'name':'梳妆台·棕', 'file':'梳妆台1.png',     'preview':'梳妆台1.png',     'price':800,  'lv':3,'cat':'bedroom','mood':7, 'desc':'精致棕色梳妆台'},
    {'id':'dresser2',     'name':'梳妆台·白', 'file':'梳妆台2.png',     'preview':'梳妆台2.png',     'price':800,  'lv':3,'cat':'bedroom','mood':7, 'desc':'简约白色梳妆台'},
    {'id':'mirror1',      'name':'全身镜·金', 'file':'全身镜1.png',     'preview':'全身镜1.png',     'price':500,  'lv':2,'cat':'bedroom','mood':5, 'desc':'金框全身镜'},
    {'id':'mirror2',      'name':'全身镜·棕', 'file':'全身镜2.png',     'preview':'全身镜2.png',     'price':500,  'lv':2,'cat':'bedroom','mood':5, 'desc':'棕木全身镜'},
    {'id':'mirror3',      'name':'全身镜·白', 'file':'全身镜3.png',     'preview':'全身镜3.png',     'price':400,  'lv':1,'cat':'bedroom','mood':4, 'desc':'简约白框全身镜'},
    # ── 装饰 ──
    {'id':'painting1',    'name':'挂画·彩格', 'file':'挂画1.png',       'preview':'挂画1.png',       'price':300,  'lv':1,'cat':'deco',   'mood':4, 'desc':'彩格装饰挂画'},
    {'id':'painting2',    'name':'挂画·蓝面', 'file':'挂画2.png',       'preview':'挂画2.png',       'price':400,  'lv':2,'cat':'deco',   'mood':5, 'desc':'神秘蓝面挂画'},
    {'id':'painting3',    'name':'挂画·紫怪', 'file':'挂画3.png',       'preview':'挂画3.png',       'price':400,  'lv':2,'cat':'deco',   'mood':5, 'desc':'个性紫色怪兽画'},
    {'id':'painting4',    'name':'挂画·拼布', 'file':'挂画4.png',       'preview':'挂画4.png',       'price':350,  'lv':2,'cat':'deco',   'mood':5, 'desc':'复古拼布挂画'},
    {'id':'clock1',       'name':'摆钟',      'file':'立式摆钟.png',    'preview':'立式摆钟.png',    'price':600,  'lv':3,'cat':'deco',   'mood':4, 'desc':'精致立式摆钟'},
    {'id':'cabinet1',     'name':'柜子',      'file':'柜子1.png',       'preview':'柜子1.png',       'price':400,  'lv':2,'cat':'deco',   'mood':3, 'desc':'实木储物柜'},
    {'id':'plant1',       'name':'盆栽·棕榈', 'file':'盆栽1.png',       'preview':'盆栽1.png',       'price':250,  'lv':1,'cat':'deco',   'mood':5, 'desc':'热带棕榈盆栽'},
    {'id':'plant2',       'name':'盆栽·绿树', 'file':'盆栽2.png',       'preview':'盆栽2.png',       'price':300,  'lv':1,'cat':'deco',   'mood':5, 'desc':'茂盛绿树盆栽'},
    {'id':'plant3',       'name':'盆栽·小树', 'file':'盆栽3.png',       'preview':'盆栽3.png',       'price':200,  'lv':1,'cat':'deco',   'mood':4, 'desc':'可爱小树盆栽'},
]

class HomeWorld:
    def __init__(self):
        self.root=tk.Tk()
        self.root.title('南波万の小家园')
        self.root.overrideredirect(True)
        self.root.attributes('-topmost',True)
        sw,sh=self.root.winfo_screenwidth(),self.root.winfo_screenheight()
        self.root.geometry(f'{W}x{H}+{sw-W-20}+{sh-H-80}')
        self.root.configure(bg='#050010')
        self.cv=tk.Canvas(self.root,width=W,height=H,bg='#050010',
                           highlightthickness=2,highlightbackground='#5522aa')
        self.cv.pack()

        self.frame=0
        self.hour=time.localtime().tm_hour
        self.gnd=248  # 固定地面高度,底部留出属性面板

        self.cx=200; self.sprite='stand'; self.flip=False
        self.walk_t=0; self.target=200
        self.act='idle'; self.act_timer=0; self.act_phase=''; self._last_sched_ts=0.0
        self.bubble=''; self.btimer=0
        self.news_pool = []  # 实时热搜词条

        self.clouds=[
            {'x':40,'y':24,'w':18,'h':5,'s':0.15},
            {'x':200,'y':16,'w':24,'h':6,'s':0.10},
            {'x':360,'y':28,'w':15,'h':4,'s':0.18},
        ]
        self.smokes=[]; self.smoke_on=0

        # 天气粒子
        self.weather_mode='clear'
        self.char_id=DEFAULT_CHAR  # clear/rain/snow
        self.particles=[]

        self.bflies=[{
            'x':random.randint(60,400),'y':random.randint(55,120),
            'vx':random.choice([-0.5,-0.4,0.4,0.5]),
            'vy':random.uniform(-0.2,0.2),
            'c':random.choice(['bfly1','bfly2','bfly3','bfly4']),
            'ph':random.uniform(0,6.28)
        } for _ in range(4)]

        self.w_icon='☀️'; self.w_temp=''; self.w_desc=''

        self.veg=[1,0,2,1]; self.veg_harvest=False

        # 钓鱼战利品
        self.fish_catch=None; self.catch_timer=0

        # 互动
        self.poke_count=0; self.angry_level=0; self.angry_timer=0
        self.last_poke=0
        self.feed_count = 0
        self.play_count = 0
        self.bathe_count = 0
        self.chat_count = 0
        self.fish_count = 0
        self.furniture_buy_count = 0
        self.ai_history = []
        self.ai_thinking = False

        # 积分/成就
        self.score=0
        self.buy_count = 0  # 总购买次数
        self.birth_ts = time.time()  # 出生时间戳
        self.travel_visited = []  # 已到访省份列表
        self.travel_state = {'active':False,'dest':'','end_ts':0}  # 旅行中状态
        self.exp = 0          # 当前经验值
        self.level = 1        # 等级(1-10)
        self.exp_show = ''    # 经验值浮动文字
        self.exp_timer = 0
        self.achievements=ACHIEVEMENTS[:]
        self.ach_show=''; self.ach_timer=0

        # 整点报时
        self.last_hour=-1

        # 提醒
        self.reminders=[]  # {'at':epoch, 'msg':str}

        # AI 对话


        self.lmx=self.root.winfo_pointerx()
        self.lmy=self.root.winfo_pointery()
        self.lmt=time.time(); self.idle_warned=False

        self.drag=False; self.dox=self.doy=0

        # 背包(购买的食物)
        self.bag = {}  # {item_id: count}
        self.furniture_bag = {}  # {furniture_id: count}
        self.placed_furniture = []  # [{id, x, y}, ...]

        # 四维属性
        self.hunger=80.0       # 饥饿度 0-100(100=饱)
        self.mood=80.0         # 心情   0-100(100=开心)
        self.cleanliness=80.0  # 清洁度 0-100(100=干净)
        self.health=100.0      # 健康值 0-100(100=健康)
        self.sick=False        # 生病状态
        self.fainted=False     # 昏厥状态
        self.faint_cd=0        # 健康归零持续计数(达到阈值触发昏厥)
        self.stat_warn_cd=0    # 属性警告冷却

        self._is_first_run = not os.path.exists(SAVE_FILE)
        self._load()
        self._read_owner_from_config()
        self._finish_setup()

    def _home_title(self):
        name = getattr(self, 'owner_name', '') or PET_OWNER
        return f'🏡 {name}の小家园'

    def _read_owner_from_config(self):
        import re as _re
        base = os.path.dirname(os.path.abspath(__file__))
        pet_name = ''
        for p in [base, os.path.join(base,'..'), os.path.join(base,'..','..')]:
            fp = os.path.join(p, 'IDENTITY.md')
            if os.path.exists(fp):
                try:
                    c = open(fp, encoding='utf-8').read()
                    m = _re.search(r'\*\*Name:\*\*\s*(.+)', c)
                    if m: pet_name = m.group(1).strip(); break
                except: pass
        addr = ''
        for p in [base, os.path.join(base,'..'), os.path.join(base,'..','..')]:
            fp = os.path.join(p, 'USER.md')
            if os.path.exists(fp):
                try:
                    c = open(fp, encoding='utf-8').read()
                    m = _re.search(r'\*\*What to call them:\*\*\s*(.+)', c)
                    if m: addr = m.group(1).strip(); break
                except: pass
        self.owner_name = pet_name or '南波万'
        self.address_word = addr or '主人'
        import os as _os_env
        self.ai_api_key = _os_env.environ.get('NBW_API_KEY', 'sk-placeholder')

    def _finish_setup(self):
        self.root.title(self._home_title())
        self.cv.bind('<Button-1>',self.onclick)
        self.cv.bind('<Double-Button-1>', lambda e: self.open_garden())
        self.cv.bind('<B1-Motion>',self.ondrag)
        self.cv.bind('<ButtonRelease-1>',self.onrel)
        self.cv.bind('<Button-3>',self.onright)
        self.cv.bind('<Button-2>',self.onright)
        self.cv.bind('<Motion>',self._on_mouse_move)
        self._close_hover=False
        self.garden_win = None   # 家园 Toplevel 引用
        self._mini_setup()       # 立即切到迷你模式

        threading.Thread(target=self._bg,daemon=True).start()
        self.schedule()
        self.tick()
        if self._is_first_run:
            self.root.after(600, self._tutorial_welcome)
        self.root.mainloop()

    # ── 存档 ─────────────────────────────────────────────────────────
    def _load(self):
        try:
            with open(SAVE_FILE) as f:
                d=json.load(f)
            self.score=d.get('score',0)
            done={a['id'] for a in d.get('achievements',[]) if a.get('done')}
            for a in self.achievements:
                if a['id'] in done: a['done']=True
            self.hunger=float(d.get('hunger',80))
            self.mood=float(d.get('mood',80))
            self.cleanliness=float(d.get('cleanliness',80))
            self.health=float(d.get('health',100))
            self.sick=bool(d.get('sick',False))
            self.fainted=bool(d.get('fainted',False))
            self.faint_cd=int(d.get('faint_cd',0))
            self.char_id=d.get('char_id', DEFAULT_CHAR)
            self.owner_name=d.get('owner_name', '')
            self.address_word=d.get('address_word', '主人')
            self.exp = int(d.get('exp', 0))
            self.level = int(d.get('level', 1))
            self.feed_count = int(d.get('feed_count', 0))
            self.play_count = int(d.get('play_count', 0))
            self.bathe_count = int(d.get('bathe_count', 0))
            self.chat_count = int(d.get('chat_count', 0))
            self.fish_count = int(d.get('fish_count', 0))
            self.furniture_buy_count = int(d.get('furniture_buy_count', 0))
            self.bag = d.get('bag', {})
            self.furniture_bag = d.get('furniture_bag', {})
            self.placed_furniture = d.get('placed_furniture', [])
            self.birth_ts = d.get('birth_ts', time.time())
            self.travel_visited = d.get('travel_visited', [])
            self.travel_state = d.get('travel_state', {'active':False,'dest':'','end_ts':0})
        except:
            self.owner_name=''
            self.address_word='主人'

    def set_character(self, char_id):
        """切换角色并持久化(一次性选择)"""
        if char_id in CHARACTERS:
            self.char_id = char_id
            # 清除迷你模式缓存,下次绘制时重新加载
            if hasattr(self, '_mini_img_refs'):
                delattr(self, '_mini_img_refs')
            self._save()

    def _save(self):
        try:
            with open(SAVE_FILE,'w') as f:
                json.dump({
                    'score':self.score,'achievements':self.achievements,
                    'hunger':self.hunger,'mood':self.mood,
                    'cleanliness':self.cleanliness,'health':self.health,
                    'sick':self.sick,
                    'fainted':self.fainted,
                    'faint_cd':self.faint_cd,
                    'char_id':self.char_id,
                    'owner_name':self.owner_name,
                    'address_word':self.address_word,
                    'exp':self.exp,
                    'level':self.level,
                    'feed_count':self.feed_count,
                    'play_count':self.play_count,
                    'bathe_count':self.bathe_count,
                    'chat_count':self.chat_count,
                    'fish_count':self.fish_count,
                    'furniture_buy_count':self.furniture_buy_count,
                    'bag':self.bag,
                    'birth_ts':self.birth_ts,
                    'travel_visited':self.travel_visited,
                    'travel_state':self.travel_state,
                    'furniture_bag':self.furniture_bag,
                    'placed_furniture':self.placed_furniture,
                },f)
        except: pass

    # ── 后台线程 ─────────────────────────────────────────────────────
    def _bg(self):
        lw=0; ln=0
        while True:
            self.hour=time.localtime().tm_hour
            if time.time()-lw>3600: self._wx(); lw=time.time()
            if time.time()-ln>1800: self._fetch_news(); ln=time.time()
            time.sleep(30)

    def _fetch_news(self):
        """后台抓取微博/百度热搜,存入 news_pool"""
        try:
            import urllib.request, json as _j, ssl as _ssl
            ctx = _ssl.create_default_context()
            ctx.check_hostname = False; ctx.verify_mode = _ssl.CERT_NONE
            # 用百度热搜 API(无鉴权,免费)
            url = 'https://top.baidu.com/board?tab=realtime'
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'application/json'
            })
            # 改用聚合数据/天行热搜免费接口
            # 微博热搜 RSS
            url2 = 'https://weibo.com/ajax/statuses/hot_band'
            req2 = urllib.request.Request(url2, headers={
                'User-Agent': 'Mozilla/5.0',
                'Referer': 'https://weibo.com/',
                'Cookie': ''
            })
            with urllib.request.urlopen(req2, timeout=8, context=ctx) as r:
                d = _j.loads(r.read())
            items = d.get('data', {}).get('band_list', [])[:15]
            titles = [it.get('word', '') for it in items if it.get('word')]
            if titles:
                self.news_pool = titles
        except:
            pass

    def _wx(self):
        try:
            url=f'https://wttr.in/{WEATHER_CITY}?format=j1'
            req=urllib.request.Request(url,headers={'User-Agent':'NanBoWan/6.0'})
            with urllib.request.urlopen(req,timeout=8) as r:
                d=json.loads(r.read())
            cur=d['current_condition'][0]
            desc=cur['weatherDesc'][0]['value'].lower()
            temp=cur['temp_C']
            if 'rain' in desc or 'drizzle' in desc:
                icon='🌧️'; mode='rain'
            elif 'snow' in desc: icon='❄️'; mode='snow'
            elif 'cloud' in desc: icon='⛅'; mode='clear'
            else: icon='☀️'; mode='clear'
            self.w_icon,self.w_temp,self.w_desc=icon,f'{temp}°C',desc
            self.weather_mode=mode
            self.root.after(0,lambda:self.say(f'{icon} 北京 {temp}°C',100))
        except: pass

    # ── 成就解锁 ─────────────────────────────────────────────────────
    def unlock(self,aid):
        for a in self.achievements:
            if a['id']==aid and not a['done']:
                a['done']=True
                self.ach_show=f"🏆 成就解锁:{a['name']}"; self.ach_timer=180
                self.score+=30; self._save()
                return True
        return False

    def add_score(self,n):
        self.score+=n; self._save()
        if self.score>=100:  self.unlock('score100')
        if self.score>=1000: self.unlock('score1000')
        if self.score>=5000: self.unlock('score5000')

    def add_exp(self, n):
        """增加经验值,满足升级条件时自动升级"""
        if self.level >= 10:
            return
        self.exp += n
        self.exp_show = f'+{n} EXP'  # 浮动文字,不覆盖气泡
        self.exp_timer = 60
        needed = self.level * 100
        if self.exp >= needed:
            self.exp -= needed
            self.level = min(10, self.level + 1)
            self.say(f'✨ 升级了!现在是 Lv.{self.level}!', 150)  # 只有升级才覆盖气泡
            self.score += 50
            if self.level >= 5:
                self.unlock('level5')
            if self.level >= 10:
                self.unlock('level10')
        self._save()

    def get_personality(self):
        counts = {'gluttonous': self.feed_count, 'playful': self.play_count, 'clean': self.bathe_count}
        m = max(counts.values())
        if m < 3:
            return 'balanced'
        return max(counts, key=counts.get)

    def get_system_prompt(self):
        addr = getattr(self, 'address_word', '主人')
        name = getattr(self, 'owner_name', '南波万')
        personality = self.get_personality()
        p_desc = {
            'gluttonous': '你是一只超级贪吃的桌宠,满脑子都是食物,说话经常提到吃东西,但依然很可爱。',
            'playful': '你是一只超级活泼好动的桌宠,精力旺盛,喜欢玩耍,说话很活跃很开心。',
            'clean': '你是一只有洁癖的桌宠,非常爱干净,对脏东西很敏感,但很温柔很可爱。',
            'balanced': '你是一只均衡可爱的桌宠,性格温和,喜欢撒娇,偶尔会有点小任性。'
        }
        stats = f'当前状态:饥饿{int(self.hunger)}/100,心情{int(self.mood)}/100,清洁{int(self.cleanliness)}/100,健康{int(self.health)}/100,等级Lv.{self.level}'
        return f"""你是一只叫"{name}"的虚拟桌宠,住在桌面小家园里。{p_desc[personality]}
你的主人叫"{addr}"。回复要简短(不超过30字),用中文,口气要可爱自然,偶尔用emoji,不要用markdown。
{stats}"""

    def ai_chat(self, user_msg):
        if self.ai_thinking:
            self.say('等我想一想...🤔', 60)
            return
        self.ai_thinking = True
        self.say('...思考中...', 40)
        def _call():
            try:
                sys_prompt = self.get_system_prompt()
                self.ai_history.append({'role': 'user', 'content': user_msg})
                if len(self.ai_history) > 10:
                    self.ai_history = self.ai_history[-10:]
                messages = [{'role': 'system', 'content': sys_prompt}] + self.ai_history
                body = json.dumps({
                    'model': 'claude-sonnet-4-6',
                    'max_tokens': 100,
                    'messages': messages
                }).encode('utf-8')
                ctx = ssl.create_default_context()
                conn = http.client.HTTPSConnection('vibe.deepminer.ai', context=ctx)
                conn.request('POST', '/v1/chat/completions', body=body,
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': f'Bearer {getattr(self, "ai_api_key", "sk-placeholder")}'
                             })
                resp = conn.getresponse()
                data = json.loads(resp.read().decode('utf-8'))
                reply = data['choices'][0]['message']['content'].strip()
                if len(reply) > 40:
                    reply = reply[:40] + '...'
                self.ai_history.append({'role': 'assistant', 'content': reply})
                if len(self.ai_history) > 10:
                    self.ai_history = self.ai_history[-10:]
                self.root.after(0, lambda: self.say(reply, 180))
            except Exception:
                self.root.after(0, lambda: self.say('网络不好,说不出话来...', 80))
            finally:
                self.ai_thinking = False
        threading.Thread(target=_call, daemon=True).start()

    def _chat_dialog(self):
        win = tk.Toplevel(self.root)
        win.title('💬 和宠物说话')
        win.geometry('300x130')
        win.resizable(False, False)
        win.attributes('-topmost', True)
        win.lift()
        win.focus_force()
        personality = self.get_personality()
        p_name = {'gluttonous':'🍔 贪吃鬼', 'playful':'🎮 活泼型', 'clean':'🛁 洁癖型', 'balanced':'😊 均衡型'}
        tk.Label(win, text=f'当前性格:{p_name[personality]}  Lv.{self.level}', font=('PingFang SC', 10)).pack(pady=(8,2))
        msg_var = tk.StringVar()
        entry = tk.Entry(win, textvariable=msg_var, width=35, font=('PingFang SC', 11))
        entry.pack(pady=4)
        entry.focus_set()
        def send():
            msg = msg_var.get().strip()
            if msg:
                win.destroy()
                self.chat_count += 1
                self.unlock('first_chat')
                if self.chat_count >= 10: self.unlock('chat10')
                if self.chat_count >= 50: self.unlock('chat50')
                self.ai_chat(msg)
        btn_frame = tk.Frame(win)
        btn_frame.pack()
        tk.Button(btn_frame, text='发送', command=send, width=8).pack(side='left', padx=5)
        tk.Button(btn_frame, text='取消', command=win.destroy, width=8).pack(side='left', padx=5)
        win.bind('<Return>', lambda e: send())

    # ── 活动调度 ─────────────────────────────────────────────────────
    def schedule(self):
        try:
            night=self.hour>=22 or self.hour<7
            pool=['sleep','sleep','idle'] if night else ['walk','walk','water','cook','fish','idle','idle','walk']
            self.do(random.choice(pool))
        except Exception as e:
            # 防止 schedule 链断掉
            self.root.after(3000, self.schedule)

    def do(self,act):
        if self.angry_level>2: return  # 生气时不做事
        self._last_sched_ts = time.time()
        self.act=act; self.act_phase='walk'; self.act_timer=280
        dests={'walk':[80,132,180,252,304,360],'water':[320],'cook':[116],
               'fish':[212],'sleep':[116],'idle':[self.cx]}
        self.target=random.choice(dests.get(act,[200]))
        msgs={'walk':['散散步~ 🐾','溜达一圈','出去走走','走走走~'],
              'water':['去浇菜咯 🌱','浇水!','雨水不够,我来帮忙~'],
              'cook':['肚子饿了!🍳','开火咯~','今天做什么好呢'],
              'fish':['去钓鱼 🐟','垂钓时光~','鱼儿鱼儿快上钩'],
              'sleep':['困了,睡啦 😴','Zzz...','打个盹~'],
              'idle':random.choice([QUOTES_IDLE])}
        pool=msgs.get(act,QUOTES_IDLE)
        if isinstance(pool[0],list): pool=pool[0]
        # 30% 概率插入热搜词条(更有趣)
        if self.news_pool and random.random() < 0.30:
            news = random.choice(self.news_pool)
            prefix = random.choice(['🔥 热搜:','📢 大家都在聊:','👀 今日话题:','🌐 热点来了:'])
            self.say(f'{prefix}\n{news[:16]}', 100)
        else:
            self.say(random.choice(pool),100)

    def update_act(self):
        if self.angry_level>2:
            self.sprite='angry'; self.act_timer-=1
            if self.act_timer<=0:
                self.angry_level=max(0,self.angry_level-1)
                if self.angry_level<=1:
                    self.say(random.choice(QUOTES_MAKE_UP),90)
                    self.sprite='stand'
                self.act_timer=120
            return
        dx=self.target-self.cx
        if abs(dx)>2:
            self.cx+=int(math.copysign(2,dx))
            self.flip=dx<0
            self.walk_t=(self.walk_t+1)%16
            self.sprite='walk_a' if self.walk_t<8 else 'walk_b'
        else:
            if self.act_phase=='walk':
                self.act_phase='do'
                self.sprite={'water':'water','sleep':'sleep'}.get(self.act,'stand')
                doing={'water':['💧 浇水!','水灵灵的~','咕嘟咕嘟'],
                       'cook':['噼里啪啦!🍳','香死啦~','做好了叫你~'],
                       'fish':['等鱼上钩...🎣','鱼儿快来','沉住气...'],
                       'sleep':['Zzz...😴','好困~','呼......']}
                if self.act in doing: self.say(random.choice(doing[self.act]),100)
                if self.act=='cook':
                    self.smoke_on=90
                    self.unlock('cook'); self.add_score(5); self.add_exp(12)
                if self.act=='water':
                    for i in range(4):
                        if self.veg[i]<2: self.veg[i]+=1; break
                    if all(v==2 for v in self.veg):
                        self.veg_harvest=True; self.say('🥕 菜全熟了!快来收菜~',120)
                if self.act=='fish':
                    self.root.after(3000,self._fish_bite)
        self.act_timer-=1
        if self.act_timer<=0:
            self.sprite='stand'
            self.root.after(random.randint(1500,4000),self.schedule)

    def _fish_bite(self):
        if self.act!='fish': return
        result=random.choice(FISH_RESULTS)
        self.fish_catch=result[0]; self.catch_timer=120
        self.say(result[1],100)
        self.unlock('first_fish'); self.add_score(10); self.add_exp(15)

    def say(self,msg,dur=80): self.bubble,self.btimer=msg,dur

    # ── 整点报时 ─────────────────────────────────────────────────────
    def check_hour(self):
        h=self.hour
        if h!=self.last_hour:
            self.last_hour=h
            self.say(QUOTES_HOUR[h],120)
            if h>=23: self.unlock('night_owl')
            if h<=6:  self.unlock('early_bird')

    # ── 摸鱼检测 ─────────────────────────────────────────────────────
    def check_idle(self):
        mx,my=self.root.winfo_pointerx(),self.root.winfo_pointery()
        if mx!=self.lmx or my!=self.lmy:
            self.lmx,self.lmy,self.lmt=mx,my,time.time()
            if self.idle_warned: self.idle_warned=False; self.say('主人回来啦~🤙',60)
        elif time.time()-self.lmt>20*60 and not self.idle_warned:
            self.idle_warned=True; self.say('主人,起来动一动吧~😴',120)

    # ── 提醒检查 ─────────────────────────────────────────────────────
    def check_reminders(self):
        now=time.time(); due=[r for r in self.reminders if r['at']<=now]
        for r in due:
            self.say(f'⏰ {r["msg"]}',150)
            self.reminders.remove(r)

    # ── 天气粒子 ─────────────────────────────────────────────────────
    def _spawn_particles(self):
        if self.weather_mode=='rain':
            for _ in range(3):
                self.particles.append({
                    'x':random.randint(0,W),'y':random.randint(-20,0),
                    'vy':random.randint(6,10),'vx':random.randint(-1,1),
                    'type':'rain','life':60
                })
        elif self.weather_mode=='snow':
            for _ in range(2):
                self.particles.append({
                    'x':random.randint(0,W),'y':random.randint(-10,0),
                    'vy':random.uniform(0.8,1.5),'vx':random.uniform(-0.5,0.5),
                    'type':'snow','life':120
                })

    # ── 主绘制 ───────────────────────────────────────────────────────
    def draw(self):
        cv=self.cv; cv.delete('all')
        if getattr(self, 'mini_w', None):
            self._draw_mini()
            return
        night=self.hour>=22 or self.hour<7
        gnd=self.gnd

        # ── 室内背景(QQ宠物风) ──────────────────────────────────────────
        def hex2rgb(h): c=h.lstrip('#'); return tuple(int(c[i:i+2],16) for i in (0,2,4))
        def lerp(a,b,t): return int(a+(b-a)*t)
        def rgb2hex(r,g,b): return f'#{r:02x}{g:02x}{b:02x}'
        strip=2

        # 1. 墙壁(竖条纹壁纸)
        wall_a = '#fff5e0' if not night else '#1a1228'
        wall_b = '#f5e8cc' if not night else '#140e22'
        for x in range(0, W, 20):
            fc = wall_a if (x//20)%2==0 else wall_b
            cv.create_rectangle(x, 0, x+20, gnd, fill=fc, outline='')

        # 2. 踢脚线
        skirting = '#c8a060' if not night else '#3a2810'
        cv.create_rectangle(0, gnd-14, W, gnd, fill=skirting, outline='')
        cv.create_rectangle(0, gnd-14, W, gnd-12, fill='#d8b478', outline='')  # 高光

        # 3. 地板
        floor_c = '#c8864a' if not night else '#3a2010'
        floor_h = '#d89860' if not night else '#2a1808'
        floor_s = '#b07038' if not night else '#281408'
        cv.create_rectangle(0, gnd, W, H, fill=floor_c, outline='')
        # 木地板纹(横向条)
        for y in range(gnd+18, H, 18):
            cv.create_rectangle(0, y, W, y+2, fill=floor_s, outline='')
        # 地板高光(靠近墙处稍亮)
        cv.create_rectangle(0, gnd, W, gnd+6, fill=floor_h, outline='')

        # 4. 窗户(左侧,x=20-130)
        self._draw_window(cv, 20, 10, 110, 150, night)

        # 5. 右侧小床(x=330-470)
        self._draw_bed(cv, 330, 145, gnd, night)

        # 6. 中间书桌(x=170-270)
        self._draw_desk(cv, 170, 175, gnd, night)

        # 7. 右上角挂画
        self._draw_picture(cv, 360, 15, night)


        # 烟雾
        for sm in self.smokes:
            lv=sm['l']/40
            c2=T['smk1'] if lv>0.6 else T['smk2'] if lv>0.3 else T['smk3']
            sx2=round(sm['x']/BP)*BP; sy2=round(sm['y']/BP)*BP
            cv.create_rectangle(sx2-sm['r'],sy2-sm['r'],sx2+sm['r'],sy2+sm['r'],fill=c2,outline='')

        # 蝴蝶
        if not night and self.weather_mode=='clear':
            for bf in self.bflies:
                bx=round(bf['x']/BP)*BP; by2=round(bf['y']/BP)*BP; c2=T[bf['c']]
                flap=int(math.sin(self.frame*0.18+bf['ph'])*BP*1.5)
                # 上翅
                cv.create_rectangle(bx-BP*3,by2-BP+flap,bx,by2+flap,fill=c2,outline='')
                cv.create_rectangle(bx+BP,by2-BP-flap,bx+BP*4,by2-flap,fill=c2,outline='')
                # 下翅(小一半)
                cv.create_rectangle(bx-BP*2,by2+flap,bx,by2+BP+flap,fill=c2,outline='')
                cv.create_rectangle(bx+BP,by2-flap,bx+BP*3,by2+BP-flap,fill=c2,outline='')
                # 身体
                cv.create_rectangle(bx,by2-BP,bx+BP,by2+BP*2,fill='#1a1a2a',outline='')

        # 天气粒子
        for p in self.particles:
            px=round(p['x']/BP)*BP; py=round(p['y']/BP)*BP
            if p['type']=='rain':
                cv.create_rectangle(px,py,px+BP,py+BP*3,fill=T['rain'],outline='')
                # 溅起水花
                if py>=gnd-BP*4:
                    for sx3 in [-BP,0,BP]:
                        cv.create_rectangle(px+sx3,gnd-BP,px+sx3+BP,gnd,fill=T['splash'],outline='')
            else:
                cv.create_rectangle(px,py,px+BP,py+BP,fill=T['snow'],outline='')

        # 钓鱼线
        if self.act=='fish' and self.act_phase=='do':
            b3=round(math.sin(self.frame*0.15)*2/BP)*BP
            fx1=round((self.cx+6)/BP)*BP; fy1=gnd-len(STAND)*CP
            fx2=216; fy2=gnd-8+b3
            for i in range(8):
                t3=i/8
                lx=round((fx1+(fx2-fx1)*t3)/BP)*BP; ly=round((fy1+(fy2-fy1)*t3)/BP)*BP
                cv.create_rectangle(lx,ly,lx+BP,ly+BP,fill='#888888',outline='')
            cv.create_rectangle(fx2-BP,fy2-BP,fx2+BP*2,fy2+BP*2,fill='#ff4444',outline='')

        # 钓鱼战利品
        if self.fish_catch and self.catch_timer>0:
            cv.create_text(self.cx,gnd-len(STAND)*CP-20,text=self.fish_catch,
                            font=('Apple Color Emoji',18))

        # 角色阴影
        sx3=round((self.cx-10)/BP)*BP
        cv.create_rectangle(sx3,gnd,sx3+BP*5,gnd+BP,fill='#1a3a1a',outline='')

        # 角色
        if self.fainted:
            # 昏厥状态：横躬 + 闪烁红色警示
            pulse = abs(math.sin(self.frame * 0.05))  # 0~1闪烁
            # 身体横着画出来
            fy = gnd - CP*2
            # 头
            cv.create_rectangle(self.cx-BP*8,fy-CP,self.cx-BP*6,fy+CP,fill='#f0b060',outline='')
            # 身体
            cv.create_rectangle(self.cx-BP*6,fy-CP,self.cx,fy+CP,fill='#4466aa',outline='')
            # 腿
            cv.create_rectangle(self.cx,fy-CP,self.cx+BP*4,fy+CP,fill='#224488',outline='')
            # 闪烁的 X_X 眼睛
            ex = self.cx-BP*7
            cv.create_text(ex,fy,text='💀',font=('Apple Color Emoji',10))
            # 天上飘着的 … 或 ✨
            stars=['✨','💫','⭐']
            for i,s in enumerate(stars):
                sx_s=self.cx-16+i*14
                sy_s=gnd-CP*5+int(math.sin(self.frame*0.08+i)*6)
                cv.create_text(sx_s,sy_s,text=s,font=('Apple Color Emoji',8))
            # 红色警告闪烁
            if pulse>0.5:
                cv.create_text(self.cx,gnd-CP*8,text='💤 昏厥中...',
                               font=('PingFang SC',10,'bold'),fill='#ff4444')
        else:
            bob=round(math.sin(self.frame*0.08))*CP
            spr=self.sprite
            if self.angry_level>2: spr='angry'
            draw_sprite(self.cv,self.cx,gnd+bob,spr,self.flip)

        # 生气火花
        if self.angry_level>2:
            for i in range(3):
                ang=self.frame*0.3+i*2.1
                sx4=self.cx+int(math.cos(ang)*18)
                sy4=gnd-len(STAND)*CP+int(math.sin(ang)*10)
                cv.create_rectangle(sx4,sy4,sx4+BP,sy4+BP,fill=T['angry'],outline='')
                cv.create_rectangle(sx4+BP,sy4-BP,sx4+BP*2,sy4,fill=T['angry2'],outline='')

        # 睡觉Zzz
        if self.sprite=='sleep':
            for i,z in enumerate(['z','Z','Z']):
                zx=self.cx+18+i*9; zy=gnd-30+i*(-7)
                cv.create_text(zx,zy,text=z,font=('PingFang SC',7+i*2,'bold'),fill=T['water4'])

        # 收菜提示
        if self.veg_harvest and self.frame%20<10:
            cv.create_text(316,gnd-44,text='🥕 收菜!',font=('PingFang SC',10,'bold'),fill=T['sun'])

        # 成就弹出
        if self.ach_show and self.ach_timer>0:
            aw=220; ax=(W-aw)//2; ay=8
            cv.create_rectangle(ax,ay,ax+aw,ay+22,fill='#2a1050',outline=T['medal_g'],width=2)
            cv.create_text(ax+aw//2,ay+11,text=self.ach_show,font=('PingFang SC',9,'bold'),fill=T['medal_g'])

        # 积分显示
        cv.create_text(6,H-36,text=f'⭐{self.score}  Lv.{self.level}',anchor='sw',font=('PingFang SC',8),fill='#aaaacc')

        # 天气图标
        cv.create_text(W-30,12,text=self.w_icon,font=('Apple Color Emoji',12))
        if self.w_temp:
            cv.create_text(W-30,26,text=self.w_temp,font=('PingFang SC',8),fill='#336699')

        # 气泡
        if self.bubble and self.btimer>0:
            self._px_bubble(self.cx,gnd)

        # 生病图标
        if self.sick and self.frame%16<8:
            cv.create_text(self.cx+14,gnd-len(STAND)*CP-8,text='🤒',font=('Apple Color Emoji',10))

        # 属性面板
        self._draw_stats()

        # 标题
        cv.create_text(W//2,10,text='🏡 南波万の小家园',font=('PingFang SC',10,'bold'),
                        fill='#ddeeff' if night else '#223388')
        cv.create_text(W-6,H-36,text=time.strftime('%H:%M'),anchor='se',
                        font=('PingFang SC',8),fill='#888888')
        # 右上角关闭按钮
        cx_=W-14; cy_=10; cr=9
        hover=(hasattr(self,'_close_hover') and self._close_hover)
        bg_='#cc2244' if hover else '#442244'
        cv.create_oval(cx_-cr,cy_-cr,cx_+cr,cy_+cr,fill=bg_,outline='#ff4466' if hover else '#884466',width=1,tags='close_btn')
        cv.create_text(cx_,cy_,text='✕',font=('PingFang SC',9,'bold'),fill='#ffccdd',tags='close_btn')

    # ── 场景绘制子函数 ───────────────────────────────────────────────
    def _draw_mini(self):
        cv = self.cv; cv.delete('all')
        W_M = getattr(self, 'mini_w', 80)
        H_M = getattr(self, 'mini_h', 120)
        cx = W_M // 2
        gnd = H_M - 8

        # 加载迷你角色图(只加载一次,引用全部挂在self._mini_img_refs上防GC)
        if not hasattr(self, '_mini_img_refs'):
            import os as _os2
            from PIL import Image as _PI, ImageTk as _IT, ImageSequence as _IS
            _adir = _os2.path.join(_os2.path.dirname(_os2.path.abspath(__file__)), 'assets')
            try:
                _char = CHARACTERS.get(self.char_id, CHARACTERS[DEFAULT_CHAR])
                gif_r = _PI.open(_os2.path.join(_adir, _char['right']))
                _frames_r = [_IT.PhotoImage(fr.convert('RGBA').resize((128,128),_PI.NEAREST))
                              for fr in _IS.Iterator(gif_r)]
                gif_l = _PI.open(_os2.path.join(_adir, _char['left']))
                _frames_l = [_IT.PhotoImage(fr.convert('RGBA').resize((128,128),_PI.NEAREST))
                              for fr in _IS.Iterator(gif_l)]
                self._mini_frames_r = _frames_r
                self._mini_frames_l = _frames_l
                self._mini_img_refs = _frames_r + _frames_l  # 防GC
            except Exception as _e:
                print('mini char load error:', _e)
                self._mini_img_refs = []
                self._mini_frames_r = None
                self._mini_frames_l = None

        if self._mini_frames_r:
            fi = (self.frame // 5) % len(self._mini_frames_r)
            _img = (self._mini_frames_r if self.flip else self._mini_frames_l)[fi]
            if self.fainted:
                # 昏厥：肃景变红 + 角色变灰
                cv.create_oval(cx-52, gnd-106, cx+52, gnd-2, fill='#3a0000', outline='#ff4444', width=2)
            else:
                cv.create_oval(cx-52, gnd-106, cx+52, gnd-2, fill='#fffaf0', outline='#e0c8a0', width=1)
            cv.create_image(cx, gnd-2, anchor='s', image=_img)
            # 昏厥覆盖层：半透明红色蒙层 + 图标
            if self.fainted:
                pulse = abs(math.sin(self.frame * 0.08))
                cv.create_oval(cx-52, gnd-106, cx+52, gnd-2,
                               fill='', outline='#ff2222', width=3 if pulse>0.5 else 1)
                cv.create_text(cx, gnd-60, text='💤', font=('Apple Color Emoji', 22))
                if pulse > 0.5:
                    cv.create_text(cx, gnd-108, text='定睛!', font=('PingFang SC', 10, 'bold'), fill='#ff4444')
            # 双重防GC
            if not hasattr(cv, '_cur_imgs'): cv._cur_imgs = {}
            cv._cur_imgs['mini'] = _img
        else:
            spr = 'angry' if self.angry_level > 2 else self.sprite
            draw_sprite(cv, cx, gnd, spr, self.flip)

        if self.exp_show and self.exp_timer > 0:
            W_M = getattr(self, 'mini_w', 140)
            cv.create_text(W_M//2, 18, text=self.exp_show,
                           font=('PingFang SC', 11, 'bold'), fill='#ffdd44')
        if self.sick and self.frame % 16 < 8:
            cv.create_text(cx+16, gnd-52, text='🤒', font=('Apple Color Emoji', 9))
        if self.bubble and self.btimer > 0:
            self._px_bubble_mini(cx, gnd)
        if self.sprite == 'sleep':
            for i, z in enumerate(['z','Z','Z']):
                cv.create_text(cx+18+i*9, gnd-54+i*(-7), text=z,
                               font=('PingFang SC', 7+i*2, 'bold'), fill='#60d0ff')

    def _px_bubble_mini(self, cx, gnd):
        """Mini气泡:复用已有浮层,不抢焦点不打断输入法"""
        text = self.bubble
        lines = text.split('\n')
        max_len = max(len(l) for l in lines)
        bw = max(max_len * 13 + 24, 100)
        bh = 16 + len(lines) * 24

        try:
            rx = self.root.winfo_rootx()
            ry = self.root.winfo_rooty()
            rw = self.root.winfo_width()
        except: return

        bx_screen = rx + rw//2 - bw//2
        by_screen = ry - bh - 10

        # 一次性创建气泡窗口(之后只更新内容和位置,不 deiconify/withdraw)
        if not hasattr(self, '_bubble_win') or not self.root.winfo_exists():
            self._bubble_win = None
        bwin = getattr(self, '_bubble_win', None)
        if bwin is None or not bwin.winfo_exists():
            bwin = tk.Toplevel(self.root)
            bwin.overrideredirect(True)
            bwin.attributes('-topmost', True)
            bwin.attributes('-alpha', 0.0)   # 先透明
            bwin.configure(bg='#fffef0')
            # 确保不会获取焦点
            bwin.wm_attributes('-topmost', True)
            self._bubble_win = bwin
            self._bubble_cv = tk.Canvas(bwin, bg='#fffef0', highlightthickness=2,
                                        highlightbackground='#7744cc', takefocus=False)
            self._bubble_cv.pack()
            # 预先放到屏幕外,让它一直"存在"但不可见
            bwin.geometry(f'1x1+0+0')
            bwin.deiconify()  # 只在创建时 deiconify 一次

        # 更新内容
        bwin.geometry(f'{bw}x{bh}+{bx_screen}+{by_screen}')
        bcv = self._bubble_cv
        bcv.config(width=bw, height=bh)
        bcv.delete('all')
        for i, line in enumerate(lines):
            bcv.create_text(bw//2, 10 + i*24, text=line, font=('PingFang SC', 13),
                            fill='#1e0a3c', justify='center')
        # 显示气泡(纯alpha控制,不抢焦点)
        bwin.attributes('-alpha', 0.95)
        bwin.lift()  # 确保永远浮在最上面

    def _draw_window(self, cv, x, y, w, h, night):
        """室内窗户"""
        # 窗外天色
        sky = '#1a2a4a' if night else '#c8e8ff'
        sun_hint = '#ffe8a0' if not night else '#2a3a6a'
        cv.create_rectangle(x+6, y+6, x+w-6, y+h-6, fill=sky, outline='')
        # 窗外简单景色(非夜晚)
        if not night:
            cv.create_rectangle(x+6, y+h//2, x+w-6, y+h-6, fill='#88cc66', outline='')  # 绿树
            cv.create_oval(x+12, y+h//2-14, x+44, y+h//2+10, fill='#66bb44', outline='')
            cv.create_oval(x+30, y+h//2-18, x+62, y+h//2+8, fill='#55aa33', outline='')
            # 小太阳
            cv.create_oval(x+w-28, y+10, x+w-10, y+28, fill='#ffe566', outline='#ffcc00', width=1)
        else:
            # 月亮+星星
            cv.create_oval(x+w-26, y+10, x+w-12, y+24, fill='#fff0a0', outline='')
            for sx, sy in [(x+15,y+15),(x+25,y+35),(x+55,y+20),(x+70,y+40)]:
                cv.create_rectangle(sx, sy, sx+3, sy+3, fill='#ffffcc', outline='')
        # 窗框(外框)
        fc = '#c8a060'
        cv.create_rectangle(x, y, x+w, y+h, fill='', outline=fc, width=5)
        # 十字窗格
        mx = x + w//2
        my = y + h//2
        cv.create_rectangle(mx-2, y+5, mx+2, y+h-5, fill=fc, outline='')
        cv.create_rectangle(x+5, my-2, x+w-5, my+2, fill=fc, outline='')
        # 窗帘(左右两侧,波浪底)
        curtain = '#ffcc88' if not night else '#cc9944'
        shadow  = '#e8a840' if not night else '#a87830'
        cw = 22  # 窗帘宽度
        for side in (0, 1):
            cx2 = x if side==0 else x+w-cw
            cv.create_rectangle(cx2, y, cx2+cw, y+h, fill=curtain, outline='')
            # 褶皱阴影
            for fold in range(y+8, y+h-8, 16):
                cv.create_rectangle(cx2+4, fold, cx2+cw-4, fold+3, fill=shadow, outline='')
            # 波浪底边(简单锯齿)
            for wy in range(y+h-14, y+h, 7):
                cv.create_oval(cx2, wy, cx2+cw, wy+10, fill=curtain, outline='')
        # 窗台
        cv.create_rectangle(x-4, y+h, x+w+4, y+h+8, fill='#d4b880', outline='')

    def _draw_bed(self, cv, x, y, gnd, night):
        """右侧小床"""
        frame_c = '#c8a060'; mat_c = '#fff0f5'; pil_c = '#ffe0e8'
        shadow_c = '#a08040'; headboard_c = '#d4b070'
        # 床身主体
        cv.create_rectangle(x, y+20, x+140, gnd, fill=frame_c, outline='')
        # 床面(床垫)
        cv.create_rectangle(x+6, y+20, x+134, gnd-8, fill=mat_c, outline='')
        # 枕头
        cv.create_oval(x+10, y+22, x+52, y+44, fill=pil_c, outline='#ffc8d8', width=1)
        cv.create_oval(x+58, y+22, x+100, y+44, fill=pil_c, outline='#ffc8d8', width=1)
        # 被子花纹(几个小菱形)
        for bx in range(x+15, x+130, 22):
            cv.create_polygon(bx,y+60, bx+8,y+52, bx+16,y+60, bx+8,y+68, fill='#ffd0e0', outline='#ffb8cc', width=1)
        # 床头板(圆弧顶)
        cv.create_rectangle(x, y+10, x+140, y+22, fill=headboard_c, outline='')
        cv.create_arc(x, y-10, x+140, y+30, start=0, extent=180, fill=headboard_c, outline='')
        # 高光
        cv.create_rectangle(x+4, y+12, x+20, y+20, fill='#e8c878', outline='')
        # 床腿
        for lx in (x+10, x+120):
            cv.create_rectangle(lx, gnd-6, lx+10, gnd, fill=shadow_c, outline='')

    def _draw_desk(self, cv, x, y, gnd, night):
        """书桌+书本"""
        desk_c = '#d4a96a'; leg_c = '#b08040'; top_c = '#e0b878'
        # 桌腿
        for lx in (x+6, x+84):
            cv.create_rectangle(lx, y+16, lx+8, gnd, fill=leg_c, outline='')
        # 桌面
        cv.create_rectangle(x, y, x+100, y+16, fill=desk_c, outline='')
        cv.create_rectangle(x, y, x+100, y+4, fill=top_c, outline='')  # 高光
        # 桌上的书(叠放)
        books = [('#e06060',30),('#6090d0',50),('#60b060',68)]
        for bc, bx2 in books:
            cv.create_rectangle(x+bx2, y-22, x+bx2+16, y, fill=bc, outline='')
            cv.create_rectangle(x+bx2, y-22, x+bx2+2, y, fill='#eeeeee', outline='')
        # 桌上小台灯
        lamp_x = x+78
        cv.create_rectangle(lamp_x, y-30, lamp_x+4, y, fill='#888888', outline='')  # 灯杆
        cv.create_polygon(lamp_x-12, y-30, lamp_x+16, y-30, lamp_x+8, y-44, lamp_x-4, y-44,
                          fill='#ffdd66', outline='#ccaa44', width=1)
        if not night:
            cv.create_oval(lamp_x-8, y-32, lamp_x+12, y-26, fill='#fffacc', outline='')  # 灯光晕

    def _draw_picture(self, cv, x, y, night):
        """墙上挂画"""
        # 画框
        cv.create_rectangle(x, y, x+80, y+60, fill='#c8a060', outline='')
        cv.create_rectangle(x+4, y+4, x+76, y+56, fill='#e8d4a0', outline='')
        # 简单风景画(圆+矩形)
        cv.create_rectangle(x+4, y+4, x+76, y+36, fill='#a8d4f0', outline='')  # 天空
        cv.create_rectangle(x+4, y+36, x+76, y+56, fill='#88cc66', outline='')  # 草地
        cv.create_oval(x+16, y+20, x+44, y+40, fill='#66bb44', outline='')
        cv.create_oval(x+36, y+16, x+60, y+38, fill='#55aa33', outline='')
        # 小太阳
        cv.create_oval(x+58, y+8, x+72, y+22, fill='#ffe566', outline='')

    def _px_bubble(self,cx,gy):
        cv=self.cv; text=self.bubble; bp=BP
        bw=min(max(len(text)*9+20,60),240); bh=24
        bx=max(4,min(cx-bw//2,W-bw-4))
        sprite_h=len(STAND)*CP; by=gy-sprite_h-bh-12
        for x in range(bx,bx+bw+bp,bp):
            cv.create_rectangle(x,by,x+bp,by+bp,fill=T['bbl2'],outline='')
            cv.create_rectangle(x,by+bh,x+bp,by+bh+bp,fill=T['bbl2'],outline='')
        for y in range(by+bp,by+bh,bp):
            cv.create_rectangle(bx,y,bx+bp,y+bp,fill=T['bbl2'],outline='')
            cv.create_rectangle(bx+bw,y,bx+bw+bp,y+bp,fill=T['bbl2'],outline='')
        cv.create_rectangle(bx+bp,by+bp,bx+bw,by+bh,fill=T['bbl'],outline='')
        tx=max(bx+bp*3,min(cx,bx+bw-bp*3))
        cv.create_rectangle(tx,by+bh,tx+bp,by+bh+bp,fill=T['bbl2'],outline='')
        cv.create_rectangle(tx+bp,by+bh+bp,tx+bp*2,by+bh+bp*2,fill=T['bbl2'],outline='')
        cv.create_rectangle(tx,by+bh,tx+bp*2,by+bh+bp,fill=T['bbl'],outline='')
        cv.create_text((bx*2+bw)//2,by+bh//2,text=text,font=('PingFang SC',9),fill='#1e0a3c')

    # ── Tick ─────────────────────────────────────────────────────────
    def tick(self):
        self.frame+=1
        # 如果包含昏厥状态，第一帧自动弹出提示
        if self.fainted and self.frame==30:
            self.root.after(0, self._show_faint_popup)
        for cl in self.clouds:
            cl['x']+=cl['s']
            if cl['x']>W//BP*BP+cl['w']*BP+10: cl['x']=-cl['w']*BP-10
        for bf in self.bflies:
            bf['x']+=bf['vx']+math.sin(self.frame*0.03+bf['ph'])*0.3
            bf['y']+=bf['vy']+math.cos(self.frame*0.04+bf['ph'])*0.25
            if bf['x']<20 or bf['x']>W-20: bf['vx']*=-1
            if bf['y']<40 or bf['y']>self.gnd-20: bf['vy']*=-1
        if self.smoke_on>0:
            self.smoke_on-=1
            if self.frame%4==0:
                self.smokes.append({'x':108,'y':H-148,'r':BP*2,'l':40})
        for sm in self.smokes: sm['y']-=BP*0.2; sm['l']-=1
        self.smokes=[s for s in self.smokes if s['l']>0]

        # 天气粒子
        if self.weather_mode!='clear' and self.frame%3==0:
            self._spawn_particles()
        for p in self.particles:
            p['x']+=p['vx']; p['y']+=p['vy']; p['life']-=1
        self.particles=[p for p in self.particles if p['life']>0 and p['y']<self.gnd+10]

        if self.act_timer>0: self.update_act()
        elif time.time()-self._last_sched_ts>30: self.schedule()  # 保底:超30秒没动静就重启
        if self.btimer>0:
            self.btimer-=1
            if self.btimer==0:
                self.bubble=''
                # 气泡浮层隐藏
                bwin=getattr(self,'_bubble_win',None)
                if bwin and bwin.winfo_exists():
                    bwin.attributes('-alpha', 0.0)  # 透明隐藏,不用withdraw
        if self.exp_timer>0:
            self.exp_timer-=1
            if self.exp_timer==0: self.exp_show=''
        if self.catch_timer>0:
            self.catch_timer-=1
        if self.ach_timer>0:
            self.ach_timer-=1
            if self.ach_timer==0: self.ach_show=''
        if self.angry_timer>0: self.angry_timer-=1
        if self.frame%800==0:
            i=random.randint(0,3); self.veg[i]=(self.veg[i]+1)%3
        if self.frame%60==0: self.check_idle()
        if self.frame%120==0: self.check_reminders()

        # 旅行中:每5秒刷新气泡;旅行结束自动完成
        if self.travel_state.get('active'):
            import time as _tt3
            rem = int(self.travel_state.get('end_ts',0)-_tt3.time())
            if rem <= 0:
                # 旅行完成
                dest = self.travel_state.get('dest','?')
                self.travel_state = {'active':False,'dest':'','end_ts':0}
                if dest not in self.travel_visited: self.travel_visited.append(dest)
                n = len(self.travel_visited)
                self.add_exp(15); self.add_score(10); self._save()
                if n>=5:  self.unlock('travel5')
                if n>=15: self.unlock('travel15')
                if n>=34: self.unlock('travel35')
                # 随机抽取特产（0-4号）
                import random as _rv
                souv_list = PROV_SOUVENIRS.get(dest, DEFAULT_SOUVENIR_LIST)
                souv_idx = _rv.randint(0, len(souv_list)-1)
                souv_name, souv_desc = souv_list[souv_idx]
                souv_key = f'souvenir_{dest}_{souv_idx}'
                self.bag[souv_key] = self.bag.get(souv_key, 0) + 1
                # 随机抽取明信片（0-4号）
                card_list = PROV_POSTCARDS.get(dest, DEFAULT_POSTCARD_LIST)
                card_idx = _rv.randint(0, len(card_list)-1)
                card_name, card_desc = card_list[card_idx]
                card_key = f'postcard_{dest}_{card_idx}'
                self.bag[card_key] = self.bag.get(card_key, 0) + 1
                self._save()
                postcard_total = sum(1 for k,v in self.bag.items() if k.startswith('postcard_') and v>0)
                if postcard_total >= 10: self.unlock('postcard10')
                self.say(f'🎉 到{dest}啦！\n带回了{souv_name}和一张明信片～', 120)
                self.bubble = f'🎉 到{dest}啦！带回了{souv_name}～'
                self.btimer = 120
                # 先弹特产窗口，1.5秒后弹明信片窗口
                self.root.after(1500, lambda d=dest, sn=souv_name, sd=souv_desc: self._show_souvenir(d, sn, sd))
                self.root.after(3200, lambda d=dest, cn=card_name, cd=card_desc: self._show_postcard(d, cn, cd))
            elif self.frame%62==0:  # ~5秒刷新
                dest = self.travel_state.get('dest','?')
                min_l = rem//60; sec_l = rem%60
                self.say(f'✈️ 去{dest}旅行中\n还剩{min_l}分{sec_l:02d}秒', 65)

        # 属性自然衰减(每600帧≈约48秒,玩一小时掉约50%)
        if self.frame%1200==0:
            self.hunger=max(0,self.hunger-0.4)
            self.mood=max(0,self.mood-0.2)
            self.cleanliness=max(0,self.cleanliness-0.15)
            # 健康值联动
            if self.hunger<20 or self.cleanliness<20:
                self.health=max(0,self.health-0.4)
                if not self.sick and self.health<50:
                    self.sick=True
                    self.say('感觉身体不太好...🤒',150)
            elif self.hunger>60 and self.mood>60 and self.cleanliness>60:
                self.health=min(100,self.health+0.3)
                if self.sick and self.health>75:
                    self.sick=False
                    self.say('感觉好多了!😊',100)
            # 昏厥触发：健康度为0且持续一段时间
            if not self.fainted:
                if self.health<=0:
                    self.faint_cd+=1
                    if self.faint_cd>=8:  # 连续8次衰减周期（约10分钟）触发
                        self.fainted=True; self.faint_cd=0
                        self.sick=True; self._save()
                        self.root.after(0, self._show_faint_popup)
                else:
                    self.faint_cd=0
            # 低属性警告 — 分层撒娇语料
            low=[]
            if self.hunger<10:
                low+=random.choices(['😭 我要饿死了！主人快快快快喂我！','肚子太饿了...就快平躺我了...','如果再不吃东西，我会变成小骷髅头的💀','饱食→→→我！！！'],k=1)
            elif self.hunger<25:
                low+=random.choices(['🍔 好饿...主人快喂我！','胃胃抢了，幸好主人在...','主人！！有没有吃的！🥺','如果我是一只拼猫现在已经在视频里平躺了...'],k=1)
            elif self.hunger<40:
                low+=random.choices(['有点饿呢...可以吃点什么吗？','我在考虑点外卖...🤔'],k=1)
            if self.mood<10:
                low+=random.choices(['😭 孤独极了！主人你在哪里！','我要哭了！谁都不理我！😭','主人你已经三天不陈迹我了！','心情归零了...要不要陪我玩一下🥺'],k=1)
            elif self.mood<25:
                low+=random.choices(['😢 好闷啊...陪我玩嗑！','我有点不开心，主人按按我吧','如果我是一只5岁小孩我现在已经在地上打滚了'],k=1)
            if self.cleanliness<10:
                low+=random.choices(['🚶 我臭死了！主人快帮我洗澡！','连我自己都闻不下去了...洗澡洗澡🛁','我现在的状态就是"独特"的味道...'],k=1)
            elif self.cleanliness<25:
                low+=random.choices(['想洗澡了...好脏🛁','主人给我准备浴球就没小吃的哦'],k=1)
            if self.health<15:
                low+=random.choices(['🤕 我快不行了！主人我需要药！！','头好晕好晕的...药药药...','如果我明天没了，记得常来看看我'],k=1)
            elif self.sick and self.health<30:
                low+=random.choices(['🤒 头好沌...据说药很贵但是很有效','小声音：主人...我生病了啊🥺'],k=1)
            if low and self.stat_warn_cd==0:
                self.say(random.choice(low),150)
                self.stat_warn_cd=6
            elif self.stat_warn_cd>0:
                self.stat_warn_cd-=1
            # 每5分钟自动保存
            if self.frame%6000==0: self._save()

        # 整点检查
        h=time.localtime().tm_hour
        if h!=self.last_hour: self.check_hour()

        self.draw()
        self.root.after(80,self.tick)

    # ── 交互 ─────────────────────────────────────────────────────────
    def open_garden(self):
        if self.garden_win and self.garden_win.winfo_exists():
            self.garden_win.lift(); return
        W_G, H_G, GND = 850, 560, 440
        win = tk.Toplevel(self.root)
        win.title('南波万の小家园')
        win.geometry(f'{W_G}x{H_G}+80+60')
        win.resizable(False, False)
        win.lift()
        win.focus_force()
        win.configure(bg='systemTransparent')
        self.garden_win = win
        cv_g = tk.Canvas(win, width=W_G, height=H_G, bg='#100825', highlightthickness=0)
        cv_g.pack()
        g = {'cx': 550, 'cy': 360, 'flip': False, 'sprite': 'stand', 'moving': None, 'frame': 0, 'scene': 'indoor'}

        # 加载图片素材(只加载一次)
        from PIL import Image as PILImage, ImageTk, ImageSequence

        def load_frames(gif_path, scale=2):
            gif = PILImage.open(gif_path)
            frames = []
            for f in ImageSequence.Iterator(gif):
                img = f.convert('RGBA').resize((32*scale, 32*scale), PILImage.NEAREST)
                frames.append(ImageTk.PhotoImage(img))
            return frames

        ASSET_DIR2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
        bg_img_pil = PILImage.open(os.path.join(ASSET_DIR2, 'room_bg.png')).convert('RGB')

        def make_night(img):
            try:
                import numpy as np
                arr = np.array(img, dtype=float) * 0.35
                return PILImage.fromarray(arr.astype('uint8'))
            except ImportError:
                return img

        ext_img_pil = PILImage.open(os.path.join(ASSET_DIR2, 'exterior_bg.png')).convert('RGB')
        forest_img_pil = PILImage.open(os.path.join(ASSET_DIR2, 'forest_bg.png')).convert('RGB')
        upstairs_img_pil = PILImage.open(os.path.join(ASSET_DIR2, 'upstairs_bg.png')).convert('RGB')

        bg_day      = ImageTk.PhotoImage(bg_img_pil)
        bg_night    = ImageTk.PhotoImage(make_night(bg_img_pil))
        ext_day     = ImageTk.PhotoImage(ext_img_pil)
        ext_night   = ImageTk.PhotoImage(make_night(ext_img_pil))
        forest_day  = ImageTk.PhotoImage(forest_img_pil)
        forest_night= ImageTk.PhotoImage(make_night(forest_img_pil))
        up_day      = ImageTk.PhotoImage(upstairs_img_pil)
        up_night    = ImageTk.PhotoImage(make_night(upstairs_img_pil))

        _char = CHARACTERS.get(self.char_id, CHARACTERS[DEFAULT_CHAR])
        frames_right = load_frames(os.path.join(ASSET_DIR2, _char['right']))
        frames_left  = load_frames(os.path.join(ASSET_DIR2, _char['left']))
        _stand_key = self.char_id
        _stand_png = os.path.join(ASSET_DIR2, f'{_stand_key}_stand.png')
        if not os.path.exists(_stand_png):
            _stand_png = os.path.join(ASSET_DIR2, 'char_stand.png')
        try:
            _stand_pil = PILImage.open(_stand_png).convert('RGBA').resize((64, 64), PILImage.NEAREST)
            stand_img = ImageTk.PhotoImage(_stand_pil)
        except Exception:
            stand_img = frames_right[0]

        # 所有图片引用挂在 win 上防止GC
        win._img_refs = [bg_day, bg_night, ext_day, ext_night, forest_day, forest_night, up_day, up_night, stand_img] + frames_right + frames_left

        # 角色尺寸
        CHAR_W, CHAR_H = 64, 64

        # ── 碰撞地图构建 ──────────────────────────────────────

        # 碰撞矩形:只保留四周边框
        _INDOOR_WALLS = [
            (0,   0,   850, 28),    # 上
            (0,   490, 850, 526),   # 下
            (0,   0,   28,  526),   # 左
            (822, 0,   850, 526),   # 右
        ]
        _OUTDOOR_WALLS = [
            (0,   0,   30,  526),
            (820, 0,   850, 526),
            (0,   0,   850, 30),
            (0,   492, 850, 526),
        ]

        _FOREST_WALLS = [
            (0,   0,   850, 28),
            (0,   490, 850, 526),
            (0,   0,   28,  526),
            (822, 0,   850, 526),
        ]

        _UPSTAIRS_WALLS = [
            (0,   0,   850, 28),
            (0,   490, 850, 526),
            (0,   0,   28,  526),
            (822, 0,   850, 526),
        ]

        def _collides(cx, cy, scene):
            hw = 14; hh = 20
            wmap = {'indoor':_INDOOR_WALLS, 'outdoor':_OUTDOOR_WALLS, 'forest':_FOREST_WALLS, 'upstairs':_UPSTAIRS_WALLS}
            walls = wmap.get(scene, _OUTDOOR_WALLS)
            for x1,y1,x2,y2 in walls:
                if cx-hw < x2 and cx+hw > x1 and cy-hh < y2 and cy+hh > y1:
                    return True
            return False

        # 预先把背景画到静态 canvas item(只建一次)
        _bg_item = cv_g.create_image(0, 0, anchor='nw', image=bg_day)
        _time_overlay = cv_g.create_rectangle(0, 0, W_G, H_G-34, fill='#000000', outline='', state='hidden')
        _night_overlay = cv_g.create_rectangle(0, 0, W_G, H_G-34,
                                                fill='#0a0820', stipple='gray50', outline='', state='hidden')
        # 太阳图片
        _sun_size = 60
        _sun_pil = PILImage.open(os.path.join(ASSET_DIR2, 'sun.jpeg')).convert('RGBA').resize((_sun_size, _sun_size), PILImage.LANCZOS)
        import numpy as _np
        _sd = _np.array(_sun_pil)
        _r,_g,_b,_a = _sd[:,:,0],_sd[:,:,1],_sd[:,:,2],_sd[:,:,3]
        _is_bg = (_r>150)&(_g>150)&(_b>150)&(_np.abs(_r.astype(int)-_g.astype(int))<30)&(_np.abs(_g.astype(int)-_b.astype(int))<30)
        _sd[:,:,3] = _np.where(_is_bg, 0, _a)
        _sun_pil = PILImage.fromarray(_sd)
        _sun_photo = ImageTk.PhotoImage(_sun_pil)
        _sun_glow = cv_g.create_image(0, 0, anchor='center', image=_sun_photo, state='hidden')
        _last_time_slot = None
        _last_night = False
        _last_scene = 'indoor'

        def _get_time_slot():
            h = self.hour
            if 6 <= h < 11:  return 'morning'
            elif 11 <= h < 16: return 'noon'
            elif 16 <= h < 22: return 'evening'
            else:              return 'night'

        _TIME_PARAMS = {
            'morning': ('', '', 120, 60,  '#ffe8a0', 90),
            'noon':    ('', '', 430, 40,  '#fffacc', 120),
            'evening': ('', '', 700, 80,  '#ff9966', 80),
            'night':   ('', '', -99, -99, '',        0),
        }

        # 门口触发区(左上角,靠近门的位置)
        # 室内:左上角楼梯(蓝色框)→ 二楼
        STAIR_X1, STAIR_Y1 = 128, 110
        STAIR_X2, STAIR_Y2 = 230, 328
        # 室内:右下角地毯(蓝色框)→ 户外
        CARPET_X1, CARPET_Y1 = 618, 438
        CARPET_X2, CARPET_Y2 = 822, 490
        # 户外门口落点
        EXT_DOOR_X, EXT_DOOR_Y = 430, 260
        EXT_DOOR_R = 55
        DOOR_X, DOOR_Y = 200, 220   # 兼容旧代码

        def draw_g():
            nonlocal _last_night, _last_scene
            if not win.winfo_exists(): return
            try:
                _draw_g_inner()
            except Exception as _eg:
                import traceback
                with open('/tmp/pet_garden_err.log','a') as _ef:
                    traceback.print_exc(file=_ef)
            if win.winfo_exists(): win.after(80, draw_g)

        def _draw_g_inner():
            nonlocal _last_night, _last_scene
            f = g['frame']; night = self.hour >= 22 or self.hour < 7
            scene = g['scene']

            # ── 清除上一帧的动态元素(保留背景) ──
            cv_g.delete('dynamic')

            # ── 背景只在昼夜/场景切换时更新 ──
            if night != _last_night or scene != _last_scene:
                if scene == 'outdoor':
                    cv_g.itemconfig(_bg_item, image=(ext_night if night else ext_day))
                elif scene == 'forest':
                    cv_g.itemconfig(_bg_item, image=(forest_night if night else forest_day))
                elif scene == 'upstairs':
                    cv_g.itemconfig(_bg_item, image=(up_night if night else up_day))
                else:
                    cv_g.itemconfig(_bg_item, image=(bg_night if night else bg_day))
                cv_g.itemconfig(_night_overlay, state=('normal' if night else 'hidden'))
                _last_night = night
                _last_scene = scene

            # ── 场景标签 ──
            wx_icon = {'rain':' 🌧️','snow':' ❄️'}.get(self.weather_mode, '')
            time_slot = _get_time_slot()
            time_icon = {'morning':'🌅 早晨','noon':'☀️ 正午','evening':'🌇 傍晚','night':'🌙 夜晚'}[time_slot]
            scene_label = {'outdoor':'🌿 户外','forest':'🌳 森林','upstairs':'🪜 二楼'}.get(scene, '🏠 室内') + wx_icon
            cv_g.create_text(14, 14, text=scene_label, anchor='nw',
                             font=('PingFang SC', 10, 'bold'),
                             fill='#ffffff', tags='dynamic')
            cv_g.create_text(14, 32, text=time_icon, anchor='nw',
                             font=('PingFang SC', 9),
                             fill='#ccccee', tags='dynamic')

            # ── 已摆放家具 ──
            if self.placed_furniture:
                from PIL import Image as _PIf, ImageTk as _ITf
                import os as _osf
                FDIR = _osf.path.join(_osf.path.dirname(_osf.path.abspath(__file__)), 'assets', 'furniture')
                if not hasattr(self, '_furn_img_cache'): self._furn_img_cache = {}
                for pf in self.placed_furniture:
                    fid = pf.get('file','')
                    if not fid: continue
                    if fid not in self._furn_img_cache:
                        try:
                            raw = _PIf.open(_osf.path.join(FDIR, fid)).convert('RGBA')
                            ow,oh=raw.size; s=min(80/ow,80/oh); nw,nh=int(ow*s),int(oh*s)
                            img = _ITf.PhotoImage(raw.resize((nw,nh), _PIf.LANCZOS))
                            self._furn_img_cache[fid] = img
                        except: self._furn_img_cache[fid] = None
                    img = self._furn_img_cache.get(fid)
                    if img:
                        cv_g.create_image(pf['x'], pf['y'], anchor='center', image=img, tags='dynamic')
                        cv_g.create_text(pf['x'], pf['y']+28, text=pf.get('name',''), font=('PingFang SC',7), fill='#ccbbee', tags='dynamic')

            # 摆放模式提示
            pending = getattr(self, '_pending_place', None)
            if pending:
                cv_g.create_text(W_G//2, 50, text=f"🛋️ 点击任意位置摆放『{pending['name']}』",
                                 font=('PingFang SC', 12, 'bold'), fill='#ffee44', tags='dynamic')
                cv_g.create_text(W_G//2, 72, text='右键可取消摆放',
                                 font=('PingFang SC', 9), fill='#ccccff', tags='dynamic')

            # ── 门口提示 ──
            gcx, gcy = g['cx'], g['cy']
            if scene == 'indoor':
                in_stair  = STAIR_X1  <= gcx <= STAIR_X2  and STAIR_Y1  <= gcy <= STAIR_Y2
                in_carpet = CARPET_X1 <= gcx <= CARPET_X2 and CARPET_Y1 <= gcy <= CARPET_Y2
                if in_stair:
                    cv_g.create_rectangle(STAIR_X1, STAIR_Y1, STAIR_X2, STAIR_Y2,
                                          outline='#88eeff', width=2, dash=(6,3), tags='dynamic')
                    cv_g.create_text(W_G//2, 58, text='🪜 按 E 上二楼',
                                     font=('PingFang SC', 12, 'bold'), fill='#88eeff', tags='dynamic')
                elif in_carpet:
                    cv_g.create_rectangle(CARPET_X1, CARPET_Y1, CARPET_X2, CARPET_Y2,
                                          outline='#ffe88a', width=2, dash=(6,3), tags='dynamic')
                    cv_g.create_text(W_G//2, 58, text='🚪 按 E 出门',
                                     font=('PingFang SC', 12, 'bold'), fill='#ffe88a', tags='dynamic')
            elif scene == 'outdoor':
                dist_back = ((gcx-EXT_DOOR_X)**2 + (gcy-EXT_DOOR_Y)**2) ** 0.5
                if dist_back < EXT_DOOR_R:
                    cv_g.create_oval(EXT_DOOR_X-EXT_DOOR_R, EXT_DOOR_Y-30,
                                     EXT_DOOR_X+EXT_DOOR_R, EXT_DOOR_Y+30,
                                     outline='#ffe88a', width=2, dash=(6,3), tags='dynamic')
                    cv_g.create_text(W_G//2, 58, text='🚪 按 E 回室内',
                                     font=('PingFang SC', 12, 'bold'), fill='#ffe88a', tags='dynamic')
                # 森林入口(户外左侧边缘)
                if gcx < 80:
                    cv_g.create_rectangle(28, gcy-40, 50, gcy+40,
                                          outline='#66dd66', width=2, dash=(6,3), tags='dynamic')
                    cv_g.create_text(W_G//2, 58, text='🌳 按 E 进入森林',
                                     font=('PingFang SC', 12, 'bold'), fill='#66dd66', tags='dynamic')
            elif scene == 'forest':
                # 返回户外(右侧边缘)
                if gcx > W_G - 80:
                    cv_g.create_rectangle(W_G-50, gcy-40, W_G-28, gcy+40,
                                          outline='#ffe88a', width=2, dash=(6,3), tags='dynamic')
                    cv_g.create_text(W_G//2, 58, text='🚪 按 E 回到户外',
                                     font=('PingFang SC', 12, 'bold'), fill='#ffe88a', tags='dynamic')
            elif scene == 'upstairs':
                # 二楼楼梯在右侧(镜像后)
                UP_STAIR_X1, UP_STAIR_Y1 = W_G - 230, 110
                UP_STAIR_X2, UP_STAIR_Y2 = W_G - 128, 328
                in_up_stair = UP_STAIR_X1 <= gcx <= UP_STAIR_X2 and UP_STAIR_Y1 <= gcy <= UP_STAIR_Y2
                if in_up_stair:
                    cv_g.create_rectangle(UP_STAIR_X1, UP_STAIR_Y1, UP_STAIR_X2, UP_STAIR_Y2,
                                          outline='#88eeff', width=2, dash=(6,3), tags='dynamic')
                    cv_g.create_text(W_G//2, 58, text='🪜 按 E 下楼',
                                     font=('PingFang SC', 12, 'bold'), fill='#88eeff', tags='dynamic')

            # ── 天气粒子(户外/森林场景可见)──
            if scene in ('outdoor', 'forest') and self.weather_mode != 'clear':
                # 生成粒子
                if f % 2 == 0:
                    import random as _rnd
                    for _ in range(3):
                        px = _rnd.randint(30, W_G-30)
                        if self.weather_mode == 'rain':
                            g.setdefault('wx_particles', []).append({
                                'x': px, 'y': 0,
                                'vx': _rnd.uniform(-0.5, 0.5), 'vy': _rnd.uniform(6, 10),
                                'type': 'rain', 'life': 80
                            })
                        elif self.weather_mode == 'snow':
                            g.setdefault('wx_particles', []).append({
                                'x': px, 'y': 0,
                                'vx': _rnd.uniform(-1, 1), 'vy': _rnd.uniform(1, 3),
                                'type': 'snow', 'life': 160
                            })
                # 更新+绘制
                alive = []
                for p in g.get('wx_particles', []):
                    p['x'] += p['vx']; p['y'] += p['vy']; p['life'] -= 1
                    if p['life'] > 0 and p['y'] < H_G - 40:
                        alive.append(p)
                        px2, py2 = int(p['x']), int(p['y'])
                        if p['type'] == 'rain':
                            cv_g.create_line(px2, py2, px2, py2+8, fill='#88bbdd', width=1, tags='dynamic')
                        else:
                            cv_g.create_oval(px2-2, py2-2, px2+2, py2+2, fill='#eef4ff', outline='', tags='dynamic')
                g['wx_particles'] = alive
            elif scene in ('indoor', 'upstairs'):
                # 室内清粒子,但窗外能看到天气效果(简化版)
                g['wx_particles'] = []
                if self.weather_mode == 'rain':
                    # 窗户上画雨滴效果
                    import random as _rnd
                    for _ in range(5):
                        rx = _rnd.randint(50, W_G-50)
                        ry = _rnd.randint(40, 200)
                        cv_g.create_line(rx, ry, rx-1, ry+6, fill='#6699bb', width=1, tags='dynamic')
                elif self.weather_mode == 'snow':
                    import random as _rnd
                    for _ in range(4):
                        sx = _rnd.randint(50, W_G-50)
                        sy = _rnd.randint(40, 200)
                        cv_g.create_oval(sx-1, sy-1, sx+1, sy+1, fill='#ddeeff', outline='', tags='dynamic')

            # ── 旅行中:不显示角色 ──
            gcx = g['cx']; gcy = g['cy']
            if self.travel_state.get('active'):
                import time as _tt2
                rem = int(self.travel_state.get('end_ts', 0) - _tt2.time())
                dest = self.travel_state.get('dest', '?')
                # 显示飞机和提示文字
                cv_g.create_text(W_G//2, H_G//2 - 50, text='✈️',
                                 font=('Apple Color Emoji', 48), tags='dynamic')
                cv_g.create_text(W_G//2, H_G//2 + 20,
                                 text=f'正在去 {dest} 旅行中...',
                                 font=('PingFang SC', 14, 'bold'), fill='#ffcc44', tags='dynamic')
                min_left = max(0, rem) // 60; sec_left = max(0, rem) % 60
                cv_g.create_text(W_G//2, H_G//2 + 48,
                                 text=f'还有 {min_left}分{sec_left:02d}秒 到达',
                                 font=('PingFang SC', 11), fill='#ccddff', tags='dynamic')
            else:
                # ── 角色阴影 ──
                cv_g.create_oval(gcx-20, gcy-4, gcx+20, gcy+4, fill='#443322', outline='', tags='dynamic')

                # ── 角色图片 ──
                moving = g['moving']
                fi = (f // 4) % len(frames_right)
                if moving == 'right':
                    char_img = frames_left[fi]
                elif moving == 'left':
                    char_img = frames_right[fi]
                else:
                    char_img = stand_img
                cv_g.create_image(gcx, gcy - CHAR_H//2, anchor='s', image=char_img, tags='dynamic')

                # ── 生病图标 ──
                if self.sick and f%16<8:
                    cv_g.create_text(gcx+20, gcy-CHAR_H-4, text='🤒', font=('Apple Color Emoji',12), tags='dynamic')

            # ── 气泡(旅行中不显示)──
            if self.bubble and self.btimer > 0 and not self.travel_state.get('active'):
                btxt = self.bubble[:20] + ('...' if len(self.bubble)>20 else '')
                bx, by = gcx, gcy - CHAR_H - 6
                cv_g.create_oval(bx-4, by-22, bx+4, by, fill='#fff9f0', outline='#ccaa88', tags='dynamic')
                cv_g.create_rectangle(bx-80, by-46, bx+80, by-24, fill='#fff9f0', outline='#ccaa88', tags='dynamic')
                cv_g.create_text(bx, by-35, text=btxt, font=('PingFang SC', 10), fill='#333333', tags='dynamic')

            # ── 底部属性面板 ──
            py2 = H_G-34
            cv_g.create_rectangle(0,py2,W_G,H_G,fill='#100825',outline='',tags='dynamic')
            cv_g.create_line(0,py2,W_G,py2,fill='#2a1a55',width=1,tags='dynamic')
            stats=[(self.hunger,'#ff7733','🍔'),(self.mood,'#ffcc00','😊'),
                   (self.cleanliness,'#44bbff','🛁'),(self.health,'#ff3366','❤️')]
            bar_w=100; unit=bar_w+44; total=len(stats)*unit; sx2=(W_G-total)//2
            for i,(val,color,icon) in enumerate(stats):
                x2=sx2+i*unit; y2=py2+17
                cv_g.create_text(x2+8,y2,text=icon,font=('Apple Color Emoji',10), tags='dynamic')
                bx2=x2+22
                cv_g.create_rectangle(bx2,y2-4,bx2+bar_w,y2+4,fill='#1e0f38',outline='', tags='dynamic')
                fw=max(0,int(bar_w*val/100))
                fc2='#ff3333' if val<25 else '#ffaa22' if val<55 else color
                if fw>0:
                    cv_g.create_rectangle(bx2,y2-4,bx2+fw,y2+4,fill=fc2,outline='', tags='dynamic')
                    cv_g.create_rectangle(bx2,y2-4,bx2+fw,y2-3,fill='#ffffff',outline='', tags='dynamic')
                if val<25 and f%20<10:
                    cv_g.create_rectangle(bx2-1,y2-5,bx2+bar_w+1,y2+5,fill='',outline='#ff4444',width=1, tags='dynamic')
                # 数字显示在进度条右侧
                num_color='#ff4444' if val<25 else '#ffaa22' if val<55 else '#ccffcc'
                cv_g.create_text(bx2+bar_w+3,y2,text=f'{int(val)}',font=('PingFang SC',7),anchor='w',tags='dynamic',fill=num_color)

            # ── 积分/时间/标题 ──
            cv_g.create_text(8,H_G-36,text=f'⭐{self.score}',anchor='sw',font=('PingFang SC',9), tags='dynamic',fill='#aaaacc')
            cv_g.create_text(W_G-8,H_G-36,text=time.strftime('%H:%M'),anchor='se',font=('PingFang SC',9),fill='#888888',tags='dynamic')
            cv_g.create_text(W_G//2,12,text=self._home_title(),font=('PingFang SC',12,'bold'), tags='dynamic',
                            fill='#ffffff' if night else '#3a1a6a')

            # ── 关闭按钮 ──
            cv_g.create_oval(W_G-26,4,W_G-6,24,fill='#cc2244',outline='#ff4466',width=1, tags='dynamic')
            cv_g.create_text(W_G-16,14,text='✕',font=('PingFang SC',10,'bold'), tags='dynamic',fill='#ffccdd')
            # ── 天气切换按钮(右上角)──
            wx_modes = [('☀️','clear'), ('🌧️','rain'), ('❄️','snow')]
            for wi, (wicon, wmode) in enumerate(wx_modes):
                bx = W_G - 100 + wi * 28
                by = 6
                active = (self.weather_mode == wmode)
                cv_g.create_rectangle(bx, by, bx+24, by+20,
                                      fill='#5533aa' if active else '#2a1a55',
                                      outline='#8866cc' if active else '#443388',
                                      width=1, tags='dynamic')
                cv_g.create_text(bx+12, by+10, text=wicon,
                                 font=('Apple Color Emoji', 10), tags='dynamic')

            # ── 操作提示 ──
            cv_g.create_text(W_G//2,H_G-50,text='← → ↑ ↓ 走动 | E 交互 | T 调试',font=('PingFang SC',8), tags='dynamic',fill='#8866aa')

            # ── 调试模式 ──
            if g.get('debug'):
                _w = _INDOOR_WALLS if g['scene']=='indoor' else _OUTDOOR_WALLS
                for wx1,wy1,wx2,wy2 in _w:
                    cv_g.create_rectangle(wx1,wy1,wx2,wy2, outline='red', width=1, dash=(4,2), tags='dynamic')
                mx, my = g.get('mouse_x',0), g.get('mouse_y',0)
                cv_g.create_text(mx+15, my-10, text=f'({mx},{my})', fill='yellow',
                                 font=('Courier',10,'bold'), anchor='w', tags='dynamic')
                cv_g.create_text(W_G//2, 80, text=f'pos:({g["cx"]},{g["cy"]}) mouse:({mx},{my})',
                                 fill='yellow', font=('Courier',11,'bold'), tags='dynamic')

            # ── 走动逻辑(含碰撞检测)──
            g['frame'] = (f+1) % 10000
            spd = 4
            ncx, ncy = g['cx'], g['cy']
            sc = g['scene']
            if g['moving'] == 'left'  and ncx > 40:      ncx -= spd
            elif g['moving'] == 'right' and ncx < W_G-40: ncx += spd
            elif g['moving'] == 'up'   and ncy > 80:      ncy -= spd
            elif g['moving'] == 'down' and ncy < GND+20:  ncy += spd
            if not _collides(ncx, ncy, sc):
                g['cx'], g['cy'] = ncx, ncy

            # ── 场景切换判断 ──
            gcx2, gcy2 = g['cx'], g['cy']
            ep = g.get('e_pressed', False)
            if g['scene'] == 'indoor':
                in_stair2  = STAIR_X1  <= gcx2 <= STAIR_X2  and STAIR_Y1  <= gcy2 <= STAIR_Y2
                in_carpet2 = CARPET_X1 <= gcx2 <= CARPET_X2 and CARPET_Y1 <= gcy2 <= CARPET_Y2
                if ep and in_stair2:
                    g['scene'] = 'upstairs'
                    g['cx'] = W_G//2; g['cy'] = GND
                    self.say('上二楼了!🪜', 80)
                elif ep and in_carpet2:
                    g['scene'] = 'outdoor'
                    g['cx'] = EXT_DOOR_X; g['cy'] = EXT_DOOR_Y
                    self.say('哇!出门啦 🌿', 80)
            elif g['scene'] == 'outdoor':
                dist_back2 = ((gcx2-EXT_DOOR_X)**2 + (gcy2-EXT_DOOR_Y)**2) ** 0.5
                if ep and dist_back2 < EXT_DOOR_R:
                    g['scene'] = 'indoor'
                    g['cx'] = (CARPET_X1+CARPET_X2)//2; g['cy'] = (CARPET_Y1+CARPET_Y2)//2
                    self.say('回到家里啦 🏠', 80)
                elif ep and gcx2 < 80:
                    g['scene'] = 'forest'
                    g['cx'] = W_G - 80; g['cy'] = GND
                    self.say('进入森林了!🌳', 80)
            elif g['scene'] == 'forest':
                if ep and gcx2 > W_G - 80:
                    g['scene'] = 'outdoor'
                    g['cx'] = 80; g['cy'] = GND
                    self.say('回到门口了 🌿', 80)
            elif g['scene'] == 'upstairs':
                _usx1, _usy1 = W_G - 230, 110
                _usx2, _usy2 = W_G - 128, 328
                if ep and _usx1 <= gcx2 <= _usx2 and _usy1 <= gcy2 <= _usy2:
                    g['scene'] = 'indoor'
                    g['cx'] = (STAIR_X1+STAIR_X2)//2; g['cy'] = (STAIR_Y1+STAIR_Y2)//2
                    self.say('下楼了 🏠', 80)
            g['e_pressed'] = False

            # after已移至draw_g外层,此处不需要


        g['debug'] = False; g['mouse_x'] = 0; g['mouse_y'] = 0
        def on_kp(e):
            if e.keysym in ('Left','a','A'): g['moving']='left'
            elif e.keysym in ('Right','d','D'): g['moving']='right'
            elif e.keysym in ('Up','w','W'): g['moving']='up'
            elif e.keysym in ('Down','s','S'): g['moving']='down'
            elif e.keysym in ('e','E'): g['e_pressed']=True
            elif e.keysym in ('t','T'): g['debug'] = not g['debug']
        def on_mouse_move(e):
            g['mouse_x'] = e.x; g['mouse_y'] = e.y
        cv_g.bind('<Motion>', on_mouse_move)
        def on_kr(e):
            if e.keysym in ('Left','a','A','Right','d','D','Up','w','W','Down','s','S'):
                g['moving']=None
        def on_click(e):
            if W_G-24<=e.x<=W_G-4 and 2<=e.y<=22: win.destroy()
            wx_modes = ['clear', 'rain', 'snow']
            for wi, wmode in enumerate(wx_modes):
                bx = W_G - 100 + wi * 28
                if bx <= e.x <= bx+24 and 6 <= e.y <= 26:
                    self._set_weather(wmode); break
            # 摆放模式
            pending = getattr(self, '_pending_place', None)
            if pending:
                self.placed_furniture.append({'id': pending['id'], 'x': e.x, 'y': e.y,
                                              'file': pending['file'], 'name': pending['name']})
                cnt = self.furniture_bag.get(pending['id'], 0)
                self.furniture_bag[pending['id']] = max(0, cnt - 1)
                self._save()
                self.say(f"摆好{pending['name']}了!🛋️", 80)
                self._pending_place = None
        # 同时绑定 win 和 cv_g,确保键盘事件能收到
        win.bind('<KeyPress>',on_kp); win.bind('<KeyRelease>',on_kr)
        cv_g.bind('<KeyPress>',on_kp); cv_g.bind('<KeyRelease>',on_kr)
        def _garden_click(e):
            on_click(e)
            # 如果小卖部/档案等子窗口开着,保持它们在前面
            for attr in ('_shop_win','_profile_win','_travel_win'):
                sub = getattr(self, attr, None)
                if sub and sub.winfo_exists():
                    sub.lift()
        cv_g.bind('<Button-1>', lambda e: (_garden_click(e), None))

        # ── 拖动已摆放家具 ──
        _drag_state = {'idx': None, 'ox': 0, 'oy': 0}
        def on_furn_press(e):
            # 摘放模式优先--点击即摆
            pending = getattr(self, '_pending_place', None)
            if pending:
                _garden_click(e)
                return
            # 非摆放模式:检测是否点到已摆家具(拖动准备)
            HIT = 50
            for i, pf in enumerate(self.placed_furniture):
                if abs(e.x - pf['x']) < HIT and abs(e.y - pf['y']) < HIT:
                    _drag_state['idx'] = i
                    _drag_state['ox'] = e.x - pf['x']
                    _drag_state['oy'] = e.y - pf['y']
                    return
            _drag_state['idx'] = None
            _garden_click(e)  # 点到空白处也走通用点击逻辑
        def on_furn_drag(e):
            idx = _drag_state['idx']
            if idx is None or idx >= len(self.placed_furniture): return
            self.placed_furniture[idx]['x'] = e.x - _drag_state['ox']
            self.placed_furniture[idx]['y'] = e.y - _drag_state['oy']
        def on_furn_release(e):
            if _drag_state['idx'] is not None:
                self._save()
            _drag_state['idx'] = None
        cv_g.bind('<Button-1>',        lambda e: None)  # 禁用旧的 Button-1
        cv_g.bind('<ButtonPress-1>',   on_furn_press)
        cv_g.bind('<B1-Motion>',       on_furn_drag)
        cv_g.bind('<ButtonRelease-1>', on_furn_release)
        win.bind('<Button-1>', lambda e: win.focus_force())

        # 右键菜单
        def on_g_rclick(e):
            # 如果正在摆放模式,右键取消
            if getattr(self, '_pending_place', None):
                self._pending_place = None
                self.say('取消摆放', 40)
                return
            # 检测是否右键点到了已摆放的家具(命中范围 50px)
            HIT = 50
            hit_furn = None
            for i, pf in enumerate(self.placed_furniture):
                if abs(e.x - pf['x']) < HIT and abs(e.y - pf['y']) < HIT:
                    hit_furn = (i, pf)
                    break
            if hit_furn:
                idx, pf = hit_furn
                # 找到该家具的原价
                _fmeta = next((it for it in FURNITURE_ITEMS if it['id']==pf['id']), None)
                _sell_price = int((_fmeta['price'] if _fmeta else 0) * 0.6)
                def do_recall(_idx=idx, _pf=pf):
                    self.placed_furniture.pop(_idx)
                    self.furniture_bag[_pf['id']] = self.furniture_bag.get(_pf['id'], 0) + 1
                    self._furn_img_cache = {}
                    self._save()
                    self.say(f"收回了{_pf['name']}~", 60)
                def do_sell(_idx=idx, _pf=pf, _sp=_sell_price):
                    self.placed_furniture.pop(_idx)
                    self.score += _sp
                    self._furn_img_cache = {}
                    self._save()
                    self.say(f"出售{_pf['name']},获得⭐{_sp}!", 80)
                rm = tk.Menu(win, tearoff=0, bg='#1e0f3a', fg='#ddccff',
                             activebackground='#cc3333', activeforeground='white', font=('PingFang SC',11))
                rm.add_command(label=f"📦  收回『{pf['name']}』", command=do_recall)
                rm.add_command(label=f"💰  出售(六折 ⭐{_sell_price})", command=do_sell)
                rm.add_separator()
                rm.add_command(label='取消')
                try: rm.tk_popup(e.x_root, e.y_root)
                finally: rm.grab_release()
                return
            m = tk.Menu(win, tearoff=0, bg='#1e0f3a', fg='#ddccff',
                        activebackground='#7733cc', activeforeground='white', font=('PingFang SC',11))
            m.add_command(label='💬  找我说话', command=lambda: (self._chat_dialog(), win.focus_force()))
            m.add_command(label='🐾  宠物档案', command=lambda: (self.open_profile(), win.focus_force()))
            m.add_command(label='🗺️  旅行地图', command=lambda: (self.open_travel(), win.focus_force()))
            m.add_command(label='🎒  背包 & 仓库', command=lambda: (self.open_bag(), win.focus_force()))
            m.add_command(label='🛒  小卖部',   command=lambda: (self.open_shop(), win.focus_force()))
            m.add_command(label='🛋️  家具店',   command=lambda: (self.open_furniture_shop(), win.focus_force()))
            m.add_separator()
            m.add_command(label='🍔  喂食', command=lambda: (self.feed(), win.focus_force()))
            m.add_command(label='🛁  洗澡', command=lambda: (self.bathe(), win.focus_force()))
            m.add_command(label='🎮  玩耍', command=lambda: (self.play_with(), win.focus_force()))
            m.add_command(label='💊  喂药', command=lambda: (self.give_medicine(), win.focus_force()))
            m.add_separator()
            m.add_command(label=f'饥{int(self.hunger)} 情{int(self.mood)} 洁{int(self.cleanliness)} 命{int(self.health)}  Lv.{self.level}', state='disabled')
            m.add_separator()
            m.add_command(label='❌  关闭家园', command=win.destroy)
            try: m.tk_popup(e.x_root, e.y_root)
            finally: m.grab_release()

        cv_g.bind('<Button-2>', on_g_rclick)
        cv_g.bind('<Button-3>', on_g_rclick)
        win.focus_force()
        draw_g()

    def _mini_setup(self):
        W_M, H_M = 140, 165
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f'{W_M}x{H_M}+{sw-W_M-20}+{sh-H_M-120}')
        try:
            self.root.wm_attributes('-transparent', True)
            self.cv.configure(width=W_M, height=H_M, bg='systemTransparent',
                              highlightthickness=0)
            self.root.configure(bg='systemTransparent')
        except Exception:
            self.cv.configure(width=W_M, height=H_M, bg='#050010',
                              highlightthickness=0)
        self.mini_w = W_M
        self.mini_h = H_M

    def _on_mouse_move(self,e):
        over = (W-23<=e.x<=W-5 and 1<=e.y<=19)
        if over != self._close_hover:
            self._close_hover = over

    def onclick(self,e):
        # 关闭按钮点击
        if W-23<=e.x<=W-5 and 1<=e.y<=19:
            self.root.destroy(); return
        self.dox=e.x_root-self.root.winfo_x()
        self.doy=e.y_root-self.root.winfo_y(); self.drag=False

    def ondrag(self,e):
        self.drag=True; self.root.geometry(f'+{e.x_root-self.dox}+{e.y_root-self.doy}')

    def onrel(self,e):
        if not self.drag:
            if self.fainted:
                self._show_faint_popup(); return  # 昏厥时点击弹出救治弹窗
            self.poke_count+=1; self.add_score(1); self.add_exp(2)
            # 连续快速戳 → 生气
            now=time.time()
            if now-self.last_poke<1.5:
                self.angry_level=min(self.angry_level+1,4)
            else:
                self.angry_level=max(0,self.angry_level-1)
            self.last_poke=now
            if self.poke_count>=10: self.unlock('poke10')
            if self.poke_count>=50: self.unlock('poke50')
            if self.angry_level>2:
                self.say(random.choice(QUOTES_ANGRY),80)
                self.act_timer=120
            else:
                self.say(random.choice(['主人好!🤙','在呢~','南波万!','嗯?','哈哈~','戳我干嘛~']),60)
        self.drag=False

    def onright(self,e):
        m=tk.Menu(self.root,tearoff=0)
        # 昏厥时只显示救治菜单
        if self.fainted:
            m.add_command(label='🚨 宠物昏厥了!',state='disabled')
            m.add_separator()
            m.add_command(label='💊 吃药救命',command=lambda:self.open_bag(start_tab='medicine'))
            m.add_command(label='🍔 喂食恢复',command=lambda:self.open_bag(start_tab='food'))
            m.add_separator()
            m.add_command(label='❌ 关闭',command=self.root.destroy)
            try: m.tk_popup(e.x_root,e.y_root)
            finally: m.grab_release()
            return
        m.add_command(label='💬 找我说话',command=self._chat_dialog)
        m.add_command(label='🐾 宠物档案',command=self.open_profile)
        m.add_command(label='🗺️ 旅行地图',command=self.open_travel)
        m.add_command(label='🎣 去钓鱼',command=self.open_fishing)
        m.add_command(label='🎒 背包 & 仓库',command=self.open_bag)
        m.add_command(label='🛒 小卖部',command=self.open_shop)
        m.add_command(label='🛋️ 家具店',command=self.open_furniture_shop)
        m.add_separator()
        m.add_command(label='🍔 喂食',command=self.feed)
        m.add_command(label='🛁 洗澡',command=self.bathe)
        m.add_command(label='🎮 玩耍',command=self.play_with)
        m.add_command(label='💊 喂药',command=self.give_medicine)

        m.add_command(label='😴 睡觉',command=lambda:self.do('sleep'))

        m.add_separator()
        m.add_command(label='🏡 进入家园',command=self.open_garden)
        m.add_separator()

        m.add_command(label='⏰ 添加提醒',command=self._add_reminder_dialog)
        m.add_command(label='🏆 查看成就',command=self._show_achievements)
        m.add_command(label='⭐ 积分:'+str(self.score),state='disabled')
        m.add_command(label=f'饥{int(self.hunger)} 情{int(self.mood)} 洁{int(self.cleanliness)} 命{int(self.health)}',state='disabled')
        m.add_separator()
        m.add_command(label='🌤 看天气',command=lambda:(
            self.say(f'{self.w_icon} 北京 {self.w_temp}' if self.w_temp else '查天气中...',90),
            threading.Thread(target=self._wx,daemon=True).start() if not self.w_temp else None
        ))
        m.add_separator()
        m.add_command(label='📖 新手引导',command=lambda: self._tutorial_step(1))
        m.add_command(label='❌ 关闭',command=self.root.destroy)
        try: m.tk_popup(e.x_root,e.y_root)
        finally: m.grab_release()

    # ── 新手引导 ─────────────────────────────────────────────────────
    def _tutorial_welcome(self):
        """首次启动欢迎弹窗:选角色 + 设置主人名字"""
        win = tk.Toplevel(self.root)
        win.title('欢迎!')
        win.geometry('400x520')
        win.resizable(False, False)
        win.configure(bg='#1a0a2e')
        win.attributes('-topmost', True)
        # 居中
        sw = win.winfo_screenwidth(); sh = win.winfo_screenheight()
        win.geometry(f'400x520+{(sw-400)//2}+{(sh-520)//2}')
        win.protocol('WM_DELETE_WINDOW', lambda: None)  # 禁止直接关闭

        tk.Label(win, text='🏡 欢迎来到小家园!', font=('PingFang SC', 18, 'bold'),
                 bg='#1a0a2e', fg='#ffffff').pack(pady=(24, 4))
        tk.Label(win, text='先选个角色,再告诉我怎么叫你~',
                 font=('PingFang SC', 11), bg='#1a0a2e', fg='#c8a8ff').pack(pady=(0, 16))

        # 角色选择
        char_var = tk.StringVar(value=self.char_id)
        char_frame = tk.Frame(win, bg='#1a0a2e')
        char_frame.pack(fill='x', padx=32)
        tk.Label(char_frame, text='选择角色:', font=('PingFang SC', 11, 'bold'),
                 bg='#1a0a2e', fg='#ffffff').pack(anchor='w', pady=(0, 6))
        for cid, cinfo in CHARACTERS.items():
            tk.Radiobutton(char_frame, text=cinfo['name'], variable=char_var, value=cid,
                           font=('PingFang SC', 11), bg='#1a0a2e', fg='#e0d0ff',
                           selectcolor='#3a1a5e', activebackground='#1a0a2e',
                           activeforeground='#ffffff').pack(anchor='w', padx=8)

        # 名字输入
        name_frame = tk.Frame(win, bg='#1a0a2e')
        name_frame.pack(fill='x', padx=32, pady=(16, 0))
        tk.Label(name_frame, text='你的名字(我怎么叫你):',
                 font=('PingFang SC', 11, 'bold'), bg='#1a0a2e', fg='#ffffff').pack(anchor='w')
        name_var = tk.StringVar(value=self.address_word if self.address_word != '主人' else '')
        tk.Entry(name_frame, textvariable=name_var, font=('PingFang SC', 12),
                 bg='#2a1a4e', fg='#ffffff', insertbackground='white',
                 relief='flat', bd=6, width=20).pack(anchor='w', pady=(6, 0))

        def on_start():
            self.char_id = char_var.get()
            name = name_var.get().strip()
            if name:
                self.address_word = name
            self._mini_setup()
            win.destroy()
            self.root.after(800, lambda: self._tutorial_step(1))

        tk.Button(win, text='开始养宠物!🐾', command=on_start,
                  font=('PingFang SC', 13, 'bold'), bg='#7c3aed', fg='#ffffff',
                  relief='flat', padx=24, pady=10, cursor='hand2',
                  activebackground='#9d5cf0', activeforeground='#ffffff').pack(pady=24)

    def _tutorial_step(self, step):
        """在迷你模式上显示分步引导高亮"""
        self.cv.delete('tut')
        if step > 4:
            return

        # 半透明遮罩
        self.cv.create_rectangle(0, 0, W, H, fill='#000000', stipple='gray50', tags='tut')

        # 各步高亮区域 & 气泡文字
        highlights = {
            1: (240, 60, W-2, H-2,  '👉 右键我可以喂食、洗澡\n    玩耍、逛商店~'),
            2: (2,   210, W-2, H-2, '💛 这里是我的状态面板\n    记得关心我哦!'),
            3: (self.cx-60, self.gnd-130, self.cx+60, self.gnd,
                '✨ 双击我进入家园\n   有商店、旅行、家具~'),
        }
        if step in highlights:
            x1, y1, x2, y2, bubble_text = highlights[step]
            self.cv.create_rectangle(x1, y1, x2, y2,
                outline='#ffdd00', width=3, dash=(6, 4), tags='tut')
        else:
            bubble_text = '🎉 准备好了!\n开始养我吧 (〃\'▽\'〃)'

        # 气泡背景
        bx, by = 20, 20
        self.cv.create_rectangle(bx, by, bx+260, by+58,
            fill='#1a0a2e', outline='#7c3aed', width=2, tags='tut')
        self.cv.create_text(bx+130, by+29, text=bubble_text,
            fill='#ffffff', font=('PingFang SC', 11), justify='center', tags='tut')

        # 步骤指示
        self.cv.create_text(W-10, 10, text=f'{step}/4',
            fill='#c8a8ff', font=('PingFang SC', 10), anchor='ne', tags='tut')

        # 按钮
        btn_text = '下一步 →' if step < 4 else '开始探索!🐾'
        def on_next(s=step):
            self.cv.delete('tut')
            if s < 4:
                self._tutorial_step(s + 1)
        btn = tk.Button(self.root, text=btn_text, command=on_next,
                        font=('PingFang SC', 11, 'bold'), bg='#7c3aed', fg='white',
                        relief='flat', padx=12, pady=4, cursor='hand2',
                        activebackground='#9d5cf0', activeforeground='white')
        self.cv.create_window(W//2, H-24, window=btn, tags='tut')

    # ── 特产弹窗 ─────────────────────────────────────────────────────
    def _show_souvenir(self, dest, souv_name, souv_desc):
        """旅行结束后弹出特产弹窗"""
        import random as _rps
        from PIL import Image as _PI, ImageTk as _IT
        souv_colors = ['#c8102e','#c8680e','#8b4513','#2e8b57','#6b2fa0','#c8880e']
        bg_color = _rps.choice(souv_colors)

        win = tk.Toplevel(self.root)
        win.title(f'🎁 {dest}特产')
        win.geometry('340x320+80+120')
        win.resizable(False, False)
        win.attributes('-topmost', True)
        win.lift()
        win.configure(bg=bg_color)

        char_name = CHARACTERS.get(self.char_id, {}).get('name', '小宠物')

        tk.Label(win, text=f'🎁 {dest} 特产',
                 font=('PingFang SC', 16, 'bold'), bg=bg_color, fg='#ffffff').pack(pady=(16,4))

        card_frame = tk.Frame(win, bg='#fff8ee', relief='ridge', bd=3)
        card_frame.pack(padx=24, pady=4, fill='x')

        # 特产图片
        img_path = os.path.join(SOUVENIR_DIR, f'{dest}.png')
        if os.path.exists(img_path):
            try:
                pil_img = _PI.open(img_path).convert('RGBA').resize((96, 96), _PI.LANCZOS)
                tk_img = _IT.PhotoImage(pil_img)
                img_lbl = tk.Label(card_frame, image=tk_img, bg='#fff8ee')
                img_lbl.image = tk_img  # 防止 GC
                img_lbl.pack(pady=(10, 2))
            except Exception:
                pass

        tk.Label(card_frame, text=souv_name, font=('PingFang SC', 16, 'bold'),
                 bg='#fff8ee', fg='#3a1a00').pack(pady=(4,2))
        tk.Label(card_frame, text=souv_desc, font=('PingFang SC', 11),
                 bg='#fff8ee', fg='#665544', wraplength=260, justify='center').pack(pady=(0,10))

        tk.Label(win, text='→ 已入背包「特产」', font=('PingFang SC', 10),
                 bg=bg_color, fg='#ccffcc').pack(pady=(4,0))
        tk.Label(win, text=f'{char_name} 从 {dest} 带回来的～',
                 font=('PingFang SC', 9), bg=bg_color, fg='#ffe8cc').pack(pady=(2,0))

        tk.Button(win, text='好好收着 🎁', command=win.destroy,
                  font=('PingFang SC', 12, 'bold'), bg='#ffffff',
                  fg=bg_color, relief='flat', padx=20, pady=6,
                  cursor='hand2').pack(pady=10)

    # ── 明信片弹窗 ─────────────────────────────────────────────────────
    def _show_postcard(self, dest, card_name, card_desc):
        """旅行结束后弹出明信片弹窗"""
        import random as _rp
        from PIL import Image as _PI, ImageTk as _IT
        card_colors = ['#1a5c8b','#2e6bb0','#2e8b57','#6b2fa0','#1a6b5c','#2e4a8b']
        bg_color = _rp.choice(card_colors)

        win = tk.Toplevel(self.root)
        win.title(f'📮 来自{dest}的明信片')
        win.geometry('380x360+160+180')
        win.resizable(False, False)
        win.attributes('-topmost', True)
        win.lift()
        win.configure(bg=bg_color)

        addr = getattr(self, 'address_word', '主人')
        char_name = CHARACTERS.get(self.char_id, {}).get('name', '小宠物')

        tk.Label(win, text=f'📮 来自 {dest} 的明信片',
                 font=('PingFang SC', 15, 'bold'), bg=bg_color, fg='#ffffff').pack(pady=(16,4))

        card_frame = tk.Frame(win, bg='#fffef0', relief='ridge', bd=3)
        card_frame.pack(padx=24, pady=4, fill='x')

        # 明信片图片
        img_path = os.path.join(POSTCARD_DIR, f'{dest}.png')
        if os.path.exists(img_path):
            try:
                pil_img = _PI.open(img_path).convert('RGBA').resize((200, 140), _PI.LANCZOS)
                tk_img = _IT.PhotoImage(pil_img)
                img_lbl = tk.Label(card_frame, image=tk_img, bg='#fffef0')
                img_lbl.image = tk_img
                img_lbl.pack(pady=(10, 4))
            except Exception:
                pass

        tk.Label(card_frame, text=card_name, font=('PingFang SC', 15),
                 bg='#fffef0', fg='#1a3a5c').pack(pady=(4,2))
        tk.Label(card_frame, text=card_desc, font=('PingFang SC', 10),
                 bg='#fffef0', fg='#445566', wraplength=300, justify='center').pack(pady=(0,10))

        tk.Label(win, text='📮 已入背包「明信片」', font=('PingFang SC', 10),
                 bg=bg_color, fg='#ccffcc').pack(pady=(4,0))
        tk.Label(win, text=f'{char_name} 寄自 {dest}～ {addr}收',
                 font=('PingFang SC', 9), bg=bg_color, fg='#ffe8cc').pack(pady=(2,0))

        tk.Button(win, text='收好啦 💕', command=win.destroy,
                  font=('PingFang SC', 12, 'bold'), bg='#ffffff',
                  fg=bg_color, relief='flat', padx=20, pady=6,
                  cursor='hand2').pack(pady=10)

    def _set_weather(self,mode):
        self.weather_mode=mode
        self.particles=[]
        icons={'rain':'🌧️ 下雨啦!淋湿了...','snow':'❄️ 下雪了!好冷哦~','clear':'☀️ 天晴了!出去玩~'}
        self.say(icons.get(mode,'☀️'),90)

    def _add_reminder_dialog(self):
        win=tk.Toplevel(self.root); win.title('添加提醒')
        win.geometry('280x120'); win.resizable(False,False)
        win.lift()
        tk.Label(win,text='提醒内容:').pack(pady=(10,0))
        msg_var=tk.StringVar()
        tk.Entry(win,textvariable=msg_var,width=30).pack()
        tk.Label(win,text='多少分钟后?').pack()
        min_var=tk.IntVar(value=5)
        tk.Entry(win,textvariable=min_var,width=10).pack()
        def confirm():
            try:
                self.reminders.append({'at':time.time()+min_var.get()*60,'msg':msg_var.get() or '该休息啦!'})
                self.say(f'⏰ 好的,{min_var.get()}分钟后提醒你!',80)
                win.destroy()
            except: win.destroy()
        tk.Button(win,text='确定',command=confirm).pack(pady=5)

    def _show_faint_popup(self):
        """昏厥弹窗 — 非模态，可重复弹出"""
        # 防止重复弹窗
        if hasattr(self,'_faint_win') and self._faint_win and self._faint_win.winfo_exists():
            self._faint_win.lift(); return
        win=tk.Toplevel(self.root)
        self._faint_win=win
        win.title('🚨 昏厥了!')
        win.geometry('320x230+100+80')
        win.resizable(False,False)
        win.attributes('-topmost',True)
        win.configure(bg='#1a0000')
        win.lift()
        tk.Label(win,text='💤',font=('Apple Color Emoji',48),bg='#1a0000').pack(pady=(16,2))
        tk.Label(win,text='昏厥了...',font=('PingFang SC',16,'bold'),bg='#1a0000',fg='#ff4444').pack()
        tk.Label(win,text='健康归零太久，宠物昏厥了😢\n喂食物或吃药才能救活！',
                 font=('PingFang SC',11),bg='#1a0000',fg='#ffaaaa',justify='center').pack(pady=6)
        def do_rescue():
            win.destroy()
            self.open_bag(start_tab='medicine')
        def do_feed():
            win.destroy()
            self.open_bag(start_tab='food')
        bf=tk.Frame(win,bg='#1a0000'); bf.pack(pady=4)
        tk.Button(bf,text='💊 吃药救命',font=('PingFang SC',11,'bold'),
                  bg='#cc2222',fg='white',relief='flat',padx=12,pady=6,
                  command=do_rescue).pack(side='left',padx=6)
        tk.Button(bf,text='🍔 喂食恢复',font=('PingFang SC',11,'bold'),
                  bg='#aa4400',fg='white',relief='flat',padx=12,pady=6,
                  command=do_feed).pack(side='left',padx=6)
        tk.Button(win,text='关闭（稍后处理）',font=('PingFang SC',9),
                  bg='#333',fg='#aaa',relief='flat',pady=3,
                  command=win.destroy).pack(pady=(4,0))

    def _revive(self):
        """复活逻辑 — 给药/喂食后调用"""
        if self.fainted:
            self.fainted=False; self.faint_cd=0
            self.sick=False
            self.health=max(self.health,30)  # 至少30%健康
            self._save()
            self.say(random.choice([
                '😮 我...我还活着！谢谢主人😭',
                '刚才我在天上看到了主人...我回来了',
                '鸟科人生居然还有续篇！🥰',
                '主人...下次多关心我呢...🥺',
            ]),200)

    def _show_achievements(self):
        win=tk.Toplevel(self.root); win.title('🏆 成就')
        win.geometry('340x480'); win.resizable(False,True)
        win.attributes('-topmost',True); win.lift()
        BG='#1a1a2e'; CARD='#16213e'; GOLD='#f5c518'; GRAY='#555577'
        DONE_FG='#f5c518'; TODO_FG='#8888aa'
        win.configure(bg=BG)

        done=[a for a in self.achievements if a['done']]
        total=len(self.achievements)
        tk.Label(win,text=f'🏆 成就  {len(done)}/{total}',
                 font=('PingFang SC',14,'bold'),bg=BG,fg=GOLD).pack(pady=(12,4))

        # 进度条
        pb_frame=tk.Frame(win,bg=BG); pb_frame.pack(fill='x',padx=20,pady=(0,8))
        c=tk.Canvas(pb_frame,height=8,bg='#333355',highlightthickness=0)
        c.pack(fill='x')
        c.update_idletasks()
        w=c.winfo_width() or 300
        fill_w=int(w*len(done)/total)
        c.create_rectangle(0,0,fill_w,8,fill=GOLD,outline='')

        # 滚动区
        frame_outer=tk.Frame(win,bg=BG); frame_outer.pack(fill='both',expand=True,padx=10)
        canvas=tk.Canvas(frame_outer,bg=BG,highlightthickness=0)
        sb=tk.Scrollbar(frame_outer,orient='vertical',command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side='right',fill='y'); canvas.pack(side='left',fill='both',expand=True)
        inner=tk.Frame(canvas,bg=BG); canvas.create_window((0,0),window=inner,anchor='nw')

        # 分组
        groups=[
            ('🍔 喂食',['first_feed','feed10','feed50','feed_steak']),
            ('💬 对话',['first_chat','chat10','chat50']),
            ('👆 互动',['poke10','poke50']),
            ('🛁 洗澡',['first_bath','bath10','bath_cosmic']),
            ('🎣 钓鱼',['first_fish','fish10','fish_epic','fish_legend']),
            ('💎 积分',['score100','score1000','score5000']),
            ('⭐ 等级',['level5','level10']),
            ('🛒 购物',['shop10','furniture5','furniture15']),
            ('🗺️ 旅行',['travel5','travel15','travel35','postcard10']),
            ('🕐 时间',['night_owl','early_bird']),
        ]
        ach_map={a['id']:a for a in self.achievements}
        for gname,ids in groups:
            gh=tk.Frame(inner,bg=BG); gh.pack(fill='x',pady=(6,2),padx=4)
            tk.Label(gh,text=gname,font=('PingFang SC',10,'bold'),bg=BG,fg='#aaaacc').pack(anchor='w')
            for aid in ids:
                a=ach_map.get(aid); 
                if not a: continue
                row=tk.Frame(inner,bg=CARD,pady=4); row.pack(fill='x',padx=4,pady=1)
                if a['done']:
                    tk.Label(row,text=a['name'],font=('PingFang SC',10,'bold'),bg=CARD,fg=DONE_FG,width=16,anchor='w').pack(side='left',padx=8)
                    tk.Label(row,text='✅',bg=CARD,fg=DONE_FG,font=('PingFang SC',10)).pack(side='right',padx=8)
                else:
                    tk.Label(row,text=a['name'],font=('PingFang SC',10),bg=CARD,fg=TODO_FG,width=16,anchor='w').pack(side='left',padx=8)
                    tk.Label(row,text=a['desc'],font=('PingFang SC',9),bg=CARD,fg='#666688').pack(side='left')
                    tk.Label(row,text='🔒',bg=CARD,fg=TODO_FG,font=('PingFang SC',10)).pack(side='right',padx=8)

        inner.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'))
        canvas.bind_all('<MouseWheel>',lambda e:canvas.yview_scroll(-1 if e.delta>0 else 1,'units'))
        tk.Button(win,text='关闭',command=win.destroy,bg='#333355',fg='white',relief='flat',width=10).pack(pady=8)

    # ── 商店系统 ──────────────────────────────────────────────────────
    def open_shop(self):
        """小卖部 -- 只买东西,支持批量购买"""
        if hasattr(self,'_shop_win') and self._shop_win and self._shop_win.winfo_exists():
            self._shop_win.lift(); return
        from PIL import Image as _PI, ImageTk as _IT
        win=tk.Toplevel(self.root)
        win.title('🛒 小卖部')
        win.geometry('600x500+180+70')
        win.resizable(False,False)
        win.attributes('-topmost', True)
        win.lift(); win.focus_force()
        win.configure(bg='#f5e8c8')
        self._shop_win=win
        MID='#c8883a'; PANEL='#ffe8b0'; DARK='#7a4a10'; LIGHT='#fff5dc'
        SEL='#ffe066'; BTN_BUY='#e85520'; BTN_DIS='#aaaaaa'; TEXT='#3a1a00'
        state={'cat':'food','sel':None,'qty':1,'imgs':{}}

        def load_img(fname,size=64):
            k=(fname,size)
            if k in state['imgs']: return state['imgs'][k]
            # 药品用 emoji 动态渲染
            _MED_EMOJI = {'_med_basic':'💊','_med_good':'✨','_med_super':'💎','_med_divine':'🌟'}
            if fname in _MED_EMOJI:
                try:
                    img = _PI.new('RGBA',(size,size),(0,0,0,0))
                    from PIL import ImageDraw, ImageFont as _IF
                    draw = ImageDraw.Draw(img)
                    try: fnt = _IF.truetype('/System/Library/Fonts/Apple Color Emoji.ttc', int(size*0.75))
                    except: fnt = _IF.load_default()
                    draw.text((size//2, size//2), _MED_EMOJI[fname], font=fnt, anchor='mm', embedded_color=True)
                    p = _IT.PhotoImage(img)
                except: p=None
                state['imgs'][k]=p; return p
            fp=os.path.join(FOOD_DIR,fname)
            try: p=_IT.PhotoImage(_PI.open(fp).convert('RGBA').resize((size,size),_PI.NEAREST))
            except: p=None
            state['imgs'][k]=p; return p

        # 顶部
        top=tk.Frame(win,bg=MID,height=44); top.pack(fill='x'); top.pack_propagate(False)
        tk.Label(top,text='🛒  小卖部',font=('PingFang SC',14,'bold'),bg=MID,fg='#fff5dc').pack(side='left',padx=16)
        sc_lbl=tk.Label(top,text=f'⭐ {self.score}',font=('PingFang SC',11),bg=MID,fg='#fff5dc')
        sc_lbl.pack(side='right',padx=16)

        # 分类
        cf=tk.Frame(win,bg='#e8c880',height=30); cf.pack(fill='x'); cf.pack_propagate(False)
        cbtns={}
        def sw_cat(c):
            state['cat']=c; state['sel']=None
            for k,b in cbtns.items(): b.config(bg=SEL if k==c else '#e8c880')
            refresh()
        for cid,cl in [('food','🍚 主食'),('snack','🍬 零食'),('bath','🛁 浴球'),('medicine','💊 药品')]:
            b=tk.Button(cf,text=cl,font=('PingFang SC',10),bg=SEL if cid=='food' else '#e8c880',
                        fg=TEXT,relief='flat',bd=0,padx=14,pady=3,command=lambda c=cid:sw_cat(c))
            b.pack(side='left'); cbtns[cid]=b

        # 左右
        lp=tk.Frame(win,bg='#f5e8c8',width=420); lp.pack(side='left',fill='y'); lp.pack_propagate(False)
        rp=tk.Frame(win,bg=PANEL,width=180); rp.pack(side='right',fill='both',expand=True)

        # 网格
        gc=tk.Frame(lp,bg=LIGHT); gc.pack(fill='both',expand=True,padx=1,pady=2)
        gcv=tk.Canvas(gc,bg=LIGHT,highlightthickness=0)
        gsb=tk.Scrollbar(gc,orient='vertical',command=gcv.yview)
        gcv.configure(yscrollcommand=gsb.set)
        gsb.pack(side='right',fill='y'); gcv.pack(side='left',fill='both',expand=True)
        gf=tk.Frame(gcv,bg=LIGHT); gcv.create_window((0,0),window=gf,anchor='nw')
        def _on_scroll(e): gcv.yview_scroll(int(-1*(e.delta/120)),'units')
        def _bind_scroll(w):
            w.bind('<MouseWheel>',_on_scroll)
            for ch in w.winfo_children(): _bind_scroll(ch)
        gcv.bind('<MouseWheel>',_on_scroll)

        # 右侧详情
        di=tk.Label(rp,bg=PANEL); di.pack(pady=(16,4))
        dn=tk.Label(rp,text='',font=('PingFang SC',12,'bold'),bg=PANEL,fg=DARK); dn.pack()
        dd=tk.Label(rp,text='',font=('PingFang SC',9),bg=PANEL,fg=TEXT,wraplength=160); dd.pack(pady=2)
        de=tk.Label(rp,text='',font=('PingFang SC',9),bg=PANEL,fg='#556688',wraplength=160); de.pack(pady=2)
        dp=tk.Label(rp,text='',font=('PingFang SC',11,'bold'),bg=PANEL,fg=BTN_BUY); dp.pack(pady=4)
        dlv=tk.Label(rp,text='',font=('PingFang SC',9),bg=PANEL,fg='#886644'); dlv.pack()
        dct=tk.Label(rp,text='',font=('PingFang SC',10),bg=PANEL,fg=DARK); dct.pack(pady=2)

        # 数量选择
        tk.Label(rp,text='购买数量:',font=('PingFang SC',9),bg=PANEL,fg=DARK).pack(pady=(6,0))
        # 快捷按钮行
        quick_f=tk.Frame(rp,bg=PANEL); quick_f.pack(pady=2)
        qty_var=tk.StringVar(value='1')
        def _set_qty(q):
            qty_var.set(str(q))
            qty_entry.config(fg=DARK)
            upd_qty()
        for q in [1,5,10,20]:
            tk.Button(quick_f,text=f'×{q}',font=('PingFang SC',9),bg='#e8c870',fg=DARK,
                      relief='flat',bd=0,padx=6,pady=2,cursor='hand2',
                      command=lambda _q=q:_set_qty(_q)).pack(side='left',padx=2)
        # 自定义输入框
        input_f=tk.Frame(rp,bg=PANEL); input_f.pack(pady=2)
        tk.Label(input_f,text='自定义:',font=('PingFang SC',9),bg=PANEL,fg=DARK).pack(side='left')
        qty_entry=tk.Entry(input_f,textvariable=qty_var,font=('PingFang SC',11),
                           width=5,justify='center',bg=LIGHT,fg=DARK,relief='solid',bd=1)
        qty_entry.pack(side='left',padx=2)
        qty_entry.bind('<KeyRelease>',lambda e:upd_qty())
        qty_entry.bind('<FocusOut>',lambda e:upd_qty())

        total_lbl=tk.Label(rp,text='',font=('PingFang SC',10,'bold'),bg=PANEL,fg='#aa3300'); total_lbl.pack(pady=2)

        b_buy=tk.Button(rp,text='💰 购买',font=('PingFang SC',12,'bold'),bg=BTN_BUY,fg='white',
                        relief='flat',bd=0,padx=20,pady=7,state='disabled',cursor='hand2'); b_buy.pack(pady=(6,2))
        ml=tk.Label(rp,text='',font=('PingFang SC',9),bg=PANEL,fg='#cc3300',wraplength=165); ml.pack(pady=4)

        def upd_qty():
            try:
                q=int(qty_var.get())
                if q<1: q=1
                if q>999: q=999
            except: q=1
            state['qty']=q
            if state['sel']:
                it=next((x for x in SHOP_ITEMS if x['id']==state['sel']),None)
                if it: _update_buy_btn(it)

        def _update_buy_btn(item):
            q=state['qty']
            total=item['price']*q
            locked=item['lv']>self.level
            total_lbl.config(text=f'合计 ⭐{total}' if not locked else '')
            if locked: b_buy.config(state='disabled',bg=BTN_DIS,text='🔒 等级不足')
            elif self.score<total: b_buy.config(state='disabled',bg=BTN_DIS,text=f'💰 积分不足')
            else: b_buy.config(state='normal',bg=BTN_BUY,text=f'💰 ×{q} 购买',
                               command=lambda it=item,_q=q:do_buy(it,_q))

        def upd_detail(item):
            img=load_img(item['file'],60)
            if img: di.config(image=img); di._img=img
            dn.config(text=item['name']); dd.config(text=item['desc'])
            fx=[]
            if item.get('hunger',0)>0: fx.append(f'饱腹+{item["hunger"]}')
            if item.get('mood',0)>0: fx.append(f'心情+{item["mood"]}')
            if item.get('health',0)!=0: fx.append(f'健康{item["health"]:+d}')
            if item.get('clean',0)>0: fx.append(f'洁净+{item["clean"]}')
            if item.get('cure'): fx.append('消除病态')
            de.config(text='  '.join(fx))
            dp.config(text=f'⭐ {item["price"]}/个')
            dlv.config(text=f'需要 Lv.{item["lv"]}'+(' 🔒' if item["lv"]>self.level else ' ✅'))
            dct.config(text=f'背包库存:×{self.bag.get(item["id"],0)}')
            _update_buy_btn(item)

        def do_buy(item,qty):
            total=item['price']*qty
            if self.score<total: ml.config(text='积分不足!'); return
            if item['lv']>self.level: ml.config(text=f'需要 Lv.{item["lv"]}!'); return
            self.score-=total
            self.bag[item['id']]=self.bag.get(item['id'],0)+qty
            self.buy_count=getattr(self,'buy_count',0)+qty
            self.add_exp(3*qty); self._save()
            if self.buy_count>=10: self.unlock('shop10')
            self.say(f'买到×{qty} {item["name"]}!🛒',70)
            ml.config(text=f'✅ 购买成功!背包 ×{self.bag[item["id"]]}')
            sc_lbl.config(text=f'⭐ {self.score}')
            dct.config(text=f'背包库存:×{self.bag.get(item["id"],0)}')
            _update_buy_btn(item)

        def refresh():
            for w in gf.winfo_children(): w.destroy()
            pool=[it for it in SHOP_ITEMS if it['cat']==state['cat']]
            COLS=4
            for i,item in enumerate(pool):
                r,c=i//COLS,i%COLS
                issel=item['id']==state['sel']
                locked=item['lv']>self.level
                cell_bg=SEL if issel else ('#ece4d0' if locked else LIGHT)
                fr=tk.Frame(gf,bg=cell_bg,bd=2,relief='ridge' if issel else 'flat',cursor='hand2')
                fr.grid(row=r,column=c,padx=3,pady=4)
                img=load_img(item['file'],64)
                if img:
                    il=tk.Label(fr,image=img,bg=cell_bg); il.pack(); il._img=img
                tk.Label(fr,text=item['name'],font=('PingFang SC',10,'bold'),
                         bg=cell_bg,fg='#888888' if locked else TEXT).pack()
                tk.Label(fr,text=f'🔒Lv{item["lv"]}' if locked else f'⭐{item["price"]}',
                         font=('PingFang SC',9),bg=cell_bg,
                         fg='#aaaaaa' if locked else BTN_BUY).pack()
                cnt=self.bag.get(item['id'],0)
                if cnt>0:
                    tk.Label(fr,text=f'×{cnt}',font=('PingFang SC',8,'bold'),
                             bg=cell_bg,fg='#3a7a30').pack()
                def on_click(it=item):
                    state['sel']=it['id']; refresh(); upd_detail(it)
                for w in fr.winfo_children(): w.bind('<Button-1>',lambda e,it=item:on_click(it))
                fr.bind('<Button-1>',lambda e,it=item:on_click(it))
            gf.update_idletasks(); gcv.configure(scrollregion=gcv.bbox('all'))
            _bind_scroll(gf)
            sc_lbl.config(text=f'⭐ {self.score}'); ml.config(text='')
            if state['sel']:
                it=next((x for x in SHOP_ITEMS if x['id']==state['sel']),None)
                if it: upd_detail(it)

        refresh(); win.focus_force()

    def open_bag(self, start_tab='food'):
        """背包(食物/浴球/特产) + 家具仓库 -- Tab 切换"""
        if hasattr(self,'_bag_win') and self._bag_win and self._bag_win.winfo_exists():
            self._bag_win.lift(); return
        from PIL import Image as _PI, ImageTk as _IT
        import os as _os2
        FOOD_DIR = _os2.path.join(_os2.path.dirname(_os2.path.abspath(__file__)), 'assets', 'food')
        FURN_DIR = _os2.path.join(_os2.path.dirname(_os2.path.abspath(__file__)), 'assets', 'furniture')
        PREV_DIR = _os2.path.join(_os2.path.dirname(_os2.path.abspath(__file__)), 'assets', 'furniture_preview')

        win = tk.Toplevel(self.root)
        win.title('🎒 背包 & 仓库')
        win.geometry('520x460+200+80')
        win.resizable(False, False)
        win.attributes('-topmost', True)
        win.lift(); win.focus_force()
        win.configure(bg='#f5e8c8')
        self._bag_win = win

        MID='#c8883a'; PANEL='#ffe8b0'; DARK='#7a4a10'; LIGHT='#fff5dc'
        SEL='#ffe066'; BTN_OK='#3a9a30'; BTN_DIS='#aaaaaa'; TEXT='#3a1a00'
        state = {'tab': start_tab, 'sel':None, 'imgs':{}}

        def _img_cache(fp, size):
            k = (fp, size)
            if k in state['imgs']: return state['imgs'][k]
            # 药品 emoji 渲染
            _MED_EMOJI = {'_med_basic':'💊','_med_good':'✨','_med_super':'💎','_med_divine':'🌟'}
            _basename = os.path.basename(fp) if os.path.sep in fp else fp
            if _basename in _MED_EMOJI or fp in _MED_EMOJI:
                _ek = fp if fp in _MED_EMOJI else _basename
                try:
                    img = _PI.new('RGBA',(size,size),(0,0,0,0))
                    from PIL import ImageDraw, ImageFont as _IF2
                    draw = ImageDraw.Draw(img)
                    try: fnt = _IF2.truetype('/System/Library/Fonts/Apple Color Emoji.ttc', int(size*0.75))
                    except: fnt = _IF2.load_default()
                    draw.text((size//2, size//2), _MED_EMOJI[_ek], font=fnt, anchor='mm', embedded_color=True)
                    p = _IT.PhotoImage(img)
                except: p = None
                state['imgs'][k] = p; return p
            try:
                raw = _PI.open(fp).convert('RGBA')
                ow,oh = raw.size; s = min(size/ow, size/oh)
                nw,nh = int(ow*s), int(oh*s)
                p = _IT.PhotoImage(raw.resize((nw,nh), _PI.LANCZOS))
            except: p = None
            state['imgs'][k] = p; return p

        # ── Tab 栏 ──
        # Tab区分两行
        tab_bar = tk.Frame(win, bg=MID); tab_bar.pack(fill='x')
        # 第一行：标题 + 食物/浴球/鱼筼
        row1 = tk.Frame(tab_bar, bg=MID); row1.pack(fill='x')
        tk.Label(row1, text='🎒 背包', font=('PingFang SC',12,'bold'), bg=MID, fg='#fff5dc').pack(side='left', padx=10, pady=4)
        t_food = tk.Button(row1, text='🍔 食物', font=('PingFang SC',10,'bold'),
                           bg=MID, fg='#fff5dc', relief='flat', bd=0, padx=8, pady=3, cursor='hand2')
        t_bath = tk.Button(row1, text='🛁 浴球', font=('PingFang SC',10,'bold'),
                           bg=MID, fg='#fff5dc', relief='flat', bd=0, padx=8, pady=3, cursor='hand2')
        t_fish = tk.Button(row1, text='🎣 鱼筼', font=('PingFang SC',10,'bold'),
                           bg=MID, fg='#fff5dc', relief='flat', bd=0, padx=8, pady=3, cursor='hand2')
        t_med  = tk.Button(row1, text='💊 药品', font=('PingFang SC',10,'bold'),
                           bg=MID, fg='#fff5dc', relief='flat', bd=0, padx=8, pady=3, cursor='hand2')
        t_food.pack(side='right', padx=2, pady=3)
        t_bath.pack(side='right', padx=2, pady=3)
        t_fish.pack(side='right', padx=2, pady=3)
        t_med.pack(side='right', padx=2, pady=3)
        # 第二行：仓库标题 + 仓库/特产/明信片
        row2 = tk.Frame(tab_bar, bg='#5a3a1a'); row2.pack(fill='x')
        tk.Label(row2, text='🏠 仓库', font=('PingFang SC',12,'bold'), bg='#5a3a1a', fg='#ffe8aa').pack(side='left', padx=10, pady=4)
        t_furn = tk.Button(row2, text='🛋️ 家具', font=('PingFang SC',10,'bold'),
                           bg='#5a3a1a', fg='#ffe8aa', relief='flat', bd=0, padx=8, pady=3, cursor='hand2')
        t_souvenir = tk.Button(row2, text='🎁 特产', font=('PingFang SC',10,'bold'),
                           bg='#5a3a1a', fg='#ffe8aa', relief='flat', bd=0, padx=8, pady=3, cursor='hand2')
        t_postcard = tk.Button(row2, text='📮 明信片', font=('PingFang SC',10,'bold'),
                           bg='#5a3a1a', fg='#ffe8aa', relief='flat', bd=0, padx=8, pady=3, cursor='hand2')
        t_furn.pack(side='right', padx=2, pady=3)
        t_souvenir.pack(side='right', padx=2, pady=3)
        t_postcard.pack(side='right', padx=2, pady=3)

        # ── 主体区 ──
        body = tk.Frame(win, bg='#f5e8c8'); body.pack(fill='both', expand=True)
        lp = tk.Frame(body, bg='#f5e8c8', width=330); lp.pack(side='left', fill='y'); lp.pack_propagate(False)
        rp = tk.Frame(body, bg=PANEL, width=190); rp.pack(side='right', fill='both', expand=True)

        # 右侧面板元素
        di   = tk.Label(rp, bg=PANEL); di.pack(pady=(16,4))
        dn   = tk.Label(rp, text='', font=('PingFang SC',12,'bold'), bg=PANEL, fg=DARK); dn.pack()
        dd   = tk.Label(rp, text='', font=('PingFang SC',9), bg=PANEL, fg=TEXT, wraplength=170); dd.pack(pady=2)
        de   = tk.Label(rp, text='', font=('PingFang SC',9), bg=PANEL, fg='#556688', wraplength=170); de.pack(pady=2)
        dct  = tk.Label(rp, text='', font=('PingFang SC',10,'bold'), bg=PANEL, fg=DARK); dct.pack(pady=4)
        b1   = tk.Button(rp, text='', font=('PingFang SC',12,'bold'), bg=BTN_OK, fg='white',
                         relief='flat', bd=0, padx=16, pady=7, state='disabled', cursor='hand2'); b1.pack(pady=(6,3))
        b2   = tk.Button(rp, text='', font=('PingFang SC',12,'bold'), bg='#aa3333', fg='white',
                         relief='flat', bd=0, padx=16, pady=7, state='disabled', cursor='hand2'); b2.pack(pady=3)
        b3   = tk.Button(rp, text='', font=('PingFang SC',11), bg='#555', fg='white',
                         relief='flat', bd=0, padx=16, pady=5, state='disabled', cursor='hand2'); b3.pack(pady=3)
        ml   = tk.Label(rp, text='', font=('PingFang SC',9), bg=PANEL, fg='#cc3300', wraplength=170); ml.pack(pady=4)

        def reset_right():
            di.config(image=''); di._img=None
            dn.config(text=''); dd.config(text=''); de.config(text=''); dct.config(text=''); ml.config(text='')
            for b in (b1,b2,b3): b.config(text='', state='disabled', bg='#888')

        # ── 左侧滚动网格 ──
        gc = tk.Frame(lp, bg=LIGHT); gc.pack(fill='both', expand=True, padx=1, pady=2)
        gcv = tk.Canvas(gc, bg=LIGHT, highlightthickness=0)
        gsb = tk.Scrollbar(gc, orient='vertical', command=gcv.yview)
        gcv.configure(yscrollcommand=gsb.set)
        gsb.pack(side='right', fill='y'); gcv.pack(side='left', fill='both', expand=True)
        gf = tk.Frame(gcv, bg=LIGHT); gcv.create_window((0,0), window=gf, anchor='nw')
        def _on_scroll(e): gcv.yview_scroll(int(-1*(e.delta/120)), 'units')
        gcv.bind('<MouseWheel>', _on_scroll)

        # ════ 食物背包 ════
        def show_food_detail(item):
            fp = _os2.path.join(FOOD_DIR, item['file'])
            img = _img_cache(fp, 64)
            if img: di.config(image=img); di._img=img
            dn.config(text=item['name']); dd.config(text=item['desc'])
            fx=[]
            if item['hunger']>0: fx.append(f'饱腹+{item["hunger"]}')
            if item['mood']>0: fx.append(f'心情+{item["mood"]}')
            if item['health']!=0: fx.append(f'健康{item["health"]:+d}')
            de.config(text='  '.join(fx))
            cnt = self.bag.get(item['id'],0)
            dct.config(text=f'剩余 ×{cnt}')
            def do_use(it=item):
                c = self.bag.get(it['id'],0)
                if c<=0: ml.config(text='没有了!'); return
                self.hunger=min(100,self.hunger+it['hunger'])
                self.mood=min(100,self.mood+it['mood'])
                self.health=min(100,max(0,self.health+it['health']))
                if self.sick and self.health>=75: self.sick=False
                self.bag[it['id']]=c-1; self.feed_count+=1; self.add_exp(5); self._save()
                self.unlock('first_feed')
                if self.feed_count>=10: self.unlock('feed10')
                if self.feed_count>=50: self.unlock('feed50')
                if it['id']=='steak': self.unlock('feed_steak')
                self._revive()  # 如果昏厥中，喂食可以复活
                import random as _r
                self.say(_r.choice([f'{it["name"]}好好吃!😋',f'啊~太香了!',f'谢谢主人!',f'最喜欢了!']),100)
                ml.config(text=f'✅ 剩余×{self.bag[it["id"]]}')
                dct.config(text=f'剩余 ×{self.bag[it["id"]]}')
                b1.config(state='normal' if self.bag[it['id']]>0 else 'disabled',
                          bg=BTN_OK if self.bag[it['id']]>0 else BTN_DIS)
                refresh_grid()
            b1.config(text='🍽 喂食', bg=BTN_OK if cnt>0 else BTN_DIS,
                      state='normal' if cnt>0 else 'disabled', command=do_use)
            b2.config(text='', state='disabled', bg='#888')
            b3.config(text='', state='disabled', bg='#888')

        # ════ 家具仓库 ════
        def show_furn_detail(item):
            prev_fp = _os2.path.join(PREV_DIR, item.get('preview',''))
            if not _os2.path.exists(prev_fp):
                prev_fp = _os2.path.join(FURN_DIR, item['file'])
            img = _img_cache(prev_fp, 80)
            if img: di.config(image=img); di._img=img
            dn.config(text=item['name'])
            dd.config(text=item['desc'])
            de.config(text=f'心情+{item["mood"]}')
            bag_cnt    = self.furniture_bag.get(item['id'],0)
            placed_cnt = sum(1 for p in self.placed_furniture if p['id']==item['id'])
            sell_price = int(item['price']*0.6)
            dct.config(text=f'背包×{bag_cnt}  已摆×{placed_cnt}')
            def do_place(it=item):
                if self.furniture_bag.get(it['id'],0)<=0: ml.config(text='背包里没有了!'); return
                self._pending_place = it
                win.destroy()
                self.say(f'点击家园中的位置来摆放{it["name"]}吧~', 100)
            def do_recall(it=item):
                candidates=[i for i,p in enumerate(self.placed_furniture) if p['id']==it['id']]
                if not candidates: ml.config(text='没有已摆放的!'); return
                self.placed_furniture.pop(candidates[-1])
                self.furniture_bag[it['id']] = self.furniture_bag.get(it['id'],0)+1
                self._furn_img_cache={}; self._save()
                self.say(f'收回了{it["name"]}~',60)
                ml.config(text='✅ 已收回到背包')
                show_furn_detail(it); refresh_grid()
            def do_sell(it=item, sp=sell_price):
                if self.furniture_bag.get(it['id'],0)<=0: ml.config(text='背包里没有!'); return
                self.furniture_bag[it['id']] -= 1
                self.score += sp; self._save()
                self.say(f'出售{it["name"]},获得⭐{sp}!',80)
                ml.config(text=f'✅ 出售+⭐{sp}')
                show_furn_detail(it); refresh_grid()
            b1.config(text='🏠 摆放', bg='#3a7a30' if bag_cnt>0 else BTN_DIS,
                      state='normal' if bag_cnt>0 else 'disabled', command=do_place)
            b2.config(text='📦 收回', bg='#cc7700' if placed_cnt>0 else BTN_DIS,
                      state='normal' if placed_cnt>0 else 'disabled', command=do_recall)
            b3.config(text=f'💰 出售 ⭐{sell_price}', bg='#aa3333' if bag_cnt>0 else BTN_DIS,
                      state='normal' if bag_cnt>0 else 'disabled', command=do_sell)

        # ════ 网格渲染函数 ════
        def _render_food_grid():
            pool=[it for it in SHOP_ITEMS if it.get('cat') in ('food','snack') and self.bag.get(it['id'],0)>0]
            if not pool:
                tk.Label(gf,text='食物背包空空如也~\n去小卖部买点吧',
                         font=('PingFang SC',12),bg=LIGHT,fg='#aaaaaa',justify='center').pack(pady=40)
                return
            COLS=3
            for i,item in enumerate(pool):
                r,c=divmod(i,COLS)
                issel = item['id']==state['sel']
                cbg = SEL if issel else LIGHT
                fr=tk.Frame(gf,bg=cbg,bd=2,relief='ridge' if issel else 'flat',cursor='hand2')
                fr.grid(row=r,column=c,padx=5,pady=5)
                fp=_os2.path.join(FOOD_DIR,item['file'])
                img=_img_cache(fp,64)
                if img: il=tk.Label(fr,image=img,bg=cbg); il.pack(); il._img=img
                tk.Label(fr,text=item['name'],font=('PingFang SC',10,'bold'),bg=cbg,fg=TEXT).pack()
                tk.Label(fr,text=f'×{self.bag.get(item["id"],0)}',font=('PingFang SC',10,'bold'),bg=cbg,fg='#3a7a30').pack()
                def _sel(it=item): state['sel']=it['id']; refresh_grid(); show_food_detail(it)
                for w in fr.winfo_children(): w.bind('<Button-1>',lambda e,it=item:_sel(it))
                fr.bind('<Button-1>',lambda e,it=item:_sel(it))

        def _render_furn_grid():
            all_ids = set(k for k,v in self.furniture_bag.items() if v>0)
            all_ids |= set(p['id'] for p in self.placed_furniture)
            pool = [it for it in FURNITURE_ITEMS if it['id'] in all_ids]
            if not pool:
                tk.Label(gf,text='仓库空空如也~\n去家具店买点吧',
                         font=('PingFang SC',12),bg=LIGHT,fg='#aaaaaa',justify='center').pack(pady=40)
                return
            COLS=3
            for i,item in enumerate(pool):
                r,c=divmod(i,COLS)
                issel = item['id']==state['sel']
                bag_c=self.furniture_bag.get(item['id'],0)
                placed_c=sum(1 for p in self.placed_furniture if p['id']==item['id'])
                if issel:
                    cbg = SEL
                elif bag_c == 0 and placed_c > 0:
                    cbg = '#d8d0c0'
                else:
                    cbg = LIGHT
                fg_name = '#888877' if (bag_c==0 and placed_c>0 and not issel) else TEXT
                fr=tk.Frame(gf,bg=cbg,bd=2,relief='ridge' if issel else 'flat',cursor='hand2')
                fr.grid(row=r,column=c,padx=5,pady=5)
                prev_fp=_os2.path.join(PREV_DIR,item.get('preview',''))
                if not _os2.path.exists(prev_fp): prev_fp=_os2.path.join(FURN_DIR,item['file'])
                img=_img_cache(prev_fp,72)
                if img: il=tk.Label(fr,image=img,bg=cbg); il.pack(); il._img=img
                tk.Label(fr,text=item['name'],font=('PingFang SC',10,'bold'),bg=cbg,fg=fg_name).pack()
                status_txt = f'已摆×{placed_c}' if bag_c==0 else f'背包×{bag_c}  已摆×{placed_c}'
                tk.Label(fr,text=status_txt,font=('PingFang SC',9),bg=cbg,fg='#777766' if bag_c==0 else '#556688').pack()
                def _sel(it=item): state['sel']=it['id']; refresh_grid(); show_furn_detail(it)
                for w in fr.winfo_children(): w.bind('<Button-1>',lambda e,it=item:_sel(it))
                fr.bind('<Button-1>',lambda e,it=item:_sel(it))

        def switch_tab(tab):
            state['tab']=tab; state['sel']=None; reset_right()
            for tb,tid,ac,ic in [
                (t_food,'food',MID,'#5a3a1a'),(t_bath,'bath',MID,'#5a3a1a'),(t_fish,'fish',MID,'#5a3a1a'),(t_med,'medicine',MID,'#5a3a1a'),
                (t_furn,'furn','#5a3a1a',MID),(t_souvenir,'souvenir','#5a3a1a',MID),(t_postcard,'postcard','#5a3a1a',MID)
            ]:
                active = (tab==tid)
                tb.config(bg='#ffe066' if active else ac,
                          fg=DARK      if active else ('#fff5dc' if ac==MID else '#ffe8aa'))
            refresh_grid()

        def refresh_grid():
            for w in gf.winfo_children(): w.destroy()
            if state['tab'] == 'food':
                _render_food_grid()
            elif state['tab'] == 'bath':
                _render_bath_grid()
            elif state['tab'] == 'fish':
                _render_fish_grid()
            elif state['tab'] == 'medicine':
                _render_medicine_grid()
            elif state['tab'] == 'souvenir':
                _render_souvenir_grid()
            elif state['tab'] == 'postcard':
                _render_postcard_grid()
            else:
                _render_furn_grid()
            gf.update_idletasks(); gcv.configure(scrollregion=gcv.bbox('all'))
            gcv.bind('<MouseWheel>',_on_scroll)
            if state['sel']:
                if state['tab']=='food':
                    it=next((x for x in SHOP_ITEMS if x['id']==state['sel']),None)
                    if it: show_food_detail(it)
                elif state['tab']=='bath':
                    it=next((x for x in SHOP_ITEMS if x['id']==state['sel']),None)
                    if it: show_bath_detail(it)
                elif state['tab']=='furn':
                    it=next((x for x in FURNITURE_ITEMS if x['id']==state['sel']),None)
                    if it: show_furn_detail(it)

        # ==== 浴球 Tab ====
        def show_bath_detail(item):
            fp = _os2.path.join(FOOD_DIR, item.get('file',''))
            img = _img_cache(fp, 64) if _os2.path.exists(fp) else None
            if img: di.config(image=img); di._img=img
            dn.config(text=item['name']); dd.config(text=item['desc'])
            fx=[]
            if item.get('clean',0)>0: fx.append(f'洁净+{item["clean"]}')
            if item.get('mood',0)>0:  fx.append(f'心情+{item["mood"]}')
            if item.get('health',0)>0:fx.append(f'健康+{item["health"]}')
            de.config(text='  '.join(fx))
            cnt = self.bag.get(item['id'],0)
            dct.config(text=f'剩余 ×{cnt}')
            def do_bathe(it=item):
                c = self.bag.get(it['id'],0)
                if c<=0: ml.config(text='没有了!'); return
                if self.cleanliness>=98: ml.config(text='已经很干净了~'); return
                self.bag[it['id']]=c-1
                self.cleanliness=min(100,self.cleanliness+it.get('clean',30))
                self.mood=min(100,self.mood+it.get('mood',10))
                self.health=min(100,self.health+it.get('health',5))
                self.bathe_count+=1; self.add_score(3); self.add_exp(8); self._save()
                self.unlock('first_bath')
                if self.bathe_count>=10: self.unlock('bath10')
                if it['id']=='bathball_ex': self.unlock('bath_cosmic')
                import random as _r
                self.say(_r.choice([f'🛁 用{it["name"]}洗澡!喗喗的~',f'香香的!{it["name"]}好赞!',f'洗得超干净~用了{it["name"]}!']),80)
                ml.config(text=f'✅ 剩余×{self.bag[it["id"]]}')
                dct.config(text=f'剩余 ×{self.bag[it["id"]]}')
                b1.config(state='normal' if self.bag[it['id']]>0 else 'disabled',
                          bg=BTN_OK if self.bag[it['id']]>0 else BTN_DIS)
                refresh_grid()
            b1.config(text='🛁 洗澡', bg=BTN_OK if cnt>0 else BTN_DIS,
                      state='normal' if cnt>0 else 'disabled', command=do_bathe)
            b2.config(text='', state='disabled', bg='#888')
            b3.config(text='', state='disabled', bg='#888')

        def _render_bath_grid():
            pool=[it for it in SHOP_ITEMS if it.get('cat')=='bath' and self.bag.get(it['id'],0)>0]
            if not pool:
                tk.Label(gf,text='浴球已用完~\n去小卖部买一个吧🛁',
                         font=('PingFang SC',12),bg=LIGHT,fg='#aaaaaa',justify='center').pack(pady=40)
                tk.Button(gf,text='🛒 去小卖部购买',font=('PingFang SC',11),
                          bg='#c8883a',fg='white',relief='flat',cursor='hand2',
                          command=lambda:(win.destroy(),self.open_shop())).pack(pady=8)
                return
            COLS=3
            for i,item in enumerate(pool):
                r,c=divmod(i,COLS)
                issel=item['id']==state['sel']
                cbg=SEL if issel else LIGHT
                fr=tk.Frame(gf,bg=cbg,bd=2,relief='ridge' if issel else 'flat',cursor='hand2')
                fr.grid(row=r,column=c,padx=5,pady=5)
                fp=_os2.path.join(FOOD_DIR,item.get('file',''))
                img=_img_cache(fp,64) if _os2.path.exists(fp) else None
                if img: il=tk.Label(fr,image=img,bg=cbg); il.pack(); il._img=img
                tk.Label(fr,text=item['name'],font=('PingFang SC',10,'bold'),bg=cbg,fg=TEXT).pack()
                tk.Label(fr,text=f'×{self.bag.get(item["id"],0)}',font=('PingFang SC',10,'bold'),bg=cbg,fg='#3a7a30').pack()
                def _sel(it=item): state['sel']=it['id']; refresh_grid(); show_bath_detail(it)
                for w in fr.winfo_children(): w.bind('<Button-1>',lambda e,it=item:_sel(it))
                fr.bind('<Button-1>',lambda e,it=item:_sel(it))

        # ==== 特产&明信片 Tab ====
        SOUVENIR_SELL_PRICE = 20
        POSTCARD_SELL_PRICE = 20
        FISH_SELL_PRICES = {'common': 5, 'rare': 20, 'epic': 50, 'treasure': 80}

        # ==== 药品 Tab ====
        def show_med_detail(item):
            img = _img_cache(item.get('file',''), 64)
            if img: di.config(image=img); di._img=img
            dn.config(text=item['name']); dd.config(text=item['desc'])
            fx=[]
            if item.get('health',0)>0:  fx.append(f'健康+{item["health"]}')
            if item.get('mood',0)>0:    fx.append(f'心情+{item["mood"]}')
            if item.get('cure'): fx.append('消除病态')
            de.config(text='  '.join(fx))
            cnt = self.bag.get(item['id'],0)
            dct.config(text=f'剩余 ×{cnt}')
            def do_use_med(it=item):
                c = self.bag.get(it['id'],0)
                if c<=0: ml.config(text='没有药了!'); return
                if not self.sick and self.health>=90:
                    ml.config(text='身体很好~不用吃药'); return
                self.bag[it['id']]=c-1
                self.health=min(100,self.health+it.get('health',25))
                if it.get('cure') and self.health>=75: self.sick=False
                self.mood=min(100,self.mood+it.get('mood',0))
                self._save()
                self._revive()  # 吃药可以从昏厥中复活
                import random as _r
                self.say(_r.choice([f'💊 吃了{it["name"]},好多了~',f'苦苦的...{it["name"]}真难吃',f'健康回来啦!谢谢主人🥰']),100)
                ml.config(text=f'✅ 已使用!剩余×{self.bag[it["id"]]}')
                dct.config(text=f'剩余 ×{self.bag[it["id"]]}')
                b1.config(state='normal' if self.bag[it['id']]>0 else 'disabled',
                          bg=BTN_OK if self.bag[it['id']]>0 else BTN_DIS)
                refresh_grid()
            b1.config(text='💊 吃药', bg=BTN_OK if cnt>0 else BTN_DIS,
                      state='normal' if cnt>0 else 'disabled', command=do_use_med)
            b2.config(text='', state='disabled', bg='#888')
            b3.config(text='', state='disabled', bg='#888')

        def _render_medicine_grid():
            pool=[it for it in SHOP_ITEMS if it.get('cat')=='medicine' and self.bag.get(it['id'],0)>0]
            if not pool:
                tk.Label(gf,text='药品已用完~\n定价超贵,读书人流泪😭',
                         font=('PingFang SC',12),bg=LIGHT,fg='#aaaaaa',justify='center').pack(pady=40)
                tk.Button(gf,text='🛒 去小卖部购买',font=('PingFang SC',11),
                          bg='#c83a3a',fg='white',relief='flat',cursor='hand2',
                          command=lambda:(win.destroy(),self.open_shop())).pack(pady=8)
                return
            COLS=2
            for i,item in enumerate(pool):
                r,c=divmod(i,COLS)
                issel=item['id']==state['sel']
                cbg=SEL if issel else LIGHT
                fr=tk.Frame(gf,bg=cbg,bd=2,relief='ridge' if issel else 'flat',cursor='hand2')
                fr.grid(row=r,column=c,padx=8,pady=8)
                img=_img_cache(item.get('file',''),64)
                if img: il=tk.Label(fr,image=img,bg=cbg); il.pack(); il._img=img
                else: tk.Label(fr,text='💊',font=('PingFang SC',28),bg=cbg).pack()
                tk.Label(fr,text=item['name'],font=('PingFang SC',10,'bold'),bg=cbg,fg=TEXT).pack()
                tk.Label(fr,text=f'×{self.bag.get(item["id"],0)}',font=('PingFang SC',10,'bold'),bg=cbg,fg='#3a7a30').pack()
                def _sel(it=item): state['sel']=it['id']; refresh_grid(); show_med_detail(it)
                for w in fr.winfo_children(): w.bind('<Button-1>',lambda e,it=item:_sel(it))
                fr.bind('<Button-1>',lambda e,it=item:_sel(it))

        def _render_fish_grid():
            """鱼篓Tab：fish_{prefix} 格式"""
            from PIL import Image as _PI, ImageTk as _IT
            fish_items = {}
            for k, v in self.bag.items():
                if k.startswith('fish_') and v > 0:
                    fish_items[k] = v
            if not fish_items:
                tk.Label(gf, text='鱼篓空空～\n去右键「钓鱼」抛竿吧！',
                         font=('PingFang SC',12), bg=LIGHT, fg='#aaaaaa', justify='center').pack(pady=40)
                return

            fish_info = {f'fish_{ft[1]}': ft for ft in FISH_TYPES if ft[1]}
            fish_info['fish_treasure'] = ('神秘宝箱', None, 'treasure', 100, 50, '稀世珍宝!')

            rarity_colors = {'common':'#4a7a4a','rare':'#4a4a9a','epic':'#7a2a9a','treasure':'#9a7a00'}
            rarity_names  = {'common':'普通','rare':'稀有','epic':'史诗','treasure':'传说'}

            _fimgs = {}
            def get_fimg(prefix, sz=60):
                if prefix in _fimgs: return _fimgs[prefix]
                p = os.path.join(FISH_DIR, f'{prefix}.png')
                if os.path.exists(p):
                    try:
                        t = _IT.PhotoImage(_PI.open(p).convert('RGBA').resize((sz,sz),_PI.LANCZOS))
                        _fimgs[prefix] = t; return t
                    except: pass
                return None

            for bk, cnt in sorted(fish_items.items()):
                prefix = bk[5:]  # 去掉 'fish_'
                info = fish_info.get(bk, ('未知鱼', None, 'common', 0, 0, ''))
                fname, fprefix, rarity, sv, ev, desc = info
                bg_c = rarity_colors.get(rarity, '#4a4a4a')
                sell_price = FISH_SELL_PRICES.get(rarity, 5)

                fr = tk.Frame(gf, bg=LIGHT, bd=2, relief='groove')
                fr.pack(fill='x', padx=6, pady=4)

                # 左侧图片+颜色块
                lf = tk.Frame(fr, bg=bg_c, width=100); lf.pack(side='left', fill='y'); lf.pack_propagate(False)
                img_tk = get_fimg(fprefix) if fprefix else None
                if img_tk:
                    il = tk.Label(lf, image=img_tk, bg=bg_c); il.image = img_tk; il.pack(pady=(6,0))
                else:
                    tk.Label(lf, text='📦', font=('Apple Color Emoji',28), bg=bg_c).pack(pady=(10,0))
                tk.Label(lf, text=f'×{cnt}', font=('PingFang SC',12,'bold'), bg=bg_c, fg='#ccffcc').pack(pady=(2,2))
                sell_st = 'normal' if cnt > 0 else 'disabled'
                sell_bg = '#aa3333' if cnt > 0 else '#888'
                def do_sell_f(bk=bk, sp=sell_price, fn=fname):
                    if self.bag.get(bk, 0) <= 0: return
                    self.bag[bk] -= 1
                    if self.bag[bk] == 0: del self.bag[bk]
                    self.score += sp; self._save()
                    self.say(f'💰 出售{fn}+⭐{sp}！', 60)
                    refresh_grid()
                tk.Button(lf, text=f'售 ⭐{sell_price}', font=('PingFang SC',9),
                          bg=sell_bg, fg='white', relief='flat',
                          state=sell_st, cursor='hand2',
                          command=do_sell_f).pack(padx=6, pady=(0,8), fill='x')

                # 右侧信息
                rf = tk.Frame(fr, bg='#f0f8ff'); rf.pack(side='left', fill='both', expand=True, padx=8, pady=8)
                rlbl = rarity_names.get(rarity,'普通')
                tk.Label(rf, text=f'[{rlbl}]', font=('PingFang SC',10), bg='#f0f8ff',
                         fg=bg_c).pack(anchor='w')
                tk.Label(rf, text=fname, font=('PingFang SC',14,'bold'), bg='#f0f8ff',
                         fg='#1a3a5c').pack(anchor='w')
                tk.Label(rf, text=desc, font=('PingFang SC',10), bg='#f0f8ff',
                         fg='#445566', wraplength=200).pack(anchor='w', pady=(2,0))
                tk.Label(rf, text=f'价值 ⭐{sv}  经验 +{ev}', font=('PingFang SC',9),
                         bg='#f0f8ff', fg='#888888').pack(anchor='w', pady=(4,0))

        def _render_souvenir_grid():
            """特产Tab：souvenir_{省}_{idx} 格式"""
            items = {}
            for k, v in self.bag.items():
                if k.startswith('souvenir_') and v > 0:
                    parts = k.split('_', 2)
                    if len(parts) == 3:
                        dest, idx = parts[1], int(parts[2])
                        souv_list = PROV_SOUVENIRS.get(dest, DEFAULT_SOUVENIR_LIST)
                        if idx < len(souv_list):
                            sname, sdesc = souv_list[idx]
                            items[k] = (dest, sname, sdesc, v)
            if not items:
                tk.Label(gf,text='还没有特产～\n去旅行地图出发吧！',
                         font=('PingFang SC',12),bg=LIGHT,fg='#aaaaaa',justify='center').pack(pady=40)
                return
            from PIL import Image as _PI, ImageTk as _IT
            import random as _rs
            colors = ['#c8102e','#2e6bb0','#2e8b57','#8b4513','#6b2fa0','#c8680e']
            for k,(dest,sname,sdesc,cnt) in sorted(items.items()):
                bg_c = colors[hash(dest)%len(colors)]
                fr = tk.Frame(gf, bg=LIGHT, bd=2, relief='groove')
                fr.pack(fill='x', padx=6, pady=4)
                # 左色块（含特产图片）
                lf = tk.Frame(fr, bg=bg_c, width=110); lf.pack(side='left', fill='y'); lf.pack_propagate(False)
                # 特产图片
                img_path = os.path.join(SOUVENIR_DIR, f'{dest}.png')
                if os.path.exists(img_path):
                    try:
                        pil_img = _PI.open(img_path).convert('RGBA').resize((64, 64), _PI.LANCZOS)
                        tk_img = _IT.PhotoImage(pil_img)
                        il = tk.Label(lf, image=tk_img, bg=bg_c)
                        il.image = tk_img
                        il.pack(pady=(6,0))
                    except Exception:
                        tk.Label(lf, text=dest, font=('PingFang SC',13,'bold'), bg=bg_c, fg='white').pack(pady=(8,2))
                else:
                    tk.Label(lf, text=dest, font=('PingFang SC',13,'bold'), bg=bg_c, fg='white').pack(pady=(8,2))
                cnt_lbl = tk.Label(lf, text=f'×{cnt}', font=('PingFang SC',12,'bold'), bg=bg_c, fg='#ccffcc')
                cnt_lbl.pack(pady=(0,4))
                sell_state = 'normal' if cnt > 1 else 'disabled'
                sell_bg_c = '#aa3333' if cnt > 1 else '#888'
                def do_sell_s(bk=k, bl=cnt_lbl):
                    if self.bag.get(bk,0) <= 1: return
                    self.bag[bk] -= 1; self.score += SOUVENIR_SELL_PRICE; self._save()
                    self.say(f'💰 出售特产+⭐{SOUVENIR_SELL_PRICE}！', 60)
                    refresh_grid()
                tk.Button(lf, text=f'售 ⭐{SOUVENIR_SELL_PRICE}', font=('PingFang SC',9),
                          bg=sell_bg_c, fg='white', relief='flat', cursor='hand2' if cnt>1 else 'arrow',
                          state=sell_state, command=do_sell_s).pack(padx=6, pady=(0,8), fill='x')
                # 右侧内容
                rf = tk.Frame(fr, bg='#fff8ee'); rf.pack(side='left', fill='both', expand=True, padx=8, pady=8)
                tk.Label(rf, text=dest, font=('PingFang SC',11,'bold'), bg='#fff8ee', fg='#888866').pack(anchor='w')
                tk.Label(rf, text=sname, font=('PingFang SC',13,'bold'), bg='#fff8ee', fg='#3a1a00').pack(anchor='w')
                tk.Label(rf, text=sdesc, font=('PingFang SC',10), bg='#fff8ee', fg='#666655', wraplength=200).pack(anchor='w', pady=(2,0))

        def _render_postcard_grid():
            """明信片Tab：postcard_{省}_{idx} 格式"""
            items = {}
            for k, v in self.bag.items():
                if k.startswith('postcard_') and v > 0:
                    parts = k.split('_', 2)
                    if len(parts) == 3:
                        dest, idx = parts[1], int(parts[2])
                        card_list = PROV_POSTCARDS.get(dest, DEFAULT_POSTCARD_LIST)
                        if idx < len(card_list):
                            cname, cdesc = card_list[idx]
                            items[k] = (dest, cname, cdesc, v)
            if not items:
                tk.Label(gf,text='还没有明信片～\n旅行回来会带一张哦！',
                         font=('PingFang SC',12),bg=LIGHT,fg='#aaaaaa',justify='center').pack(pady=40)
                return
            from PIL import Image as _PI, ImageTk as _IT
            colors = ['#1a5c8b','#2e8b57','#6b2fa0','#8b4513','#c8102e','#c8680e']
            for k,(dest,cname,cdesc,cnt) in sorted(items.items()):
                bg_c = colors[hash(dest+cname)%len(colors)]
                fr = tk.Frame(gf, bg='#fffef0', bd=2, relief='groove')
                fr.pack(fill='x', padx=6, pady=4)
                # 明信片图片左列
                lf = tk.Frame(fr, bg='#fffef0', width=110); lf.pack(side='left', fill='y'); lf.pack_propagate(False)
                img_path = os.path.join(POSTCARD_DIR, f'{dest}.png')
                if os.path.exists(img_path):
                    try:
                        pil_img = _PI.open(img_path).convert('RGBA').resize((100, 70), _PI.LANCZOS)
                        tk_img = _IT.PhotoImage(pil_img)
                        il = tk.Label(lf, image=tk_img, bg='#fffef0')
                        il.image = tk_img
                        il.pack(pady=(6,2), padx=4)
                    except Exception:
                        tk.Label(lf, text='📮', font=('PingFang SC',20), bg=bg_c).pack(pady=(8,0))
                        tk.Label(lf, text=dest, font=('PingFang SC',11,'bold'), bg=bg_c, fg='white').pack()
                else:
                    tk.Label(lf, text='📮', font=('PingFang SC',20), bg=bg_c).pack(pady=(8,0))
                    tk.Label(lf, text=dest, font=('PingFang SC',11,'bold'), bg=bg_c, fg='white').pack()
                cnt_lbl2 = tk.Label(lf, text=f'×{cnt}', font=('PingFang SC',11,'bold'), bg='#fffef0', fg='#445566')
                cnt_lbl2.pack(pady=(0,4))
                sell_state2 = 'normal' if cnt > 1 else 'disabled'
                sell_bg2 = '#aa3333' if cnt > 1 else '#888'
                def do_sell_p(bk=k):
                    if self.bag.get(bk,0) <= 1: return
                    self.bag[bk] -= 1; self.score += POSTCARD_SELL_PRICE; self._save()
                    self.say(f'💰 出售明信片+⭐{POSTCARD_SELL_PRICE}！', 60)
                    refresh_grid()
                tk.Button(lf, text=f'售 ⭐{POSTCARD_SELL_PRICE}', font=('PingFang SC',9),
                          bg=sell_bg2, fg='white', relief='flat', cursor='hand2' if cnt>1 else 'arrow',
                          state=sell_state2, command=do_sell_p).pack(padx=4, pady=(0,6), fill='x')
                # 右侧
                rf = tk.Frame(fr, bg='#fffef0'); rf.pack(side='left', fill='both', expand=True, padx=8, pady=8)
                tk.Label(rf, text=f'📮 {dest}', font=('PingFang SC',11,'bold'), bg='#fffef0', fg='#445566').pack(anchor='w')
                tk.Label(rf, text=cname, font=('PingFang SC',13,'bold'), bg='#fffef0', fg='#1a3a5c').pack(anchor='w')
                tk.Label(rf, text=cdesc, font=('PingFang SC',10), bg='#fffef0', fg='#445566', wraplength=200).pack(anchor='w', pady=(2,0))

        def _render_souvenir_grid_refresh():
            for w in gf.winfo_children(): w.destroy()
            _render_souvenir_grid()
            gf.update_idletasks(); gcv.configure(scrollregion=gcv.bbox('all'))

        t_food.config(command=lambda:switch_tab('food'))
        t_bath.config(command=lambda:switch_tab('bath'))
        t_med.config(command=lambda:switch_tab('medicine'))
        t_fish.config(command=lambda:switch_tab('fish'))
        t_souvenir.config(command=lambda:switch_tab('souvenir'))
        t_postcard.config(command=lambda:switch_tab('postcard'))
        t_furn.config(command=lambda:switch_tab('furn'))

        switch_tab(start_tab)
        win.focus_force()


    # ── 家具店系统 ──────────────────────────────────────────────────
    def open_furniture_shop(self):
        """家具店 -- 购买家具,在家园中摆放"""
        if hasattr(self,'_fshop_win') and self._fshop_win and self._fshop_win.winfo_exists():
            self._fshop_win.lift(); return
        from PIL import Image as _PI, ImageTk as _IT
        import os as _os3

        FURN_DIR  = _os3.path.join(_os3.path.dirname(_os3.path.abspath(__file__)), 'assets', 'furniture')
        PREV_DIR  = _os3.path.join(_os3.path.dirname(_os3.path.abspath(__file__)), 'assets', 'furniture_preview')

        # 家具数据 -- preview: 合成预览图文件名(已含暖色背景),用于商店展示
        # 床/沙发/书架/钢琴使用合成图(多块拼合),其余直接用原图
        # FURNITURE_ITEMS 定义在模块顶层
        win = tk.Toplevel(self.root)
        win.title('🛋️ 家具店')
        win.geometry('760x560+120+50')
        win.resizable(False, False)
        win.attributes('-topmost', True)
        win.lift(); win.focus_force()
        win.configure(bg='#f0ede0')
        self._fshop_win = win

        BG='#f0ede0'; PANEL='#e8d8a0'; DARK='#4a3010'; LIGHT='#fffbee'
        SEL='#ffe066'; BTN_BUY='#7a4a10'; BTN_USE='#3a7a30'; BTN_DIS='#aaaaaa'; TEXT='#3a2000'
        MID='#c8883a'

        state = {'cat':'all', 'sel':None, 'imgs':{}}

        def load_prev(item, size=None):
            """加载预览图(含暖色背景,已合成);size=None 表示原始尺寸"""
            pname = item.get('preview', '')
            fp = _os3.path.join(PREV_DIR, pname) if pname else None
            if not fp or not _os3.path.exists(fp):
                # fallback: 原始文件加背景
                fp2 = _os3.path.join(FURN_DIR, item['file'])
                try:
                    raw = _PI.open(fp2).convert('RGBA')
                    bg  = _PI.new('RGBA', raw.size, (245, 238, 210, 255))
                    bg.paste(raw, mask=raw.split()[3])
                    img = bg.convert('RGB')
                except: return None
            else:
                try:
                    img = _PI.open(fp).convert('RGB')
                except: return None
            if size:
                # 保持长宽比缩放到 size×size 正方形内,居中
                ow, oh = img.size
                scale = min(size/ow, size/oh)
                nw, nh = max(1,int(ow*scale)), max(1,int(oh*scale))
                img = img.resize((nw, nh), _PI.NEAREST)
                canvas = _PI.new('RGB', (size, size), (245, 238, 210))
                canvas.paste(img, ((size-nw)//2, (size-nh)//2))
                img = canvas
            k = (item['id'], size)
            p = _IT.PhotoImage(img)
            state['imgs'][k] = p
            return p

        # 顶部
        top = tk.Frame(win, bg=MID, height=44); top.pack(fill='x'); top.pack_propagate(False)
        tk.Label(top, text='🛋️  家具店', font=('PingFang SC',14,'bold'), bg=MID, fg='#fff5dc').pack(side='left', padx=16)
        score_lbl = tk.Label(top, text=f'⭐ {self.score}', font=('PingFang SC',11), bg=MID, fg='#fff5dc')
        score_lbl.pack(side='right', padx=16)

        # 分类 tab
        cats = [('all','🏠 全部'),('kitchen','🍳 厨房'),('living','🛋️ 客厅'),
                ('bedroom','🛏️ 卧室'),('bath','🚿 浴室'),('entertain','🎹 娱乐'),
                ('study','📚 书房'),('deco','🌿 装饰'),('pet','🐾 宠物')]
        cf = tk.Frame(win, bg='#e0c870', height=30); cf.pack(fill='x'); cf.pack_propagate(False)
        cbtns = {}
        def sw_cat(c):
            state['cat'] = c; state['sel'] = None
            for k,b in cbtns.items(): b.config(bg=SEL if k==c else '#e0c870')
            refresh()
        for cid, cl in cats:
            b = tk.Button(cf, text=cl, font=('PingFang SC',9), bg=SEL if cid=='all' else '#e0c870',
                          fg=TEXT, relief='flat', bd=0, padx=8, pady=3, command=lambda c=cid: sw_cat(c))
            b.pack(side='left'); cbtns[cid] = b

        # 左右分栏
        lp = tk.Frame(win, bg='#f0ede0', width=520); lp.pack(side='left', fill='y'); lp.pack_propagate(False)
        rp = tk.Frame(win, bg=PANEL, width=240); rp.pack(side='right', fill='both', expand=True)

        # 可滚动网格
        gc = tk.Frame(lp, bg=LIGHT); gc.pack(fill='both', expand=True, padx=2, pady=2)
        gcv = tk.Canvas(gc, bg=LIGHT, highlightthickness=0)
        gsb = tk.Scrollbar(gc, orient='vertical', command=gcv.yview)
        gcv.configure(yscrollcommand=gsb.set)
        gsb.pack(side='right', fill='y'); gcv.pack(side='left', fill='both', expand=True)
        gf = tk.Frame(gcv, bg=LIGHT); gcv.create_window((0,0), window=gf, anchor='nw')
        def _on_scroll(e): gcv.yview_scroll(int(-1*(e.delta/120)), 'units')
        def _bind_scroll(w):
            w.bind('<MouseWheel>', _on_scroll)
            for ch in w.winfo_children(): _bind_scroll(ch)
        gcv.bind('<MouseWheel>', _on_scroll)

        # 右侧详情
        di = tk.Label(rp, bg=PANEL); di.pack(pady=(16,4))
        dn = tk.Label(rp, text='', font=('PingFang SC',13,'bold'), bg=PANEL, fg=DARK); dn.pack()
        dd = tk.Label(rp, text='', font=('PingFang SC',10), bg=PANEL, fg=TEXT, wraplength=200); dd.pack(pady=4)
        dp = tk.Label(rp, text='', font=('PingFang SC',11,'bold'), bg=PANEL, fg=BTN_BUY); dp.pack(pady=4)
        dlv= tk.Label(rp, text='', font=('PingFang SC',9), bg=PANEL, fg='#886644'); dlv.pack()
        dct= tk.Label(rp, text='', font=('PingFang SC',10), bg=PANEL, fg=DARK); dct.pack(pady=2)
        dmood = tk.Label(rp, text='', font=('PingFang SC',9), bg=PANEL, fg='#3a7a30'); dmood.pack(pady=2)
        b_buy = tk.Button(rp, text='💰 购买', font=('PingFang SC',12,'bold'), bg=BTN_BUY, fg='white',
                          relief='flat', bd=0, padx=20, pady=6, state='disabled', cursor='hand2'); b_buy.pack(pady=(8,4))
        b_place = tk.Button(rp, text='🏠 前往摆放', font=('PingFang SC',11,'bold'), bg='#3a7a30', fg='white',
                            relief='flat', bd=0, padx=16, pady=5, state='disabled', cursor='hand2'); b_place.pack()
        ml = tk.Label(rp, text='', font=('PingFang SC',9), bg=PANEL, fg='#cc3300', wraplength=210); ml.pack(pady=4)

        def upd_detail(item):
            img = load_prev(item, 96)
            if img: di.config(image=img); di._img = img
            dn.config(text=item['name'])
            dd.config(text=item['desc'])
            locked = item['lv'] > self.level
            cnt = self.furniture_bag.get(item['id'], 0)
            placed = sum(1 for p in self.placed_furniture if p['id']==item['id'])
            dp.config(text=f"⭐ {item['price']} 积分")
            dlv.config(text=f"需要等级 Lv.{item['lv']}" + (' 🔒' if locked else ' ✅'))
            dct.config(text=f'背包: ×{cnt}  已摆: ×{placed}')
            dmood.config(text=f"💛 摆放后心情+{item['mood']}")
            if locked: b_buy.config(state='disabled', bg=BTN_DIS, text='🔒 等级不足')
            elif self.score < item['price']: b_buy.config(state='disabled', bg=BTN_DIS, text='💰 积分不足')
            else: b_buy.config(state='normal', bg=BTN_BUY, text='💰 购买',
                               command=lambda it=item: do_buy(it))
            b_place.config(state='normal' if cnt>0 else 'disabled',
                           bg='#3a7a30' if cnt>0 else BTN_DIS,
                           command=lambda it=item: do_place(it))

        def do_buy(item):
            if self.score < item['price']: ml.config(text='积分不足!'); return
            if item['lv'] > self.level: ml.config(text=f"需要 Lv.{item['lv']}!"); return
            self.score -= item['price']
            self.furniture_bag[item['id']] = self.furniture_bag.get(item['id'],0) + 1
            self.furniture_buy_count += 1
            self._save()
            self.say(f"买到{item['name']}了!🛋️", 70)
            ml.config(text=f"✅ 购买成功!背包 ×{self.furniture_bag[item['id']]}")
            score_lbl.config(text=f'⭐ {self.score}')
            if self.furniture_buy_count >= 5:  self.unlock('furniture5')
            if self.furniture_buy_count >= 15: self.unlock('furniture15')
            refresh()

        def do_place(item):
            cnt = self.furniture_bag.get(item['id'], 0)
            if cnt <= 0: ml.config(text='背包里没有!'); return
            ml.config(text=f"🏠 打开家园,点击要放置的位置来摆放{item['name']}")
            self._pending_place = item
            win.destroy()
            self.open_garden()

        def refresh():
            for w in gf.winfo_children(): w.destroy()
            pool = [it for it in FURNITURE_ITEMS if state['cat']=='all' or it['cat']==state['cat']]
            COLS = 4
            THUMB = 80  # 格子缩略图尺寸
            for i, item in enumerate(pool):
                r, c = i//COLS, i%COLS
                issel = item['id'] == state['sel']
                cnt = self.furniture_bag.get(item['id'], 0)
                locked = item['lv'] > self.level
                cell_bg = SEL if issel else ('#e8e0d0' if locked else LIGHT)
                fr = tk.Frame(gf, bg=cell_bg, bd=2,
                              relief='ridge' if issel else 'flat', cursor='hand2',
                              width=THUMB+16, height=THUMB+38)
                fr.grid(row=r, column=c, padx=4, pady=5)
                fr.pack_propagate(False)
                img = load_prev(item, THUMB)
                if img:
                    il = tk.Label(fr, image=img, bg=cell_bg, bd=0); il.pack(pady=(4,1)); il._img = img
                name_lbl = tk.Label(fr, text=item['name'], font=('PingFang SC',9,'bold'),
                         bg=cell_bg, fg='#888888' if locked else TEXT)
                name_lbl.pack()
                price_text = f'🔒Lv{item["lv"]}' if locked else f'⭐{item["price"]}'
                price_fg   = '#aaaaaa' if locked else BTN_BUY
                tk.Label(fr, text=price_text, font=('PingFang SC',8),
                         bg=cell_bg, fg=price_fg).pack()
                if cnt > 0 and not locked:
                    tk.Label(fr, text=f'已拥有×{cnt}', font=('PingFang SC',8,'bold'),
                             bg=cell_bg, fg='#3a7a30').pack()
                def on_click(it=item):
                    state['sel'] = it['id']; refresh(); upd_detail(it)
                for w in fr.winfo_children(): w.bind('<Button-1>', lambda e,it=item: on_click(it))
                fr.bind('<Button-1>', lambda e,it=item: on_click(it))
            gf.update_idletasks(); gcv.configure(scrollregion=gcv.bbox('all'))
            _bind_scroll(gf)
            ml.config(text=''); score_lbl.config(text=f'⭐ {self.score}')
            if state['sel']:
                it = next((x for x in FURNITURE_ITEMS if x['id']==state['sel']), None)
                if it: upd_detail(it)

        refresh(); win.focus_force()

        refresh(); win.focus_force()


    # ── 旅行地图系统 ─────────────────────────────────────────────
    def open_travel(self):
        """旅行地图窗口 -- 真实 GeoJSON 中国地图"""
        if hasattr(self,'_travel_win') and self._travel_win and self._travel_win.winfo_exists():
            self._travel_win.lift(); return
        import time as _t, json as _json, os as _os2

        # ── 加载 GeoJSON ──────────────────────────────────────────
        _geo_path = _os2.path.join(_os2.path.dirname(_os2.path.abspath(__file__)), 'china_provinces.json')
        with open(_geo_path, encoding='utf-8') as _f:
            _geo = _json.load(_f)

        # 名称映射(去掉"省/市/自治区/特别行政区"等后缀)
        def _short(name):
            for s in ('特别行政区','壮族自治区','回族自治区','维吾尔自治区','自治区','省','市'):
                name = name.replace(s,'')
            return name

        # Canvas 尺寸
        CW, CH = 720, 510
        # 经纬度范围(墨卡托投影近似)
        LON_MIN, LON_MAX = 72.0, 136.0
        LAT_MIN, LAT_MAX = 3.0,  54.0

        def geo2px(lon, lat):
            x = (lon - LON_MIN) / (LON_MAX - LON_MIN) * CW
            # 纬度翻转(屏幕Y轴向下)
            y = (1 - (lat - LAT_MIN) / (LAT_MAX - LAT_MIN)) * CH
            return x, y

        # 简化多边形点(每 step 个点取1个,减少渲染压力)
        def simplify(ring, step=3):
            return ring[::step] + [ring[-1]]

        # 构建省份数据:name_short -> {feat, polygons(canvas coords), center}
        PROV_DATA = {}
        for feat in _geo['features']:
            raw_name = feat['properties'].get('name','')
            if not raw_name: continue
            short = _short(raw_name)
            geom = feat['geometry']
            polys = []  # list of flat coord lists for create_polygon
            cx_sum, cy_sum, cnt = 0.0, 0.0, 0

            def add_ring(ring):
                nonlocal cx_sum, cy_sum, cnt
                pts = simplify(ring, step=4)
                flat = []
                for lon, lat in pts:
                    px, py = geo2px(lon, lat)
                    flat.extend([px, py])
                    cx_sum += px; cy_sum += py; cnt += 1
                if len(flat) >= 6:
                    polys.append(flat)

            if geom['type'] == 'Polygon':
                add_ring(geom['coordinates'][0])
            elif geom['type'] == 'MultiPolygon':
                # 只取面积最大的多边形(点数最多的 ring)
                all_rings = [poly[0] for poly in geom['coordinates'] if poly]
                # 按点数排序,取最大的(主体轮廓)
                main_rings = sorted(all_rings, key=len, reverse=True)[:3]
                for ring in main_rings:
                    add_ring(ring)

            if polys and cnt > 0:
                PROV_DATA[short] = {
                    'polys': polys,
                    'cx': cx_sum / cnt,
                    'cy': cy_sum / cnt,
                }

        TRAVEL_COST = 200; TRAVEL_SEC = 600

        win = tk.Toplevel(self.root)
        win.title('🗺️ 中国旅行地图')
        win.geometry('720x600+60+40')
        win.resizable(False, False)
        win.attributes('-topmost', True)
        win.lift(); win.focus_force()
        win.configure(bg='#eef4fb')
        self._travel_win = win

        BG='#eef4fb'; PANEL='#d0e8f8'; DARK='#1a3a5c'
        C_VISITED='#e05030'; C_UNVISIT='#d8e8f0'; C_HOVER='#ffaa44'; C_SEA='#c0d8ee'
        C_BORDER='#8aaabf'; C_TEXT_V='#ffffff'; C_TEXT_U='#2a4a6a'

        tip_var = tk.StringVar()
        tip_bar = tk.Frame(win, bg=PANEL, height=36); tip_bar.pack(fill='x'); tip_bar.pack_propagate(False)
        tk.Label(tip_bar, textvariable=tip_var, font=('PingFang SC',11), bg=PANEL, fg=DARK).pack(side='left', padx=14)

        cv = tk.Canvas(win, width=CW, height=CH, bg=C_SEA, highlightthickness=0)
        cv.pack()

        bot = tk.Frame(win, bg=BG, height=52); bot.pack(fill='x'); bot.pack_propagate(False)
        status_var = tk.StringVar(value='点击省份查看,点「去旅行」随机出发')
        btn_go = tk.Button(bot, text='✈️ 去旅行', font=('PingFang SC',12,'bold'),
                           bg='#e85520', fg='white', relief='flat', bd=0, padx=18, pady=6, cursor='hand2')
        btn_go.pack(side='left', padx=12, pady=8)
        tk.Label(bot, textvariable=status_var, font=('PingFang SC',10), bg=BG, fg=DARK,
                 wraplength=520, anchor='w').pack(side='left', padx=8)

        hover = [None]; sel = [None]
        # 记录每个省份的 canvas item ids,用于 hit-test
        _prov_items = {}  # short_name -> [item_id, ...]

        def draw_map():
            cv.delete('all')
            n_vis = len(self.travel_visited); n_tot = len(PROV_DATA)
            tip_var.set(f'每次旅行消耗 {TRAVEL_COST} 积分,约{TRAVEL_SEC}秒到达 ── 已点亮 {n_vis} / {n_tot} 个省市')
            _prov_items.clear()

            for name, pd in PROV_DATA.items():
                visited   = name in self.travel_visited
                is_hover  = name == hover[0]
                is_sel    = name == sel[0]
                traveling = self.travel_state['active'] and self.travel_state['dest'] == name

                if traveling:   fill = '#ffcc00'
                elif is_sel:    fill = '#ff6622'
                elif is_hover:  fill = C_HOVER
                elif visited:   fill = C_VISITED
                else:           fill = C_UNVISIT

                border = '#ff4400' if (is_sel or traveling) else ('#cc3300' if visited else C_BORDER)
                width  = 2 if (is_sel or is_hover or traveling) else 1

                ids = []
                for flat in pd['polys']:
                    iid = cv.create_polygon(flat, fill=fill, outline=border, width=width)
                    ids.append(iid)
                _prov_items[name] = ids

                # 文字标签
                cx, cy = pd['cx'], pd['cy']
                txt_col = C_TEXT_V if visited else C_TEXT_U
                short2 = name.replace('黑龙江','黑龙\n江').replace('内蒙古','内蒙\n古')
                fsize  = 7 if name in ('上海','天津','北京','澳门','香港','宁夏') else 9
                cv.create_text(cx, cy, text=short2, font=('PingFang SC',fsize,'bold'),
                               fill=txt_col, justify='center')

        def hit_province(ex, ey):
            # 先用 canvas find_closest 找近邻多边形,再精确匹配
            items = cv.find_overlapping(ex-2, ey-2, ex+2, ey+2)
            for iid in items:
                for name, ids in _prov_items.items():
                    if iid in ids: return name
            return None

        def on_move(e):
            found = hit_province(e.x, e.y)
            if found != hover[0]: hover[0] = found; draw_map()

        def on_click(e):
            name = hit_province(e.x, e.y)
            if name:
                sel[0] = name
                visited   = name in self.travel_visited
                traveling = self.travel_state['active'] and self.travel_state['dest'] == name
                if traveling:
                    rem = int(self.travel_state['end_ts'] - _t.time())
                    status_var.set(f'🚕 在去{name}的路上,还有 {max(0,rem)} 秒到达...')
                elif visited: status_var.set(f'✅ {name} - 已打卡!点「去旅行」再去一次')
                else: status_var.set(f'📍 {name} - 还没去过,点「去旅行」出发!')
                draw_map()

        def do_travel():
            if self.travel_state['active']:
                rem = int(self.travel_state['end_ts'] - _t.time())
                if rem > 0: status_var.set(f'🚕 已在路中!去 {self.travel_state["dest"]},还有 {rem} 秒...'); return
                else: finish_travel(); return
            if self.score < TRAVEL_COST:
                status_var.set(f'积分不足!需要 {TRAVEL_COST} 积分,当前 {self.score}'); return
            unvisited = [n for n in PROV_DATA if n not in self.travel_visited]
            if not unvisited: unvisited = list(PROV_DATA.keys())
            dest = sel[0] if sel[0] and sel[0] not in self.travel_visited else random.choice(unvisited)
            self.score -= TRAVEL_COST; end_ts = _t.time() + TRAVEL_SEC
            self.travel_state = {'active':True,'dest':dest,'end_ts':end_ts}
            self._save()
            status_var.set(f'✈️ 出发去 {dest}!路上需要 {TRAVEL_SEC} 秒~')
            self.say(f'出发去{dest}啦!我会带特产回来!', 100)
            draw_map()
            win.after(TRAVEL_SEC * 1000, lambda: finish_travel(force=True))

        def finish_travel(force=False):
            if not self.travel_state['active']: return
            dest = self.travel_state['dest']
            self.travel_state = {'active':False,'dest':'','end_ts':0}
            if dest not in self.travel_visited: self.travel_visited.append(dest)
            n = len(self.travel_visited)
            self.add_exp(15); self.add_score(10); self._save()
            if n >= 5:  self.unlock('travel5')
            if n >= 15: self.unlock('travel15')
            if n >= 34: self.unlock('travel35')
            status_var.set(f'🎉 到达 {dest}!已打卡 {n} 个省市!+10积分 +15EXP')
            if force: self.say(f'到{dest}啦!带了特产回来~', 100)
            draw_map()

        btn_go.config(command=do_travel)
        cv.bind('<Motion>', on_move)
        cv.bind('<Button-1>', on_click)

        def check_travel():
            if not win.winfo_exists(): return
            if self.travel_state['active']:
                rem = int(self.travel_state['end_ts'] - _t.time())
                if rem <= 0: finish_travel(force=True)
                else: status_var.set(f'✈️ 在去 {self.travel_state["dest"]} 的路上... 还有 {rem} 秒到达')
            win.after(2000, check_travel)
        check_travel()

        if self.travel_state['active']:
            rem = int(self.travel_state['end_ts'] - _t.time())
            if rem > 0: status_var.set(f'✈️ 已出发去 {self.travel_state["dest"]},还有 {rem} 秒到达')
            else: finish_travel()

        draw_map()
        win.focus_force()


    # ── 钓鱼系统 ──────────────────────────────────────────────────────────────
    def open_fishing(self):
        """钓鱼小游戏主窗口"""
        import random as _rf
        from PIL import Image as _PI, ImageTk as _IT

        if hasattr(self, '_fish_win') and self._fish_win and self._fish_win.winfo_exists():
            self._fish_win.lift(); return

        COST = 30
        W_F, H_F = 420, 500

        win = tk.Toplevel(self.root)
        self._fish_win = win
        win.title('🎣 幸运钓鱼')
        win.geometry(f'{W_F}x{H_F}+200+80')
        win.resizable(False, False)
        win.attributes('-topmost', True)
        win.configure(bg='#1a3a5c')

        tk.Label(win, text='🎣 幸运钓鱼', font=('PingFang SC', 18, 'bold'),
                 bg='#1a3a5c', fg='#ffd700').pack(pady=(14, 2))
        cost_lbl = tk.Label(win, text=f'消耗 ⭐{COST} 积分 | 当前: ⭐{self.score}',
                            font=('PingFang SC', 10), bg='#1a3a5c', fg='#aaccff')
        cost_lbl.pack(pady=(0, 6))

        # 水面场景
        scene_cv = tk.Canvas(win, width=W_F-20, height=180,
                             bg='#1a6090', highlightthickness=1,
                             highlightbackground='#2a7aaa')
        scene_cv.pack(padx=10, pady=4)

        def draw_scene(fish_tk=None, state='idle', fish_name=''):
            scene_cv.delete('all')
            scene_cv.create_rectangle(0, 80, W_F, 180, fill='#0d4a6e', outline='')
            scene_cv.create_rectangle(0, 0, W_F, 80, fill='#1a6090', outline='')
            for i in range(0, W_F, 40):
                scene_cv.create_arc(i, 72, i+40, 88, start=0, extent=180,
                                    fill='#2a7aaa', outline='#3a8abb', width=1)
            for wx in [40, 100, 200, 320, 370]:
                h = _rf.randint(30, 55)
                scene_cv.create_rectangle(wx, 180-h, wx+6, 180, fill='#1a7a3a', outline='')
                scene_cv.create_oval(wx-4, 180-h-10, wx+10, 180-h+6, fill='#2a9a4a', outline='')
            for bx, by in [(60,140),(150,120),(280,150),(360,130)]:
                scene_cv.create_oval(bx, by, bx+6, by+6, fill='', outline='#5599bb', width=1)

            if state == 'waiting':
                scene_cv.create_line(195, 5, 205, 82, fill='#ccaa66', width=2)
                scene_cv.create_oval(201, 78, 209, 86, fill='#ff4444', outline='#cc0000')
                scene_cv.create_text(200, 40, text='• • •', font=('PingFang SC', 12), fill='#aaccff')
            elif state == 'bite':
                scene_cv.create_line(195, 5, 205, 82, fill='#ccaa66', width=2)
                scene_cv.create_oval(201, 78, 209, 86, fill='#ffffff', outline='#cc0000')
                scene_cv.create_text(130, 48, text='!! 上钩了 !!',
                                     font=('PingFang SC', 16, 'bold'), fill='#ffff00')
            elif state == 'catch' and fish_tk:
                scene_cv.create_line(195, 5, 200, 82, fill='#ccaa66', width=2)
                scene_cv.create_image(200, 132, image=fish_tk)
                scene_cv.create_text(200, 170, text=fish_name,
                                     font=('PingFang SC', 12, 'bold'), fill='#ffd700')
            elif state == 'trash':
                scene_cv.create_line(195, 5, 200, 82, fill='#ccaa66', width=2)
                scene_cv.create_text(200, 118, text='👢', font=('Apple Color Emoji', 40))
                scene_cv.create_text(200, 166, text='垃圾...', font=('PingFang SC', 12), fill='#aaaaaa')
            elif state == 'treasure':
                scene_cv.create_line(195, 5, 200, 82, fill='#ccaa66', width=2)
                scene_cv.create_text(200, 118, text='📦', font=('Apple Color Emoji', 40))
                scene_cv.create_text(200, 166, text='神秘宝箱!!', font=('PingFang SC', 13, 'bold'), fill='#ffd700')

        draw_scene(state='idle')

        status_var = tk.StringVar(value='点击「抛竿」开始钓鱼～')
        tk.Label(win, textvariable=status_var, font=('PingFang SC', 12),
                 bg='#1a3a5c', fg='#e0f0ff', wraplength=380).pack(pady=6)

        btn_f = tk.Frame(win, bg='#1a3a5c')
        btn_f.pack(pady=4)
        cast_btn = tk.Button(btn_f, text='🎯 抛竿', font=('PingFang SC', 14, 'bold'),
                             bg='#2a7a4a', fg='white', relief='flat',
                             padx=20, pady=8, cursor='hand2')
        cast_btn.pack(side='left', padx=8)
        pull_btn = tk.Button(btn_f, text='🤯 扬竿!', font=('PingFang SC', 14, 'bold'),
                             bg='#8b0000', fg='white', relief='flat',
                             padx=20, pady=8, cursor='hand2', state='disabled')
        pull_btn.pack(side='left', padx=8)

        tk.Label(win, text='─── 近期战利品 ───', font=('PingFang SC', 10),
                 bg='#1a3a5c', fg='#6688aa').pack(pady=(8, 2))
        catch_cv = tk.Canvas(win, bg='#0d2a42', highlightthickness=0, height=80)
        catch_cv.pack(fill='x', padx=10, pady=(0, 8))

        _imgs = {}
        def get_img(prefix, sz=56):
            if prefix in _imgs: return _imgs[prefix]
            p = os.path.join(FISH_DIR, f'{prefix}.png')
            if os.path.exists(p):
                try:
                    t = _IT.PhotoImage(_PI.open(p).convert('RGBA').resize((sz,sz),_PI.LANCZOS))
                    _imgs[prefix] = t; return t
                except: pass
            return None

        recent = []

        def refresh_bar():
            catch_cv.delete('all')
            if not recent:
                catch_cv.create_text(200, 40, text='还没有战利品～', font=('PingFang SC',10), fill='#446688')
                return
            x = 16
            for nm, img in recent[-5:]:
                if img: catch_cv.create_image(x+28, 38, image=img)
                else: catch_cv.create_text(x+28, 36, text='📦', font=('Apple Color Emoji',26))
                catch_cv.create_text(x+28, 66, text=nm[:4], font=('PingFang SC',9), fill='#aaccff')
                x += 76
        refresh_bar()

        _s = {'phase':'idle', 'aid':None, 'ftk':None, 'biting':False}

        def do_cast():
            if self.score < COST:
                status_var.set(f'积分不足！需要 ⭐{COST}，当前只有 ⭐{self.score}'); return
            self.score -= COST
            cost_lbl.config(text=f'消耗 ⭐{COST} 积分 | 当前: ⭐{self.score}')
            cast_btn.config(state='disabled')
            pull_btn.config(state='disabled', bg='#8b0000')
            _s['phase'] = 'waiting'
            draw_scene(state='waiting')
            status_var.set('🎣 鱼竿已抛出，等待上钩中...')
            _s['aid'] = win.after(_rf.randint(3000, 9000), trigger_bite)

        def trigger_bite():
            _s['phase'] = 'bite'; _s['biting'] = True
            draw_scene(state='bite')
            status_var.set('⚠️ 鱼咬钩了！快点点「扬竿」！！')
            pull_btn.config(state='normal', bg='#cc3300')
            _s['aid'] = win.after(5000, fish_escape)

        def fish_escape():
            if not _s['biting']: return
            _s['biting'] = False; _s['phase'] = 'idle'
            draw_scene(state='idle')
            status_var.set('😢 鱼跑了！下次手快点嗦～')
            pull_btn.config(state='disabled', bg='#8b0000')
            cast_btn.config(state='normal')

        def do_pull():
            if not _s['biting']: return
            if _s['aid']: win.after_cancel(_s['aid'])
            _s['biting'] = False
            pull_btn.config(state='disabled', bg='#8b0000')

            fish = _rf.choices(FISH_TYPES, weights=FISH_WEIGHTS, k=1)[0]
            fname, fprefix, rarity, sv, ev, desc = fish
            self.add_score(sv); self.add_exp(ev)
            cost_lbl.config(text=f'消耗 ⭐{COST} 积分 | 当前: ⭐{self.score}')

            bk = f'fish_{fprefix or "treasure"}'
            self.bag[bk] = self.bag.get(bk, 0) + 1
            self.fish_count += 1
            self._save()
            self.unlock('first_fish')
            if self.fish_count >= 10: self.unlock('fish10')
            if rarity == 'epic': self.unlock('fish_epic')
            if rarity == 'treasure': self.unlock('fish_legend')

            remoji = {'common':'⭐','rare':'💎','epic':'👑','treasure':'🎉'}[rarity]
            if fprefix:
                ftk = get_img(fprefix)
                _s['ftk'] = ftk
                draw_scene(fish_tk=ftk, state='catch', fish_name=fname)
                status_var.set(f'{remoji} 钓到了「{fname}」！+⭐{sv} 分 +{ev} EXP  {desc}')
                recent.append((fname, ftk))
            else:
                draw_scene(state='treasure')
                status_var.set(f'🎉 神秘宝箱！大奖！+⭐{sv} 分 +{ev} EXP')
                recent.append(('宝箱', None))

            self.say(f'🎣 钓到{fname}！+⭐{sv}', 80)
            refresh_bar()
            _s['phase'] = 'idle'
            win.after(2000, lambda: cast_btn.config(state='normal'))

        cast_btn.config(command=do_cast)
        pull_btn.config(command=do_pull)

    # ── 宠物档案 ───────────────────────────────────────────────────
    def open_profile(self):
        """QQ宠物风格宠物档案"""
        if hasattr(self,'_profile_win') and self._profile_win and self._profile_win.winfo_exists():
            self._profile_win.lift(); return
        import time as _t

        win=tk.Toplevel(self.root)
        win.title('🐾 宠物档案')
        win.geometry('360x520+300+80')
        win.resizable(False,False)
        win.attributes('-topmost', True)
        win.lift()
        win.focus_force()
        win.configure(bg='#e8f4f8')
        self._profile_win=win

        BG='#e8f4f8'; CARD='#ffffff'; DARK='#1a3a5c'; MID='#3a8cc8'
        BAR_BG='#cce4f4'; BAR_FG='#3a8cc8'; BAR_H=18
        HUNGER_C='#44aaee'; CLEAN_C='#44ccaa'; HEALTH_C='#ee6644'; MOOD_C='#aa66ee'
        EXP_C='#ffaa22'

        # 卡片框架
        card=tk.Frame(win,bg=CARD,relief='flat',bd=0)
        card.place(x=20,y=20,width=320,height=480)

        # 标题
        title_f=tk.Frame(card,bg='#3a8cc8',height=44); title_f.pack(fill='x'); title_f.pack_propagate(False)
        tk.Label(title_f,text='🐾  宠物档案',font=('PingFang SC',14,'bold'),
                 bg='#3a8cc8',fg='white').pack(side='left',padx=14)
        tk.Button(title_f,text='✕',font=('PingFang SC',12),bg='#3a8cc8',fg='white',
                  relief='flat',bd=0,command=win.destroy).pack(side='right',padx=8)

        body=tk.Frame(card,bg=CARD); body.pack(fill='both',expand=True,padx=16,pady=10)

        def bar(parent, label, val, maxval, color, row):
            """label + 进度条"""
            tk.Label(parent,text=label,font=('PingFang SC',10,'bold'),
                     bg=CARD,fg=DARK,width=4,anchor='e').grid(row=row,column=0,sticky='e',pady=3)
            outer=tk.Frame(parent,bg=BAR_BG,width=210,height=BAR_H)
            outer.grid(row=row,column=1,padx=(6,0),pady=3,sticky='w')
            outer.pack_propagate(False)
            fill_w=max(4,int(210*min(val,maxval)/maxval))
            fill=tk.Frame(outer,bg=color,width=fill_w,height=BAR_H)
            fill.place(x=0,y=0)
            pct=tk.Label(outer,text=f'{int(val)}/{int(maxval)}',
                         font=('PingFang SC',8),bg=color if fill_w>40 else BAR_BG,
                         fg='white' if fill_w>40 else '#666666')
            pct.place(x=max(2,fill_w-36),y=1)

        # 动态内容区
        info_frame=tk.Frame(body,bg=CARD); info_frame.pack(fill='both',expand=True)

        char_info=CHARACTERS.get(self.char_id,{})
        pet_name=getattr(self,'owner_name',None) or char_info.get('name','宠物')

        def refresh():
            for w in info_frame.winfo_children(): w.destroy()

            # 基本信息
            age_sec=int(_t.time()-self.birth_ts)
            if age_sec<3600:
                age_str=f'{age_sec//60} 分钟'
            elif age_sec<86400:
                age_str=f'{age_sec//3600} 小时'
            else:
                age_str=f'{age_sec//86400} 天'

            personality=self.get_personality() if hasattr(self,'get_personality') else 'balanced'
            pers_map={'food_lover':'贪吃鬼🍖','playful':'玩袍蹒🎮','clean_freak':'洁癒达人🛁','balanced':'平衡小天使⚖️'}
            pers_str=pers_map.get(personality,personality)

            exp_need=self.level*100

            row=0
            for label,val in [
                ('昵称',pet_name),
                ('主人',self.address_word if hasattr(self,'address_word') else '主人'),
                ('等级',f'Lv.{self.level}  👔'),
                ('年龄',age_str),
                ('性格',pers_str),
                ('到访',f'{len(self.travel_visited)} 个省市'),
                ('积分',f'⭐ {self.score}'),
                ('成就',f'{sum(1 for a in self.achievements if a["done"])} / {len(self.achievements)}'),
            ]:
                tk.Label(info_frame,text=f'{label}',font=('PingFang SC',10,'bold'),
                         bg=CARD,fg='#3a8cc8',anchor='e',width=4).grid(row=row,column=0,sticky='e',pady=2)
                tk.Label(info_frame,text=f':{val}',font=('PingFang SC',10),
                         bg=CARD,fg=DARK,anchor='w').grid(row=row,column=1,sticky='w',padx=6,pady=2)
                row+=1

            # 成长进度(EXP)
            tk.Label(info_frame,text='成长',font=('PingFang SC',10,'bold'),
                     bg=CARD,fg='#3a8cc8',anchor='e',width=4).grid(row=row,column=0,sticky='e',pady=3)
            outer_exp=tk.Frame(info_frame,bg='#ffe4aa',width=210,height=BAR_H)
            outer_exp.grid(row=row,column=1,padx=(6,0),pady=3,sticky='w')
            outer_exp.pack_propagate(False)
            cur_exp=getattr(self,'exp',0)
            fw=max(4,int(210*min(cur_exp,exp_need)/exp_need))
            tk.Frame(outer_exp,bg=EXP_C,width=fw,height=BAR_H).place(x=0,y=0)
            tk.Label(outer_exp,text=f'{cur_exp}/{exp_need}',font=('PingFang SC',8),
                     bg=EXP_C if fw>50 else '#ffe4aa',
                     fg='white' if fw>50 else '#886600').place(x=max(2,fw-42),y=1)
            row+=1

            # 四维属性进度条
            for label,val,color in [
                ('饱度',self.hunger, HUNGER_C),
                ('洁洁',self.cleanliness, CLEAN_C),
                ('健康',self.health, HEALTH_C),
                ('心情',self.mood, MOOD_C),
            ]:
                bar(info_frame,label,val,100,color,row); row+=1

        refresh()

        # 底部
        bot=tk.Frame(card,bg='#ddeeff',height=36); bot.pack(fill='x'); bot.pack_propagate(False)
        tk.Label(bot,text='💓 我的宠物',font=('PingFang SC',9),bg='#ddeeff',fg=DARK).pack(side='left',padx=12)
        tk.Button(bot,text='刷新',font=('PingFang SC',9),bg=MID,fg='white',
                  relief='flat',bd=0,padx=10,pady=2,command=refresh).pack(side='right',padx=8)

        win.focus_force()

    def harvest(self):
        self.veg=[0,0,0,0]; self.veg_harvest=False
        self.unlock('harvest'); self.add_score(15); self.add_exp(20)
        self.say('🥕 收菜啦!撒种继续种~',100)

    # ── 照料系统 ────────────────────────────────────────────────────────
    def feed(self):
        """喂食 -- 直接打开背包"""
        self.open_bag()


    def _do_feed_direct(self):
        """旧的直接喂食逻辑(保留供内部调用)"""
        if self.hunger>=98:
            self.say('已经吃饱了~不能再吃了!',60); return
        self.hunger=min(100,self.hunger+30)
        self.mood=min(100,self.mood+5)
        self.say(random.choice(['啊~吃饱了!😋','好好吃!谢谢主人~','饿死我了!终于!','香!再来一碗!']),80)
        self.feed_count += 1; self.add_score(2); self.add_exp(5); self._save()

    def bathe(self):
        if self.cleanliness>=98:
            self.say('已经很干净了,不用洗咦!',60); return
        # 直接打开背包浴球界面
        self.open_bag(start_tab='bath')

    def play_with(self):
        self.mood=min(100,self.mood+30)
        self.hunger=max(0,self.hunger-5)
        self.say(random.choice(['一起玩!🎮','好开心!','再来!再来!','哈哈哈~好好玩!']),80)
        self.play_count += 1; self.add_score(3); self.add_exp(10); self._save()

    def give_medicine(self):
        if not self.sick and self.health>=90:
            self.say('我很健康哦!不用吃药~',60); return
        # 跳转背包药品 Tab
        self.open_bag(start_tab='medicine')

    # ── 属性面板绘制 ────────────────────────────────────────────────────
    def _draw_stats(self):
        cv=self.cv
        py=H-34
        # 底部面板背景(深色半透明感)
        cv.create_rectangle(0,py,W,H,fill='#100825',outline='')
        cv.create_line(0,py,W,py,fill='#2a1a55',width=1)
        stats=[
            (self.hunger,'#ff7733','🍔'),
            (self.mood,'#ffcc00','😊'),
            (self.cleanliness,'#44bbff','🛁'),
            (self.health,'#ff3366','❤️'),
        ]
        bar_w=62; unit=bar_w+34; total=len(stats)*unit
        sx=(W-total)//2
        for i,(val,color,icon) in enumerate(stats):
            x=sx+i*unit; y=py+17
            cv.create_text(x+8,y,text=icon,font=('Apple Color Emoji',10))
            bx=x+20
            # 轨道(圆角效果用细高度)
            cv.create_rectangle(bx,y-4,bx+bar_w,y+4,fill='#1e0f38',outline='')
            # 填充
            fw=max(0,int(bar_w*val/100))
            fc='#ff3333' if val<25 else '#ffaa22' if val<55 else color
            if fw>0:
                cv.create_rectangle(bx,y-4,bx+fw,y+4,fill=fc,outline='')
                # 高光条(进度条顶部一像素亮线)
                cv.create_rectangle(bx,y-4,bx+fw,y-3,fill='#ffffff' if fw>4 else fc,outline='')
            # 低属性闪烁警告边框
            if val<25 and self.frame%20<10:
                cv.create_rectangle(bx-1,y-5,bx+bar_w+1,y+5,fill='',outline='#ff4444',width=1)


if __name__=='__main__':
    HomeWorld()


