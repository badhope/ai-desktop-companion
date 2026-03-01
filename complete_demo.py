#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整系统演示脚本
展示所有深化的修仙系统和世界观
"""

import sys
import os
import time
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def complete_demo():
    """完整系统演示"""
    print("道士职业模拟器 - 完整系统演示")
    print("=" * 60)
    
    # 演示各个系统
    demo_modules = [
        ("世界观构建系统", demo_world_building),
        ("炼丹系统", demo_alchemy_system),
        ("法宝系统", demo_treasure_system),
        ("AI引导系统", demo_ai_guide),
        ("剧情任务系统", demo_story_system)
    ]
    
    for module_name, demo_func in demo_modules:
        print(f"\n{'='*20} {module_name} 演示 {'='*20}")
        try:
            demo_func()
            input("\n按回车键继续...")
        except Exception as e:
            print(f"演示出错: {e}")
            
    print("\n演示结束！感谢体验完整的道士职业模拟器！")

def demo_world_building():
    """演示世界观构建系统"""
    from game_modules.world_building import WorldBuildingSystem
    
    print("构建修仙世界背景...")
    world_builder = WorldBuildingSystem()
    
    # 显示世界概况
    overview = world_builder.get_world_overview()
    print(overview)
    
    # 显示重要事件
    print("\n当前重要事件：")
    events = world_builder.get_dynamic_events()
    for event in events:
        print(f"  • {event}")
        
    # 显示势力信息
    print("\n主要势力：")
    factions = world_builder.factions.factions
    for name, info in list(factions.items())[:3]:
        print(f"  {name}: {info['type']} - {info['strength']}")
        
    # 显示地理信息
    print("\n重要地点：")
    locations = world_builder.geography.locations
    for name, info in list(locations.items())[:3]:
        print(f"  {name}: {info['type']} - 危险等级{info['danger_level']}")

def demo_alchemy_system():
    """演示炼丹系统"""
    from game_modules.alchemy_system import AlchemySystem
    
    print("初始化炼丹系统...")
    alchemy = AlchemySystem()
    
    # 创建测试炼丹师
    alchemist = alchemy.get_player_alchemist("测试修士")
    alchemist.alchemy_level = 3  # 提高等级以便演示
    
    print(f"炼丹师等级：{alchemist.alchemy_level}")
    print(f"控火能力：{alchemist.fire_control}")
    print(f"炼丹运气：{alchemist.luck}")
    
    # 显示可学丹方
    print("\n可学习的基础丹方：")
    basic_formulas = ["聚气丹", "凝神丹", "筑基丹"]
    for formula_name in basic_formulas:
        if formula_name in alchemy.formulas:
            formula = alchemy.formulas[formula_name]
            print(f"  {formula.name} (等级{formula.level})")
            print(f"    需要：{', '.join([f'{name}×{qty}' for name, qty in formula.ingredients])}")
            print(f"    效果：{formula.effects}")
            print()
            
    # 演示学习丹方
    print("演示学习聚气丹丹方...")
    if alchemist.learn_formula(alchemy.formulas["聚气丹"]):
        print("✓ 学习成功！")
        
    # 演示控火练习
    print("\n演示控火练习...")
    alchemist.improve_fire_control(2)
    print(f"控火能力提升至：{alchemist.fire_control:.1f}")

def demo_treasure_system():
    """演示法宝系统"""
    from game_modules.treasure_system import TreasureSystem, TreasureCollection
    
    print("初始化法宝系统...")
    treasure_sys = TreasureSystem()
    
    # 创建测试收藏
    collection = TreasureCollection()
    
    # 演示寻找法宝
    print("\n演示寻找法宝...")
    test_treasures = ["青锋剑", "混元盾", "遁天梭"]
    for treasure_name in test_treasures:
        if treasure_name in treasure_sys.treasure_database:
            treasure = treasure_sys.treasure_database[treasure_name]
            collection.add_treasure(treasure)
            
    # 显示收藏
    print("\n法宝收藏：")
    collection.show_collection()
    
    # 显示总威力
    print(f"总威力评分：{collection.get_total_power()}")
    
    # 演示精炼
    print("\n演示法宝精炼...")
    weapon = collection.collection["武器"][0]  # 取第一个武器
    print(f"精炼前等级：{weapon.refinement_level}")
    
    # 模拟精炼过程
    if weapon.can_refine():
        weapon.refinement_level += 1
        print(f"精炼后等级：{weapon.refinement_level}")
        print("✓ 精炼成功！")

def demo_ai_guide():
    """演示AI引导系统"""
    from game_modules.ai_guide_system import AIGuideSystem
    
    print("初始化AI引导系统...")
    ai_guide = AIGuideSystem()
    
    # 创建测试玩家状态
    class TestPlayer:
        def __init__(self):
            self.name = "测试修士"
            self.realm = "练气期"
            self.cultivation = 45
            self.resources = {'灵石': 30}
            self.stats = {'体质': 6, '灵根': 7, '悟性': 5, '机缘': 4}
            
    player = TestPlayer()
    
    # 获取AI引导员
    guide = ai_guide.get_player_guide(player.name)
    print(f"AI引导员：{guide.personality['name']}")
    print(f"引导风格：{guide.personality['style']}")
    
    # 模拟世界状态
    world_state = {
        '灵气浓度': 65,
        'season': '春季',
        'weather': '晴朗'
    }
    
    # 获取建议
    print("\nAI建议：")
    suggestions = guide.provide_guidance(player, world_state)
    for suggestion in suggestions[:3]:
        print(f"  {suggestion}")
        
    # 情感回应演示
    print("\n情感回应演示：")
    responses = [
        ("胜利", "太棒了！我就知道你能行的！"),
        ("发现宝藏", "哇！发财了发财了！"),
        ("遇到危险", "小心点啊！安全第一！")
    ]
    
    for event_type, expected in responses:
        response = ai_guide.emotional_response(player, event_type)
        print(f"  {event_type}: {response}")

def demo_story_system():
    """演示剧情任务系统"""
    from game_modules.story_quest_system import StoryQuestSystem
    
    print("初始化剧情任务系统...")
    story_sys = StoryQuestSystem()
    
    # 创建测试玩家
    class TestPlayer:
        def __init__(self):
            self.name = "测试修士"
            self.realm = "练气期"
            
    player = TestPlayer()
    
    # 显示可用任务
    print("\n可接任务：")
    available_quests = story_sys.get_available_quests(player)
    for quest in available_quests[:3]:
        print(f"  {quest.title}")
        print(f"    {quest.description}")
        print()
        
    # 显示任务状态
    print("任务面板：")
    story_sys.show_quest_status()
    
    # 演示接受任务
    print("\n演示接受任务...")
    if available_quests:
        quest_id = available_quests[0].quest_id
        if story_sys.accept_quest(quest_id):
            print(f"✓ 成功接受任务：{available_quests[0].title}")
            
    # 演示剧情触发
    print("\n演示剧情触发...")
    story_sys.trigger_story_event("first_blood", player)
    print("✓ 首次战斗剧情触发")

if __name__ == "__main__":
    complete_demo()