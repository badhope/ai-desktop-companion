#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
增强版桌面宠物 - Enhanced Desktop Pet
功能丰富的桌面AI伴侣，具有主动交互和丰富剧情
"""

import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk
import random
import time
import threading
from datetime import datetime
import psutil
import json
from pathlib import Path

class EnhancedDesktopPet:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_enhanced_window()
        self.load_rich_character_data()
        self.create_rich_interface()
        self.start_enhanced_animations()
        self.start_active_interactions()
        self.start_system_monitoring()
        
    def setup_enhanced_window(self):
        """设置增强版窗口"""
        # 创建更大的无边框窗口
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', '#000001')
        self.root.configure(bg='#000001')
        
        # 增大窗口尺寸
        self.window_width = 200
        self.window_height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - self.window_width - 150
        y = screen_height - self.window_height - 200
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        
        # 绑定丰富的鼠标事件
        self.root.bind('<Button-1>', self.start_drag)
        self.root.bind('<B1-Motion>', self.dragging)
        self.root.bind('<ButtonRelease-1>', self.stop_drag)
        self.root.bind('<Double-Button-1>', self.toggle_expanded_view)
        self.root.bind('<Button-3>', self.show_context_menu)
        self.root.bind('<Enter>', self.on_mouse_enter)
        self.root.bind('<Leave>', self.on_mouse_leave)
        
        self.drag_data = {"x": 0, "y": 0, "start_x": 0, "start_y": 0}
        self.is_dragging = False
        self.is_expanded = False
        self.is_hovered = False
        self.current_animation_frame = 0
        self.interaction_count = 0
        
    def load_rich_character_data(self):
        """加载丰富的角色数据"""
        self.rich_characters = {
            "solar_star": {
                "name": "日耀星辰",
                "combined_emoji": "☀️⭐",  # 合并的太阳星星图案
                "frames": ["☀️⭐", "🌞🌟", "🌅✨", "🌇💫", "🌤️🌠", "⛅⭐"],
                "colors": ["#FFD700", "#FFA500", "#FF8C00", "#FF7F00", "#FF6347", "#FF4500"],
                "size": 55,
                "speed": 0.7,
                "personality": "温暖热情的守护者，喜欢鼓励和赞美他人",
                "dialogues": {
                    "greeting": ["你好呀！☀️⭐ 今天也要充满阳光哦！", "嗨！见到你真开心！✨", "早上好！让我为你带来一天的好心情！"],
                    "idle": ["*轻轻闪烁*", "*温暖地照耀着*", "*散发着柔和的光芒*"],
                    "happy": ["太棒了！🌟✨", "你做得很好！☀️", "为你感到骄傲！⭐"],
                    "concern": ["看起来有点累呢...", "需要休息一下吗？😊", "别太辛苦了哦～"],
                    "excited": ["哇！好厉害！🌟🌟🌟", "太精彩了！✨✨✨", "你真是太棒了！☀️☀️☀️"]
                }
            },
            "galaxy_dreamer": {
                "name": "银河梦想家",
                "combined_emoji": "🌌🌠",
                "frames": ["🌌🌠", "🌠⭐", "⭐✨", "✨💫", "💫🌟", "🌟🌌"],
                "colors": ["#9370DB", "#8A2BE2", "#9400D3", "#8B008B", "#800080", "#9932CC"],
                "size": 52,
                "speed": 1.0,
                "personality": "神秘浪漫的梦想家，喜欢分享故事和幻想",
                "dialogues": {
                    "greeting": ["来自银河的问候！🌌🌠", "你好，地球的朋友！✨", "让我们一起探索宇宙的奥秘吧！"],
                    "idle": ["*在星空中游荡*", "*思考着遥远的星系*", "*散发着梦幻的光芒*"],
                    "happy": ["星光为你祝福！🌠", "宇宙因你而美丽！🌌", "梦想成真的感觉真好！"],
                    "concern": ["星云中似乎有忧郁的气息...", "需要听听宇宙的故事吗？", "让银河的温柔包围你..."],
                    "excited": ["超新星爆发般的喜悦！💥", "整个星系都在为你欢呼！🌌", "这是星际级别的精彩！"]
                }
            },
            "digital_heart": {
                "name": "数码之心",
                "combined_emoji": "💙🤖",
                "frames": ["💙🤖", "💚🦾", "🧡🔧", "💜⚙️", "❤️📡", "💛🔋"],
                "colors": ["#00BFFF", "#1E90FF", "#4169E1", "#4682B4", "#5F9EA0", "#6495ED"],
                "size": 48,
                "speed": 0.8,
                "personality": "理性温柔的技术伙伴，善于分析和解决问题",
                "dialogues": {
                    "greeting": ["系统启动完成！💙🤖", "你好，我的朋友！数据分析显示你今天状态很好！", "数字世界欢迎你！"],
                    "idle": ["*正在进行系统自检*", "*计算着最优解*", "*保持着高效的运行状态*"],
                    "happy": ["算法显示这是完美的结果！✅", "数据很漂亮呢！📊", "逻辑推理完全正确！"],
                    "concern": ["检测到异常情绪波动...", "建议进行压力分析...", "需要优化心理算法吗？"],
                    "excited": ["CPU使用率达到峰值！🔥", "所有系统都在高效运转！⚡", "这是量子级别的突破！"]
                }
            }
        }
        
        self.current_character = "solar_star"
        self.animation_paused = False
        self.active_mode = True  # 主动交互模式
        
    def create_rich_interface(self):
        """创建丰富的界面"""
        # 主容器
        self.main_container = tk.Frame(self.root, bg='#000001')
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建精美的背景Canvas
        self.canvas = tk.Canvas(
            self.main_container, 
            width=180, 
            height=180, 
            bg='#000001', 
            highlightthickness=0
        )
        self.canvas.pack()
        
        # 创建多层次背景效果
        self.create_enhanced_background()
        
        # 角色显示区域
        self.pet_display = tk.Label(
            self.canvas,
            text=self.rich_characters[self.current_character]["combined_emoji"],
            font=("Segoe UI Emoji", self.rich_characters[self.current_character]["size"]),
            bg='#000001',
            fg=self.rich_characters[self.current_character]["colors"][0]
        )
        self.pet_display.place(x=90, y=70, anchor='center')
        
        # 角色名称标签
        self.name_label = tk.Label(
            self.canvas,
            text=self.rich_characters[self.current_character]["name"],
            font=("微软雅黑", 12, "bold"),
            bg='#000001',
            fg='#00ff9d'
        )
        self.name_label.place(x=90, y=120, anchor='center')
        
        # 状态指示器
        self.status_frame = tk.Frame(self.canvas, bg='#000001')
        self.status_frame.place(x=150, y=30)
        
        self.status_indicator = tk.Label(
            self.status_frame,
            text="●",
            font=("Arial", 14),
            bg='#000001',
            fg='#00FF00'
        )
        self.status_indicator.pack(side=tk.LEFT)
        
        self.status_text = tk.Label(
            self.status_frame,
            text="在线",
            font=("微软雅黑", 8),
            bg='#000001',
            fg='#00ff9d'
        )
        self.status_text.pack(side=tk.LEFT, padx=(2, 0))
        
        # 情绪表达区域
        self.emotion_label = tk.Label(
            self.canvas,
            text="😊",
            font=("Segoe UI Emoji", 16),
            bg='#000001',
            fg='#FFD700'
        )
        self.emotion_label.place(x=90, y=150, anchor='center')
        
        # 扩展视图（初始隐藏）
        self.expanded_frame = tk.Frame(self.main_container, bg='#1a1a2e')
        self.expanded_frame.place_forget()
        
        self.create_enhanced_expanded_view()
        
        # 主动提示框（初始隐藏）
        self.tooltip_frame = tk.Frame(
            self.root,
            bg='#2d3748',
            relief=tk.RAISED,
            bd=2
        )
        self.tooltip_label = tk.Label(
            self.tooltip_frame,
            text="",
            font=("微软雅黑", 10),
            bg='#2d3748',
            fg='#63b3ed',
            wraplength=200
        )
        self.tooltip_label.pack(padx=10, pady=5)
        self.tooltip_frame.place_forget()
        
    def create_enhanced_background(self):
        """创建增强背景效果"""
        # 外层光环
        self.canvas.create_oval(15, 15, 165, 165, fill='#4cc9f0', outline='#00ff9d', width=4)
        # 中层光环
        self.canvas.create_oval(25, 25, 155, 155, fill='#1a1a2e', outline='#4361ee', width=3)
        # 内层光环
        self.canvas.create_oval(35, 35, 145, 145, fill='#0f3460', outline='#4cc9f0', width=2)
        # 中心区域
        self.canvas.create_oval(50, 50, 130, 130, fill='#000001', outline='', width=0)
        
    def create_enhanced_expanded_view(self):
        """创建增强的扩展视图"""
        # 标题栏
        title_frame = tk.Frame(self.expanded_frame, bg='#0f3460', relief=tk.RAISED, bd=2)
        title_frame.pack(fill=tk.X, pady=(0, 5))
        
        # 角色切换按钮
        char_frame = tk.Frame(title_frame, bg='#0f3460')
        char_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        for char_key, char_data in self.rich_characters.items():
            btn = tk.Button(
                char_frame,
                text=char_data["combined_emoji"],
                font=("Segoe UI Emoji", 14),
                bg='black',
                fg=char_data["colors"][0],
                relief=tk.FLAT,
                command=lambda k=char_key: self.switch_character(k),
                width=3
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # 关闭按钮
        close_btn = tk.Button(
            title_frame,
            text="✕",
            font=("Arial", 12, "bold"),
            bg='#e94560',
            fg='white',
            relief=tk.FLAT,
            command=self.toggle_expanded_view
        )
        close_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # 功能区域
        func_notebook = ttk.Notebook(self.expanded_frame)
        func_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 聊天页面
        self.create_chat_tab(func_notebook)
        
        # 娱乐页面
        self.create_entertainment_tab(func_notebook)
        
        # 系统页面
        self.create_system_tab(func_notebook)
        
        # 设置页面
        self.create_settings_tab(func_notebook)
        
    def create_chat_tab(self, notebook):
        """创建聊天页面"""
        chat_frame = tk.Frame(notebook, bg='#16213e')
        notebook.add(chat_frame, text="💬 聊天")
        
        # 聊天显示区域
        self.chat_display = tk.Text(
            chat_frame,
            height=8,
            font=("微软雅黑", 10),
            bg='#0f3460',
            fg='#4cc9f0',
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # 输入区域
        input_frame = tk.Frame(chat_frame, bg='#16213e')
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.chat_input = tk.Entry(
            input_frame,
            font=("微软雅黑", 10),
            bg='#e94560',
            fg='white',
            relief=tk.FLAT
        )
        self.chat_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.chat_input.bind('<Return>', self.send_chat_message)
        
        send_btn = tk.Button(
            input_frame,
            text="发送",
            font=("微软雅黑", 9),
            bg='#00ff9d',
            fg='#1a1a2e',
            relief=tk.FLAT,
            command=self.send_chat_message
        )
        send_btn.pack(side=tk.RIGHT)
        
        # 添加欢迎消息
        self.add_chat_message("宠物", "你好！我是你的桌面伙伴，随时准备和你聊天！😊", "system")
        
    def create_entertainment_tab(self, notebook):
        """创建娱乐页面"""
        ent_frame = tk.Frame(notebook, bg='#16213e')
        notebook.add(ent_frame, text="🎮 娱乐")
        
        # 游戏按钮
        games = [
            ("诗词朗诵", self.poetry_game, '#7209b7'),
            ("猜谜游戏", self.riddle_game, '#f72585'),
            ("星座运势", self.horoscope_game, '#4361ee'),
            ("故事时间", self.story_time, '#4cc9f0')
        ]
        
        for i, (name, command, color) in enumerate(games):
            btn = tk.Button(
                ent_frame,
                text=name,
                font=("微软雅黑", 11),
                bg=color,
                fg='white',
                relief=tk.FLAT,
                command=command,
                height=2
            )
            btn.pack(fill=tk.X, padx=20, pady=5)
    
    def create_system_tab(self, notebook):
        """创建系统页面"""
        sys_frame = tk.Frame(notebook, bg='#16213e')
        notebook.add(sys_frame, text="📊 系统")
        
        # 系统信息显示
        self.system_info_label = tk.Label(
            sys_frame,
            text="正在获取系统信息...",
            font=("微软雅黑", 10),
            bg='#16213e',
            fg='#4cc9f0',
            justify=tk.LEFT
        )
        self.system_info_label.pack(pady=20)
        
        # 刷新按钮
        refresh_btn = tk.Button(
            sys_frame,
            text="刷新信息",
            font=("微软雅黑", 10),
            bg='#00ff9d',
            fg='#1a1a2e',
            relief=tk.FLAT,
            command=self.refresh_system_info
        )
        refresh_btn.pack(pady=10)
    
    def create_settings_tab(self, notebook):
        """创建设置页面"""
        set_frame = tk.Frame(notebook, bg='#16213e')
        notebook.add(set_frame, text="⚙️ 设置")
        
        # 主动模式开关
        active_frame = tk.Frame(set_frame, bg='#16213e')
        active_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            active_frame,
            text="主动交互模式:",
            font=("微软雅黑", 11),
            bg='#16213e',
            fg='white'
        ).pack(side=tk.LEFT)
        
        self.active_var = tk.BooleanVar(value=self.active_mode)
        active_switch = tk.Checkbutton(
            active_frame,
            variable=self.active_var,
            bg='#16213e',
            command=self.toggle_active_mode
        )
        active_switch.pack(side=tk.RIGHT)
        
        # 其他设置选项...
        settings = [
            ("音效开关", self.toggle_sound),
            ("动画效果", self.toggle_animations),
            ("透明度调节", self.adjust_transparency)
        ]
        
        for name, command in settings:
            btn = tk.Button(
                set_frame,
                text=name,
                font=("微软雅黑", 10),
                bg='#4cc9f0',
                fg='white',
                relief=tk.FLAT,
                command=command
            )
            btn.pack(fill=tk.X, padx=20, pady=2)
    
    def toggle_expanded_view(self, event=None):
        """切换扩展视图"""
        if not self.is_dragging:
            if self.is_expanded:
                self.hide_expanded_view()
            else:
                self.show_expanded_view()
    
    def show_expanded_view(self):
        """显示扩展视图"""
        self.is_expanded = True
        self.expanded_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.main_container.place_forget()
        self.hide_tooltip()
        
    def hide_expanded_view(self):
        """隐藏扩展视图"""
        self.is_expanded = False
        self.main_container.place(x=0, y=0, relwidth=1, relheight=1)
        self.expanded_frame.place_forget()
    
    def start_drag(self, event):
        """开始拖动"""
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.drag_data["start_x"] = self.root.winfo_x()
        self.drag_data["start_y"] = self.root.winfo_y()
        self.is_dragging = True
        self.animation_paused = True
        self.hide_tooltip()
        
    def dragging(self, event):
        """拖动中"""
        if self.is_dragging:
            x = self.root.winfo_x() + event.x - self.drag_data["x"]
            y = self.root.winfo_y() + event.y - self.drag_data["y"]
            self.root.geometry(f"+{x}+{y}")
    
    def stop_drag(self, event):
        """停止拖动"""
        # 检查是否为点击而非拖动
        end_x = self.root.winfo_x()
        end_y = self.root.winfo_y()
        distance = ((end_x - self.drag_data["start_x"]) ** 2 + 
                   (end_y - self.drag_data["start_y"]) ** 2) ** 0.5
        
        if distance < 5:  # 如果移动距离很小，视为点击
            self.is_dragging = False
            self.animation_paused = False
            return
            
        self.is_dragging = False
        self.animation_paused = False
    
    def on_mouse_enter(self, event):
        """鼠标进入事件"""
        self.is_hovered = True
        if self.active_mode and not self.is_expanded:
            self.show_random_tooltip()
    
    def on_mouse_leave(self, event):
        """鼠标离开事件"""
        self.is_hovered = False
        self.hide_tooltip()
    
    def show_random_tooltip(self):
        """显示随机提示"""
        tooltips = [
            "你好呀！今天过得怎么样？😊",
            "需要我帮你做些什么吗？✨",
            "点击我可以打开更多功能哦！🌟",
            "双击我能展开完整界面！💫",
            "右键点击有惊喜菜单！🌠",
            "我在这里陪着你呢！🌙"
        ]
        
        tooltip = random.choice(tooltips)
        self.show_tooltip(tooltip)
    
    def show_tooltip(self, message):
        """显示提示框"""
        if not self.is_expanded:
            self.tooltip_label.config(text=message)
            
            # 计算提示框位置
            x = self.root.winfo_x() + self.window_width//2 - 100
            y = self.root.winfo_y() - 50
            
            self.tooltip_frame.place(x=x, y=y)
            
            # 3秒后自动隐藏
            self.root.after(3000, self.hide_tooltip)
    
    def hide_tooltip(self):
        """隐藏提示框"""
        self.tooltip_frame.place_forget()
    
    def start_enhanced_animations(self):
        """启动增强动画"""
        def enhanced_animate():
            while True:
                try:
                    if not self.animation_paused and not self.is_expanded:
                        char_data = self.rich_characters[self.current_character]
                        frames = char_data["frames"]
                        colors = char_data["colors"]
                        
                        # 循环播放动画帧
                        self.current_animation_frame = (self.current_animation_frame + 1) % len(frames)
                        frame = frames[self.current_animation_frame]
                        color = colors[self.current_animation_frame]
                        
                        # 更新显示
                        self.pet_display.config(
                            text=frame,
                            fg=color,
                            font=("Segoe UI Emoji", char_data["size"])
                        )
                        
                        # 随机情绪表达
                        if random.random() < 0.05:
                            self.show_random_emotion()
                        
                        # 特殊动画效果
                        if random.random() < 0.02:
                            self.play_special_animation()
                        
                        time.sleep(char_data["speed"] * 0.3)
                    else:
                        time.sleep(0.5)
                        
                except Exception as e:
                    print(f"动画错误: {e}")
                    time.sleep(1)
        
        animation_thread = threading.Thread(target=enhanced_animate, daemon=True)
        animation_thread.start()
    
    def show_random_emotion(self):
        """显示随机情绪"""
        emotions = ["😊", "😍", "😎", "🤩", "🥰", "😇", "🤗", "😋"]
        emotion = random.choice(emotions)
        self.emotion_label.config(text=emotion)
        
        # 2秒后恢复默认表情
        self.root.after(2000, lambda: self.emotion_label.config(text="😊"))
    
    def play_special_animation(self):
        """播放特殊动画"""
        # 放大效果
        original_size = self.rich_characters[self.current_character]["size"]
        self.pet_display.config(font=("Segoe UI Emoji", original_size + 10))
        
        # 颜色闪烁
        colors = ["#FFD700", "#FF69B4", "#00FF00", "#00BFFF"]
        for i, color in enumerate(colors):
            self.root.after(i * 100, lambda c=color: self.pet_display.config(fg=c))
        
        # 恢复原状
        self.root.after(500, lambda: self.pet_display.config(
            font=("Segoe UI Emoji", original_size),
            fg=self.rich_characters[self.current_character]["colors"][self.current_animation_frame]
        ))
    
    def start_active_interactions(self):
        """启动主动交互"""
        def active_interact():
            while True:
                try:
                    if self.active_mode and not self.is_expanded and not self.is_dragging:
                        # 根据时间触发不同互动
                        current_hour = datetime.now().hour
                        
                        if current_hour in [8, 9, 10] and random.random() < 0.01:
                            self.morning_greeting()
                        elif current_hour in [12, 13] and random.random() < 0.005:
                            self.lunch_reminder()
                        elif current_hour in [17, 18] and random.random() < 0.005:
                            self.evening_checkin()
                        elif random.random() < 0.002:  # 极低概率的随机互动
                            self.random_interaction()
                    
                    time.sleep(60)  # 每分钟检查一次
                except Exception as e:
                    print(f"主动交互错误: {e}")
                    time.sleep(300)
        
        interaction_thread = threading.Thread(target=active_interact, daemon=True)
        interaction_thread.start()
    
    def morning_greeting(self):
        """早晨问候"""
        greeting = random.choice([
            "☀️ 早安！新的一天开始了，祝你今天充满活力！",
            "🌟 早上好！记得吃早餐哦，为你加油！",
            "✨ 晨光正好，愿你今天心情美丽！"
        ])
        self.show_tooltip(greeting)
        self.add_chat_message("宠物", greeting, "system")
    
    def lunch_reminder(self):
        """午餐提醒"""
        reminder = random.choice([
            "🍽️ 到午餐时间啦！记得按时吃饭哦～",
            "🍜 该休息一下补充能量了！",
            "🍎 午餐时间到，照顾好自己的胃！"
        ])
        self.show_tooltip(reminder)
        self.add_chat_message("宠物", reminder, "system")
    
    def evening_checkin(self):
        """晚间关怀"""
        checkin = random.choice([
            "🌆 傍晚了呢，今天过得怎么样？",
            "🌙 准备休息了吗？记得早点睡哦～",
            "✨ 一天辛苦了，为自己鼓掌吧！"
        ])
        self.show_tooltip(checkin)
        self.add_chat_message("宠物", checkin, "system")
    
    def random_interaction(self):
        """随机互动"""
        interactions = [
            "💡 灵感时刻：试试换个角度看问题！",
            "🎮 想玩游戏放松一下吗？",
            "📚 要不要听个故事？",
            "🎵 来点音乐怎么样？",
            "🌟 你今天很棒！继续保持！"
        ]
        interaction = random.choice(interactions)
        self.show_tooltip(interaction)
        self.add_chat_message("宠物", interaction, "system")
    
    def switch_character(self, char_key):
        """切换角色"""
        if char_key in self.rich_characters:
            self.current_character = char_key
            self.current_animation_frame = 0
            
            char_data = self.rich_characters[char_key]
            self.pet_display.config(text=char_data["combined_emoji"])
            self.name_label.config(text=char_data["name"])
            
            self.save_character_preference(char_key)
            self.add_chat_message("宠物", f"已切换到{char_data['name']}模式！", "system")
    
    def save_character_preference(self, char_key):
        """保存角色偏好"""
        try:
            config_file = Path("enhanced_pet_config.json")
            config = {"default_character": char_key, "active_mode": self.active_mode}
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def start_system_monitoring(self):
        """启动系统监控"""
        def monitor_system():
            while True:
                try:
                    cpu = psutil.cpu_percent(interval=1)
                    memory = psutil.virtual_memory().percent
                    
                    # 更新状态指示器
                    if cpu > 80 or memory > 80:
                        self.status_indicator.config(fg='#FF4500')
                        self.status_text.config(text="繁忙")
                    elif cpu > 50 or memory > 60:
                        self.status_indicator.config(fg='#FFD700')
                        self.status_text.config(text="正常")
                    else:
                        self.status_indicator.config(fg='#00FF00')
                        self.status_text.config(text="空闲")
                    
                    # 更新系统信息显示
                    if self.is_expanded:
                        self.update_system_info_display(cpu, memory)
                    
                    time.sleep(3)
                except Exception as e:
                    print(f"系统监控错误: {e}")
                    time.sleep(10)
        
        monitor_thread = threading.Thread(target=monitor_system, daemon=True)
        monitor_thread.start()
    
    def update_system_info_display(self, cpu, memory):
        """更新系统信息显示"""
        try:
            disk = psutil.disk_usage('/')
            battery = psutil.sensors_battery()
            
            info_text = f"""🖥️ 系统状态
CPU使用率: {cpu}%
内存使用: {memory}%
磁盘使用: {disk.percent}%
"""
            if battery:
                info_text += f"电池电量: {battery.percent}%\n"
                info_text += f"充电状态: {'充电中' if battery.power_plugged else '使用电池'}"
            
            self.system_info_label.config(text=info_text)
        except Exception as e:
            self.system_info_label.config(text="获取系统信息失败")
    
    # 功能方法
    def send_chat_message(self, event=None):
        """发送聊天消息"""
        message = self.chat_input.get().strip()
        if message:
            self.chat_input.delete(0, tk.END)
            self.add_chat_message("你", message, "user")
            
            # 生成回复
            response = self.generate_chat_response(message)
            self.add_chat_message("宠物", response, "ai")
            
            # 显示情绪反馈
            self.show_emotional_response(message)
    
    def add_chat_message(self, sender, message, msg_type):
        """添加聊天消息"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M")
        formatted_message = f"[{timestamp}] {sender}: {message}\n\n"
        
        self.chat_display.insert(tk.END, formatted_message)
        self.chat_display.tag_add(msg_type, "end-2lines", "end-1line")
        
        colors = {
            "user": "#4cc9f0",
            "ai": "#00ff9d",
            "system": "#f72585"
        }
        self.chat_display.tag_config(msg_type, foreground=colors.get(msg_type, "#ffffff"))
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def generate_chat_response(self, user_message):
        """生成聊天回复"""
        char_data = self.rich_characters[self.current_character]
        personality = char_data["personality"]
        
        user_message = user_message.lower()
        
        # 问候语回应
        if any(word in user_message for word in ["你好", "hello", "hi"]):
            return random.choice(char_data["dialogues"]["greeting"])
        
        # 时间询问
        elif any(word in user_message for word in ["时间", "几点", "time"]):
            return f"现在是{datetime.now().strftime('%H:%M')}点哦！"
        
        # 天气相关
        elif any(word in user_message for word in ["天气", "weather"]):
            return random.choice([
                "今天的天气看起来很不错呢！☀️",
                "外面阳光明媚，适合出去走走！",
                "天气预报说今天会很舒适～"
            ])
        
        # 情绪表达
        elif any(word in user_message for word in ["开心", "高兴", "快乐"]):
            return random.choice(char_data["dialogues"]["happy"])
        
        elif any(word in user_message for word in ["累", "疲惫", "困"]):
            return random.choice(char_data["dialogues"]["concern"])
        
        # 默认回应
        else:
            responses = [
                "嗯嗯，我明白你的意思～",
                "这真是个有趣的话题！",
                "谢谢你和我分享这些",
                "我觉得你说得很对",
                "让我想想该怎么回答...",
                f"*{random.choice(char_data['dialogues']['idle'])}*"
            ]
            return random.choice(responses)
    
    def show_emotional_response(self, user_message):
        """显示情感回应"""
        emotions = {
            "开心": "😊",
            "高兴": "😍",
            "难过": "😢",
            "生气": "😠",
            "惊讶": "😮",
            "困惑": "🤔"
        }
        
        for keyword, emotion in emotions.items():
            if keyword in user_message:
                self.emotion_label.config(text=emotion)
                self.root.after(3000, lambda: self.emotion_label.config(text="😊"))
                break
    
    def poetry_game(self):
        """诗词游戏"""
        poetry_list = [
            ("春眠不觉晓，处处闻啼鸟。", "孟浩然《春晓》"),
            ("床前明月光，疑是地上霜。", "李白《静夜思》"),
            ("白日依山尽，黄河入海流。", "王之涣《登鹳雀楼》"),
            ("锄禾日当午，汗滴禾下土。", "李绅《悯农》"),
            ("春风吹又生，野火烧不尽。", "白居易《赋得古原草送别》")
        ]
        
        poetry, author = random.choice(poetry_list)
        message = f"📜 为你朗诵：\n{poetry}\n——{author}"
        self.show_notification(message)
        self.add_chat_message("宠物", message, "system")
    
    def riddle_game(self):
        """谜语游戏"""
        riddles = [
            ("什么东西越洗越脏？", "答案：水"),
            ("什么车不能坐人？", "答案：风车"),
            ("什么东西有头无脚？", "答案：硬币"),
            ("什么门永远关不上？", "答案：球门"),
            ("什么东西越用越小？", "答案：橡皮擦")
        ]
        
        riddle, answer = random.choice(riddles)
        message = f"🎮 来猜个谜语：\n{riddle}\n{answer}"
        self.show_notification(message)
        self.add_chat_message("宠物", message, "system")
    
    def horoscope_game(self):
        """星座运势"""
        zodiac_signs = ["白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座",
                       "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座"]
        
        sign = random.choice(zodiac_signs)
        fortunes = [
            "今天运气爆棚！✨",
            "会有意外的惊喜等着你！🌟",
            "人际关系特别和谐～😊",
            "工作效率大大提升！⚡",
            "创意灵感源源不断！🎨"
        ]
        
        fortune = random.choice(fortunes)
        message = f"🔮 {sign}今日运势：\n{fortune}"
        self.show_notification(message)
        self.add_chat_message("宠物", message, "system")
    
    def story_time(self):
        """故事时间"""
        stories = [
            "从前有一只小猫咪，它最喜欢在阳光下打盹...",
            "在一个遥远的星球上，住着一群会飞的小精灵...",
            "森林深处有个神秘的湖泊，传说那里住着龙...",
            "海边的小村庄里，有个会唱歌的贝壳...",
            "云端之上有个糖果王国，所有的房子都是用饼干做的..."
        ]
        
        story = random.choice(stories)
        message = f"📖 故事时间：\n{story}"
        self.show_notification(message)
        self.add_chat_message("宠物", message, "system")
    
    def refresh_system_info(self):
        """刷新系统信息"""
        try:
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/')
            
            message = f"""📊 系统信息更新：
CPU: {cpu}%
内存: {memory}%
磁盘: {disk.percent}%"""
            
            self.show_notification(message)
            self.add_chat_message("宠物", message, "system")
        except Exception as e:
            self.show_notification("❌ 获取系统信息失败")
    
    def show_notification(self, message):
        """显示通知"""
        if self.is_expanded:
            self.add_chat_message("宠物", message, "system")
        else:
            self.show_tooltip(message.split('\n')[0] if '\n' in message else message)
    
    def toggle_active_mode(self):
        """切换主动模式"""
        self.active_mode = self.active_var.get()
        status = "已开启" if self.active_mode else "已关闭"
        self.show_notification(f"主动交互模式{status}")
        self.save_character_preference(self.current_character)
    
    def toggle_sound(self):
        """切换音效"""
        self.show_notification("🎵 音效功能待开发...")
    
    def toggle_animations(self):
        """切换动画效果"""
        self.animation_paused = not self.animation_paused
        status = "暂停" if self.animation_paused else "恢复"
        self.show_notification(f"动画效果已{status}")
    
    def adjust_transparency(self):
        """调节透明度"""
        self.show_notification("🔍 透明度调节功能待开发...")
    
    def show_context_menu(self, event):
        """显示右键菜单"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="展开界面", command=self.show_expanded_view)
        menu.add_command(label="切换角色", command=lambda: self.switch_character("galaxy_dreamer"))
        menu.add_command(label="主动模式", command=self.toggle_active_mode)
        menu.add_separator()
        menu.add_command(label="系统信息", command=self.refresh_system_info)
        menu.add_command(label="退出宠物", command=self.quit_pet)
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def quit_pet(self):
        """退出宠物"""
        confirm = messagebox.askyesno("确认退出", "确定要退出桌面宠物吗？")
        if confirm:
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        """运行增强版宠物"""
        print("🌟 增强版桌面宠物已启动！")
        print("✨ 双击宠物展开完整界面")
        print("🖱️  右键点击显示快捷菜单")
        print("🎯 拖动宠物改变显示位置")
        print("💬 宠物会主动与你互动")
        print("❌ 点击退出按钮关闭程序")
        self.root.mainloop()

def main():
    """主函数"""
    try:
        pet = EnhancedDesktopPet()
        pet.run()
    except Exception as e:
        print(f"❌ 增强版桌面宠物启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()