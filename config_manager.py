#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置文件管理器
管理API密钥、用户设置等配置信息
"""

import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_file = Path('ai_companion_config.json')
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        default_config = {
            'kimi_api_key': '',
            'user_settings': {
                'username': '主人',
                'default_mode': 'desktop',
                'auto_start': False,
                'sound_enabled': True,
                'animation_enabled': True
            },
            'character_preferences': {
                'default_character': 'kaguya',
                'favorite_characters': ['kaguya', 'hatsune_miku'],
                'character_size': 70
            },
            'api_endpoints': {
                'kimi_api': 'https://api.moonshot.cn/v1/chat/completions',
                'joke_api': 'https://official-joke-api.appspot.com/jokes/random',
                'quote_api': 'https://api.quotable.io/random'
            }
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    # 合并默认配置和保存的配置
                    default_config.update(saved_config)
                    for key in default_config:
                        if isinstance(default_config[key], dict) and key in saved_config:
                            default_config[key].update(saved_config[key])
            except Exception as e:
                print(f"配置文件加载错误: {e}")
        
        return default_config
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"配置文件保存错误: {e}")
            return False
    
    def get_kimi_api_key(self):
        """获取KimiAI API密钥"""
        # 优先级：环境变量 > 配置文件 > 硬编码备份
        env_key = os.getenv('KIMI_API_KEY')
        if env_key:
            return env_key
        
        config_key = self.config.get('kimi_api_key', '')
        if config_key:
            return config_key
        
        # 备份密钥（您提供的）
        return "sk-XQX3VrDUarK"
    
    def set_kimi_api_key(self, api_key):
        """设置KimiAI API密钥"""
        self.config['kimi_api_key'] = api_key
        return self.save_config()
    
    def get_user_setting(self, setting_name, default_value=None):
        """获取用户设置"""
        return self.config['user_settings'].get(setting_name, default_value)
    
    def set_user_setting(self, setting_name, value):
        """设置用户设置"""
        self.config['user_settings'][setting_name] = value
        return self.save_config()
    
    def get_character_preference(self, pref_name, default_value=None):
        """获取角色偏好设置"""
        return self.config['character_preferences'].get(pref_name, default_value)
    
    def set_character_preference(self, pref_name, value):
        """设置角色偏好设置"""
        self.config['character_preferences'][pref_name] = value
        return self.save_config()
    
    def reset_to_defaults(self):
        """重置为默认配置"""
        self.config = {
            'kimi_api_key': '',
            'user_settings': {
                'username': '主人',
                'default_mode': 'desktop',
                'auto_start': False,
                'sound_enabled': True,
                'animation_enabled': True
            },
            'character_preferences': {
                'default_character': 'kaguya',
                'favorite_characters': ['kaguya', 'hatsune_miku'],
                'character_size': 70
            },
            'api_endpoints': {
                'kimi_api': 'https://api.moonshot.cn/v1/chat/completions',
                'joke_api': 'https://official-joke-api.appspot.com/jokes/random',
                'quote_api': 'https://api.quotable.io/random'
            }
        }
        return self.save_config()

def main():
    """配置管理器主界面"""
    manager = ConfigManager()
    
    while True:
        print("\n" + "="*50)
        print("⚙️  AI桌面伴侣 配置管理器")
        print("="*50)
        print("1. 查看当前配置")
        print("2. 设置KimiAI API密钥")
        print("3. 修改用户设置")
        print("4. 角色偏好设置")
        print("5. 重置为默认配置")
        print("6. 退出")
        print("="*50)
        
        choice = input("请选择操作: ").strip()
        
        if choice == '1':
            print("\n📋 当前配置:")
            print(json.dumps(manager.config, ensure_ascii=False, indent=2))
            
        elif choice == '2':
            api_key = input("请输入KimiAI API密钥: ").strip()
            if api_key:
                if manager.set_kimi_api_key(api_key):
                    print("✅ API密钥已保存")
                else:
                    print("❌ API密钥保存失败")
            else:
                print("❌ API密钥不能为空")
                
        elif choice == '3':
            print("\n👤 用户设置:")
            username = input(f"用户名 (当前: {manager.get_user_setting('username')}): ").strip()
            if username:
                manager.set_user_setting('username', username)
                print("✅ 用户名已更新")
            
        elif choice == '4':
            print("\n🎭 角色设置:")
            size = input(f"角色大小 (当前: {manager.get_character_preference('character_size')}): ").strip()
            if size.isdigit():
                manager.set_character_preference('character_size', int(size))
                print("✅ 角色大小已更新")
                
        elif choice == '5':
            confirm = input("确定要重置所有配置为默认值吗？(y/N): ").strip().lower()
            if confirm == 'y':
                if manager.reset_to_defaults():
                    print("✅ 配置已重置为默认值")
                else:
                    print("❌ 配置重置失败")
                    
        elif choice == '6':
            print("👋 再见！")
            break
            
        else:
            print("❌ 无效选择")

if __name__ == "__main__":
    main()