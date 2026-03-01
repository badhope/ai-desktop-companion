#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修炼功法系统
管理各种修炼功法和心法
"""

import random
from typing import Dict, List

class CultivationTechnique:
    """修炼功法类"""
    
    def __init__(self, name: str, level: int, effects: Dict, requirements: Dict):
        self.name = name
        self.level = level  # 功法等级：1-9
        self.effects = effects  # 功法效果
        self.requirements = requirements  # 修炼要求
        self.mastery = 0  # 掌握程度 0-100
        
    def get_effect(self, stat: str) -> float:
        """获取特定属性的加成"""
        return self.effects.get(stat, 0) * (self.mastery / 100)

class TechniqueSystem:
    """功法系统"""
    
    def __init__(self):
        self.available_techniques = self._initialize_techniques()
        self.learned_techniques = {}
        
    def _initialize_techniques(self) -> Dict[str, CultivationTechnique]:
        """初始化功法库"""
        techniques = {
            # 基础功法
            "长春功": CultivationTechnique(
                "长春功", 1,
                {"体质": 2, " lifetime": 10},
                {"境界": "凡人", "悟性": 3}
            ),
            "聚灵诀": CultivationTechnique(
                "聚灵诀", 2,
                {"灵根": 3, "修炼效率": 1.2},
                {"境界": "练气期", "灵根": 5}
            ),
            "凝神诀": CultivationTechnique(
                "凝神诀", 2,
                {"悟性": 2, "心境稳定": 1},
                {"境界": "练气期", "悟性": 4}
            ),
            # 中级功法
            "九转玄功": CultivationTechnique(
                "九转玄功", 5,
                {"体质": 5, "抗性": 2},
                {"境界": "筑基期", "体质": 8}
            ),
            "太虚剑意": CultivationTechnique(
                "太虚剑意", 6,
                {"攻击力": 8, "剑术": 3},
                {"境界": "金丹期", "悟性": 7}
            ),
            # 高级功法
            "混沌经": CultivationTechnique(
                "混沌经", 9,
                {"全属性": 3, "悟性": 5, "机缘": 3},
                {"境界": "大乘期", "全属性": 15}
            )
        }
        return techniques
        
    def get_available_techniques(self, player) -> List[str]:
        """获取玩家可学习的功法"""
        available = []
        for name, technique in self.available_techniques.items():
            if self._check_requirements(technique, player):
                available.append(name)
        return available
        
    def _check_requirements(self, technique: CultivationTechnique, player) -> bool:
        """检查修炼要求"""
        # 境界要求
        realm_levels = {
            "凡人": 0, "练气期": 1, "筑基期": 2, "金丹期": 3,
            "元婴期": 4, "化神期": 5, "合体期": 6, "大乘期": 7, "渡劫期": 8
        }
        
        required_realm_level = realm_levels.get(technique.requirements.get("境界", "凡人"), 0)
        player_realm_level = realm_levels.get(player.realm, 0)
        
        if player_realm_level < required_realm_level:
            return False
            
        # 属性要求
        for stat, required_value in technique.requirements.items():
            if stat != "境界" and player.stats.get(stat, 0) < required_value:
                return False
                
        # 不能重复学习
        if technique.name in self.learned_techniques:
            return False
            
        return True
        
    def learn_technique(self, technique_name: str, player) -> bool:
        """学习功法"""
        if technique_name not in self.available_techniques:
            print("未知功法")
            return False
            
        technique = self.available_techniques[technique_name]
        
        if not self._check_requirements(technique, player):
            print("不满足修炼条件")
            return False
            
        # 消耗资源学习
        cost = technique.level * 20
        if not player.consume_resource("灵石", cost):
            print(f"灵石不足，需要 {cost} 枚")
            return False
            
        # 学习成功
        self.learned_techniques[technique_name] = technique
        print(f"成功学会《{technique_name}》")
        
        # 初始掌握度
        technique.mastery = 10
        return True
        
    def practice_technique(self, technique_name: str, player, hours: int = 1):
        """练习功法"""
        if technique_name not in self.learned_techniques:
            print("未学会此功法")
            return
            
        technique = self.learned_techniques[technique_name]
        practice_efficiency = player.stats['悟性'] / 10 + hours * 0.1
        
        # 增加掌握度
        mastery_gain = min(practice_efficiency, 100 - technique.mastery)
        technique.mastery += mastery_gain
        
        print(f"练习《{technique_name}》{hours}小时")
        print(f"掌握度+{mastery_gain:.1f}，当前掌握度：{technique.mastery:.1f}%")
        
        # 根据掌握度获得属性加成
        if technique.mastery >= 50 and technique.mastery - mastery_gain < 50:
            print("功法掌握达到熟练，获得永久属性加成！")
            # 可以在这里添加永久属性加成
            
    def get_total_effects(self, player) -> Dict[str, float]:
        """获取所有已学功法的总效果"""
        total_effects = {}
        
        for technique in self.learned_techniques.values():
            for stat, effect in technique.effects.items():
                if stat not in total_effects:
                    total_effects[stat] = 0
                total_effects[stat] += technique.get_effect(stat)
                
        return total_effects