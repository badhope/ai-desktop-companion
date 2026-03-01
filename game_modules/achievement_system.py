#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
成就系统模块
追踪和奖励玩家达成的各种成就
"""

from typing import Dict, List
from datetime import datetime

class Achievement:
    """成就类"""
    
    def __init__(self, name: str, description: str, condition: str, reward: Dict):
        self.name = name
        self.description = description
        self.condition = condition  # 达成条件
        self.reward = reward  # 奖励
        self.unlocked = False
        self.unlock_time = None
        
    def check_unlock(self, player_stats: Dict) -> bool:
        """检查是否达成成就"""
        if self.unlocked:
            return False
            
        # 解析条件字符串
        try:
            # 简单条件检查示例
            if "realm:" in self.condition:
                required_realm = self.condition.split(":")[1]
                if player_stats.get('realm') == required_realm:
                    return self._unlock_achievement(player_stats)
                    
            elif "cultivation:" in self.condition:
                required_cultivation = int(self.condition.split(":")[1])
                if player_stats.get('cultivation', 0) >= required_cultivation:
                    return self._unlock_achievement(player_stats)
                    
            elif "lifetime:" in self.condition:
                max_lifetime = int(self.condition.split(":")[1])
                if player_stats.get('lifetime', 0) <= max_lifetime:
                    return self._unlock_achievement(player_stats)
                    
        except Exception as e:
            print(f"成就条件解析错误: {e}")
            
        return False
        
    def _unlock_achievement(self, player_stats: Dict) -> bool:
        """解锁成就"""
        self.unlocked = True
        self.unlock_time = datetime.now()
        print(f"🎉 成就解锁：{self.name}")
        print(f"描述：{self.description}")
        
        # 发放奖励
        for reward_type, amount in self.reward.items():
            if reward_type == "灵石":
                player_stats['resources']['灵石'] += amount
            elif reward_type == "属性":
                # 假设格式为 "体质:+2"
                stat, value = amount.split(":+")
                player_stats['stats'][stat] += int(value)
                
        print(f"获得奖励：{self.reward}")
        return True

class AchievementSystem:
    """成就系统"""
    
    def __init__(self):
        self.achievements = self._initialize_achievements()
        
    def _initialize_achievements(self) -> Dict[str, Achievement]:
        """初始化成就"""
        achievements = {
            "初入仙途": Achievement(
                "初入仙途",
                "成功踏入练气期",
                "realm:练气期",
                {"灵石": 100, "属性": "体质:+1"}
            ),
            "筑基成功": Achievement(
                "筑基成功",
                "突破至筑基期",
                "realm:筑基期",
                {"灵石": 300, "属性": "灵根:+2"}
            ),
            "金丹大道": Achievement(
                "金丹大道",
                "凝聚金丹，实力大增",
                "realm:金丹期",
                {"灵石": 800, "属性": "悟性:+3"}
            ),
            "天才修士": Achievement(
                "天才修士",
                "在100年内达到元婴期",
                "realm:元婴期,lifetime:100",
                {"灵石": 1500, "属性": "机缘:+5"}
            ),
            "苦修成圣": Achievement(
                "苦修成圣",
                "修为达到满值100",
                "cultivation:100",
                {"灵石": 500, "属性": "全属性:+1"}
            ),
            "长寿仙人": Achievement(
                "长寿仙人",
                "寿元超过500年",
                "lifetime:500",
                {"灵石": 1000}
            )
        }
        return achievements
        
    def check_achievements(self, player) -> List[str]:
        """检查所有成就"""
        unlocked = []
        player_stats = {
            'realm': player.realm,
            'cultivation': player.cultivation,
            'lifetime': player.lifetime,
            'resources': player.resources,
            'stats': player.stats
        }
        
        for name, achievement in self.achievements.items():
            if achievement.check_unlock(player_stats):
                unlocked.append(name)
                
        return unlocked
        
    def get_unlocked_achievements(self) -> List[Achievement]:
        """获取已解锁的成就"""
        return [ach for ach in self.achievements.values() if ach.unlocked]
        
    def get_locked_achievements(self) -> List[Achievement]:
        """获取未解锁的成就"""
        return [ach for ach in self.achievements.values() if not ach.unlocked]
        
    def show_achievements(self, player):
        """显示成就状态"""
        print("\n=== 成就系统 ===")
        
        # 显示已解锁成就
        unlocked = self.get_unlocked_achievements()
        if unlocked:
            print("✅ 已解锁成就：")
            for achievement in unlocked:
                print(f"  🎉 {achievement.name} - {achievement.description}")
                print(f"     解锁时间：{achievement.unlock_time.strftime('%Y-%m-%d %H:%M')}")
        else:
            print("❌ 暂无已解锁成就")
            
        # 显示可达成的成就
        locked = self.get_locked_achievements()
        if locked:
            print("\n🎯 可达成成就：")
            for achievement in locked:
                print(f"  🔒 {achievement.name} - {achievement.description}")
                print(f"     条件：{achievement.condition}")