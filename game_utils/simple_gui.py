#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简易图形界面模块
提供基本的文本界面美化功能
"""

import os
import time
from typing import List, Dict

class SimpleGUI:
    """简易图形界面"""
    
    def __init__(self):
        self.clear_screen()
        
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_header(self, title: str):
        """打印标题栏"""
        width = 50
        print("=" * width)
        print(f"{title:^{width}}")
        print("=" * width)
        
    def print_box(self, content: str):
        """打印带边框的内容"""
        lines = content.split('\n')
        max_length = max(len(line) for line in lines) + 4
        
        print("+" + "-" * (max_length - 2) + "+")
        for line in lines:
            print(f"| {line:<{max_length-4}} |")
        print("+" + "-" * (max_length - 2) + "+")
        
    def print_progress_bar(self, current: int, total: int, width: int = 30):
        """打印进度条"""
        progress = current / total if total > 0 else 0
        filled = int(width * progress)
        bar = "█" * filled + "░" * (width - filled)
        percent = progress * 100
        print(f"[{bar}] {percent:.1f}% ({current}/{total})")
        
    def print_colored_text(self, text: str, color: str = "white"):
        """打印彩色文本（简化版）"""
        colors = {
            "red": "\033[91m",
            "green": "\033[92m", 
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "purple": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
            "reset": "\033[0m"
        }
        
        # 简化处理，实际使用时可能需要检查终端支持
        try:
            print(f"{colors.get(color, '')}{text}{colors['reset']}")
        except:
            print(text)  # 如果不支持颜色则正常打印
            
    def show_main_menu(self) -> str:
        """显示主菜单"""
        self.clear_screen()
        self.print_header("道士职业模拟器")
        
        menu_items = [
            "1. 新游戏",
            "2. 读取存档", 
            "3. 游戏设置",
            "4. 退出游戏"
        ]
        
        print("\n请选择:")
        for item in menu_items:
            print(f"  {item}")
            
        return input("\n请输入选择: ").strip()
        
    def show_character_creation(self) -> Dict[str, any]:
        """显示角色创建界面"""
        self.clear_screen()
        self.print_header("创建角色")
        
        # 获取角色名
        name = input("请输入你的道号: ").strip()
        if not name:
            name = "无名修士"
            
        # 属性分配
        total_points = 20
        stats = {"体质": 0, "灵根": 0, "悟性": 0, "机缘": 0}
        
        print(f"\n你有 {total_points} 点属性点可以分配")
        print("属性说明：")
        print("  体质 - 影响生命值和恢复速度")
        print("  灵根 - 影响灵气吸收效率") 
        print("  悟性 - 影响学习和领悟速度")
        print("  机缘 - 影响奇遇概率\n")
        
        for stat in stats:
            while True:
                try:
                    points = int(input(f"{stat} 分配点数 (剩余{total_points}点): "))
                    if 0 <= points <= total_points:
                        stats[stat] = points
                        total_points -= points
                        break
                    else:
                        print("输入无效，请重新输入")
                except ValueError:
                    print("请输入数字")
                    
            if total_points == 0:
                break
                
        return {
            'name': name,
            'stats': stats
        }
        
    def show_game_interface(self, player, world_state):
        """显示游戏主界面"""
        self.clear_screen()
        
        # 顶部状态栏
        self.print_header(f"道士职业模拟器 - {player.name}")
        
        # 玩家状态
        status_lines = [
            f"境界: {player.realm}",
            f"修为: {player.cultivation}/100",
            f"寿元: {player.lifetime}年",
            f"灵石: {player.resources['灵石']}"
        ]
        
        if hasattr(player, 'sect') and player.sect:
            status_lines.append(f"门派: {player.sect.name}")
            
        status_text = "\n".join(status_lines)
        self.print_box(status_text)
        
        # 世界状态
        world_lines = [
            f"季节: {world_state['season']}",
            f"天气: {world_state['weather']}", 
            f"灵气浓度: {world_state['灵气浓度']}"
        ]
        world_text = "\n".join(world_lines)
        print("\n世界状态:")
        self.print_box(world_text)
        
    def show_loading_screen(self, message: str = "加载中"):
        """显示加载界面"""
        self.clear_screen()
        self.print_header("Loading...")
        print(f"\n{message}")
        print("请稍候...")
        
    def pause(self, message: str = "按回车键继续..."):
        """暂停等待用户输入"""
        input(message)
        
    def show_message(self, message: str, msg_type: str = "info"):
        """显示消息"""
        type_icons = {
            "info": "[ℹ]",
            "success": "[✓]", 
            "warning": "[!]",
            "error": "[✗]"
        }
        
        icon = type_icons.get(msg_type, "[?]")
        print(f"{icon} {message}")

# 全局GUI实例
gui = SimpleGUI()