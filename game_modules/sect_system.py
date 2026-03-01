#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
门派系统模块
处理修仙门派相关功能
"""

import random
from typing import Dict, List

class Sect:
    """门派类"""
    
    def __init__(self, name: str, sect_type: str, reputation: int):
        self.name = name
        self.type = sect_type  # 门派类型：剑修、丹修、器修、符修等
        self.reputation = reputation  # 门派声望
        self.members = []  # 门派成员
        self.skills = self._initialize_sect_skills()
        self.resources = {
            "贡献点": 1000,
            "秘籍": 5,
            "法宝": 3
        }
        
    def _initialize_sect_skills(self) -> List[str]:
        """初始化门派特有技能"""
        skill_sets = {
            "青云剑派": ["御剑术", "剑心通明", "万剑归宗"],
            "丹霞宗": ["炼丹术", "药理精通", "丹火控制"],
            "器符门": ["炼器术", "符箓制作", "阵法布置"],
            "天机阁": ["推演术", "占卜预测", "机关制造"]
        }
        return skill_sets.get(self.name, ["基础修炼"])
        
    def join_sect(self, player) -> bool:
        """加入门派"""
        # 检查入门条件
        if player.realm == "凡人":
            print("凡人无法加入门派")
            return False
            
        if hasattr(player, 'sect') and player.sect:
            print("你已经有门派了")
            return False
            
        # 入门测试（简化版）
        test_difficulty = max(1, self.reputation // 100)
        success_chance = (player.stats['悟性'] + player.stats['机缘']) / 20
        
        if random.random() < success_chance / test_difficulty:
            player.sect = self
            self.members.append(player.name)
            print(f"恭喜加入{self.name}！")
            
            # 新手奖励
            player.add_resource("灵石", 100)
            player.add_resource("贡献点", 50)
            return True
        else:
            print("入门测试失败")
            return False
            
    def sect_task(self, player) -> bool:
        """门派任务"""
        if not hasattr(player, 'sect') or not player.sect:
            print("你还没有门派")
            return False
            
        tasks = [
            "采集灵草", "护送物资", "清理妖兽", 
            "协助炼丹", "维护阵法", "教导新弟子"
        ]
        
        task = random.choice(tasks)
        difficulty = random.randint(1, 5)
        reward = difficulty * 20
        
        print(f"门派任务：{task}")
        print(f"难度等级：{difficulty}")
        print(f"奖励：{reward}贡献点")
        
        # 任务成功率
        success_rate = (
            player.stats['体质'] * 0.2 + 
            player.stats['悟性'] * 0.15 + 
            player.stats['机缘'] * 0.1 +
            random.randint(-10, 10)
        ) / 100
        
        if success_rate > 0.5:
            print("任务完成！")
            player.add_resource("贡献点", reward)
            
            # 随机获得物品奖励
            if random.random() < 0.3:
                items = ["丹药", "法器", "秘籍"]
                item = random.choice(items)
                player.add_resource(item, 1)
                print(f"额外获得{item}一件")
            return True
        else:
            print("任务失败...")
            return False
            
    def sect_exchange(self, player, item: str) -> bool:
        """门派兑换"""
        if not hasattr(player, 'sect') or not player.sect:
            print("你还没有门派")
            return False
            
        exchange_rates = {
            "丹药": {"贡献点": 50},
            "法器": {"贡献点": 100},
            "秘籍": {"贡献点": 200},
            "高级丹药": {"贡献点": 150}
        }
        
        if item not in exchange_rates:
            print("该物品无法兑换")
            return False
            
        cost = exchange_rates[item]["贡献点"]
        if player.resources.get("贡献点", 0) >= cost:
            player.resources["贡献点"] -= cost
            player.add_resource(item, 1)
            print(f"成功兑换{item}")
            return True
        else:
            print(f"贡献点不足，需要{cost}点")
            return False

class SectSystem:
    """门派系统管理类"""
    
    def __init__(self):
        self.sects = self._initialize_sects()
        
    def _initialize_sects(self) -> Dict[str, Sect]:
        """初始化门派"""
        sects = {
            "青云剑派": Sect("青云剑派", "剑修", 800),
            "丹霞宗": Sect("丹霞宗", "丹修", 700),
            "器符门": Sect("器符门", "器修", 600),
            "天机阁": Sect("天机阁", "智修", 750)
        }
        return sects
        
    def get_available_sects(self, player) -> List[Sect]:
        """获取可加入的门派"""
        available = []
        for sect in self.sects.values():
            if not hasattr(player, 'sect') or not player.sect:
                available.append(sect)
        return available
        
    def list_all_sects(self) -> List[Sect]:
        """列出所有门派"""
        return list(self.sects.values())