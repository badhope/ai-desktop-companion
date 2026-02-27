#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
增强版GUI界面 - Enhanced GUI Interface
具有丰富的视觉效果和高级功能的桌面AI伴侣界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import tkinter.font as tkFont
from PIL import Image, ImageTk
import random
import threading
import time
import json
from datetime import datetime
import psutil
import webbrowser

class EnhancedGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.animate_elements()
        self.update_system_info()
        
    def setup_window(self):
        """设置窗口属性"""
        self.root.title("🌟 AI桌面伴侣 - 增强版")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        
        # 设置窗口属性
        self.root.resizable(True, True)
        self.root.minsize(900, 600)
        
        # 创建自定义字体
        self.title_font = tkFont.Font(family="微软雅黑", size=16, weight="bold")
        self.normal_font = tkFont.Font(family="微软雅黑", size=12)
        self.small_font = tkFont.Font(family="微软雅黑", size=10)
        
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题区域
        self.create_title_section(main_frame)
        
        # 聊天区域
        self.create_chat_section(main_frame)
        
        # 功能面板
        self.create_function_panel(main_frame)
        
        # 系统信息面板
        self.create_system_panel(main_frame)
        
        # 底部状态栏
        self.create_status_bar()
    
    def create_title_section(self, parent):
        """创建标题区域"""
        title_frame = tk.Frame(parent, bg='#16213e', relief=tk.RAISED, bd=2)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 主标题
        title_label = tk.Label(
            title_frame, 
            text="🌟 AI桌面伴侣 增强版", 
            font=self.title_font,
            fg='#00ff9d',
            bg='#16213e'
        )
        title_label.pack(pady=15)
        
        # 副标题
        subtitle_label = tk.Label(
            title_frame,
            text=f"当前时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}",
            font=self.small_font,
            fg='#4cc9f0',
            bg='#16213e'
        )
        subtitle_label.pack()
        
        # 更新时间
        def update_time():
            subtitle_label.config(text=f"当前时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
            self.root.after(1000, update_time)
        
        update_time()
    
    def create_chat_section(self, parent):
        """创建聊天区域"""
        chat_frame = tk.LabelFrame(
            parent,
            text="💬 智能对话系统",
            font=self.normal_font,
            fg='#00ff9d',
            bg='#16213e'
        )
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 聊天显示区域
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            height=15,
            font=self.normal_font,
            bg='#0f3460',
            fg='#e94560',
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 输入框架
        input_frame = tk.Frame(chat_frame, bg='#16213e')
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 输入框
        self.user_input = tk.Entry(
            input_frame,
            font=self.normal_font,
            bg='#e94560',
            fg='white',
            relief=tk.FLAT
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_input.bind('<Return>', self.send_message)
        
        # 发送按钮
        send_button = tk.Button(
            input_frame,
            text="发送 🚀",
            font=self.normal_font,
            bg='#00ff9d',
            fg='#1a1a2e',
            relief=tk.FLAT,
            command=self.send_message
        )
        send_button.pack(side=tk.RIGHT)
        
        # 添加欢迎消息
        self.add_message("系统", "🌟 欢迎使用AI桌面伴侣增强版！我是您的智能助手，随时为您服务。", "system")
    
    def create_function_panel(self, parent):
        """创建功能面板"""
        func_frame = tk.LabelFrame(
            parent,
            text="🎮 功能中心",
            font=self.normal_font,
            fg='#00ff9d',
            bg='#16213e'
        )
        func_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 功能按钮框架
        button_frame = tk.Frame(func_frame, bg='#16213e')
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 功能按钮
        functions = [
            ("🎵 音乐播放", self.play_music),
            ("📚 古诗词库", self.tell_poetry),
            ("🎮 趣味游戏", self.start_game),
            ("🧠 知识问答", self.knowledge_qa),
            ("🎨 创意启发", self.creative_inspiration),
            ("⚙️ 系统工具", self.system_tools)
        ]
        
        for i, (text, command) in enumerate(functions):
            row = i // 3
            col = i % 3
            btn = tk.Button(
                button_frame,
                text=text,
                font=self.small_font,
                bg='#4cc9f0',
                fg='white',
                relief=tk.FLAT,
                command=command,
                width=15,
                height=2
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
        
        # 配置网格权重
        for i in range(3):
            button_frame.columnconfigure(i, weight=1)
    
    def create_system_panel(self, parent):
        """创建系统信息面板"""
        sys_frame = tk.LabelFrame(
            parent,
            text="💻 系统状态监控",
            font=self.normal_font,
            fg='#00ff9d',
            bg='#16213e'
        )
        sys_frame.pack(fill=tk.X)
        
        # 系统信息显示
        self.system_info = tk.Text(
            sys_frame,
            height=6,
            font=self.small_font,
            bg='#0f3460',
            fg='#4cc9f0',
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.system_info.pack(fill=tk.X, padx=10, pady=10)
    
    def create_status_bar(self):
        """创建状态栏"""
        status_frame = tk.Frame(self.root, bg='#16213e', relief=tk.SUNKEN, bd=1)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = tk.Label(
            status_frame,
            text="🟢 系统就绪",
            font=self.small_font,
            fg='#00ff9d',
            bg='#16213e'
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # 网络状态
        self.network_label = tk.Label(
            status_frame,
            text="🌐 网络: 离线模式",
            font=self.small_font,
            fg='#4cc9f0',
            bg='#16213e'
        )
        self.network_label.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def send_message(self, event=None):
        """发送消息"""
        user_message = self.user_input.get().strip()
        if not user_message:
            return
        
        # 显示用户消息
        self.add_message("你", user_message, "user")
        self.user_input.delete(0, tk.END)
        
        # 获取AI回复（在后台线程中）
        threading.Thread(target=self.get_ai_response, args=(user_message,), daemon=True).start()
    
    def get_ai_response(self, user_message):
        """获取AI回复"""
        try:
            self.update_status("🟡 思考中...")
            
            # 模拟思考延迟
            time.sleep(0.8)
            
            # 生成智能回复
            response = self.generate_intelligent_response(user_message)
            
            # 在主线程中更新UI
            self.root.after(0, lambda: self.add_message("AI助手", response, "ai"))
            self.root.after(0, lambda: self.update_status("🟢 系统就绪"))
            
        except Exception as e:
            self.root.after(0, lambda: self.add_message(
                "系统", 
                f"抱歉，出现了一些问题: {str(e)}", 
                "error"
            ))
            self.root.after(0, lambda: self.update_status("🔴 错误"))
    
    def generate_intelligent_response(self, user_input):
        """生成智能回复"""
        user_input = user_input.lower().strip()
        
        # 问候语处理
        greetings = {
            "早上好": ["早上好！新的一天开始了呢！😊", "早安！今天也要元气满满哦！", "Good morning！希望你今天心情愉快！"],
            "下午好": ["下午好！工作累了的话要记得休息哦～", "午后时光，要不要来杯咖啡？☕", "下午好呀！今天的阳光很温暖呢"],
            "晚上好": ["晚上好！今天过得怎么样？", "晚安好！准备休息了吗？😴", "Good evening！今天辛苦了"],
            "你好": ["你好呀！很高兴见到你！👋", "Hello！有什么我可以帮助你的吗？", "こんにちは！今日はどんなご用件ですか？"],
            "再见": ["再见！期待下次见面！😊", "Bye bye！路上小心哦～", "さようなら！また明日！"]
        }
        
        for key, responses in greetings.items():
            if key in user_input:
                return random.choice(responses)
        
        # 日常对话处理
        daily_topics = {
            "天气": ["今天的天气真不错呢！☀️", "外面好像要下雨了，记得带伞哦～", "天气预报说今天会很热，要注意防暑！"],
            "心情": ["我很好呀，谢谢关心！😊", "有点累，想休息一下...", "很开心能和你聊天！"],
            "时间": [f"现在是{datetime.now().strftime('%H:%M')}点", "时间过得真快呢...", "该休息了，现在已经很晚了"]
        }
        
        for topic, responses in daily_topics.items():
            if topic in user_input:
                return random.choice(responses)
        
        # 古诗词处理
        if any(word in user_input for word in ["古诗", "诗词", "诗歌"]):
            poetry_list = [
                "春眠不觉晓，处处闻啼鸟。——孟浩然《春晓》",
                "床前明月光，疑是地上霜。——李白《静夜思》",
                "白日依山尽，黄河入海流。——王之涣《登鹳雀楼》",
                "但愿人长久，千里共婵娟。——苏轼《水调歌头》"
            ]
            return f"📜 为您朗诵古诗:\n{random.choice(poetry_list)}"
        
        # 知识问答处理
        if any(word in user_input for word in ["为什么", "什么", "how", "知识"]):
            knowledge_list = [
                "水的化学分子式是H₂O",
                "地球是太阳系的第三颗行星",
                "光速是每秒299,792,458米",
                "人体大约由37万亿个细胞组成"
            ]
            return f"🧠 知识小百科:\n{random.choice(knowledge_list)}"
        
        # 游戏娱乐处理
        if any(word in user_input for word in ["游戏", "谜语", "脑筋急转弯"]):
            games_list = [
                "什么东西越洗越脏？——答案：水",
                "什么车不能坐人？——答案：风车",
                "什么东西有头无脚？——答案：硬币"
            ]
            return f"🎮 来玩个小游戏吧:\n{random.choice(games_list)}"
        
        # 情感支持处理
        if any(word in user_input for word in ["难过", "沮丧", "鼓励", "安慰"]):
            support_list = [
                "加油！我相信你可以做到的！💪",
                "不要放弃，成功就在前方！",
                "你已经很棒了，继续努力！",
                "抱抱你～一切都会好起来的"
            ]
            return random.choice(support_list)
        
        # 通用回复
        general_responses = [
            "嗯嗯，我明白了～",
            "这真是个有趣的话题！",
            "谢谢你和我分享这些",
            "我觉得你说得很对",
            "让我想想该怎么回答...",
            "这个想法很不错呢！"
        ]
        return random.choice(general_responses)
    
    def add_message(self, sender, message, msg_type):
        """添加消息到聊天显示区"""
        self.chat_display.config(state=tk.NORMAL)
        
        # 根据消息类型设置样式
        colors = {
            "user": "#4cc9f0",
            "ai": "#00ff9d", 
            "system": "#f72585",
            "error": "#e94560"
        }
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {sender}: {message}\n\n"
        
        # 插入消息
        self.chat_display.insert(tk.END, formatted_message)
        self.chat_display.tag_add(msg_type, "end-2lines", "end-1line")
        self.chat_display.tag_config(msg_type, foreground=colors.get(msg_type, "#ffffff"))
        
        # 滚动到底部
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def update_status(self, status_text):
        """更新状态栏"""
        self.status_label.config(text=status_text)
    
    def update_system_info(self):
        """更新系统信息"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info_text = f"🖥️ CPU使用率: {cpu_percent}%\n"
            info_text += f"💾 内存使用: {memory.percent}% ({memory.used//1024//1024}MB/{memory.total//1024//1024}MB)\n"
            info_text += f"📂 磁盘使用: {disk.percent}% ({disk.used//1024//1024//1024}GB/{disk.total//1024//1024//1024}GB)\n"
            info_text += f"🌐 网络连接: {len(psutil.net_connections())}个活动连接"
            
            self.system_info.config(state=tk.NORMAL)
            self.system_info.delete(1.0, tk.END)
            self.system_info.insert(1.0, info_text)
            self.system_info.config(state=tk.DISABLED)
            
        except Exception as e:
            pass
        
        # 每2秒更新一次
        self.root.after(2000, self.update_system_info)
    
    # 功能方法
    def play_music(self):
        """播放音乐功能"""
        self.add_message("系统", "🎵 正在为您播放轻音乐放松心情...", "system")
    
    def tell_poetry(self):
        """讲古诗功能"""
        poetry_list = [
            "春眠不觉晓，处处闻啼鸟。——孟浩然《春晓》",
            "床前明月光，疑是地上霜。——李白《静夜思》",
            "白日依山尽，黄河入海流。——王之涣《登鹳雀楼》",
            "但愿人长久，千里共婵娟。——苏轼《水调歌头》"
        ]
        poetry = random.choice(poetry_list)
        self.add_message("系统", f"📜 古诗词欣赏:\n{poetry}", "system")
    
    def start_game(self):
        """小游戏功能"""
        games_list = [
            "什么东西越洗越脏？——答案：水",
            "什么车不能坐人？——答案：风车",
            "什么东西有头无脚？——答案：硬币",
            "什么门永远关不上？——答案：球门"
        ]
        game_content = random.choice(games_list)
        self.add_message("系统", f"🎮 趣味猜谜:\n{game_content}", "system")
    
    def knowledge_qa(self):
        """知识问答功能"""
        knowledge_list = [
            "💧 水的化学分子式是H₂O",
            "🌍 地球是太阳系的第三颗行星",
            "⚡ 光速是每秒299,792,458米",
            "🧬 人体大约由37万亿个细胞组成",
            "🌋 火山喷发是地球内部能量释放的表现",
            "🌌 银河系包含约1000-4000亿颗恒星"
        ]
        answer = random.choice(knowledge_list)
        self.add_message("系统", f"🧠 科学知识:\n{answer}", "system")
    
    def creative_inspiration(self):
        """创意启发功能"""
        inspirations = [
            "试着从不同的角度看问题，也许会有新的发现💡",
            "灵感往往来自于日常生活的小细节✨",
            "不要害怕犯错，错误是学习的最佳机会🎯",
            "保持好奇心，探索未知的领域🚀",
            "创意来源于生活的点点滴滴🌟"
        ]
        inspiration = random.choice(inspirations)
        self.add_message("系统", f"🎨 创意启发:\n{inspiration}", "system")
    
    def system_tools(self):
        """系统工具功能"""
        tools_msg = "⚙️ 可用的系统工具:\n"
        tools_msg += "• 🖥️ 系统监控\n• 📁 文件管理\n• 🌐 网络诊断\n• 🔄 进程管理\n• 🔧 注册表编辑"
        self.add_message("系统", tools_msg, "system")
    
    def animate_elements(self):
        """添加动画效果"""
        # 这里可以添加各种动画效果
        pass
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()

def main():
    app = EnhancedGUI()
    app.run()

if __name__ == "__main__":
    main()