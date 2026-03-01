#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
存档系统模块
处理游戏的保存和读取功能
"""

import json
import os
from datetime import datetime
from typing import Dict, List

class SaveSystem:
    """存档系统"""
    
    def __init__(self, save_dir: str = "saves"):
        self.save_dir = save_dir
        self._ensure_save_directory()
        
    def _ensure_save_directory(self):
        """确保存档目录存在"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            
    def save_game(self, player, game_state: Dict, save_name: str = None) -> str:
        """保存游戏"""
        if not save_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_name = f"save_{timestamp}"
            
        save_data = {
            'player': player.get_save_data(),
            'game_state': game_state,
            'save_time': datetime.now().isoformat(),
            'version': '1.0'
        }
        
        save_path = os.path.join(self.save_dir, f"{save_name}.json")
        
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            print(f"游戏已保存至: {save_path}")
            return save_path
        except Exception as e:
            print(f"保存失败: {e}")
            return None
            
    def load_game(self, save_name: str):
        """读取游戏存档"""
        save_path = os.path.join(self.save_dir, f"{save_name}.json")
        
        if not os.path.exists(save_path):
            print(f"存档不存在: {save_path}")
            return None
            
        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
                
            print(f"成功读取存档: {save_path}")
            return save_data
        except Exception as e:
            print(f"读取存档失败: {e}")
            return None
            
    def list_saves(self) -> List[str]:
        """列出所有存档"""
        saves = []
        if os.path.exists(self.save_dir):
            for file in os.listdir(self.save_dir):
                if file.endswith('.json'):
                    saves.append(file[:-5])  # 移除.json后缀
        return sorted(saves)
        
    def delete_save(self, save_name: str) -> bool:
        """删除存档"""
        save_path = os.path.join(self.save_dir, f"{save_name}.json")
        
        if os.path.exists(save_path):
            try:
                os.remove(save_path)
                print(f"已删除存档: {save_name}")
                return True
            except Exception as e:
                print(f"删除失败: {e}")
                return False
        else:
            print(f"存档不存在: {save_name}")
            return False
            
    def auto_save(self, player, game_state: Dict):
        """自动保存"""
        return self.save_game(player, game_state, "auto_save")