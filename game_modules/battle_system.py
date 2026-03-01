#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
战斗系统模块
处理修士之间的战斗和冲突
"""

import random
from typing import Dict, List

class BattleSystem:
    """战斗系统"""
    
    def __init__(self):
        self.battle_log = []
        
    def start_battle(self, player, enemy) -> bool:
        """开始战斗"""
        print(f"\n⚔️ 战斗开始！")
        print(f"对手：{enemy['name']} ({enemy['realm']})")
        
        player_hp = self._calculate_hp(player)
        enemy_hp = self._calculate_enemy_hp(enemy)
        
        round_num = 1
        
        while player_hp > 0 and enemy_hp > 0:
            print(f"\n--- 第 {round_num} 回合 ---")
            
            # 玩家攻击
            player_damage = self._calculate_damage(player, enemy)
            enemy_hp -= player_damage
            print(f"你造成 {player_damage} 点伤害")
            
            if enemy_hp <= 0:
                print(" побед了！")
                self._handle_victory(player, enemy)
                return True
                
            # 敌人攻击
            enemy_damage = self._calculate_enemy_damage(enemy, player)
            player_hp -= enemy_damage
            print(f"{enemy['name']} 造成 {enemy_damage} 点伤害")
            
            if player_hp <= 0:
                print("你败了...")
                self._handle_defeat(player)
                return False
                
            print(f"你的血量：{max(0, player_hp)}")
            print(f"敌人血量：{max(0, enemy_hp)}")
            
            round_num += 1
            
            # 战斗间隔
            input("按回车继续...")
            
    def _calculate_hp(self, player) -> int:
        """计算玩家血量"""
        base_hp = 100
        realm_bonus = {"练气期": 0, "筑基期": 50, "金丹期": 100, "元婴期": 200}
        hp = base_hp + realm_bonus.get(player.realm, 0) + (player.stats['体质'] * 10)
        return hp
        
    def _calculate_enemy_hp(self, enemy) -> int:
        """计算敌人血量"""
        base_hp = 80
        realm_multipliers = {"练气期": 1, "筑基期": 2, "金丹期": 4, "元婴期": 8}
        multiplier = realm_multipliers.get(enemy['realm'], 1)
        return base_hp * multiplier
        
    def _calculate_damage(self, player, enemy) -> int:
        """计算玩家伤害"""
        base_damage = 20
        realm_bonus = {"练气期": 0, "筑基期": 10, "金丹期": 25, "元婴期": 50}
        damage = (base_damage + 
                 realm_bonus.get(player.realm, 0) + 
                 player.stats['体质'] + 
                 random.randint(-5, 10))
        return max(1, damage)
        
    def _calculate_enemy_damage(self, enemy, player) -> int:
        """计算敌人伤害"""
        base_damage = 15
        realm_multipliers = {"练气期": 1, "筑基期": 1.5, "金丹期": 2.5, "元婴期": 4}
        multiplier = realm_multipliers.get(enemy['realm'], 1)
        damage = int(base_damage * multiplier) + random.randint(-3, 8)
        return max(1, damage)
        
    def _handle_victory(self, player, enemy):
        """处理胜利结果"""
        rewards = {
            "灵石": random.randint(20, 100),
            "经验值": random.randint(10, 30)
        }
        
        print(f"获得奖励：")
        for item, amount in rewards.items():
            if item == "灵石":
                player.add_resource(item, amount)
            print(f"- {item}: {amount}")
            
        # 修为提升
        cultivation_gain = rewards["经验值"]
        player.cultivation += cultivation_gain
        print(f"修为+{cultivation_gain}")
        
    def _handle_defeat(self, player):
        """处理失败结果"""
        # 损失一些资源
        loss = min(20, player.resources['灵石'])
        player.resources['灵石'] -= loss
        print(f"损失灵石 {loss} 枚")
        
        # 小幅度修为下降
        player.cultivation = max(0, player.cultivation - 5)