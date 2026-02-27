#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
终极AI桌面伴侣启动器 - Ultimate AI Desktop Companion Starter
统一入口，智能启动各种模式
"""

import sys
import os
import importlib.util
import json
from pathlib import Path

class UltimateStarter:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.config = self.load_configuration()
        
    def load_configuration(self):
        """加载配置"""
        config_file = self.project_dir / "ultimate_config.json"
        default_config = {
            "startup_mode": "enhanced_gui",
            "enable_animations": True,
            "performance_level": "high"
        }
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return default_config
        else:
            self.save_configuration(default_config)
            return default_config
    
    def save_configuration(self, config):
        """保存配置"""
        config_file = self.project_dir / "ultimate_config.json"
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def check_environment(self):
        """检查运行环境"""
        print("🔍 正在检查运行环境...")
        
        # 检查必需依赖
        required_packages = ['tkinter', 'PIL', 'psutil']
        missing_packages = []
        
        for package in required_packages:
            try:
                if package == 'PIL':
                    importlib.util.find_spec('PIL')
                else:
                    importlib.util.find_spec(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ 缺失必需包: {', '.join(missing_packages)}")
            print("💡 建议运行: pip install pillow psutil")
            return False
        
        print("✅ 环境检查通过")
        return True
    
    def launch_enhanced_gui(self):
        """启动增强版GUI"""
        print("🚀 正在启动增强版GUI界面...")
        try:
            from enhanced_gui import EnhancedGUI
            app = EnhancedGUI()
            app.run()
        except Exception as e:
            print(f"❌ GUI启动失败: {e}")
            self.launch_console_mode()
    
    def launch_desktop_pet(self):
        """启动桌面宠物"""
        print("🌟 正在启动桌面宠物...")
        try:
            # 优先使用增强版（功能最丰富）
            try:
                from enhanced_desktop_pet import EnhancedDesktopPet
                pet = EnhancedDesktopPet()
                pet.run()
            except ImportError:
                # 回退到简化版
                try:
                    from simple_desktop_pet import SimpleDesktopPet
                    pet = SimpleDesktopPet()
                    pet.run()
                except ImportError:
                    # 最后尝试基础版本
                    from desktop_pet import DesktopPet
                    pet = DesktopPet()
                    pet.run()
        except Exception as e:
            print(f"❌ 桌面宠物启动失败: {e}")
            print("💡 尝试运行基础模式...")
            self.launch_basic_mode()
    
    def launch_console_mode(self):
        """启动控制台模式"""
        print("⌨️ 正在启动控制台模式...")
        try:
            print("=" * 50)
            print("🤖 AI桌面伴侣 控制台模式")
            print("=" * 50)
            print("🌟 欢迎使用AI桌面伴侣！我是您的智能助手。")
            print("输入 'quit' 或 'exit' 退出程序")
            print("-" * 30)
            
            while True:
                try:
                    user_input = input("你: ").strip()
                    
                    if user_input.lower() in ['quit', 'exit', '退出']:
                        print("再见！👋")
                        break
                    
                    if user_input:
                        response = self.generate_simple_response(user_input)
                        print(f"AI助手: {response}")
                        
                except KeyboardInterrupt:
                    print("\n再见！👋")
                    break
                    
        except Exception as e:
            print(f"❌ 控制台模式启动失败: {e}")
    
    def launch_basic_mode(self):
        """启动基础模式"""
        print("🔄 正在启动基础模式...")
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.title("AI桌面伴侣 - 基础模式")
            root.geometry("500x400")
            root.configure(bg='#1a1a2e')
            
            # 标题
            title_label = tk.Label(
                root,
                text="🌟 AI桌面伴侣",
                font=("微软雅黑", 20, "bold"),
                fg='#00ff9d',
                bg='#1a1a2e'
            )
            title_label.pack(pady=30)
            
            # 状态信息
            status_label = tk.Label(
                root,
                text="当前运行基础模式\n部分功能可能受限",
                font=("微软雅黑", 12),
                fg='#4cc9f0',
                bg='#1a1a2e'
            )
            status_label.pack(pady=10)
            
            # 功能按钮
            def show_info():
                info = f"""系统信息：
Python版本: {sys.version.split()[0]}
平台: {sys.platform}
项目路径: {self.project_dir}
工作目录: {os.getcwd()}"""
                messagebox.showinfo("系统信息", info)
            
            def show_features():
                features = """可用功能：
• 基础对话交流
• 简单系统信息
• 离线模式运行

建议：
1. 安装完整依赖包
2. 使用增强GUI模式"""
                messagebox.showinfo("功能说明", features)
            
            tk.Button(
                root,
                text="系统信息 🖥️",
                font=("微软雅黑", 12),
                bg='#4cc9f0',
                fg='white',
                command=show_info,
                width=20,
                height=2
            ).pack(pady=10)
            
            tk.Button(
                root,
                text="功能说明 ℹ️",
                font=("微软雅黑", 12),
                bg='#00ff9d',
                fg='#1a1a2e',
                command=show_features,
                width=20,
                height=2
            ).pack(pady=10)
            
            tk.Button(
                root,
                text="退出程序 🚪",
                font=("微软雅黑", 12),
                bg='#e94560',
                fg='white',
                command=root.destroy,
                width=20,
                height=2
            ).pack(pady=20)
            
            print("✅ 基础模式启动成功")
            root.mainloop()
            
        except Exception as e:
            print(f"❌ 基础模式启动失败: {e}")
    
    def generate_simple_response(self, user_input):
        """生成简单回复"""
        user_input = user_input.lower().strip()
        
        # 问候语
        greetings = {
            "早上好": ["早上好！新的一天开始了呢！😊", "早安！今天也要元气满满哦！", "Good morning！"],
            "下午好": ["下午好！记得休息哦～", "午后时光很美好呢", "下午好呀！"],
            "晚上好": ["晚上好！今天过得怎么样？", "晚安好！准备休息了吗？", "Good evening！"],
            "你好": ["你好呀！很高兴见到你！👋", "Hello！有什么可以帮助你的吗？", "こんにちは！"],
            "再见": ["再见！期待下次见面！😊", "Bye bye！路上小心", "さようなら！"]
        }
        
        for key, responses in greetings.items():
            if key in user_input:
                return random.choice(responses)
        
        # 日常话题
        if "天气" in user_input:
            return "今天的天气真不错呢！☀️"
        elif "心情" in user_input:
            return "我很好呀，谢谢关心！😊"
        elif "时间" in user_input:
            return f"现在是{datetime.now().strftime('%H:%M')}点"
        elif any(word in user_input for word in ["古诗", "诗词"]):
            poetry_list = [
                "春眠不觉晓，处处闻啼鸟。——孟浩然《春晓》",
                "床前明月光，疑是地上霜。——李白《静夜思》"
            ]
            return f"📜 {random.choice(poetry_list)}"
        else:
            responses = [
                "嗯嗯，我明白了～",
                "这真是个有趣的话题！",
                "谢谢你和我分享",
                "让我想想..."
            ]
            return random.choice(responses)
    
    def show_startup_menu(self):
        """显示启动菜单"""
        print("=" * 60)
        print("🤖 AI桌面伴侣 终极版启动器")
        print("=" * 60)
        print("请选择启动模式：")
        print("1. 🌟 增强GUI模式（推荐）- 完整功能体验")
        print("2. 🐱 桌面宠物模式      - 可爱的悬浮伴侣")
        print("3. ⌨️  控制台模式       - 轻量级运行")
        print("4. 🔄 基础模式         - 兜底运行")
        print("5. 🚪 退出程序")
        print("-" * 40)
        
        while True:
            try:
                choice = input("请输入选择 (1-5): ").strip()
                
                if choice == '1':
                    if self.check_environment():
                        self.launch_enhanced_gui()
                    else:
                        print("⚠️ 环境检查未通过，建议选择其他模式")
                elif choice == '2':
                    # 桌面宠物模式不需要复杂环境检查
                    self.launch_desktop_pet()
                elif choice == '3':
                    self.launch_console_mode()
                elif choice == '4':
                    self.launch_basic_mode()
                elif choice == '5':
                    print("👋 再见！")
                    return
                else:
                    print("❌ 无效选择，请重新输入")
                    continue
                
                break
                
            except KeyboardInterrupt:
                print("\n\n👋 程序已退出")
                return
            except Exception as e:
                print(f"❌ 发生错误: {e}")
    
    def run(self):
        """主运行函数"""
        try:
            self.show_startup_menu()
        except Exception as e:
            print(f"❌ 程序运行出错: {e}")
        finally:
            print("🔚 程序结束")

# 导入需要的模块
import random
from datetime import datetime

def main():
    starter = UltimateStarter()
    starter.run()

if __name__ == "__main__":
    main()