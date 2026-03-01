#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏引擎核心类
负责游戏的整体流程控制和状态管理
"""

import time
import random
from typing import Dict, List
from datetime import datetime
from game_modules.cultivation_techniques import TechniqueSystem
from game_modules.sect_system import SectSystem
from game_modules.achievement_system import AchievementSystem
from game_modules.battle_system import BattleSystem
from game_modules.save_system import SaveSystem
from game_modules.ai_guide_system import AIGuideSystem
from game_modules.farming_system import FarmingSystem
from game_modules.story_quest_system import StoryQuestSystem
from game_modules.world_building import WorldBuildingSystem
from game_modules.alchemy_system import AlchemySystem
from game_modules.treasure_system import TreasureSystem

class GameEngine:
    """游戏引擎主类"""
    
    def __init__(self):
        self.running = False
        self.game_time = 0  # 游戏内时间
        self.difficulty = 1  # 难度等级
        self.events_queue = []  # 事件队列
        
        # 初始化功能模块
        self.technique_system = TechniqueSystem()
        self.sect_system = SectSystem()
        self.achievement_system = AchievementSystem()
        self.battle_system = BattleSystem()
        self.save_system = SaveSystem()
        self.ai_guide_system = AIGuideSystem()
        self.farming_system = FarmingSystem()
        self.story_quest_system = StoryQuestSystem()
        self.world_building = WorldBuildingSystem()
        self.alchemy_system = AlchemySystem()
        self.treasure_system = TreasureSystem()
        
    def start_game(self, player, world_sim):
        """开始游戏主循环"""
        self.running = True
        self.player = player
        self.world_sim = world_sim
        
        print(f"\n欢迎 {player.name} 道友进入修仙世界！")
        print("当前境界：凡人")
        
        # 显示世界背景
        self.show_world_background()
        
        # AI引导员首次问候
        guide_greeting = self.ai_guide_system.daily_check_in(player, world_sim.world_state)
        print(f"\n🤖 AI引导员：{guide_greeting}")
        
        print("\n请选择你的初始属性分配：")
        
        # 属性分配
        self.allocate_initial_stats()
        
        # 游戏主循环
        while self.running:
            self.game_loop()
            
    def show_world_background(self):
        """显示世界背景介绍"""
        print("\n" + "="*60)
        print("世界观背景")
        print("="*60)
        world_overview = self.world_building.get_world_overview()
        print(world_overview)
        print("="*60)
        
        # 显示当前重要事件
        current_events = self.world_building.get_dynamic_events()
        print("\n近期重要事件：")
        for event in current_events:
            print(f"  • {event}")
            
    def allocate_initial_stats(self):
        """初始属性分配"""
        total_points = 20
        print(f"你有 {total_points} 点属性点可以分配")
        print("属性包括：体质、灵根、悟性、机缘")
        
        stats = {"体质": 0, "灵根": 0, "悟性": 0, "机缘": 0}
        
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
                
        self.player.stats.update(stats)
        print(f"属性分配完成：{stats}")
        
        # AI引导员点评
        guide = self.ai_guide_system.get_player_guide(self.player.name)
        print(f"\n🤖 {guide.personality['name']}: 属性分配很均衡呢，看得出你是个有想法的修士！")
        
    def game_loop(self):
        """游戏主循环"""
        # 更新农场
        self.farming_system.update_farm(self.game_time, self.player.stats)
        
        # 显示当前状态和AI建议
        self.display_status()
        self.show_ai_guidance()
        
        # 检查成就
        self.check_achievements()
        
        # 检查剧情触发
        self.check_story_triggers()
        
        # 处理玩家行动
        action = self.get_player_action()
        
        # 执行行动
        self.execute_action(action)
        
        # 世界时间推进
        self.advance_time()
        
        # 生成随机事件
        self.generate_events()
        
        # 处理事件队列
        self.process_events()
        
        # 自动保存
        if self.game_time % 20 == 0:  # 每20个回合自动保存
            self.save_system.auto_save(self.player, self.get_game_state())
        
        # 检查游戏结束条件
        if self.check_game_end():
            self.end_game()
            
    def display_status(self):
        """显示游戏状态"""
        print("\n" + "="*50)
        print(f"道士职业：{self.player.name}")
        print(f"境界：{self.player.realm}")
        print(f"修为：{self.player.cultivation}/100")
        print(f"寿元：{self.player.lifetime}年")
        print(f"灵石：{self.player.resources['灵石']}")
        if hasattr(self.player, 'sect') and self.player.sect:
            print(f"门派：{self.player.sect.name}")
        print("="*50)
        
    def show_ai_guidance(self):
        """显示AI引导建议"""
        guide = self.ai_guide_system.get_player_guide(self.player.name)
        suggestions = guide.provide_guidance(self.player, self.world_sim.world_state)
        
        if suggestions:
            print(f"\n🤖 {guide.personality['name']}的建议：")
            for suggestion in suggestions[:2]:  # 只显示前两条建议
                print(f"  {suggestion}")
                
    def get_player_action(self):
        """获取玩家行动选择"""
        actions = {
            "1": "修炼",
            "2": "探索",
            "3": "炼丹",
            "4": "炼器/法宝",
            "5": "与其他修士交流",
            "6": "查看背包",
            "7": "休息",
            "8": "功法系统",
            "9": "门派系统",
            "10": "成就系统",
            "11": "农场系统",
            "12": "任务系统",
            "13": "世界信息",
            "14": "保存游戏",
            "15": "退出游戏"
        }
        
        print("\n可选行动：")
        for key, action in actions.items():
            print(f"{key}. {action}")
            
        while True:
            choice = input("请选择行动 (输入数字): ")
            if choice in actions:
                return actions[choice]
            print("无效选择，请重新输入")
            
    def execute_action(self, action):
        """执行玩家行动"""
        action_map = {
            "修炼": self.player_cultivate,
            "探索": self.explore_world,
            "炼丹": self.alchemy_operation,
            "炼器/法宝": self.treasure_operation,
            "与其他修士交流": self.interact_with_cultivators,
            "查看背包": self.show_inventory,
            "休息": self.rest,
            "功法系统": self.manage_techniques,
            "门派系统": self.manage_sect,
            "成就系统": self.show_achievements,
            "农场系统": self.manage_farm,
            "任务系统": self.manage_quests,
            "世界信息": self.show_world_info,
            "保存游戏": self.save_game,
            "退出游戏": self.quit_game
        }
        
        if action in action_map:
            action_map[action]()
            
    def player_cultivate(self):
        """玩家修炼"""
        self.player.cultivate()
        
        # AI引导员互动
        guide = self.ai_guide_system.get_player_guide(self.player.name)
        response = self.ai_guide_system.contextual_help(self.player, "修炼", self.world_sim.world_state)
        print(f"\n🤖 {guide.personality['name']}: {response}")
        
        # 检查是否触发首次突破剧情
        if self.player.cultivation >= 100:
            self.story_quest_system.trigger_story_event("first_breakthrough", self.player)
            
    def alchemy_operation(self):
        """炼丹操作"""
        self.alchemy_system.alchemy_interface(self.player.name, self.player.stats)
        
    def treasure_operation(self):
        """法宝操作"""
        self.treasure_system.treasure_interface(self.player.name, self.player.stats)
        
    def show_world_info(self):
        """显示世界信息"""
        print("\n=== 修仙世界信息 ===")
        print("1. 世界背景")
        print("2. 势力分布")
        print("3. 地理环境")
        print("4. 历史大事")
        
        choice = input("请选择查看内容: ")
        
        if choice == "1":
            print(self.world_building.get_world_overview())
        elif choice == "2":
            self.show_faction_info()
        elif choice == "3":
            self.show_geography_info()
        elif choice == "4":
            self.show_history_info()
            
    def show_faction_info(self):
        """显示势力信息"""
        print("\n主要修仙势力：")
        factions = self.world_building.factions.factions
        for name, info in list(factions.items())[:5]:  # 显示前5个
            print(f"\n{name}:")
            print(f"  类型：{info['type']}")
            print(f"  特长：{info['specialty']}")
            print(f"  实力：{info['strength']}")
            print(f"  哲学：{info['philosophy']}")
            
    def show_geography_info(self):
        """显示地理信息"""
        print("\n重要地理区域：")
        locations = self.world_building.geography.locations
        for name, info in list(locations.items())[:5]:  # 显示前5个
            print(f"\n{name}:")
            print(f"  类型：{info['type']}")
            print(f"  危险等级：{info['danger_level']}")
            print(f"  主要资源：{', '.join(info['resources'][:2])}")
            print(f"  控制势力：{info['controlled_by']}")
            
    def show_history_info(self):
        """显示历史信息"""
        print("\n重要历史事件：")
        events = self.world_building.history.major_events
        for event in events[-3:]:  # 显示最近3个
            print(f"\n{event['name']} ({event['era']}):")
            print(f"  {event['description']}")
            print(f"  影响：{event['impact']}")
            
    def manage_farm(self):
        """管理农场系统"""
        print("\n=== 灵田管理系统 ===")
        print("1. 查看农场状态")
        print("2. 种植作物")
        print("3. 农事操作")
        print("4. 收获作物")
        
        choice = input("请选择操作: ")
        
        if choice == "1":
            self.farming_system.show_farm_status()
            
        elif choice == "2":
            self.farming_system.plant_operation(self.player.stats)
            
        elif choice == "3":
            print("农事操作：")
            print("1. 浇水  2. 施肥  3. 除草")
            op_choice = input("选择操作: ")
            operations = {"1": "浇水", "2": "施肥", "3": "除草"}
            if op_choice in operations:
                self.farming_system.farming_operations(operations[op_choice], self.player.stats)
                
        elif choice == "4":
            rewards = self.farming_system.harvest_operation()
            # 这里应该添加奖励到玩家资源中
            
    def manage_quests(self):
        """管理任务系统"""
        print("\n=== 任务系统 ===")
        print("1. 查看任务状态")
        print("2. 接受新任务")
        print("3. 查看剧情进展")
        
        choice = input("请选择操作: ")
        
        if choice == "1":
            self.story_quest_system.show_quest_status()
            
        elif choice == "2":
            available = self.story_quest_system.get_available_quests(self.player)
            if available:
                print("可接任务：")
                for i, quest in enumerate(available[:3], 1):  # 显示前3个
                    print(f"{i}. {quest.title}")
                    print(f"   {quest.description}")
                try:
                    idx = int(input("选择任务编号: ")) - 1
                    if 0 <= idx < len(available):
                        if self.story_quest_system.accept_quest(available[idx].quest_id):
                            print("任务接受成功！")
                        else:
                            print("任务接受失败")
                except ValueError:
                    print("输入无效")
            else:
                print("暂无可接任务")
                
        elif choice == "3":
            # 显示当前剧情进展
            flags = self.story_quest_system.story_flags
            print("剧情进展：")
            for flag, status in flags.items():
                if status:
                    print(f"  ✓ {flag}")
                    
    def manage_techniques(self):
        """管理功法系统"""
        print("\n=== 功法系统 ===")
        print("1. 查看已学功法")
        print("2. 学习新功法")
        print("3. 练习功法")
        
        choice = input("请选择操作: ")
        
        if choice == "1":
            # 显示已学功法
            if self.technique_system.learned_techniques:
                print("已学功法：")
                for name, technique in self.technique_system.learned_techniques.items():
                    print(f"  {name} (掌握度: {technique.mastery}%)")
            else:
                print("暂无已学功法")
                
        elif choice == "2":
            # 学习新功法
            available = self.technique_system.get_available_techniques(self.player)
            if available:
                print("可学习功法：")
                for i, tech in enumerate(available, 1):
                    print(f"{i}. {tech}")
                try:
                    idx = int(input("选择要学习的功法: ")) - 1
                    if 0 <= idx < len(available):
                        self.technique_system.learn_technique(available[idx], self.player)
                except ValueError:
                    print("输入无效")
            else:
                print("暂无可学习的功法")
                
        elif choice == "3":
            # 练习功法
            if self.technique_system.learned_techniques:
                techniques = list(self.technique_system.learned_techniques.keys())
                print("已学功法：")
                for i, tech in enumerate(techniques, 1):
                    print(f"{i}. {tech}")
                try:
                    idx = int(input("选择要练习的功法: ")) - 1
                    if 0 <= idx < len(techniques):
                        hours = int(input("练习时长(小时): "))
                        self.technique_system.practice_technique(techniques[idx], self.player, hours)
                except ValueError:
                    print("输入无效")
            else:
                print("暂无已学功法可练习")
                
    def manage_sect(self):
        """管理门派系统"""
        print("\n=== 门派系统 ===")
        print("1. 查看门派信息")
        print("2. 加入门派")
        print("3. 门派任务")
        print("4. 门派兑换")
        
        choice = input("请选择操作: ")
        
        if choice == "1":
            # 查看门派信息
            sects = self.sect_system.list_all_sects()
            print("各大门派：")
            for sect in sects:
                status = "✓ 已加入" if hasattr(self.player, 'sect') and self.player.sect == sect else "✗ 未加入"
                print(f"  {sect.name} [{sect.type}] - 声望:{sect.reputation} {status}")
                
        elif choice == "2":
            # 加入门派
            if hasattr(self.player, 'sect') and self.player.sect:
                print(f"你已经是{self.player.sect.name}的弟子了")
            else:
                available_sects = self.sect_system.get_available_sects(self.player)
                if available_sects:
                    print("可加入的门派：")
                    for i, sect in enumerate(available_sects, 1):
                        print(f"{i}. {sect.name} [{sect.type}] - 声望:{sect.reputation}")
                    try:
                        idx = int(input("选择要加入的门派: ")) - 1
                        if 0 <= idx < len(available_sects):
                            available_sects[idx].join_sect(self.player)
                    except ValueError:
                        print("输入无效")
                else:
                    print("暂无可加入的门派")
                    
        elif choice == "3":
            # 门派任务
            if hasattr(self.player, 'sect') and self.player.sect:
                self.player.sect.sect_task(self.player)
            else:
                print("你还不是任何门派的弟子")
                
        elif choice == "4":
            # 门派兑换
            if hasattr(self.player, 'sect') and self.player.sect:
                print("可兑换物品：丹药(50贡献点) 法器(100贡献点) 秘籍(200贡献点)")
                item = input("请输入要兑换的物品: ")
                self.player.sect.sect_exchange(self.player, item)
            else:
                print("你还不是任何门派的弟子")
                
    def show_achievements(self):
        """显示成就系统"""
        self.achievement_system.show_achievements(self.player)
        
    def save_game(self):
        """保存游戏"""
        save_name = input("请输入存档名称(留空使用默认名称): ")
        if not save_name:
            save_name = None
        self.save_system.save_game(self.player, self.get_game_state(), save_name)
        
    def quit_game(self):
        """退出游戏"""
        confirm = input("确定要退出游戏吗？(y/n): ")
        if confirm.lower() == 'y':
            self.running = False
            print("游戏已保存并退出")
            
    def check_achievements(self):
        """检查成就解锁"""
        unlocked = self.achievement_system.check_achievements(self.player)
        return unlocked
        
    def advance_time(self):
        """推进游戏时间"""
        self.game_time += 1
        self.player.lifetime += 1
        
        # 定期更新世界状态
        if self.game_time % 10 == 0:
            self.world_sim.update_world_state()
            
    def generate_events(self):
        """生成随机事件"""
        # 基于概率生成事件
        event_chance = random.random()
        
        if event_chance < 0.15:  # 15%概率
            events = [
                "发现灵草",
                "遇到同门师兄弟",
                "天降机缘",
                "遭遇妖兽",
                "心境波动",
                "神秘商人出现",
                "古遗迹现世",
                "天地异象"
            ]
            event = random.choice(events)
            self.events_queue.append({
                'type': event,
                'time': self.game_time,
                'processed': False
            })
            
    def process_events(self):
        """处理事件队列"""
        for event in self.events_queue:
            if not event['processed']:
                self.handle_event(event)
                event['processed'] = True
                
        # 清理已处理事件
        self.events_queue = [e for e in self.events_queue if not e['processed']]
        
    def handle_event(self, event):
        """处理具体事件"""
        event_type = event['type']
        print(f"\n【事件】{event_type}")
        
        if event_type == "发现灵草":
            reward = random.randint(10, 50)
            self.player.add_resource('灵石', reward)
            print(f"获得灵石 {reward} 枚")
            
        elif event_type == "遇到同门师兄弟":
            print("与同门交流心得，悟性+1")
            self.player.stats['悟性'] += 1
            
        elif event_type == "天降机缘":
            print("机缘巧合，修为大增！")
            self.player.cultivation += random.randint(5, 15)
            
        elif event_type == "遭遇妖兽":
            print("遇到强大的妖兽！")
            # 触发战斗
            enemy = {
                'name': '三眼狼妖',
                'realm': '练气期'
            }
            victory = self.battle_system.start_battle(self.player, enemy)
            if victory:
                print("战胜妖兽，获得丰厚奖励！")
            else:
                print("败给妖兽，需要休养恢复...")
                
        elif event_type == "心境波动":
            print("心境不稳，修炼效率下降...")
            # 可以添加临时debuff
            
        elif event_type == "神秘商人出现":
            print("神秘商人出现，可购买稀有物品")
            # 可以添加商店功能
            
        elif event_type == "古遗迹现世":
            print("发现古老遗迹，内藏珍宝")
            # 可以添加探索功能
            
        elif event_type == "天地异象":
            print("天地异象显现，灵气大增")
            self.player.cultivation += 10
            
    def explore_world(self):
        """探索世界（增强版）"""
        print("你开始探索周围的环境...")
        time.sleep(1)
        
        # 获取可前往的地点
        locations = self.world_sim.get_available_locations()
        print("可探索地点：")
        for i, location in enumerate(locations, 1):
            print(f"{i}. {location}")
            
        try:
            choice = int(input("选择探索地点: ")) - 1
            if 0 <= choice < len(locations):
                location = locations[choice]
                print(f"前往 {location} 探索...")
                
                # 不同地点有不同的发现概率
                discoveries = {
                    "青云山脉": ["灵草", "矿石", "古洞府", "野生妖兽"],
                    "幽冥谷": ["阴属性材料", "鬼物", "禁制", "古老墓穴"],
                    "天机城": ["功法秘籍", "法宝", "情报", "神秘商人"],
                    "万宝阁": ["珍稀材料", "古董", "拍卖会", "特殊任务"],
                    "紫霄宫": ["仙缘", "高深功法", "仙器", "长老指点"],
                    "血魔宗": ["魔道功法", "邪器", "危险机遇", "黑暗交易"]
                }
                
                possible_discoveries = discoveries.get(location, ["普通材料", "灵石", "小妖"])
                discovery = random.choice(possible_discoveries)
                
                print(f"在{location}发现了{discovery}")
                
                # 根据发现给予奖励和触发事件
                if "灵石" in discovery:
                    reward = random.randint(20, 100)
                    self.player.add_resource('灵石', reward)
                    print(f"获得灵石 {reward} 枚")
                    
                elif "灵草" in discovery or "材料" in discovery:
                    self.player.add_resource('灵药', 1)
                    # 更新任务进度
                    self.story_quest_system.update_quest_progress("collect_herbs")
                    
                elif "功法" in discovery:
                    print("获得了珍贵的修炼心得")
                    self.player.stats['悟性'] += 1
                    
                elif "法宝" in discovery or "法器" in discovery:
                    self.player.add_resource('法器', 1)
                    
                elif "野生妖兽" in discovery or "小妖" in discovery:
                    print("遭遇了妖兽！")
                    enemy = {'name': '山中妖兽', 'realm': '练气期'}
                    victory = self.battle_system.start_battle(self.player, enemy)
                    if victory:
                        print("战胜妖兽，获得战利品！")
                        self.player.add_resource('灵石', random.randint(30, 80))
                        self.story_quest_system.update_quest_progress("defeat_wolf")
                    else:
                        print("败给妖兽，需要休养恢复...")
                        
                elif "特殊任务" in discovery:
                    print("触发了特殊任务！")
                    # 可以在这里添加特殊任务逻辑
                    
                # AI引导员评论
                guide = self.ai_guide_system.get_player_guide(self.player.name)
                comment = self.ai_guide_system.emotional_response(self.player, "发现宝藏" if "灵石" in discovery else "遇到危险")
                print(f"\n🤖 {guide.personality['name']}: {comment}")
                
        except ValueError:
            print("输入无效")
            
    def check_story_triggers(self):
        """检查剧情触发条件"""
        # 检查首次战斗
        if self.game_time > 5 and not self.story_quest_system.story_flags.get("first_combat"):
            self.story_quest_system.trigger_story_event("first_blood", self.player)
            
        # 检查门派选择
        if hasattr(self.player, 'sect') and self.player.sect:
            self.story_quest_system.trigger_story_event("sect_choice", self.player)
            
    def alchemy(self):
        """炼丹"""
        if self.player.resources.get('灵药', 0) > 0:
            print("开始炼制丹药...")
            success_rate = 0.6 + (self.player.stats['悟性'] * 0.05)
            
            if random.random() < success_rate:
                print("炼丹成功！获得丹药")
                self.player.add_resource('丹药', 1)
                self.player.resources['灵药'] -= 1
            else:
                print("炼丹失败...")
                self.player.resources['灵药'] -= 1
        else:
            print("没有足够的灵药进行炼丹")
            
    def crafting(self):
        """炼器"""
        print("炼器功能暂未开放")
        
    def interact_with_cultivators(self):
        """与其他修士交流"""
        print("与其他修士交流中...")
        nearby_cultivators = self.world_sim.get_nearby_cultivators()
        
        if nearby_cultivators:
            print("附近有以下修士：")
            for i, npc in enumerate(nearby_cultivators, 1):
                print(f"{i}. {npc['name']} ({npc['realm']}) - {npc['personality']}")
                
            try:
                choice = int(input("选择交流对象: ")) - 1
                if 0 <= choice < len(nearby_cultivators):
                    npc = nearby_cultivators[choice]
                    print(f"与{npc['name']}交流...")
                    
                    # 根据性格和境界产生不同结果
                    if npc['personality'] == '友善':
                        cultivation_gain = 3 + self.player.stats['悟性'] // 2
                        self.player.cultivation += cultivation_gain
                        print(f"友好交流，修为+{cultivation_gain}")
                    elif npc['personality'] == '正直':
                        print("获得修炼心得指导")
                        self.player.stats['悟性'] += 1
                    elif npc['personality'] == '狡诈':
                        if random.random() < 0.3:
                            print("被骗失去了一些资源...")
                            loss = min(30, self.player.resources['灵石'])
                            self.player.resources['灵石'] -= loss
                        else:
                            print("识破对方诡计，心境提升")
                            self.player.cultivation += 5
                    else:  # 冷漠
                        print("对方不愿交流")
                        
            except ValueError:
                print("输入无效")
        else:
            print("附近没有其他修士")
            
    def show_inventory(self):
        """显示背包"""
        print("\n=== 背包 ===")
        for item, count in self.player.resources.items():
            if count > 0:
                print(f"{item}: {count}")
                
        # 显示贡献点（如果有门派）
        if hasattr(self.player, 'sect') and self.player.sect:
            contribution = self.player.resources.get('贡献点', 0)
            print(f"贡献点: {contribution}")
            
    def rest(self):
        """休息恢复"""
        recovery = 5 + self.player.stats['体质'] // 2
        self.player.cultivation = min(100, self.player.cultivation + recovery)
        print(f"休息后恢复修为 {recovery} 点")
        
    def get_game_state(self):
        """获取游戏状态用于保存"""
        return {
            'game_time': self.game_time,
            'difficulty': self.difficulty,
            'world_state': self.world_sim.world_state,
            'story_flags': self.story_quest_system.story_flags,
            'completed_quests': [q.quest_id for q in self.story_quest_system.completed_quests],
            'world_context': self.world_building.world_context
        }
        
    def check_game_end(self):
        """检查游戏结束条件"""
        # 寿元耗尽
        if self.player.lifetime >= 1000:  # 延长寿元限制
            return True
        # 达到最高境界
        if self.player.realm == "渡劫期" and self.player.cultivation >= 100:
            return True
        return False
        
    def end_game(self):
        """结束游戏"""
        self.running = False
        print("\n" + "="*40)
        print("游戏结束！")
        
        if self.player.realm == "渡劫期":
            print("恭喜你成功飞升仙界！")
        else:
            print("寿元已尽，轮回转世...")
            
        print(f"最终境界：{self.player.realm}")
        print(f"最终修为：{self.player.cultivation}")
        print(f"游戏时长：{self.player.lifetime}年")
        print("="*40)
        
        # 显示最终成就
        unlocked_count = len(self.achievement_system.get_unlocked_achievements())
        total_count = len(self.achievement_system.achievements)
        print(f"成就完成度：{unlocked_count}/{total_count}")