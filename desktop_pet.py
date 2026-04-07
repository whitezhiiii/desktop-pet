#!/usr/bin/env python3
"""南波万小家园 🏡 - 全像素风 v8 对话版"""
import tkinter as tk
import random, math, time, threading, urllib.request, json, os, http.client, ssl

W, H = 480, 332
WEATHER_CITY = 'Beijing'
BP = 4   # 背景像素格
CP = 3   # 角色像素格

SAVE_FILE = os.path.expanduser('~/.nbw_pet_save.json')

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
    '今天也是美好的一天~','发什么呆好呢…','嗯……','天气不错！','摸会儿鱼先',
    '主人在吗？','风好凉爽','有点无聊……','想睡觉了','南波万！🤙',
    '今天吃什么呢🍜','好想晒太阳啊','云朵好漂亮~','菜地要浇水了吗？',
]
QUOTES_ANGRY=[
    '够了够了！烦死了！😤','再戳我我生气了！','戳什么戳！','…哼！',
    '主人你很烦诶！','不理你了！','我会咬人的！🐾',
]
QUOTES_MAKE_UP=[
    '好啦好啦…不生气了😤','主人你认错了我就原谅你','哼，算了','还是喜欢主人嘛~',
]
QUOTES_HOUR=[
    '一点了，好困哦😴','两点，悄悄睡一会儿…','三点，夜深了~',
    '四点，早起的鸟儿有虫吃！','五点，天快亮了🌄','六点早安！☀️',
    '七点，吃早饭了吗？','八点，上班加油💪','九点，开始工作~',
    '十点了，喝杯茶休息下~☕','十一点，快中午了！🍱','十二点，午饭时间！',
    '下午一点，犯困的时间到了😪','两点，摸鱼正当时~🐟','三点，下午茶！☕',
    '四点，再坚持一下！','五点，快下班了🎉','六点，下班！吃饭！',
    '七点，晚上好~','八点，放松一下吧🎮','九点，今天辛苦了',
    '十点了，该休息了😴','十一点，熬夜伤身体哦','零点，跨过今天了！✨',
]

FISH_RESULTS=[
    ('🐟 小鲫鱼','钓到小鲫鱼！咕嘟咕嘟~',None),
    ('🐠 热带鱼','哇！热带鱼！好漂亮！',None),
    ('🦈 小鲨鱼','！！鲨鱼？！放生放生！',None),
    ('👢 破靴子','……钓到一只臭靴子……',None),
    ('💎 宝石','天啊！水晶宝石！！✨',None),
    ('📦 宝箱','宝箱！！里面有什么！',None),
    ('🍺 易拉罐','垃圾……主人来捡垃圾啦',None),
    ('🐙 小章鱼','章鱼！你怎么在这里！',None),
]

ACHIEVEMENTS=[
    {'id':'first_fish','name':'🎣 初次垂钓','desc':'第一次钓到东西','done':False},
    {'id':'harvest','name':'🥕 丰收喜悦','desc':'第一次收菜','done':False},
    {'id':'cook','name':'🍳 大厨出道','desc':'第一次做饭','done':False},
    {'id':'poke10','name':'👆 戳戳达人','desc':'戳了我10次','done':False},
    {'id':'score100','name':'💎 百分达人','desc':'积分达到100','done':False},
    {'id':'night_owl','name':'🦉 夜猫子','desc':'23点后还在','done':False},
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
        self.gnd=248  # 固定地面高度，底部留出属性面板

        self.cx=200; self.sprite='stand'; self.flip=False
        self.walk_t=0; self.target=200
        self.act='idle'; self.act_timer=0; self.act_phase=''
        self.bubble=''; self.btimer=0

        self.clouds=[
            {'x':40,'y':24,'w':18,'h':5,'s':0.15},
            {'x':200,'y':16,'w':24,'h':6,'s':0.10},
            {'x':360,'y':28,'w':15,'h':4,'s':0.18},
        ]
        self.smokes=[]; self.smoke_on=0

        # 天气粒子
        self.weather_mode='clear'  # clear/rain/snow
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

        # 积分/成就
        self.score=0
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

        # 四维属性
        self.hunger=80.0       # 饥饿度 0-100（100=饱）
        self.mood=80.0         # 心情   0-100（100=开心）
        self.cleanliness=80.0  # 清洁度 0-100（100=干净）
        self.health=100.0      # 健康值 0-100（100=健康）
        self.sick=False        # 生病状态
        self.stat_warn_cd=0    # 属性警告冷却

        self._load()

        self.cv.bind('<Button-1>',self.onclick)
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
        except: pass

    def _save(self):
        try:
            with open(SAVE_FILE,'w') as f:
                json.dump({
                    'score':self.score,'achievements':self.achievements,
                    'hunger':self.hunger,'mood':self.mood,
                    'cleanliness':self.cleanliness,'health':self.health,
                    'sick':self.sick
                },f)
        except: pass

    # ── 后台线程 ─────────────────────────────────────────────────────
    def _bg(self):
        lw=0
        while True:
            self.hour=time.localtime().tm_hour
            if time.time()-lw>3600: self._wx(); lw=time.time()
            time.sleep(30)

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
                self.ach_show=f"🏆 成就解锁：{a['name']}"; self.ach_timer=180
                self.score+=30; self._save()
                return True
        return False

    def add_score(self,n):
        self.score+=n; self._save()
        if self.score>=100: self.unlock('score100')

    # ── 活动调度 ─────────────────────────────────────────────────────
    def schedule(self):
        night=self.hour>=22 or self.hour<7
        pool=['sleep','sleep','idle'] if night else ['walk','walk','water','cook','fish','idle','idle','walk']
        self.do(random.choice(pool))

    def do(self,act):
        if self.angry_level>2: return  # 生气时不做事
        self.act=act; self.act_phase='walk'; self.act_timer=280
        dests={'walk':[80,132,180,252,304,360],'water':[320],'cook':[116],
               'fish':[212],'sleep':[116],'idle':[self.cx]}
        self.target=random.choice(dests.get(act,[200]))
        msgs={'walk':['散散步~ 🐾','溜达一圈','出去走走','走走走~'],
              'water':['去浇菜咯 🌱','浇水！','雨水不够，我来帮忙~'],
              'cook':['肚子饿了！🍳','开火咯~','今天做什么好呢'],
              'fish':['去钓鱼 🐟','垂钓时光~','鱼儿鱼儿快上钩'],
              'sleep':['困了，睡啦 😴','Zzz…','打个盹~'],
              'idle':random.choice([QUOTES_IDLE])}
        pool=msgs.get(act,QUOTES_IDLE)
        if isinstance(pool[0],list): pool=pool[0]
        self.say(random.choice(pool),65)

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
                doing={'water':['💧 浇水！','水灵灵的~','咕嘟咕嘟'],
                       'cook':['噼里啪啦！🍳','香死啦~','做好了叫你~'],
                       'fish':['等鱼上钩…🎣','鱼儿快来','沉住气…'],
                       'sleep':['Zzz…😴','好困~','呼……']}
                if self.act in doing: self.say(random.choice(doing[self.act]),100)
                if self.act=='cook':
                    self.smoke_on=90
                    self.unlock('cook'); self.add_score(5)
                if self.act=='water':
                    for i in range(4):
                        if self.veg[i]<2: self.veg[i]+=1; break
                    if all(v==2 for v in self.veg):
                        self.veg_harvest=True; self.say('🥕 菜全熟了！快来收菜~',120)
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
        self.unlock('first_fish'); self.add_score(10)

    def say(self,msg,dur=80): self.bubble,self.btimer=msg,dur

    # ── 整点报时 ─────────────────────────────────────────────────────
    def check_hour(self):
        h=self.hour
        if h!=self.last_hour:
            self.last_hour=h
            self.say(QUOTES_HOUR[h],120)
            if h>=23: self.unlock('night_owl')

    # ── 摸鱼检测 ─────────────────────────────────────────────────────
    def check_idle(self):
        mx,my=self.root.winfo_pointerx(),self.root.winfo_pointery()
        if mx!=self.lmx or my!=self.lmy:
            self.lmx,self.lmy,self.lmt=mx,my,time.time()
            if self.idle_warned: self.idle_warned=False; self.say('主人回来啦~🤙',60)
        elif time.time()-self.lmt>20*60 and not self.idle_warned:
            self.idle_warned=True; self.say('主人，起来动一动吧~😴',120)

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
        night=self.hour>=21 or self.hour<6
        gnd=self.gnd

        # ── 室内背景（QQ宠物风） ──────────────────────────────────────────
        def hex2rgb(h): c=h.lstrip('#'); return tuple(int(c[i:i+2],16) for i in (0,2,4))
        def lerp(a,b,t): return int(a+(b-a)*t)
        def rgb2hex(r,g,b): return f'#{r:02x}{g:02x}{b:02x}'
        strip=2

        # 1. 墙壁（竖条纹壁纸）
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
        # 木地板纹（横向条）
        for y in range(gnd+18, H, 18):
            cv.create_rectangle(0, y, W, y+2, fill=floor_s, outline='')
        # 地板高光（靠近墙处稍亮）
        cv.create_rectangle(0, gnd, W, gnd+6, fill=floor_h, outline='')

        # 4. 窗户（左侧，x=20-130）
        self._draw_window(cv, 20, 10, 110, 150, night)

        # 5. 右侧小床（x=330-470）
        self._draw_bed(cv, 330, 145, gnd, night)

        # 6. 中间书桌（x=170-270）
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
                # 下翅（小一半）
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
            cv.create_text(316,gnd-44,text='🥕 收菜！',font=('PingFang SC',10,'bold'),fill=T['sun'])

        # 成就弹出
        if self.ach_show and self.ach_timer>0:
            aw=220; ax=(W-aw)//2; ay=8
            cv.create_rectangle(ax,ay,ax+aw,ay+22,fill='#2a1050',outline=T['medal_g'],width=2)
            cv.create_text(ax+aw//2,ay+11,text=self.ach_show,font=('PingFang SC',9,'bold'),fill=T['medal_g'])

        # 积分显示
        cv.create_text(6,H-36,text=f'⭐{self.score}',anchor='sw',font=('PingFang SC',8),fill='#aaaacc')

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

        # 加载迷你角色图（只加载一次，引用全部挂在self._mini_img_refs上防GC）
        if not hasattr(self, '_mini_img_refs'):
            import os as _os2
            from PIL import Image as _PI, ImageTk as _IT, ImageSequence as _IS
            _adir = _os2.path.join(_os2.path.dirname(_os2.path.abspath(__file__)), 'assets')
            try:
                gif_r = _PI.open(_os2.path.join(_adir, 'walk_right.gif'))
                _frames_r = [_IT.PhotoImage(fr.convert('RGBA').resize((128,128),_PI.NEAREST))
                              for fr in _IS.Iterator(gif_r)]
                gif_l = _PI.open(_os2.path.join(_adir, 'walk_left.gif'))
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
            _img = (self._mini_frames_l if self.flip else self._mini_frames_r)[fi]
            cv.create_oval(cx-52, gnd-106, cx+52, gnd-2, fill='#fffaf0', outline='#e0c8a0', width=1)
            cv.create_image(cx, gnd-2, anchor='s', image=_img)
            # 双重防GC
            if not hasattr(cv, '_cur_imgs'): cv._cur_imgs = {}
            cv._cur_imgs['mini'] = _img
        else:
            spr = 'angry' if self.angry_level > 2 else self.sprite
            draw_sprite(cv, cx, gnd, spr, self.flip)

        if self.sick and self.frame % 16 < 8:
            cv.create_text(cx+16, gnd-52, text='🤒', font=('Apple Color Emoji', 9))
        if self.bubble and self.btimer > 0:
            self._px_bubble_mini(cx, gnd)
        if self.sprite == 'sleep':
            for i, z in enumerate(['z','Z','Z']):
                cv.create_text(cx+18+i*9, gnd-54+i*(-7), text=z,
                               font=('PingFang SC', 7+i*2, 'bold'), fill='#60d0ff')

    def _px_bubble_mini(self, cx, gnd):
        cv = self.cv; text = self.bubble
        bw = min(max(len(text)*7+12, 40), 200)
        bh = 20
        bx = max(2, cx - bw//2)
        sprite_h = len(STAND)*CP
        by = gnd - sprite_h - bh - 8
        cv.create_rectangle(bx, by, bx+bw, by+bh, fill='#fffef0', outline='#7744cc', width=1)
        cv.create_text(bx+bw//2, by+bh//2, text=text, font=('PingFang SC', 8), fill='#1e0a3c')

    def _draw_window(self, cv, x, y, w, h, night):
        """室内窗户"""
        # 窗外天色
        sky = '#1a2a4a' if night else '#c8e8ff'
        sun_hint = '#ffe8a0' if not night else '#2a3a6a'
        cv.create_rectangle(x+6, y+6, x+w-6, y+h-6, fill=sky, outline='')
        # 窗外简单景色（非夜晚）
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
        # 窗框（外框）
        fc = '#c8a060'
        cv.create_rectangle(x, y, x+w, y+h, fill='', outline=fc, width=5)
        # 十字窗格
        mx = x + w//2
        my = y + h//2
        cv.create_rectangle(mx-2, y+5, mx+2, y+h-5, fill=fc, outline='')
        cv.create_rectangle(x+5, my-2, x+w-5, my+2, fill=fc, outline='')
        # 窗帘（左右两侧，波浪底）
        curtain = '#ffcc88' if not night else '#cc9944'
        shadow  = '#e8a840' if not night else '#a87830'
        cw = 22  # 窗帘宽度
        for side in (0, 1):
            cx2 = x if side==0 else x+w-cw
            cv.create_rectangle(cx2, y, cx2+cw, y+h, fill=curtain, outline='')
            # 褶皱阴影
            for fold in range(y+8, y+h-8, 16):
                cv.create_rectangle(cx2+4, fold, cx2+cw-4, fold+3, fill=shadow, outline='')
            # 波浪底边（简单锯齿）
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
        # 床面（床垫）
        cv.create_rectangle(x+6, y+20, x+134, gnd-8, fill=mat_c, outline='')
        # 枕头
        cv.create_oval(x+10, y+22, x+52, y+44, fill=pil_c, outline='#ffc8d8', width=1)
        cv.create_oval(x+58, y+22, x+100, y+44, fill=pil_c, outline='#ffc8d8', width=1)
        # 被子花纹（几个小菱形）
        for bx in range(x+15, x+130, 22):
            cv.create_polygon(bx,y+60, bx+8,y+52, bx+16,y+60, bx+8,y+68, fill='#ffd0e0', outline='#ffb8cc', width=1)
        # 床头板（圆弧顶）
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
        # 桌上的书（叠放）
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
        # 简单风景画（圆+矩形）
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
        if self.btimer>0:
            self.btimer-=1
            if self.btimer==0: self.bubble=''
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

        # 属性自然衰减（每600帧≈约48秒，玩一小时掉约50%）
        if self.frame%600==0:
            self.hunger=max(0,self.hunger-0.8)
            self.mood=max(0,self.mood-0.4)
            self.cleanliness=max(0,self.cleanliness-0.3)
            # 健康值联动
            if self.hunger<20 or self.cleanliness<20:
                self.health=max(0,self.health-0.8)
                if not self.sick and self.health<50:
                    self.sick=True
                    self.say('感觉身体不太好…🤒',150)
            elif self.hunger>60 and self.mood>60 and self.cleanliness>60:
                self.health=min(100,self.health+0.3)
                if self.sick and self.health>75:
                    self.sick=False
                    self.say('感觉好多了！😊',100)
            # 低属性警告（冷却节流）
            low=[]
            if self.hunger<25: low.append('好饿…主人快喂我！🍔')
            if self.mood<25: low.append('好闷哦…陪我玩嘛🎮')
            if self.cleanliness<25: low.append('想洗澡了…好脏🛁')
            if self.health<30: low.append('身体不舒服…🤒')
            if low and self.stat_warn_cd==0:
                self.say(random.choice(low),130)
                self.stat_warn_cd=8
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
        win.attributes('-topmost', True)
        win.configure(bg='systemTransparent')
        self.garden_win = win
        cv_g = tk.Canvas(win, width=W_G, height=H_G, bg='systemTransparent', highlightthickness=0)
        cv_g.pack()
        g = {'cx': 550, 'cy': 360, 'flip': False, 'sprite': 'stand', 'moving': None, 'frame': 0, 'scene': 'indoor'}

        # 加载图片素材（只加载一次）
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

        frames_right = load_frames(os.path.join(ASSET_DIR2, 'walk_right.gif'))
        frames_left  = load_frames(os.path.join(ASSET_DIR2, 'walk_left.gif'))
        stand_img    = frames_right[0]

        # 所有图片引用挂在 win 上防止GC
        win._img_refs = [bg_day, bg_night, ext_day, ext_night, forest_day, forest_night, up_day, up_night] + frames_right + frames_left

        # 角色尺寸
        CHAR_W, CHAR_H = 64, 64

        # ── 碰撞地图构建 ──────────────────────────────────────

        # 碰撞矩形：只保留四周边框
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

        # 预先把背景画到静态 canvas item（只建一次）
        _bg_item = cv_g.create_image(0, 0, anchor='nw', image=bg_day)
        _night_overlay = cv_g.create_rectangle(0, 0, W_G, H_G-34,
                                                fill='#0a0820', stipple='gray50', outline='', state='hidden')
        _last_night = False
        _last_scene = 'indoor'

        # 门口触发区（左上角，靠近门的位置）
        # 室内：左上角楼梯（蓝色框）→ 二楼
        STAIR_X1, STAIR_Y1 = 128, 110
        STAIR_X2, STAIR_Y2 = 230, 328
        # 室内：右下角地毯（蓝色框）→ 户外
        CARPET_X1, CARPET_Y1 = 618, 438
        CARPET_X2, CARPET_Y2 = 822, 490
        # 户外门口落点
        EXT_DOOR_X, EXT_DOOR_Y = 450, 380
        EXT_DOOR_R = 55
        DOOR_X, DOOR_Y = 200, 220   # 兼容旧代码

        def draw_g():
            nonlocal _last_night, _last_scene
            if not win.winfo_exists(): return
            f = g['frame']; night = self.hour >= 21 or self.hour < 6
            scene = g['scene']

            # ── 清除上一帧的动态元素（保留背景） ──
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
            scene_label = {'outdoor':'🌿 户外','forest':'🌳 森林','upstairs':'🪜 二楼'}.get(scene, '🏠 室内')
            cv_g.create_text(14, 14, text=scene_label, anchor='nw',
                             font=('PingFang SC', 10, 'bold'),
                             fill='#ffffff', tags='dynamic')

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
                # 森林入口（户外左侧边缘）
                if gcx < 80:
                    cv_g.create_rectangle(28, gcy-40, 50, gcy+40,
                                          outline='#66dd66', width=2, dash=(6,3), tags='dynamic')
                    cv_g.create_text(W_G//2, 58, text='🌳 按 E 进入森林',
                                     font=('PingFang SC', 12, 'bold'), fill='#66dd66', tags='dynamic')
            elif scene == 'forest':
                # 返回户外（右侧边缘）
                if gcx > W_G - 80:
                    cv_g.create_rectangle(W_G-50, gcy-40, W_G-28, gcy+40,
                                          outline='#ffe88a', width=2, dash=(6,3), tags='dynamic')
                    cv_g.create_text(W_G//2, 58, text='🚪 按 E 回到户外',
                                     font=('PingFang SC', 12, 'bold'), fill='#ffe88a', tags='dynamic')
            elif scene == 'upstairs':
                # 二楼楼梯在右侧（镜像后）
                UP_STAIR_X1, UP_STAIR_Y1 = W_G - 230, 110
                UP_STAIR_X2, UP_STAIR_Y2 = W_G - 128, 328
                in_up_stair = UP_STAIR_X1 <= gcx <= UP_STAIR_X2 and UP_STAIR_Y1 <= gcy <= UP_STAIR_Y2
                if in_up_stair:
                    cv_g.create_rectangle(UP_STAIR_X1, UP_STAIR_Y1, UP_STAIR_X2, UP_STAIR_Y2,
                                          outline='#88eeff', width=2, dash=(6,3), tags='dynamic')
                    cv_g.create_text(W_G//2, 58, text='🪜 按 E 下楼',
                                     font=('PingFang SC', 12, 'bold'), fill='#88eeff', tags='dynamic')

            # ── 角色阴影 ──
            gcx = g['cx']; gcy = g['cy']
            cv_g.create_oval(gcx-20, gcy-4, gcx+20, gcy+4, fill='#443322', outline='', tags='dynamic')

            # ── 角色图片 ──
            moving = g['moving']
            fi = (f // 4) % len(frames_right)
            if moving == 'right':
                char_img = frames_right[fi]
            elif moving == 'left':
                char_img = frames_left[fi]
            else:
                char_img = stand_img
            cv_g.create_image(gcx, gcy - CHAR_H//2, anchor='s', image=char_img, tags='dynamic')

            # ── 生病图标 ──
            if self.sick and f%16<8:
                cv_g.create_text(gcx+20, gcy-CHAR_H-4, text='🤒', font=('Apple Color Emoji',12), tags='dynamic')

            # ── 气泡（简洁版，小圆角文字框）──
            if self.bubble and self.btimer > 0:
                btxt = self.bubble[:20] + ('…' if len(self.bubble)>20 else '')
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

            # ── 积分/时间/标题 ──
            cv_g.create_text(8,H_G-36,text=f'⭐{self.score}',anchor='sw',font=('PingFang SC',9), tags='dynamic',fill='#aaaacc')
            cv_g.create_text(W_G-8,H_G-36,text=time.strftime('%H:%M'),anchor='se',font=('PingFang SC',9),fill='#888888',tags='dynamic')
            cv_g.create_text(W_G//2,12,text='🏡 南波万の小家园',font=('PingFang SC',12,'bold'), tags='dynamic',
                            fill='#ffffff' if night else '#3a1a6a')

            # ── 关闭按钮 ──
            cv_g.create_oval(W_G-26,4,W_G-6,24,fill='#cc2244',outline='#ff4466',width=1, tags='dynamic')
            cv_g.create_text(W_G-16,14,text='✕',font=('PingFang SC',10,'bold'), tags='dynamic',fill='#ffccdd')

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

            # ── 走动逻辑（含碰撞检测）──
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
                    self.say('上二楼了！🪜', 80)
                elif ep and in_carpet2:
                    g['scene'] = 'outdoor'
                    g['cx'] = EXT_DOOR_X; g['cy'] = EXT_DOOR_Y
                    self.say('哇！出门啦 🌿', 80)
            elif g['scene'] == 'outdoor':
                dist_back2 = ((gcx2-EXT_DOOR_X)**2 + (gcy2-EXT_DOOR_Y)**2) ** 0.5
                if ep and dist_back2 < EXT_DOOR_R:
                    g['scene'] = 'indoor'
                    g['cx'] = (CARPET_X1+CARPET_X2)//2; g['cy'] = (CARPET_Y1+CARPET_Y2)//2
                    self.say('回到家里啦 🏠', 80)
                elif ep and gcx2 < 80:
                    g['scene'] = 'forest'
                    g['cx'] = W_G - 80; g['cy'] = GND
                    self.say('进入森林了！🌳', 80)
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

            if win.winfo_exists(): win.after(80, draw_g)


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
        # 同时绑定 win 和 cv_g，确保键盘事件能收到
        win.bind('<KeyPress>',on_kp); win.bind('<KeyRelease>',on_kr)
        cv_g.bind('<KeyPress>',on_kp); cv_g.bind('<KeyRelease>',on_kr)
        cv_g.bind('<Button-1>', lambda e: (on_click(e), win.focus_force()))
        win.bind('<Button-1>', lambda e: win.focus_force())

        # 右键菜单
        def on_g_rclick(e):
            m = tk.Menu(win, tearoff=0, bg='#1e0f3a', fg='#ddccff',
                        activebackground='#7733cc', activeforeground='white', font=('PingFang SC',11))
            m.add_command(label='🍔  喂食', command=lambda: (self.feed(), win.focus_force()))
            m.add_command(label='🛁  洗澡', command=lambda: (self.bathe(), win.focus_force()))
            m.add_command(label='🎮  玩耍', command=lambda: (self.play(), win.focus_force()))
            m.add_command(label='💊  喂药', command=lambda: (self.medicine(), win.focus_force()))
            m.add_separator()
            m.add_command(label=f'饥{int(self.hunger)} 情{int(self.mood)} 洁{int(self.cleanliness)} 命{int(self.health)}', state='disabled')
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
            self.poke_count+=1; self.add_score(1)
            # 连续快速戳 → 生气
            now=time.time()
            if now-self.last_poke<1.5:
                self.angry_level=min(self.angry_level+1,4)
            else:
                self.angry_level=max(0,self.angry_level-1)
            self.last_poke=now
            if self.poke_count>=10: self.unlock('poke10')
            if self.angry_level>2:
                self.say(random.choice(QUOTES_ANGRY),80)
                self.act_timer=120
            else:
                self.say(random.choice(['主人好！🤙','在呢~','南波万！','嗯？','哈哈~','戳我干嘛~']),60)
        self.drag=False

    def onright(self,e):
        m=tk.Menu(self.root,tearoff=0)
        m.add_command(label='🍔 喂食',command=self.feed)
        m.add_command(label='🛁 洗澡',command=self.bathe)
        m.add_command(label='🎮 玩耍',command=self.play_with)
        m.add_command(label='💊 喂药',command=self.give_medicine)
        m.add_separator()
        m.add_command(label='🌱 浇菜',command=lambda:self.do('water'))
        m.add_command(label='🍳 做饭',command=lambda:self.do('cook'))
        m.add_command(label='🎣 钓鱼',command=lambda:self.do('fish'))
        m.add_command(label='🚶 散步',command=lambda:self.do('walk'))
        m.add_command(label='😴 睡觉',command=lambda:self.do('sleep'))
        if self.veg_harvest:
            m.add_command(label='🥕 收菜！',command=self.harvest)
        m.add_separator()
        m.add_command(label='🌧️ 下雨效果',command=lambda:self._set_weather('rain'))
        m.add_command(label='❄️ 下雪效果',command=lambda:self._set_weather('snow'))
        m.add_command(label='☀️ 晴天',command=lambda:self._set_weather('clear'))
        m.add_separator()
        m.add_command(label='🏡 进入家园',command=self.open_garden)
        m.add_separator()

        m.add_command(label='⏰ 添加提醒',command=self._add_reminder_dialog)
        m.add_command(label='🏆 查看成就',command=self._show_achievements)
        m.add_command(label='⭐ 积分：'+str(self.score),state='disabled')
        m.add_command(label=f'饥{int(self.hunger)} 情{int(self.mood)} 洁{int(self.cleanliness)} 命{int(self.health)}',state='disabled')
        m.add_separator()
        m.add_command(label='🌤 看天气',command=lambda:(
            self.say(f'{self.w_icon} 北京 {self.w_temp}' if self.w_temp else '查天气中…',90),
            threading.Thread(target=self._wx,daemon=True).start() if not self.w_temp else None
        ))
        m.add_separator()
        m.add_command(label='❌ 关闭',command=self.root.destroy)
        try: m.tk_popup(e.x_root,e.y_root)
        finally: m.grab_release()

    def _set_weather(self,mode):
        self.weather_mode=mode
        self.particles=[]
        icons={'rain':'🌧️ 下雨啦！淋湿了…','snow':'❄️ 下雪了！好冷哦~','clear':'☀️ 天晴了！出去玩~'}
        self.say(icons.get(mode,'☀️'),90)

    def _add_reminder_dialog(self):
        win=tk.Toplevel(self.root); win.title('添加提醒')
        win.geometry('280x120'); win.resizable(False,False)
        win.attributes('-topmost',True)
        tk.Label(win,text='提醒内容：').pack(pady=(10,0))
        msg_var=tk.StringVar()
        tk.Entry(win,textvariable=msg_var,width=30).pack()
        tk.Label(win,text='多少分钟后？').pack()
        min_var=tk.IntVar(value=5)
        tk.Entry(win,textvariable=min_var,width=10).pack()
        def confirm():
            try:
                self.reminders.append({'at':time.time()+min_var.get()*60,'msg':msg_var.get() or '该休息啦！'})
                self.say(f'⏰ 好的，{min_var.get()}分钟后提醒你！',80)
                win.destroy()
            except: win.destroy()
        tk.Button(win,text='确定',command=confirm).pack(pady=5)

    def _show_achievements(self):
        done=[a for a in self.achievements if a['done']]
        todo=[a for a in self.achievements if not a['done']]
        lines=['🏆 已解锁：']+[f"  {a['name']}" for a in done]+['','🔒 未解锁：']+[f"  {a['name']}  ({a['desc']})" for a in todo]
        win=tk.Toplevel(self.root); win.title('成就'); win.attributes('-topmost',True)
        win.geometry('260x'+str(30+len(lines)*18))
        for l in lines:
            tk.Label(win,text=l,anchor='w',font=('PingFang SC',9)).pack(fill='x',padx=8)
        tk.Button(win,text='关闭',command=win.destroy).pack(pady=4)

    def harvest(self):
        self.veg=[0,0,0,0]; self.veg_harvest=False
        self.unlock('harvest'); self.add_score(15)
        self.say('🥕 收菜啦！撒种继续种~',100)

    # ── 照料系统 ────────────────────────────────────────────────────────
    def feed(self):
        if self.hunger>=98:
            self.say('已经吃饱了~不能再吃了！',60); return
        self.hunger=min(100,self.hunger+30)
        self.mood=min(100,self.mood+5)
        self.say(random.choice(['啊~吃饱了！😋','好好吃！谢谢主人~','饿死我了！终于！','香！再来一碗！']),80)
        self.add_score(2); self._save()

    def bathe(self):
        if self.cleanliness>=98:
            self.say('今天已经洗过了~很干净的！',60); return
        self.cleanliness=min(100,self.cleanliness+40)
        self.mood=min(100,self.mood+10)
        self.say(random.choice(['🛁 洗干净了！好舒服~','香香的~☁️','冲澡真爽！','泡澡太幸福了~']),80)
        self.add_score(3); self._save()

    def play_with(self):
        self.mood=min(100,self.mood+30)
        self.hunger=max(0,self.hunger-5)
        self.say(random.choice(['一起玩！🎮','好开心！','再来！再来！','哈哈哈~好好玩！']),80)
        self.add_score(3); self._save()

    def give_medicine(self):
        if not self.sick and self.health>=90:
            self.say('我很健康哦！不用吃药~',60); return
        self.health=min(100,self.health+25)
        if self.health>=75: self.sick=False
        self.say(random.choice(['苦死了…但谢谢主人🤒','吃完药好多了~','身体慢慢好起来了']),80)
        self.add_score(5); self._save()

    # ── 属性面板绘制 ────────────────────────────────────────────────────
    def _draw_stats(self):
        cv=self.cv
        py=H-34
        # 底部面板背景（深色半透明感）
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
            # 轨道（圆角效果用细高度）
            cv.create_rectangle(bx,y-4,bx+bar_w,y+4,fill='#1e0f38',outline='')
            # 填充
            fw=max(0,int(bar_w*val/100))
            fc='#ff3333' if val<25 else '#ffaa22' if val<55 else color
            if fw>0:
                cv.create_rectangle(bx,y-4,bx+fw,y+4,fill=fc,outline='')
                # 高光条（进度条顶部一像素亮线）
                cv.create_rectangle(bx,y-4,bx+fw,y-3,fill='#ffffff' if fw>4 else fc,outline='')
            # 低属性闪烁警告边框
            if val<25 and self.frame%20<10:
                cv.create_rectangle(bx-1,y-5,bx+bar_w+1,y+5,fill='',outline='#ff4444',width=1)


if __name__=='__main__':
    HomeWorld()
