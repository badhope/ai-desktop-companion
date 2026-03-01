#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
法宝系统
完整的法宝体系，参照《仙逆》等经典作品
"""

import random
from typing import Dict, List, Tuple
from datetime import datetime

class Treasure:
    """法宝基类"""
    
    def __init__(self, name: str, grade: str, type_: str, attributes: Dict[str, int]):
        self.name = name
        self.grade = grade  # 法宝等级：法器、灵器、宝器、仙器、神器
        self.type = type_   # 法宝类型：攻击、防御、辅助、特殊
        self.attributes = attributes  # 属性值
        self.refinement_level = 0     # 精炼等级 0-12
        self.soul_imprint = None      # 器灵/认主
        self.special_effects = []     # 特殊效果
        
    def get_power_rating(self) -> int:
        """计算法宝威力评分"""
        grade_values = {"法器": 100, "灵器": 500, "宝器": 2000, "仙器": 8000, "神器": 30000}
        base_power = grade_values.get(self.grade, 100)
        
        # 属性加成
        attr_bonus = sum(self.attributes.values()) * 10
        
        # 精炼加成
        refinement_bonus = self.refinement_level * 50
        
        return base_power + attr_bonus + refinement_bonus
        
    def can_refine(self) -> bool:
        """检查是否可以继续精炼"""
        max_refinement = {"法器": 3, "灵器": 6, "宝器": 9, "仙器": 12, "神器": 15}
        return self.refinement_level < max_refinement.get(self.grade, 3)
        
    def imprint_soul(self, cultivator_name: str) -> bool:
        """器灵认主"""
        if self.soul_imprint is None:
            self.soul_imprint = cultivator_name
            self.attributes = {k: v * 1.2 for k, v in self.attributes.items()}  # 认主后属性提升
            return True
        return False

class Weapon(Treasure):
    """武器类法宝"""
    
    def __init__(self, name: str, grade: str, weapon_type: str, attack_power: int):
        super().__init__(name, grade, "攻击", {"攻击力": attack_power})
        self.weapon_type = weapon_type  # 剑、刀、枪、鞭等
        self.element = None  # 附加元素属性
        
    def set_element(self, element: str):
        """设置元素属性"""
        elements = ["火", "冰", "雷", "风", "土", "光", "暗"]
        if element in elements:
            self.element = element
            self.attributes["元素伤害"] = self.attributes["攻击力"] // 3

class Armor(Treasure):
    """防具类法宝"""
    
    def __init__(self, name: str, grade: str, armor_type: str, defense_power: int):
        super().__init__(name, grade, "防御", {"防御力": defense_power})
        self.armor_type = armor_type  # 盔甲、护盾、披风等
        self.resistances = {}  # 抗性属性
        
    def add_resistance(self, damage_type: str, resistance: int):
        """添加抗性"""
        self.resistances[damage_type] = resistance

class AuxiliaryTreasure(Treasure):
    """辅助类法宝"""
    
    def __init__(self, name: str, grade: str, function: str, power_level: int):
        super().__init__(name, grade, "辅助", {"辅助效果": power_level})
        self.function = function  # 飞行、隐身、加速等功能
        self.energy_consumption = power_level // 10

class SpecialTreasure(Treasure):
    """特殊类法宝"""
    
    def __init__(self, name: str, grade: str, unique_ability: str, cooldown: int):
        super().__init__(name, grade, "特殊", {"独特能力": 100})
        self.unique_ability = unique_ability  # 独特能力描述
        self.cooldown = cooldown  # 冷却时间
        self.current_cooldown = 0

class TreasureRefining:
    """法宝精炼系统"""
    
    def __init__(self):
        self.materials = self._initialize_materials()
        self.refining_recipes = self._initialize_recipes()
        
    def _initialize_materials(self) -> Dict[str, Dict]:
        """初始化精炼材料"""
        return {
            "玄铁": {"grade": "普通", "rarity": "常见", "effect": "基础强化"},
            "星辰砂": {"grade": "灵品", "rarity": "稀有", "effect": "属性提升"},
            "九天神火": {"grade": "仙品", "rarity": "珍贵", "effect": "品质飞跃"},
            "混沌精华": {"grade": "神品", "rarity": "传说", "effect": "突破极限"}
        }
        
    def _initialize_recipes(self) -> Dict[str, List[Tuple[str, int]]]:
        """初始化精炼配方"""
        return {
            "基础强化": [("玄铁", 10)],
            "属性提升": [("星辰砂", 5), ("玄铁", 20)],
            "品质飞跃": [("九天神火", 1), ("星辰砂", 10)],
            "突破极限": [("混沌精华", 1), ("九天神火", 3)]
        }
        
    def refine_treasure(self, treasure: Treasure, player_level: int) -> bool:
        """精炼法宝"""
        if not treasure.can_refine():
            print("已达到最大精炼等级")
            return False
            
        # 检查所需材料
        recipe_key = self._get_recipe_key(treasure.refinement_level)
        if recipe_key not in self.refining_recipes:
            return False
            
        required_materials = self.refining_recipes[recipe_key]
        # 这里应该检查玩家是否有足够材料
        
        # 精炼成功率
        success_rate = max(0.3, 0.9 - (treasure.refinement_level * 0.05))
        if random.random() > success_rate:
            print("精炼失败...")
            return False
            
        # 精炼成功
        treasure.refinement_level += 1
        print(f"精炼成功！当前等级：{treasure.refinement_level}")
        
        # 提升属性
        for attr in treasure.attributes:
            treasure.attributes[attr] = int(treasure.attributes[attr] * 1.1)
            
        return True
        
    def _get_recipe_key(self, current_level: int) -> str:
        """根据当前等级获取配方key"""
        if current_level < 3:
            return "基础强化"
        elif current_level < 6:
            return "属性提升"
        elif current_level < 9:
            return "品质飞跃"
        else:
            return "突破极限"

class TreasureCollection:
    """法宝收藏系统"""
    
    def __init__(self):
        self.collection = {
            "武器": [],
            "防具": [],
            "辅助法宝": [],
            "特殊法宝": []
        }
        
    def add_treasure(self, treasure: Treasure):
        """添加法宝到收藏"""
        type_mapping = {
            "攻击": "武器",
            "防御": "防具", 
            "辅助": "辅助法宝",
            "特殊": "特殊法宝"
        }
        
        collection_type = type_mapping.get(treasure.type, "特殊法宝")
        self.collection[collection_type].append(treasure)
        print(f"获得法宝：{treasure.name}")
        
    def get_total_power(self) -> int:
        """计算总威力"""
        total = 0
        for treasures in self.collection.values():
            for treasure in treasures:
                total += treasure.get_power_rating()
        return total
        
    def show_collection(self):
        """显示法宝收藏"""
        print("\n=== 法宝收藏 ===")
        for category, treasures in self.collection.items():
            if treasures:
                print(f"\n{category}：")
                for treasure in treasures:
                    print(f"  • {treasure.name} ({treasure.grade})")
                    print(f"    威力评分：{treasure.get_power_rating()}")
                    if treasure.soul_imprint:
                        print(f"    已认主：{treasure.soul_imprint}")
                    if treasure.refinement_level > 0:
                        print(f"    精炼等级：{treasure.refinement_level}")
                    print()

class TreasureSystem:
    """法宝系统主类"""
    
    def __init__(self):
        self.refining_system = TreasureRefining()
        self.treasure_database = self._initialize_treasure_database()
        
    def _initialize_treasure_database(self) -> Dict[str, Treasure]:
        """初始化法宝数据库"""
        treasures = {
            # 经典武器
            "青锋剑": Weapon("青锋剑", "灵器", "剑", 500),
            "玄铁重剑": Weapon("玄铁重剑", "宝器", "剑", 1200),
            "诛仙剑": Weapon("诛仙剑", "仙器", "剑", 5000),
            "开天斧": Weapon("开天斧", "神器", "斧", 15000),
            
            # 经典防具
            "混元盾": Armor("混元盾", "灵器", "盾牌", 300),
            "金刚罩": Armor("金刚罩", "宝器", "护甲", 800),
            "九天玄衣": Armor("九天玄衣", "仙器", "披风", 2500),
            "混沌钟": Armor("混沌钟", "神器", "钟", 8000),
            
            # 辅助法宝
            "遁天梭": AuxiliaryTreasure("遁天梭", "灵器", "飞行", 200),
            "缩地尺": AuxiliaryTreasure("缩地尺", "宝器", "瞬移", 500),
            "乾坤袋": AuxiliaryTreasure("乾坤袋", "仙器", "储物", 1500),
            "时空镜": AuxiliaryTreasure("时空镜", "神器", "时空穿梭", 5000),
            
            # 特殊法宝
            "照妖镜": SpecialTreasure("照妖镜", "宝器", "洞察妖气", 10),
            "捆仙绳": SpecialTreasure("捆仙绳", "仙器", "束缚强敌", 30),
            "混沌珠": SpecialTreasure("混沌珠", "神器", "演化混沌", 100)
        }
        
        # 为部分法宝添加特殊效果
        treasures["青锋剑"].set_element("雷")
        treasures["混元盾"].add_resistance("物理", 50)
        treasures["遁天梭"].special_effects = ["极速飞行", "隐形功能"]
        
        return treasures
        
    def treasure_interface(self, player_name: str, player_stats: Dict):
        """法宝系统主界面"""
        print("\n=== 法宝系统 ===")
        
        # 初始化玩家法宝收藏
        if not hasattr(self, 'player_collections'):
            self.player_collections = {}
            
        if player_name not in self.player_collections:
            self.player_collections[player_name] = TreasureCollection()
            
        collection = self.player_collections[player_name]
        
        while True:
            print(f"\n总威力评分：{collection.get_total_power()}")
            print("\n操作选项：")
            print("1. 查看法宝收藏")
            print("2. 精炼法宝")
            print("3. 寻找法宝")
            print("4. 器灵认主")
            print("5. 返回")
            
            choice = input("请选择: ")
            
            if choice == "1":
                collection.show_collection()
            elif choice == "2":
                self.refine_treasure_interface(collection, player_stats)
            elif choice == "3":
                self.search_treasure(collection)
            elif choice == "4":
                self.soul_imprint_interface(collection)
            elif choice == "5":
                break
            else:
                print("无效选择")
                
    def refine_treasure_interface(self, collection: TreasureCollection, player_stats: Dict):
        """精炼法宝界面"""
        # 显示可精炼的法宝
        refinable_treasures = []
        for treasures in collection.collection.values():
            for treasure in treasures:
                if treasure.can_refine():
                    refinable_treasures.append(treasure)
                    
        if not refinable_treasures:
            print("没有可精炼的法宝")
            return
            
        print("可精炼法宝：")
        for i, treasure in enumerate(refinable_treasures, 1):
            print(f"{i}. {treasure.name} (当前等级：{treasure.refinement_level})")
            
        try:
            choice = int(input("选择法宝: ")) - 1
            if 0 <= choice < len(refinable_treasures):
                treasure = refinable_treasures[choice]
                success = self.refining_system.refine_treasure(treasure, player_stats.get('realm_level', 1))
                if success:
                    print("精炼完成！")
        except ValueError:
            print("输入错误")
            
    def search_treasure(self, collection: TreasureCollection):
        """寻找法宝"""
        print("\n寻找法宝...")
        
        # 根据运气和境界决定获得品质
        search_results = random.choices(
            list(self.treasure_database.keys()),
            weights=[10, 8, 5, 2, 15, 12, 8, 3, 10, 8, 5, 2, 5, 3, 1, 1],
            k=1
        )
        
        treasure_name = search_results[0]
        treasure = self.treasure_database[treasure_name]
        
        print(f"找到了{treasure.name}({treasure.grade})！")
        
        # 加入收藏
        collection.add_treasure(treasure)
        
    def soul_imprint_interface(self, collection: TreasureCollection):
        """器灵认主界面"""
        # 收集所有未认主的法宝
        unimprinted = []
        for treasures in collection.collection.values():
            for treasure in treasures:
                if treasure.soul_imprint is None:
                    unimprinted.append(treasure)
                    
        if not unimprinted:
            print("没有可认主的法宝")
            return
            
        print("可认主法宝：")
        for i, treasure in enumerate(unimprinted, 1):
            print(f"{i}. {treasure.name}")
            
        try:
            choice = int(input("选择法宝: ")) - 1
            if 0 <= choice < len(unimprinted):
                treasure = unimprinted[choice]
                # 这里应该传递玩家名字
                success = treasure.imprint_soul("玩家")
                if success:
                    print(f"{treasure.name}成功认主！")
        except ValueError:
            print("输入错误")