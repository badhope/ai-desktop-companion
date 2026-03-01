#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
炼丹系统
完整的丹药体系，参照《凡人修仙传》等经典作品
"""

import random
from typing import Dict, List, Tuple
from datetime import datetime

class AlchemyIngredient:
    """炼丹原料类"""
    
    def __init__(self, name: str, grade: str, properties: List[str], rarity: str):
        self.name = name
        self.grade = grade  # 品级：凡品、灵品、仙品、神品
        self.properties = properties  # 药性：热、寒、平、毒等
        self.rarity = rarity  # 稀有度：常见、稀有、珍贵、传说
        self.purity = 1.0  # 纯度 0.0-1.0
        
    def get_quality_score(self) -> float:
        """计算原料品质分数"""
        grade_scores = {"凡品": 1.0, "灵品": 2.0, "仙品": 3.0, "神品": 5.0}
        rarity_scores = {"常见": 1.0, "稀有": 2.0, "珍贵": 3.0, "传说": 5.0}
        
        base_score = grade_scores.get(self.grade, 1.0) * rarity_scores.get(self.rarity, 1.0)
        return base_score * self.purity

class AlchemyFormula:
    """丹方类"""
    
    def __init__(self, name: str, level: int, ingredients: List[Tuple[str, int]], 
                 effects: Dict[str, any], difficulty: int, success_rate_base: float):
        self.name = name
        self.level = level  # 丹方等级 1-9
        self.ingredients = ingredients  # [(原料名, 数量), ...]
        self.effects = effects  # 丹药效果
        self.difficulty = difficulty  # 炼制难度
        self.success_rate_base = success_rate_base  # 基础成功率
        
    def calculate_success_rate(self, alchemist_level: int, fire_control: int, 
                             luck: int, ingredients_quality: float) -> float:
        """计算实际成功率"""
        # 等级修正
        level_bonus = max(0, alchemist_level - self.level) * 0.05
        
        # 控火能力修正
        fire_bonus = fire_control * 0.03
        
        # 运气修正
        luck_bonus = luck * 0.02
        
        # 原料品质修正
        quality_bonus = (ingredients_quality - 1.0) * 0.2
        
        # 难度惩罚
        difficulty_penalty = self.difficulty * 0.08
        
        success_rate = (self.success_rate_base + level_bonus + fire_bonus + 
                       luck_bonus + quality_bonus - difficulty_penalty)
        
        return max(0.05, min(0.95, success_rate))  # 限制在5%-95%之间

class AlchemyFurnace:
    """丹炉类"""
    
    def __init__(self, name: str, level: int, fire_types: List[str], special_effects: List[str]):
        self.name = name
        self.level = level  # 丹炉等级
        self.fire_types = fire_types  # 支持的火焰类型
        self.special_effects = special_effects  # 特殊效果
        self.durability = 100  # 耐久度
        self.temperature_control = level * 10  # 温度控制精度
        
    def can_support_formula(self, formula: AlchemyFormula, fire_type: str) -> bool:
        """检查是否支持某个丹方"""
        return (self.level >= formula.level and 
                fire_type in self.fire_types and
                self.durability > 0)

class MasterAlchemist:
    """炼丹大师类"""
    
    def __init__(self, name: str, sect: str):
        self.name = name
        self.sect = sect
        self.alchemy_level = 1  # 炼丹等级
        self.fire_control = 1   # 控火能力
        self.luck = 0           # 炼丹运气
        self.known_formulas = []  # 已掌握的丹方
        self.experience = 0     # 炼丹经验
        self.furnaces = []      # 拥有的丹炉
        
    def learn_formula(self, formula: AlchemyFormula) -> bool:
        """学习新丹方"""
        if self.alchemy_level >= formula.level:
            if formula.name not in [f.name for f in self.known_formulas]:
                self.known_formulas.append(formula)
                print(f"成功学会丹方：{formula.name}")
                return True
        return False
        
    def improve_fire_control(self, practice_hours: int):
        """提升控火能力"""
        improvement = practice_hours * 0.1 * (self.alchemy_level / 10)
        self.fire_control = min(10, self.fire_control + improvement)
        
    def increase_luck(self, special_events: int = 1):
        """增加炼丹运气（通过特殊事件）"""
        self.luck = min(10, self.luck + special_events)

class AlchemySystem:
    """炼丹系统主类"""
    
    def __init__(self):
        self.ingredients = self._initialize_ingredients()
        self.formulas = self._initialize_formulas()
        self.furnaces = self._initialize_furnaces()
        self.alchemists = {}  # 玩家炼丹师对象
        
    def _initialize_ingredients(self) -> Dict[str, AlchemyIngredient]:
        """初始化炼丹原料"""
        ingredients = {
            # 基础药材
            "聚灵草": AlchemyIngredient("聚灵草", "灵品", ["补气", "聚灵"], "常见"),
            "凝神花": AlchemyIngredient("凝神花", "灵品", ["安神", "凝神"], "常见"),
            "忘忧草": AlchemyIngredient("忘忧草", "灵品", ["解毒", "忘忧"], "稀有"),
            
            # 中级药材
            "千年灵芝": AlchemyIngredient("千年灵芝", "仙品", ["续命", "固本"], "稀有"),
            "九转灵果": AlchemyIngredient("九转灵果", "仙品", ["造化", "重生"], "珍贵"),
            "紫阳花": AlchemyIngredient("紫阳花", "仙品", ["纯阳", "驱寒"], "稀有"),
            
            # 高级药材
            "万年人参": AlchemyIngredient("万年人参", "神品", ["逆天", "改命"], "珍贵"),
            "凤凰羽": AlchemyIngredient("凤凰羽", "神品", ["涅槃", "重生"], "传说"),
            "龙涎香": AlchemyIngredient("龙涎香", "神品", ["真龙", "霸气"], "传说"),
            
            # 特殊材料
            "天材地宝": AlchemyIngredient("天材地宝", "神品", ["万能", "神奇"], "传说"),
            "混沌石": AlchemyIngredient("混沌石", "神品", ["开天", "辟地"], "传说")
        }
        return ingredients
        
    def _initialize_formulas(self) -> Dict[str, AlchemyFormula]:
        """初始化丹方"""
        formulas = {
            # 基础丹药
            "聚气丹": AlchemyFormula(
                "聚气丹", 1,
                [("聚灵草", 3), ("凝神花", 2)],
                {"修为增长": 10, "修炼速度": 1.1},
                difficulty=2, success_rate_base=0.8
            ),
            "凝神丹": AlchemyFormula(
                "凝神丹", 2,
                [("凝神花", 5), ("忘忧草", 1)],
                {"心境稳定": 5, "悟性提升": 1},
                difficulty=3, success_rate_base=0.7
            ),
            
            # 中级丹药
            "筑基丹": AlchemyFormula(
                "筑基丹", 3,
                [("千年灵芝", 1), ("聚灵草", 10), ("九转灵果", 1)],
                {"突破筑基": 0.3, "体质提升": 2},
                difficulty=5, success_rate_base=0.6
            ),
            "金元丹": AlchemyFormula(
                "金元丹", 4,
                [("九转灵果", 2), ("紫阳花", 3), ("千年灵芝", 1)],
                {"金丹凝结": 0.2, "灵根改善": 1},
                difficulty=6, success_rate_base=0.5
            ),
            
            # 高级丹药
            "元婴丹": AlchemyFormula(
                "元婴丹", 6,
                [("万年人参", 1), ("凤凰羽", 1), ("九转灵果", 5)],
                {"元婴孕育": 0.15, "寿命延长": 100},
                difficulty=8, success_rate_base=0.4
            ),
            "化神丹": AlchemyFormula(
                "化神丹", 7,
                [("凤凰羽", 2), ("龙涎香", 1), ("万年人参", 1)],
                {"神魂凝练": 0.1, "精神力提升": 50},
                difficulty=9, success_rate_base=0.3
            ),
            
            # 传说丹药
            "九转金丹": AlchemyFormula(
                "九转金丹", 9,
                [("天材地宝", 1), ("混沌石", 1), ("凤凰羽", 3), ("龙涎香", 2)],
                {"立地成仙": 0.05, "全属性提升": 10, "寿命无限": True},
                difficulty=12, success_rate_base=0.1
            )
        }
        return formulas
        
    def _initialize_furnaces(self) -> Dict[str, AlchemyFurnace]:
        """初始化丹炉"""
        furnaces = {
            "普通丹炉": AlchemyFurnace(
                "普通丹炉", 1, 
                ["凡火", "灵火"], 
                ["基础炼制"]
            ),
            "灵品丹炉": AlchemyFurnace(
                "灵品丹炉", 3,
                ["灵火", "地火", "天火"],
                ["品质提升", "成功率+10%"]
            ),
            "仙品丹炉": AlchemyFurnace(
                "仙品丹炉", 6,
                ["天火", "真火", "仙火"],
                ["品质大幅提升", "成功率+20%", "特殊效果"]
            ),
            "神品丹炉": AlchemyFurnace(
                "神品丹炉", 9,
                ["仙火", "神火", "混沌火"],
                ["完美品质", "成功率+30%", "创造奇迹"]
            )
        }
        return furnaces
        
    def get_player_alchemist(self, player_name: str) -> MasterAlchemist:
        """获取玩家炼丹师对象"""
        if player_name not in self.alchemists:
            self.alchemists[player_name] = MasterAlchemist(player_name, "散修")
            # 初始掌握基础丹方
            basic_formulas = ["聚气丹", "凝神丹"]
            for formula_name in basic_formulas:
                if formula_name in self.formulas:
                    self.alchemists[player_name].learn_formula(self.formulas[formula_name])
        return self.alchemists[player_name]
        
    def alchemy_interface(self, player_name: str, player_stats: Dict):
        """炼丹主界面"""
        alchemist = self.get_player_alchemist(player_name)
        print("\n=== 炼丹堂 ===")
        print(f"炼丹等级：{alchemist.alchemy_level}")
        print(f"控火能力：{alchemist.fire_control:.1f}")
        print(f"炼丹运气：{alchemist.luck}")
        
        while True:
            print("\n操作选项：")
            print("1. 查看已学丹方")
            print("2. 学习新丹方")
            print("3. 开始炼丹")
            print("4. 练习控火")
            print("5. 查看丹炉")
            print("6. 返回")
            
            choice = input("请选择: ")
            
            if choice == "1":
                self.show_known_formulas(alchemist)
            elif choice == "2":
                self.learn_new_formula(alchemist)
            elif choice == "3":
                self.start_alchemy(alchemist, player_stats)
            elif choice == "4":
                self.practice_fire_control(alchemist)
            elif choice == "5":
                self.show_furnaces(alchemist)
            elif choice == "6":
                break
            else:
                print("无效选择")
                
    def show_known_formulas(self, alchemist: MasterAlchemist):
        """显示已学丹方"""
        print("\n已掌握丹方：")
        for formula in alchemist.known_formulas:
            print(f"  • {formula.name} (等级{formula.level})")
            print(f"    需要原料：{', '.join([f'{name}×{qty}' for name, qty in formula.ingredients])}")
            print(f"    效果：{formula.effects}")
            print()
            
    def learn_new_formula(self, alchemist: MasterAlchemist):
        """学习新丹方"""
        print("\n可学习的丹方：")
        available_formulas = []
        
        for name, formula in self.formulas.items():
            if (formula.level <= alchemist.alchemy_level and 
                formula.name not in [f.name for f in alchemist.known_formulas]):
                available_formulas.append((name, formula))
                
        for i, (name, formula) in enumerate(available_formulas, 1):
            print(f"{i}. {name} (等级{formula.level})")
            
        if not available_formulas:
            print("暂无可学习的丹方")
            return
            
        try:
            choice = int(input("选择要学习的丹方: ")) - 1
            if 0 <= choice < len(available_formulas):
                formula = available_formulas[choice][1]
                if alchemist.learn_formula(formula):
                    # 消耗资源
                    cost = formula.level * 50
                    print(f"学习成功！消耗灵石 {cost}")
                else:
                    print("学习失败")
        except ValueError:
            print("输入错误")
            
    def start_alchemy(self, alchemist: MasterAlchemist, player_stats: Dict):
        """开始炼丹"""
        if not alchemist.known_formulas:
            print("还未掌握任何丹方")
            return
            
        print("选择要炼制的丹药：")
        for i, formula in enumerate(alchemist.known_formulas, 1):
            print(f"{i}. {formula.name}")
            
        try:
            choice = int(input("选择丹方: ")) - 1
            if 0 <= choice < len(alchemist.known_formulas):
                formula = alchemist.known_formulas[choice]
                self.perform_alchemy(alchemist, formula, player_stats)
        except ValueError:
            print("输入错误")
            
    def perform_alchemy(self, alchemist: MasterAlchemist, formula: AlchemyFormula, 
                       player_stats: Dict):
        """执行炼丹过程"""
        print(f"\n开始炼制 {formula.name}...")
        
        # 检查原料
        missing_ingredients = []
        for ingredient_name, required_qty in formula.ingredients:
            # 这里应该检查玩家背包中的原料
            available = 0  # 假设有检查机制
            if available < required_qty:
                missing_ingredients.append(f"{ingredient_name}(缺少{required_qty-available}个)")
                
        if missing_ingredients:
            print(f"原料不足：{', '.join(missing_ingredients)}")
            return
            
        # 选择丹炉
        print("选择丹炉：")
        usable_furnaces = [f for f in self.furnaces.values() 
                          if f.level <= alchemist.alchemy_level]
        for i, furnace in enumerate(usable_furnaces, 1):
            print(f"{i}. {furnace.name} (等级{furnace.level})")
            
        try:
            furnace_choice = int(input("选择丹炉: ")) - 1
            if 0 <= furnace_choice < len(usable_furnaces):
                furnace = usable_furnaces[furnace_choice]
                
                # 选择火焰类型
                print("选择火焰：")
                for i, fire_type in enumerate(furnace.fire_types, 1):
                    print(f"{i}. {fire_type}")
                    
                fire_choice = int(input("选择火焰: ")) - 1
                if 0 <= fire_choice < len(furnace.fire_types):
                    fire_type = furnace.fire_types[fire_choice]
                    
                    # 计算成功率
                    ingredients_quality = 1.2  # 简化处理
                    success_rate = formula.calculate_success_rate(
                        alchemist.alchemy_level, alchemist.fire_control,
                        alchemist.luck, ingredients_quality
                    )
                    
                    print(f"炼制成功率：{success_rate*100:.1f}%")
                    
                    # 炼制过程
                    if random.random() < success_rate:
                        print("🔥 炼制成功！")
                        # 获得丹药
                        print(f"获得 {formula.name} x1")
                        # 提升经验
                        exp_gain = formula.level * 10
                        alchemist.experience += exp_gain
                        print(f"炼丹经验+{exp_gain}")
                        
                        # 检查升级
                        if alchemist.experience >= alchemist.alchemy_level * 100:
                            alchemist.alchemy_level += 1
                            print(f"炼丹等级提升至 {alchemist.alchemy_level}!")
                    else:
                        print("💥 炼制失败...")
                        # 消耗原料但有一定概率保留下部分
                        preservation_chance = 0.3
                        print("部分原料在高温中损毁...")
                        
        except ValueError:
            print("输入错误")
            
    def practice_fire_control(self, alchemist: MasterAlchemist):
        """练习控火能力"""
        hours = int(input("练习时长(小时): "))
        alchemist.improve_fire_control(hours)
        print(f"控火能力提升至 {alchemist.fire_control:.1f}")
        
    def show_furnaces(self, alchemist: MasterAlchemist):
        """显示丹炉信息"""
        print("\n可用丹炉：")
        for name, furnace in self.furnaces.items():
            if furnace.level <= alchemist.alchemy_level:
                print(f"  • {furnace.name}")
                print(f"    等级：{furnace.level}")
                print(f"    支持火焰：{', '.join(furnace.fire_types)}")
                print(f"    特殊效果：{', '.join(furnace.special_effects)}")
                print()