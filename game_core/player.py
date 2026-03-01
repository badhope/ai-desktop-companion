#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
玩家角色类
定义玩家的基本属性和行为
"""

from typing import Dict, List

class Player:
    """玩家角色类"""
    
    REALMS = [
        "凡人", "练气期", "筑基期", "金丹期", 
        "元婴期", "化神期", "合体期", "大乘期", "渡劫期"
    ]
    
    def __init__(self, name: str):
        self.name = name
        self.realm = "凡人"  # 当前境界
        self.cultivation = 0  # 修为值 (0-100)
        self.lifetime = 0  # 寿元
        
        # 基础属性
        self.stats = {
            "体质": 5,      # 影响生命值和恢复速度
            "灵根": 5,      # 影响灵气吸收效率
            "悟性": 5,      # 影响学习和领悟速度
            "机缘": 5       # 影响奇遇概率
        }
        
        # 资源系统
        self.resources = {
            "灵石": 100,    # 基础货币
            "灵药": 0,      # 炼丹材料
            "法器": 0,      # 装备
            "丹药": 0       # 消耗品
        }
        
        # 技能系统
        self.skills = {
            "基础修炼": 1,
            "炼丹术": 0,
            "炼器术": 0,
            "阵法": 0,
            "符箓": 0
        }
        
        # 成就系统
        self.achievements = []
        
    def cultivate(self):
        """修炼行为"""
        base_gain = 3
        # 根据灵根属性增加收益
        gain = base_gain + (self.stats['灵根'] // 2)
        # 根据悟性增加额外收益
        if self.stats['悟性'] > 7:
            gain += 1
            
        self.cultivation += gain
        
        # 检查是否突破境界
        if self.cultivation >= 100:
            self.breakthrough()
        else:
            print(f"修炼中...修为+{gain}，当前修为 {self.cultivation}/100")
            
    def breakthrough(self):
        """境界突破"""
        current_index = self.REALMS.index(self.realm)
        
        if current_index < len(self.REALMS) - 1:
            next_realm = self.REALMS[current_index + 1]
            breakthrough_cost = (current_index + 1) * 20
            
            # 检查是否满足突破条件
            if self.stats['机缘'] + random.randint(1, 10) > breakthrough_cost:
                self.realm = next_realm
                self.cultivation = 0
                print(f"🎉 突破成功！境界提升至 {self.realm}")
                
                # 突破奖励
                self.stats['体质'] += 1
                self.stats['灵根'] += 1
                self.add_resource('灵石', 50)
            else:
                print("突破失败，需要更多积累...")
                self.cultivation = 90  # 失败后修为下降
        else:
            print("已达最高境界！")
            
    def add_resource(self, resource_type: str, amount: int):
        """添加资源"""
        if resource_type in self.resources:
            self.resources[resource_type] += amount
            print(f"获得 {resource_type} x{amount}")
        else:
            print(f"未知资源类型：{resource_type}")
            
    def consume_resource(self, resource_type: str, amount: int) -> bool:
        """消耗资源"""
        if resource_type in self.resources and self.resources[resource_type] >= amount:
            self.resources[resource_type] -= amount
            return True
        return False
        
    def learn_skill(self, skill_name: str):
        """学习技能"""
        if skill_name in self.skills:
            self.skills[skill_name] += 1
            print(f"{skill_name} 等级提升至 {self.skills[skill_name]}")
            return True
        return False
        
    def get_save_data(self) -> dict:
        """获取存档数据"""
        return {
            'name': self.name,
            'realm': self.realm,
            'cultivation': self.cultivation,
            'lifetime': self.lifetime,
            'stats': self.stats.copy(),
            'resources': self.resources.copy(),
            'skills': self.skills.copy(),
            'achievements': self.achievements.copy()
        }
        
    def load_from_data(self, data: dict):
        """从存档数据加载"""
        self.name = data.get('name', self.name)
        self.realm = data.get('realm', self.realm)
        self.cultivation = data.get('cultivation', self.cultivation)
        self.lifetime = data.get('lifetime', self.lifetime)
        self.stats.update(data.get('stats', {}))
        self.resources.update(data.get('resources', {}))
        self.skills.update(data.get('skills', {}))
        self.achievements = data.get('achievements', [])