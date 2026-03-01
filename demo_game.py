#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修仙游戏完整演示脚本
展示所有游戏功能
"""

import sys
import os
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_core.game_engine import GameEngine
from game_core.player import Player
from game_core.world_simulator import WorldSimulator
from game_utils.simple_gui import gui

def demo_game():
    """游戏演示"""
    print("道士职业模拟器 - 完整演示版")
    print("=" * 50)
    
    # 创建游戏角色
    player_name = "测试修士"
    player = Player(player_name)
    
    # 设置初始属性（演示用）
    player.stats = {"体质": 8, "灵根": 7, "悟性": 6, "机缘": 5}
    
    # 初始化游戏引擎
    game_engine = GameEngine()
    world_sim = WorldSimulator()
    
    print(f"欢迎 {player_name} 道友！")
    print("这是修仙游戏的功能演示...")
    
    # 演示各种功能
    demo_functions = [
        ("修炼系统", lambda: demo_cultivation(player)),
        ("功法系统", lambda: demo_techniques(game_engine, player)),
        ("门派系统", lambda: demo_sect_system(game_engine, player)),
        ("战斗系统", lambda: demo_battle_system(game_engine, player)),
        ("成就系统", lambda: demo_achievements(game_engine, player)),
        ("世界探索", lambda: demo_exploration(game_engine, player, world_sim))
    ]
    
    for func_name, func in demo_functions:
        print(f"\n{'='*20} {func_name} 演示 {'='*20}")
        try:
            func()
            input("\n按回车键继续...")
        except Exception as e:
            print(f"演示出错: {e}")
            
    print("\n演示结束！感谢体验道士职业模拟器！")

def demo_cultivation(player):
    """演示修炼系统"""
    print("基础修炼演示：")
    print(f"初始境界: {player.realm}")
    print(f"初始修为: {player.cultivation}")
    
    # 模拟几次修炼
    for i in range(3):
        player.cultivate()
        print(f"第{i+1}次修炼后: {player.realm} - 修为 {player.cultivation}")
        
def demo_techniques(game_engine, player):
    """演示功法系统"""
    print("功法系统演示：")
    
    # 学习一个基础功法
    available = game_engine.technique_system.get_available_techniques(player)
    if available:
        print(f"可学习功法: {available[0]}")
        game_engine.technique_system.learn_technique(available[0], player)
        
        # 练习功法
        game_engine.technique_system.practice_technique(available[0], player, 2)
        
def demo_sect_system(game_engine, player):
    """演示门派系统"""
    print("门派系统演示：")
    
    # 显示可加入的门派
    sects = game_engine.sect_system.list_all_sects()
    print("各大门派:")
    for sect in sects[:2]:  # 只显示前两个
        print(f"  {sect.name} - {sect.type}")
        
    # 模拟加入门派
    if sects and player.realm != "凡人":
        print(f"模拟加入 {sects[0].name}")
        # 这里简化处理，实际需要满足条件
        
def demo_battle_system(game_engine, player):
    """演示战斗系统"""
    print("战斗系统演示：")
    
    enemy = {
        'name': '测试妖兽',
        'realm': '练气期'
    }
    
    print("模拟一场简单战斗...")
    # 这里不实际执行战斗，只是展示
    
def demo_achievements(game_engine, player):
    """演示成就系统"""
    print("成就系统演示：")
    
    # 检查当前成就
    unlocked = game_engine.achievement_system.get_unlocked_achievements()
    locked = game_engine.achievement_system.get_locked_achievements()
    
    print(f"已解锁成就数: {len(unlocked)}")
    print(f"可达成成就数: {len(locked)}")
    
    if locked:
        print("即将可达成的成就:")
        for ach in locked[:2]:
            print(f"  {ach.name}: {ach.description}")
            
def demo_exploration(game_engine, player, world_sim):
    """演示探索系统"""
    print("世界探索演示：")
    
    # 显示可探索地点
    locations = world_sim.get_available_locations()
    print("可探索地点:")
    for loc in locations[:3]:
        print(f"  {loc}")
        
    # 模拟探索
    print("模拟探索青云山脉...")
    discoveries = ["灵草", "古洞府", "灵石"]
    import random
    discovery = random.choice(discoveries)
    print(f"发现: {discovery}")

if __name__ == "__main__":
    demo_game()