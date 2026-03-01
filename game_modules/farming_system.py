#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
互动式种植系统
让玩家可以种植灵草、培育灵药等
"""

import random
import time
from typing import Dict, List
from datetime import datetime, timedelta

class Crop:
    """作物类"""
    
    def __init__(self, name: str, growth_time: int, rarity: str, requirements: Dict):
        self.name = name
        self.growth_time = growth_time  # 生长时间（游戏回合）
        self.rarity = rarity  # 稀有度：普通、稀有、传说
        self.requirements = requirements  # 种植要求
        self.plant_time = None  # 种植时间
        self.current_stage = 0  # 当前生长阶段
        self.is_ready = False   # 是否成熟
        self.quality = 1.0      # 品质系数
        
    def plant(self, current_time):
        """种植作物"""
        self.plant_time = current_time
        self.current_stage = 1
        print(f"🌱 成功种植{self.name}！")
        
    def grow(self, current_time, player_stats: Dict):
        """作物生长"""
        if not self.plant_time:
            return False
            
        # 计算经过的时间
        time_passed = current_time - self.plant_time
        
        # 根据时间推进生长阶段
        expected_stage = min(int(time_passed / (self.growth_time / 4)) + 1, 4)
        
        if expected_stage > self.current_stage:
            self.current_stage = expected_stage
            stage_names = ["种子", "发芽", "成长", "成熟"]
            print(f"🌿 {self.name}进入了{stage_names[self.current_stage-1]}阶段！")
            
            # 成熟时计算品质
            if self.current_stage == 4:
                self.is_ready = True
                self._calculate_quality(player_stats)
                quality_desc = ["普通", "良好", "优秀", "完美"]
                quality_index = min(int(self.quality * 3), 3)
                print(f"✅ {self.name}已经成熟！品质：{quality_desc[quality_index]}")
                
            return True
        return False
        
    def _calculate_quality(self, player_stats: Dict):
        """计算作物品质"""
        base_quality = 0.7
        # 根据玩家属性调整品质
        quality_bonus = (
            player_stats.get('灵根', 0) * 0.02 +
            player_stats.get('悟性', 0) * 0.01 +
            random.uniform(-0.2, 0.3)
        )
        self.quality = max(0.1, min(1.0, base_quality + quality_bonus))
        
    def harvest(self) -> Dict[str, int]:
        """收获作物"""
        if not self.is_ready:
            return {}
            
        # 根据稀有度和品质计算收获数量
        base_yield = {"普通": 2, "稀有": 1, "传说": 1}[self.rarity]
        yield_multiplier = self.quality * 2
        
        rewards = {}
        if self.name == "聚灵草":
            rewards['灵药'] = int(base_yield * yield_multiplier)
            rewards['灵石'] = int(10 * yield_multiplier)
        elif self.name == "凝神花":
            rewards['丹药材料'] = int(base_yield * yield_multiplier)
            rewards['灵石'] = int(15 * yield_multiplier)
        elif self.name == "九转灵果":
            rewards['高级材料'] = 1
            rewards['灵石'] = int(50 * yield_multiplier)
            
        print(f"🎉 收获{self.name}！获得：{rewards}")
        return rewards

class FarmPlot:
    """农田地块"""
    
    def __init__(self, plot_id: int, size: int = 4):
        self.plot_id = plot_id
        self.size = size
        self.crops = [None] * size  # 每个格子的作物
        self.fertilizer_level = 0   # 肥料等级
        self.water_level = 100      # 水分等级
        self.last_watered = None    # 最后浇水时间
        
    def plant_crop(self, slot: int, crop: Crop, current_time) -> bool:
        """在指定位置种植作物"""
        if 0 <= slot < self.size and self.crops[slot] is None:
            self.crops[slot] = crop
            crop.plant(current_time)
            return True
        return False
        
    def water_plot(self):
        """浇水平台"""
        self.water_level = min(100, self.water_level + 30)
        self.last_watered = time.time()
        print("💧 浇水完成！作物生长环境改善。")
        return True
        
    def add_fertilizer(self, level: int = 1):
        """施肥"""
        self.fertilizer_level = min(5, self.fertilizer_level + level)
        print(f"🌾 施肥成功！肥料等级：{self.fertilizer_level}")
        return True
        
    def update_plots(self, current_time, player_stats: Dict):
        """更新所有作物"""
        for i, crop in enumerate(self.crops):
            if crop:
                grew = crop.grow(current_time, player_stats)
                if grew and crop.is_ready:
                    print(f"第{i+1}格的{crop.name}已经成熟了！")
                    
    def harvest_slot(self, slot: int) -> Dict[str, int]:
        """收获指定格子的作物"""
        if 0 <= slot < self.size and self.crops[slot] and self.crops[slot].is_ready:
            crop = self.crops[slot]
            rewards = crop.harvest()
            self.crops[slot] = None  # 清空格子
            return rewards
        return {}

class FarmingSystem:
    """种植系统主类"""
    
    def __init__(self):
        self.available_crops = self._initialize_crops()
        self.plots = [FarmPlot(i) for i in range(2)]  # 默认2块地
        self.tools = {
            '浇水壶': 1,
            '肥料': 5,
            '除草剂': 3
        }
        
    def _initialize_crops(self) -> Dict[str, Crop]:
        """初始化可种植作物"""
        crops = {
            "聚灵草": Crop("聚灵草", 20, "普通", {"灵根": 3}),
            "凝神花": Crop("凝神花", 30, "稀有", {"悟性": 5}),
            "九转灵果": Crop("九转灵果", 50, "传说", {"全属性": 10}),
            "忘忧草": Crop("忘忧草", 15, "普通", {"体质": 4}),
            "紫阳花": Crop("紫阳花", 25, "稀有", {"机缘": 6})
        }
        return crops
        
    def show_farm_status(self):
        """显示农场状态"""
        print("\n=== 我的灵田 ===")
        
        for plot in self.plots:
            print(f"\n第{plot.plot_id + 1}号田地:")
            print(f"水分：{plot.water_level}% | 肥料：{plot.fertilizer_level}级")
            
            for i, crop in enumerate(plot.crops):
                if crop:
                    stage_names = ["种子", "发芽", "成长", "成熟"]
                    status = stage_names[crop.current_stage-1] if crop.current_stage > 0 else "空闲"
                    ready_mark = "✅" if crop.is_ready else "⏳"
                    print(f"  {i+1}号位：{crop.name} - {status} {ready_mark}")
                else:
                    print(f"  {i+1}号位：空闲 🌾")
                    
        print(f"\n工具库存：{self.tools}")
        
    def plant_operation(self, player_stats: Dict):
        """种植操作"""
        print("\n🌱 种植操作")
        print("可种植的作物：")
        for name, crop in self.available_crops.items():
            print(f"- {name} (生长时间：{crop.growth_time}回合，要求：{crop.requirements})")
            
        crop_name = input("选择要种植的作物: ")
        if crop_name not in self.available_crops:
            print("未知作物")
            return
            
        # 选择地块和位置
        print("可用田地：")
        for i, plot in enumerate(self.plots):
            empty_slots = [j for j, crop in enumerate(plot.crops) if crop is None]
            if empty_slots:
                print(f"第{i+1}号田地 - 可用位置：{[x+1 for x in empty_slots]}")
                
        try:
            plot_choice = int(input("选择田地编号: ")) - 1
            slot_choice = int(input("选择位置编号: ")) - 1
            
            if 0 <= plot_choice < len(self.plots):
                plot = self.plots[plot_choice]
                crop = self.available_crops[crop_name]
                
                if plot.plant_crop(slot_choice, crop, time.time()):
                    print(f"成功在第{plot_choice+1}号田地第{slot_choice+1}位种植{crop_name}")
                else:
                    print("种植失败，请检查位置是否可用")
            else:
                print("无效的田地编号")
                
        except ValueError:
            print("输入格式错误")
            
    def farming_operations(self, operation: str, player_stats: Dict):
        """农事操作"""
        if operation == "浇水":
            print("选择要浇水的田地：")
            for i, plot in enumerate(self.plots):
                print(f"{i+1}. 第{i+1}号田地 (当前水分：{plot.water_level}%)")
                
            try:
                choice = int(input("选择田地: ")) - 1
                if 0 <= choice < len(self.plots):
                    self.plots[choice].water_plot()
            except ValueError:
                print("输入错误")
                
        elif operation == "施肥":
            if self.tools['肥料'] > 0:
                print("选择要施肥的田地：")
                for i, plot in enumerate(self.plots):
                    print(f"{i+1}. 第{i+1}号田地 (当前肥料：{plot.fertilizer_level}级)")
                    
                try:
                    choice = int(input("选择田地: ")) - 1
                    if 0 <= choice < len(self.plots):
                        if self.plots[choice].add_fertilizer():
                            self.tools['肥料'] -= 1
                except ValueError:
                    print("输入错误")
            else:
                print("没有足够的肥料")
                
        elif operation == "除草":
            if self.tools['除草剂'] > 0:
                print("使用除草剂清理杂草...")
                self.tools['除草剂'] -= 1
                print("除草完成！作物生长环境改善")
            else:
                print("没有除草剂了")
                
    def harvest_operation(self):
        """收获操作"""
        print("\n🌾 收获作物")
        rewards = {}
        
        for plot in self.plots:
            ready_crops = [(i, crop) for i, crop in enumerate(plot.crops) if crop and crop.is_ready]
            if ready_crops:
                print(f"第{plot.plot_id + 1}号田地有成熟的作物：")
                for slot, crop in ready_crops:
                    print(f"  {slot+1}. {crop.name}")
                    
                choice = input("是否收获？(y/n): ")
                if choice.lower() == 'y':
                    for slot, crop in ready_crops:
                        crop_rewards = plot.harvest_slot(slot)
                        for item, amount in crop_rewards.items():
                            rewards[item] = rewards.get(item, 0) + amount
                            
        if rewards:
            print(f"收获总计：{rewards}")
            return rewards
        return {}
        
    def update_farm(self, current_time, player_stats: Dict):
        """更新农场状态"""
        for plot in self.plots:
            plot.update_plots(current_time, player_stats)
            
    def expand_farm(self):
        """扩建农场"""
        cost = len(self.plots) * 100  # 扩建费用递增
        print(f"扩建新田地需要 {cost} 灵石")
        return cost