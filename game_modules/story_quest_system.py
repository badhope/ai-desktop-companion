#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剧情任务系统
提供丰富的剧情线和任务链
"""

import random
from typing import Dict, List, Callable
from datetime import datetime

class Quest:
    """任务类"""
    
    def __init__(self, quest_id: str, title: str, description: str, 
                 objectives: List[Dict], rewards: Dict, 
                 prerequisites: List[str] = None):
        self.quest_id = quest_id
        self.title = title
        self.description = description
        self.objectives = objectives  # 任务目标列表
        self.rewards = rewards        # 奖励
        self.prerequisites = prerequisites or []  # 前置任务
        self.status = "available"     # available, active, completed, failed
        self.progress = {}           # 任务进度
        self.accept_time = None      # 接受时间
        
    def can_accept(self, completed_quests: List[str]) -> bool:
        """检查是否可以接受任务"""
        return all(prereq in completed_quests for prereq in self.prerequisites)
        
    def start_quest(self):
        """开始任务"""
        self.status = "active"
        self.accept_time = datetime.now()
        self.progress = {obj['id']: 0 for obj in self.objectives}
        print(f"📋 任务已接受：{self.title}")
        print(f"📝 任务描述：{self.description}")
        
    def update_progress(self, objective_id: str, amount: int = 1):
        """更新任务进度"""
        if self.status == "active" and objective_id in self.progress:
            self.progress[objective_id] += amount
            
    def check_completion(self) -> bool:
        """检查任务是否完成"""
        if self.status != "active":
            return False
            
        for obj in self.objectives:
            obj_id = obj['id']
            required = obj['required']
            current = self.progress.get(obj_id, 0)
            if current < required:
                return False
                
        self.status = "completed"
        return True
        
    def get_rewards(self) -> Dict:
        """获取任务奖励"""
        return self.rewards.copy()

class StoryQuestSystem:
    """剧情任务系统"""
    
    def __init__(self):
        self.quests = self._initialize_quests()
        self.active_quests = []
        self.completed_quests = []
        self.story_flags = {}  # 故事标志位
        
    def _initialize_quests(self) -> Dict[str, Quest]:
        """初始化所有任务"""
        quests = {
            # 新手村任务线
            "q001_find_master": Quest(
                "q001_find_master",
                "寻找师父",
                "初入仙途的小修士需要找到一位师父指导修炼",
                [
                    {"id": "find_npc", "required": 1, "desc": "找到玄机老人"}
                ],
                {"灵石": 50, "经验值": 20, "next_quest": "q002_first_trial"}
            ),
            
            "q002_first_trial": Quest(
                "q002_first_trial", 
                "入门试炼",
                "通过师父的入门试炼，证明自己的资质",
                [
                    {"id": "collect_herbs", "required": 3, "desc": "收集3株聚灵草"},
                    {"id": "defeat_wolf", "required": 1, "desc": "击败一只三眼狼妖"}
                ],
                {"灵石": 100, "功法": "长春功", "next_quest": "q003_join_sect"},
                ["q001_find_master"]
            ),
            
            "q003_join_sect": Quest(
                "q003_join_sect",
                "选择门派",
                "在各大门派中选择一个加入，开始真正的修仙之路",
                [
                    {"id": "join_sect", "required": 1, "desc": "加入任意一个门派"}
                ],
                {"灵石": 150, "贡献点": 50, "法器": 1},
                ["q002_first_trial"]
            ),
            
            # 主线剧情
            "q010_ancient_secret": Quest(
                "q010_ancient_secret",
                "古老秘密",
                "在青云山脉深处发现了一个古老的洞府遗迹",
                [
                    {"id": "explore_mountain", "required": 1, "desc": "深入青云山脉探索"},
                    {"id": "solve_puzzle", "required": 1, "desc": "解开洞府封印"}
                ],
                {"灵石": 300, "古籍": 1, "机缘": 3},
                ["q003_join_sect"]
            ),
            
            "q020_sect_conflict": Quest(
                "q020_sect_conflict",
                "门派纷争",
                "卷入门派之间的利益冲突，需要做出选择",
                [
                    {"id": "gather_intelligence", "required": 3, "desc": "收集各方情报"},
                    {"id": "make_choice", "required": 1, "desc": "在两派之间做出立场选择"}
                ],
                {"声望": 20, "法器": 2, "next_quest": "q021_final_test"},
                ["q010_ancient_secret"]
            ),
            
            "q021_final_test": Quest(
                "q021_final_test",
                "终极考验",
                "面对修仙路上的最大挑战",
                [
                    {"id": "defeat_boss", "required": 1, "desc": "击败强大的敌人"},
                    {"id": "protect_friend", "required": 1, "desc": "保护重要的人"}
                ],
                {"灵石": 500, "境界突破": 1, "传说功法": 1},
                ["q020_sect_conflict"]
            ),
            
            # 支线任务
            "q101_lost_apprentice": Quest(
                "q101_lost_apprentice",
                "失踪的弟子",
                "帮助寻找走失的同门师兄弟",
                [
                    {"id": "search_locations", "required": 3, "desc": "搜索3个可疑地点"},
                    {"id": "rescue_apprentice", "required": 1, "desc": "救出被困的弟子"}
                ],
                {"灵石": 80, "丹药": 2, "好感度": 10}
            ),
            
            "q102_mysterious_merchant": Quest(
                "q102_mysterious_merchant",
                "神秘商人",
                "遇到一个售卖奇特物品的神秘商人",
                [
                    {"id": "trade_items", "required": 1, "desc": "与商人进行交易"},
                    {"id": "discover_truth", "required": 1, "desc": "发现商人的真实身份"}
                ],
                {"特殊物品": 1, "情报": 1, "机缘": 2}
            ),
            
            "q103_ancient_book": Quest(
                "q103_ancient_book",
                "古籍寻踪",
                "寻找失落的古代修炼典籍",
                [
                    {"id": "collect_pages", "required": 5, "desc": "收集散落的书页"},
                    {"id": "decipher_text", "required": 1, "desc": "破译古老文字"}
                ],
                {"功法残卷": 1, "悟性": 2, "灵石": 120}
            )
        }
        return quests
        
    def get_available_quests(self, player) -> List[Quest]:
        """获取当前可接任务"""
        available = []
        completed_ids = [q.quest_id for q in self.completed_quests]
        
        for quest in self.quests.values():
            if (quest.status == "available" and 
                quest.can_accept(completed_ids) and
                quest not in self.active_quests):
                available.append(quest)
                
        return available
        
    def accept_quest(self, quest_id: str) -> bool:
        """接受任务"""
        if quest_id in self.quests:
            quest = self.quests[quest_id]
            completed_ids = [q.quest_id for q in self.completed_quests]
            
            if quest.can_accept(completed_ids) and quest not in self.active_quests:
                quest.start_quest()
                self.active_quests.append(quest)
                return True
        return False
        
    def update_quest_progress(self, objective_id: str, amount: int = 1):
        """更新任务进度"""
        for quest in self.active_quests:
            quest.update_progress(objective_id, amount)
            if quest.check_completion():
                self.complete_quest(quest)
                
    def complete_quest(self, quest: Quest):
        """完成任务"""
        print(f"\n🎉 任务完成：{quest.title}")
        print("获得奖励：")
        
        rewards = quest.get_rewards()
        for reward_type, amount in rewards.items():
            if reward_type == "灵石":
                # 这里应该调用玩家的添加资源方法
                print(f"  - {amount} 灵石")
            elif reward_type == "经验值":
                print(f"  - {amount} 经验值")
            elif reward_type == "next_quest":
                # 自动触发下一个任务
                next_quest_id = amount
                if next_quest_id in self.quests:
                    self.quests[next_quest_id].status = "available"
                    print(f"  - 解锁新任务：{self.quests[next_quest_id].title}")
            else:
                print(f"  - {amount} {reward_type}")
                
        # 移动到完成列表
        self.active_quests.remove(quest)
        self.completed_quests.append(quest)
        
        # 设置故事标志
        self.story_flags[f"completed_{quest.quest_id}"] = True
        
    def show_quest_status(self):
        """显示任务状态"""
        print("\n=== 任务面板 ===")
        
        if self.active_quests:
            print("📋 进行中的任务：")
            for quest in self.active_quests:
                print(f"  🎯 {quest.title}")
                print(f"    {quest.description}")
                print("    进度：")
                for obj in quest.objectives:
                    current = quest.progress.get(obj['id'], 0)
                    print(f"      {obj['desc']}: {current}/{obj['required']}")
                print()
                
        available_quests = self.get_available_quests(None)  # 简化处理
        if available_quests:
            print("🆕 可接任务：")
            for quest in available_quests[:3]:  # 只显示前3个
                print(f"  🆕 {quest.title}")
                print(f"    {quest.description}")
                print()
                
        if self.completed_quests:
            print("✅ 已完成任务：")
            for quest in self.completed_quests[-3:]:  # 只显示最近3个
                print(f"  ✅ {quest.title}")
                
    def trigger_story_event(self, event_type: str, player) -> bool:
        """触发剧情事件"""
        story_events = {
            "first_blood": {
                "condition": lambda p: not self.story_flags.get("first_combat"),
                "trigger": lambda p: self._first_combat_event(p)
            },
            "first_breakthrough": {
                "condition": lambda p: p.realm != "凡人" and not self.story_flags.get("first_breakthrough"),
                "trigger": lambda p: self._first_breakthrough_event(p)
            },
            "sect_choice": {
                "condition": lambda p: hasattr(p, 'sect') and p.sect and not self.story_flags.get("sect_chosen"),
                "trigger": lambda p: self._sect_choice_event(p)
            }
        }
        
        if event_type in story_events:
            event = story_events[event_type]
            if event["condition"](player):
                return event["trigger"](player)
        return False
        
    def _first_combat_event(self, player):
        """首次战斗剧情"""
        print("\n🎭 剧情触发：初次战斗")
        print("这是你第一次真正意义上的战斗...")
        print("紧张、兴奋、还有一丝不安...")
        print("但这就是修仙路上必经的考验！")
        
        self.story_flags["first_combat"] = True
        return True
        
    def _first_breakthrough_event(self, player):
        """首次突破剧情"""
        print("\n🎭 剧情触发：境界突破")
        print(f"恭喜你，{player.name}！")
        print(f"从凡人成功突破至{player.realm}！")
        print("这只是一个开始，前方还有更广阔的天地等着你探索...")
        
        self.story_flags["first_breakthrough"] = True
        return True
        
    def _sect_choice_event(self, player):
        """门派选择剧情"""
        print("\n🎭 剧情触发：门派归属")
        print(f"欢迎加入{player.sect.name}！")
        print("从此你不再是孤身一人，有了同门师兄弟姐妹。")
        print("门派将为你提供资源、指导和保护...")
        
        self.story_flags["sect_chosen"] = True
        return True