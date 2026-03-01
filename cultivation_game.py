#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修仙桌面游戏主程序
Author: Lingma
Description: 基于AI的修仙模拟游戏
"""

import sys
import os
from datetime import datetime
from game_core.game_engine import GameEngine
from game_core.player import Player
from game_core.world_simulator import WorldSimulator

def main():
    """游戏主函数"""
    print("=" * 50)
    print("道士职业模拟器 v1.0")
    print("开启你的修仙之路...")
    print("=" * 50)
    
    # 初始化游戏引擎
    game_engine = GameEngine()
    
    # 创建玩家角色
    player_name = input("请输入你的道号: ")
    player = Player(player_name)
    
    # 初始化世界模拟器
    world_sim = WorldSimulator()
    
    # 开始游戏循环
    game_engine.start_game(player, world_sim)

if __name__ == "__main__":
    main()