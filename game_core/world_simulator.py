#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界模拟器
负责生成和管理游戏世界的动态内容
"""

import random
from typing import Dict, List
from datetime import datetime

class WorldSimulator:
    """世界模拟器类"""
    
    def __init__(self):
        self.world_state = {
            'season': '春季',
            'weather': '晴朗',
            '灵气浓度': 50,
            'world_events': [],
            'npc_cultivators': [],
            'locations': self._generate_locations()
        }
        self.time_cycle = 0
        
    def _generate_locations(self) -> List[str]:
        """生成世界地点"""
        locations = [
            "青云山脉", "幽冥谷", "天机城", "万宝阁",
            "紫霄宫", "血魔宗", "逍遥派", "昆仑仙境",
            "蓬莱岛", "九幽冥府"
        ]
        return locations[:6]  # 初始开放6个地点
        
    def update_world_state(self):
        """更新世界状态"""
        self.time_cycle += 1
        
        # 季节变化
        seasons = ['春季', '夏季', '秋季', '冬季']
        self.world_state['season'] = seasons[(self.time_cycle // 4) % 4]
        
        # 天气变化
        weathers = ['晴朗', '多云', '小雨', '雷暴', '大雾']
        weather_weights = [0.4, 0.3, 0.15, 0.1, 0.05]
        self.world_state['weather'] = random.choices(weathers, weights=weather_weights)[0]
        
        # 灵气浓度波动
        base_spirit = 50
        season_modifier = {'春季': 10, '夏季': 5, '秋季': 0, '冬季': -5}
        weather_modifier = {'晴朗': 5, '多云': 0, '小雨': -3, '雷暴': 15, '大雾': -10}
        
        spirit_level = (base_spirit + 
                       season_modifier[self.world_state['season']] + 
                       weather_modifier[self.world_state['weather']] +
                       random.randint(-10, 10))
        self.world_state['灵气浓度'] = max(10, min(100, spirit_level))
        
        # 生成世界事件
        self._generate_world_events()
        
        # 更新NPC状态
        self._update_npc_states()
        
    def _generate_world_events(self):
        """生成世界事件"""
        event_chance = random.random()
        
        if event_chance < 0.15:  # 15%概率生成事件
            events = [
                {
                    'name': '灵气潮汐',
                    'description': '天地灵气异常活跃',
                    'effect': '修炼效率提升',
                    'duration': 3
                },
                {
                    'name': '妖兽出没',
                    'description': '附近出现强大妖兽',
                    'effect': '危险但有机缘',
                    'duration': 2
                },
                {
                    'name': '拍卖会',
                    'description': '万宝阁举办珍品拍卖',
                    'effect': '可购买珍贵物品',
                    'duration': 1
                },
                {
                    'name': '门派招收',
                    'description': '各大门派开始招收弟子',
                    'effect': '可加入门派',
                    'duration': 5
                }
            ]
            
            event = random.choice(events)
            event['start_time'] = self.time_cycle
            self.world_state['world_events'].append(event)
            
            # 清理过期事件
            self.world_state['world_events'] = [
                e for e in self.world_state['world_events'] 
                if self.time_cycle - e['start_time'] < e['duration']
            ]
            
    def _update_npc_states(self):
        """更新NPC状态"""
        # 生成新的NPC修士
        if len(self.world_state['npc_cultivators']) < 10 and random.random() < 0.3:
            npc = self._generate_npc_cultivator()
            self.world_state['npc_cultivators'].append(npc)
            
        # 更新现有NPC位置和状态
        for npc in self.world_state['npc_cultivators']:
            if random.random() < 0.4:  # 40%概率移动
                npc['location'] = random.choice(self.world_state['locations'])
                
    def _generate_npc_cultivator(self) -> Dict:
        """生成NPC修士"""
        realms = ["练气期", "筑基期", "金丹期", "元婴期"]
        names = ["李青云", "王玄机", "张无忌", "赵敏", "周芷若", "小龙女", "杨过", "令狐冲"]
        
        return {
            'name': random.choice(names),
            'realm': random.choice(realms),
            'personality': random.choice(['友善', '冷漠', '狡诈', '正直']),
            'location': random.choice(self.world_state['locations']),
            'relationship': '陌生'  # 与玩家的关系
        }
        
    def get_current_weather(self) -> str:
        """获取当前天气"""
        return self.world_state['weather']
        
    def get_spirit_concentration(self) -> int:
        """获取当前灵气浓度"""
        return self.world_state['灵气浓度']
        
    def get_active_events(self) -> List[Dict]:
        """获取当前活动事件"""
        return self.world_state['world_events']
        
    def get_nearby_cultivators(self, location: str = None) -> List[Dict]:
        """获取附近的修士"""
        if location:
            return [npc for npc in self.world_state['npc_cultivators'] 
                   if npc['location'] == location]
        return self.world_state['npc_cultivators'][:3]  # 返回最近的3个
        
    def get_available_locations(self) -> List[str]:
        """获取可前往的地点"""
        return self.world_state['locations']
        
    def travel_to_location(self, location: str) -> bool:
        """前往指定地点"""
        if location in self.world_state['locations']:
            print(f"前往 {location}...")
            # 可以添加旅行时间和事件
            return True
        return False