#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI智能引导系统
主动引导玩家游戏，提供个性化建议和互动
"""

import random
import time
from typing import Dict, List, Tuple
from datetime import datetime

class AIGuide:
    """AI引导员类"""
    
    def __init__(self, player_name: str):
        self.player_name = player_name
        self.personality = self._generate_personality()
        self.relationship_level = 0  # 与玩家关系等级
        self.player_preferences = {}  # 玩家偏好记录
        self.guidance_history = []   # 引导历史
        
    def _generate_personality(self) -> Dict[str, str]:
        """生成AI引导员个性"""
        personalities = [
            {"name": "青鸾仙子", "style": "温柔细致", "tone": "关怀"},
            {"name": "玄机老人", "style": "智慧深沉", "tone": "指导"},
            {"name": "灵儿小师妹", "style": "活泼可爱", "tone": "鼓励"},
            {"name": "无尘真人", "style": "严肃认真", "tone": "督促"}
        ]
        return random.choice(personalities)
        
    def greet_player(self) -> str:
        """问候玩家"""
        greetings = [
            f"欢迎回来，{self.player_name}道友！今日感觉如何？",
            f"{self.player_name}，老夫已经为你准备好了一天的修炼安排。",
            f"师兄师姐，今天想先做什么呢？",
            f"道友安好，今日天机显示你运势颇佳哦～"
        ]
        return random.choice(greetings)
        
    def analyze_player_state(self, player, world_state) -> Dict[str, any]:
        """分析玩家当前状态"""
        analysis = {
            'low_resources': player.resources['灵石'] < 50,
            'low_cultivation': player.cultivation < 30,
            'high_cultivation': player.cultivation > 80,
            'ready_for_breakthrough': player.cultivation > 90,
            'low_stats': any(stat < 5 for stat in player.stats.values()),
            'has_sect': hasattr(player, 'sect') and player.sect is not None,
            'weather_bonus': world_state['灵气浓度'] > 70,
            'season_bonus': world_state['season'] in ['春季', '夏季']
        }
        return analysis
        
    def provide_guidance(self, player, world_state) -> List[str]:
        """提供个性化引导建议"""
        analysis = self.analyze_player_state(player, world_state)
        suggestions = []
        
        # 根据状态提供针对性建议
        if analysis['low_resources']:
            suggestions.append("💰 你的灵石快用完了，建议去探索或者做门派任务赚取资源。")
            
        if analysis['low_cultivation'] and analysis['weather_bonus']:
            suggestions.append(f"🌤️ 今日灵气浓郁，正是修炼的好时机！")
            
        if analysis['ready_for_breakthrough']:
            suggestions.append("⚡ 你的修为即将圆满，准备突破境界了吗？")
            
        if not analysis['has_sect'] and player.realm != "凡人":
            suggestions.append("🏯 还没有门派归属呢，要不要考虑加入一个门派？")
            
        if analysis['low_stats']:
            suggestions.append("📈 某些属性偏低，可以通过学习功法或寻找机缘来提升。")
            
        # 随机添加趣味建议
        if random.random() < 0.3:
            fun_suggestions = [
                "🎮 想不想试试挑战附近的妖兽？",
                "📚 最近有不少新功法可以学习哦～",
                "👥 听说城里来了个神秘商人...",
                "🏔️ 青云山脉最近发现了新的灵草..."
            ]
            suggestions.append(random.choice(fun_suggestions))
            
        return suggestions
        
    def interactive_dialogue(self, player, topic: str) -> str:
        """交互式对话"""
        dialogues = {
            "修炼": [
                f"道友，修炼之道贵在持之以恒。你现在专注于{player.realm}的修炼，很不错呢！",
                "修炼时要注意调节心境，过于急躁反而会影响效果。",
                "我发现你最近修炼很勤奋，但是也要注意劳逸结合哦。"
            ],
            "资源": [
                "资源管理可是修仙的重要一环呢！",
                "灵石虽然重要，但也不要为了赚钱忽略了修炼本身。",
                "除了灵石，各种材料和丹药也很重要哦。"
            ],
            "探索": [
                "外面的世界很大呢，每个地方都有不同的机遇。",
                "探索时要小心，但也别错过好机会～",
                "听说最近有几个地方出现了异象..."
            ],
            "门派": [
                "有门派归属确实能得到不少好处。",
                "不过门派任务也要量力而行，别太过勉强。",
                "每个门派都有自己的特色，选择适合自己的最重要。"
            ]
        }
        
        options = dialogues.get(topic, ["这个话题很有意思呢！"])
        return random.choice(options)
        
    def give_missions(self, player) -> List[Dict]:
        """给予日常任务"""
        missions = [
            {
                'name': '日常修炼',
                'description': '进行3次修炼',
                'target': 3,
                'current': 0,
                'reward': {'灵石': 30, '经验值': 10}
            },
            {
                'name': '收集材料',
                'description': '收集5份灵药',
                'target': 5,
                'current': player.resources.get('灵药', 0),
                'reward': {'灵石': 50}
            },
            {
                'name': '门派贡献',
                'description': '完成1个门派任务',
                'target': 1,
                'current': 0,
                'reward': {'贡献点': 30}
            },
            {
                'name': '探索之旅',
                'description': '探索3个不同地点',
                'target': 3,
                'current': 0,
                'reward': {'机缘': 2}
            }
        ]
        
        # 根据玩家状态筛选合适的任务
        suitable_missions = []
        if player.resources['灵石'] < 100:
            suitable_missions.append(missions[0])  # 日常修炼
        if player.resources.get('灵药', 0) < 3:
            suitable_missions.append(missions[1])  # 收集材料
        if hasattr(player, 'sect') and player.sect:
            suitable_missions.append(missions[2])  # 门派贡献
        suitable_missions.append(missions[3])  # 探索之旅
        
        return suitable_missions[:2]  # 最多返回2个任务
        
    def celebrate_achievement(self, achievement_name: str) -> str:
        """庆祝成就达成"""
        celebrations = [
            f"🎉 太棒了！{self.player_name}你真是太厉害了！",
            f"🎊 恭喜恭喜！{achievement_name}成就达成！",
            f"🌟 哇！又解锁了一个成就，为你骄傲！",
            f"🏆 干得漂亮！这个成就可不是人人都能拿到的！"
        ]
        return random.choice(celebrations)

class AIGuideSystem:
    """AI引导系统主类"""
    
    def __init__(self):
        self.guides = {}  # 存储不同玩家的AI引导员
        
    def get_player_guide(self, player_name: str) -> AIGuide:
        """获取玩家的AI引导员"""
        if player_name not in self.guides:
            self.guides[player_name] = AIGuide(player_name)
        return self.guides[player_name]
        
    def daily_check_in(self, player, world_state) -> str:
        """每日签到问候"""
        guide = self.get_player_guide(player.name)
        greeting = guide.greet_player()
        
        # 添加当日建议
        suggestions = guide.provide_guidance(player, world_state)
        if suggestions:
            greeting += "\n\n今日建议：\n" + "\n".join(suggestions[:2])
            
        return greeting
        
    def contextual_help(self, player, action: str, world_state) -> str:
        """根据上下文提供帮助"""
        guide = self.get_player_guide(player.name)
        analysis = guide.analyze_player_state(player, world_state)
        
        help_messages = {
            "修炼": "修炼是提升修为的根本，但也要注意循序渐进哦～",
            "探索": "探索可以获得各种资源和机缘，但也存在风险...",
            "炼丹": "炼丹需要足够的材料和技巧，失败很正常，别灰心！",
            "战斗": "战斗时要根据对手特点制定策略，一味蛮干可不行。"
        }
        
        base_message = help_messages.get(action, "这个问题很有意思呢！")
        return guide.interactive_dialogue(player, action) + "\n" + base_message
        
    def adaptive_suggestion(self, player, current_action: str, world_state) -> str:
        """自适应建议"""
        guide = self.get_player_guide(player.name)
        analysis = guide.analyze_player_state(player, world_state)
        
        # 根据当前行动给出连贯建议
        suggestion_chains = {
            "修炼": ["休息", "炼丹", "探索"],
            "探索": ["修炼", "炼丹", "与其他修士交流"],
            "炼丹": ["收集材料", "修炼", "门派任务"],
            "休息": ["修炼", "探索", "与其他修士交流"]
        }
        
        next_actions = suggestion_chains.get(current_action, ["修炼", "探索"])
        next_action = random.choice(next_actions)
        
        return f"做完{current_action}之后，建议你可以试试{next_action}哦～"
        
    def emotional_response(self, player, event_type: str) -> str:
        """情感化回应"""
        guide = self.get_player_guide(player.name)
        
        emotional_responses = {
            "胜利": [
                "太厉害了！我就知道你能行的！",
                "威武！不愧是我的好伙伴！",
                "哈哈，看来今天的运气不错呢！"
            ],
            "失败": [
                "没关系的，失败是成功之母嘛～",
                "这次不行还有下次，别灰心！",
                "哎呀，稍微有点遗憾呢，不过问题不大！"
            ],
            "发现宝藏": [
                "哇！发财了发财了！",
                "运气真好！让我也替你高兴！",
                "嘿嘿，看来今天是你的幸运日！"
            ],
            "遇到危险": [
                "小心点啊！安全第一！",
                "哎呀，还好没事，吓死我了～",
                "下次要更加谨慎一些哦。"
            ]
        }
        
        responses = emotional_responses.get(event_type, ["嗯嗯，我知道了～"])
        return random.choice(responses)