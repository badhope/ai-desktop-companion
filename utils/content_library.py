#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
内容库系统
管理各种文本、图片、音频等内容资源
"""

import json
import random
from typing import Dict, List, Any
from pathlib import Path

class ContentLibrary:
    def __init__(self):
        self.content_dir = Path("content")
        self.content_dir.mkdir(exist_ok=True)
        
        # 初始化各类内容库
        self.jokes = self._load_jokes()
        self.quotes = self._load_quotes()
        self.facts = self._load_facts()
        self.stories = self._load_stories()
        self.trivia = self._load_trivia()
        self.poems = self._load_poems()
        
    def _load_jokes(self) -> List[str]:
        """加载笑话库"""
        jokes = [
            "为什么程序员喜欢黑暗模式？因为bug在黑暗中更难被发现！",
            "电脑对程序员说：你又熬夜了，注意身体。程序员说：你又关机了，注意电源。",
            "为什么Java开发者穿格子衬衫？因为他们喜欢面向对象！",
            "程序员的女朋友说：你爱我还是爱代码？程序员说：我爱Python！",
            "为什么程序员总是分不清万圣节和圣诞节？因为 Oct 31 = Dec 25！",
            "有一个程序员去买菜，老婆说：买一斤苹果，如果有鸡蛋的话，买十个。程序员回来买了十斤苹果。",
            "程序员面试官问：你有什么优点？应聘者答：我能准确预测项目完成时间。面试官：什么时候能入职？应聘者：昨天。",
            "为什么程序员不喜欢在户外工作？因为那里有太多的 bugs。"
        ]
        return jokes
    
    def _load_quotes(self) -> List[str]:
        """加载名言库"""
        quotes = [
            "业精于勤荒于嬉，行成于思毁于随。",
            "书山有路勤为径，学海无涯苦作舟。",
            "宝剑锋从磨砺出，梅花香自苦寒来。",
            "世上无难事，只要肯登攀。",
            "天道酬勤，厚德载物。",
            "千里之行，始于足下。",
            "学而不思则罔，思而不学则殆。",
            "知之者不如好之者，好之者不如乐之者。"
        ]
        return quotes
    
    def _load_facts(self) -> List[str]:
        """加载有趣事实库"""
        facts = [
            "章鱼有三个心脏，其中两个在给鳃供血，第三个给身体其他部位供血。",
            "蜂蜜永远不会变质，考古学家曾在古埃及 tombs 中发现过3000年前的蜂蜜，仍然可以食用。",
            "企鹅求婚时会送对方一颗漂亮的石头。",
            "香蕉其实是浆果，而草莓却不是浆果。",
            "人类和香蕉共享约60%的DNA。",
            "猫的呼噜声频率在20-50赫兹之间，这种频率有助于骨骼生长和愈合。",
            "地球上所有的蚂蚁重量加起来大约等于所有人类的重量。",
            "海马是唯一由雄性怀孕生育的动物。"
        ]
        return facts
    
    def _load_stories(self) -> List[Dict[str, str]]:
        """加载故事库"""
        stories = [
            {
                "title": "勇敢的小兔子",
                "content": "从前有一只小兔子，它虽然胆小但很善良。一天森林着火了，小兔子勇敢地叫醒了所有动物，帮助大家安全撤离。从此大家都称它为'勇敢的小兔子'。"
            },
            {
                "title": "聪明的乌鸦",
                "content": "一只乌鸦口渴了，看到瓶子里有水但够不到。它想了个办法，叼来小石子一颗颗放进瓶子里，水位慢慢上升，终于喝到了水。"
            },
            {
                "title": "勤劳的蜜蜂",
                "content": "小蜜蜂每天辛勤采蜜，从不偷懒。它告诉朋友们：只有努力工作，才能酿造出甜美的蜂蜜。大家都被它的精神感动了。"
            }
        ]
        return stories
    
    def _load_trivia(self) -> List[str]:
        """加载冷知识库"""
        trivia = [
            "蜗牛的牙齿长在舌头上，称为齿舌，有数千颗细小的牙齿。",
            "考拉宝宝吃的第一个固体食物是妈妈的便便，这有助于消化桉树叶。",
            "长颈鹿的舌头是蓝黑色的，这样可以防止晒伤。",
            "北极熊的皮肤其实是黑色的，毛发是透明的。",
            "鲨鱼可以感知到水中百万分之一浓度的血液。",
            "蝴蝶的味觉器官在脚上，它们用脚来品尝花朵。",
            "企鹅走路时摇摆是为了节省能量，比直线行走节能20%。",
            "大象是唯一不能跳跃的哺乳动物。"
        ]
        return trivia
    
    def _load_poems(self) -> List[str]:
        """加载诗歌库"""
        poems = [
            """春晓
春眠不觉晓，
处处闻啼鸟。
夜来风雨声，
花落知多少。""",
            
            """静夜思
床前明月光，
疑是地上霜。
举头望明月，
低头思故乡。""",
            
            """咏鹅
鹅，鹅，鹅，
曲项向天歌。
白毛浮绿水，
红掌拨清波。"""
        ]
        return poems
    
    def get_random_joke(self) -> str:
        """获取随机笑话"""
        return random.choice(self.jokes)
    
    def get_random_quote(self) -> str:
        """获取随机名言"""
        return random.choice(self.quotes)
    
    def get_random_fact(self) -> str:
        """获取随机事实"""
        return random.choice(self.facts)
    
    def get_random_story(self) -> Dict[str, str]:
        """获取随机故事"""
        return random.choice(self.stories)
    
    def get_random_trivia(self) -> str:
        """获取随机冷知识"""
        return random.choice(self.trivia)
    
    def get_random_poem(self) -> str:
        """获取随机诗歌"""
        return random.choice(self.poems)
    
    def search_content(self, keyword: str, content_type: str = "all") -> List[Any]:
        """搜索内容"""
        results = []
        keyword = keyword.lower()
        
        content_mapping = {
            "jokes": self.jokes,
            "quotes": self.quotes,
            "facts": self.facts,
            "stories": self.stories,
            "trivia": self.trivia,
            "poems": self.poems
        }
        
        if content_type == "all":
            content_lists = content_mapping.values()
        else:
            content_lists = [content_mapping.get(content_type, [])]
        
        for content_list in content_lists:
            for item in content_list:
                if isinstance(item, dict):
                    # 处理故事等字典类型
                    text = " ".join(item.values()).lower()
                else:
                    text = str(item).lower()
                
                if keyword in text:
                    results.append(item)
        
        return results
    
    def add_content(self, content_type: str, content: Any):
        """添加新内容"""
        if hasattr(self, content_type):
            getattr(self, content_type).append(content)
            return True
        return False
    
    def get_content_stats(self) -> Dict[str, int]:
        """获取内容统计"""
        return {
            "jokes": len(self.jokes),
            "quotes": len(self.quotes),
            "facts": len(self.facts),
            "stories": len(self.stories),
            "trivia": len(self.trivia),
            "poems": len(self.poems),
            "total": len(self.jokes) + len(self.quotes) + len(self.facts) + 
                    len(self.stories) + len(self.trivia) + len(self.poems)
        }

# 全局内容库实例
content_library = ContentLibrary()