#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界观构建系统
构建完整的修仙世界背景、势力分布和历史脉络
"""

import random
from typing import Dict, List, Tuple
from datetime import datetime

class WorldHistory:
    """世界历史系统"""
    
    def __init__(self):
        self.epochs = self._initialize_epochs()
        self.major_events = self._initialize_major_events()
        self.current_era = "末法时代"  # 当前时代
        
    def _initialize_epochs(self) -> Dict[str, Dict]:
        """初始化修仙时代划分"""
        return {
            "洪荒时代": {
                "duration": "开天辟地至万族争霸",
                "characteristics": "神魔共存，法则初显",
                "power_level": "大罗金仙以上",
                "ended_by": "巫妖大战"
            },
            "上古时代": {
                "duration": "万族争霸至人族崛起", 
                "characteristics": "万族鼎立，人族弱势",
                "power_level": "大乘期至渡劫期",
                "ended_by": "人族统一战争"
            },
            "远古时代": {
                "duration": "人族统一至百家争鸣",
                "characteristics": "修仙文明繁荣，宗门林立",
                "power_level": "化神期至合体期",
                "ended_by": "第一次魔劫"
            },
            "上界时代": {
                "duration": "百家争鸣至上界降临",
                "characteristics": "上界修士下凡，技术革新",
                "power_level": "元婴期至化神期",
                "ended_by": "上界封闭"
            },
            "末法时代": {
                "duration": "上界封闭至今",
                "characteristics": "灵气稀薄，修炼艰难",
                "power_level": "练气期至元婴期",
                "ended_by": "未知"
            }
        }
        
    def _initialize_major_events(self) -> List[Dict]:
        """初始化重大历史事件"""
        return [
            {
                "name": "开天辟地",
                "era": "洪荒时代",
                "description": "盘古开天，清气上升为天，浊气下沉为地",
                "impact": "奠定世界基础法则"
            },
            {
                "name": "巫妖大战",
                "era": "洪荒时代", 
                "description": "巫族与妖族为争夺天地主角地位爆发大战",
                "impact": "导致洪荒破碎，万族凋零"
            },
            {
                "name": "人族崛起",
                "era": "上古时代",
                "description": "人族在夹缝中发展壮大，逐渐成为主导种族",
                "impact": "确立人族在修仙界的统治地位"
            },
            {
                "name": "百家争鸣",
                "era": "远古时代",
                "description": "各大修仙宗门创立，修炼体系日趋完善",
                "impact": "形成完整的修仙文明体系"
            },
            {
                "name": "第一次魔劫",
                "era": "远古时代",
                "description": "魔界入侵，修仙界面临灭顶之灾",
                "impact": "重塑修仙界格局，催生新的修炼法门"
            },
            {
                "name": "上界降临",
                "era": "上界时代",
                "description": "上界修士大规模下凡，带来先进修炼技术",
                "impact": "修仙文明飞跃发展，但也埋下隐患"
            },
            {
                "name": "上界封闭",
                "era": "上界时代",
                "description": "上界突然封闭，断绝与下界的联系",
                "impact": "灵气枯竭，修仙文明衰落，进入末法时代"
            }
        ]
        
    def get_current_context(self) -> Dict[str, any]:
        """获取当前世界背景"""
        return {
            "era": self.current_era,
            "era_details": self.epochs[self.current_era],
            "recent_events": self._get_recent_events(),
            "world_state": self._get_world_state()
        }
        
    def _get_recent_events(self) -> List[str]:
        """获取近期重要事件"""
        recent = [
            "青云山脉发现上古遗迹",
            "天机城出现神秘商人",
            "魔气在幽冥谷重现",
            "万宝阁举办百年拍卖会",
            "各大门派开始招收新弟子"
        ]
        return random.sample(recent, 3)
        
    def _get_world_state(self) -> Dict[str, any]:
        """获取当前世界状态"""
        return {
            "灵气浓度": random.randint(30, 70),  # 末法时代特征
            "修仙资源": "稀缺",
            "主要威胁": ["魔气复苏", "妖兽暴动", "人心不古"],
            "发展机遇": ["古遗迹现世", "新修炼法门", "跨界机缘"]
        }

class MajorFactions:
    """主要势力系统"""
    
    def __init__(self):
        self.factions = self._initialize_factions()
        self.relations = self._initialize_relations()
        
    def _initialize_factions(self) -> Dict[str, Dict]:
        """初始化主要势力"""
        return {
            "青云剑派": {
                "type": "正道宗门",
                "founder": "青云子",
                "specialty": "剑修",
                "territory": "青云山脉",
                "strength": "强大",
                "philosophy": "以剑证道，除魔卫道",
                "relations": {"友好": ["天道盟"], "敌对": ["血魔宗"]}
            },
            "天道盟": {
                "type": "正道联盟",
                "founder": "天机老人",
                "specialty": "综合修仙",
                "territory": "天机城周边",
                "strength": "最强",
                "philosophy": "天道酬勤，厚德载物",
                "relations": {"友好": ["青云剑派", "丹霞宗"], "中立": ["器符门"]}
            },
            "丹霞宗": {
                "type": "丹修宗门",
                "founder": "丹霞真人",
                "specialty": "炼丹术",
                "territory": "丹霞山",
                "strength": "中等",
                "philosophy": "丹道通神，延年益寿",
                "relations": {"友好": ["天道盟"], "竞争": ["万毒门"]}
            },
            "器符门": {
                "type": "器修宗门",
                "founder": "器符子",
                "specialty": "炼器制符",
                "territory": "器符谷",
                "strength": "中等",
                "philosophy": "巧夺天工，以器证道",
                "relations": {"中立": ["天道盟"], "合作": ["万宝阁"]}
            },
            "血魔宗": {
                "type": "魔道宗门",
                "founder": "血魔老祖",
                "specialty": "血魔法",
                "territory": "血魔岭",
                "strength": "强大",
                "philosophy": "弱肉强食，唯我独尊",
                "relations": {"敌对": ["青云剑派", "天道盟"], "同盟": ["万毒门"]}
            },
            "万毒门": {
                "type": "邪修宗门",
                "founder": "万毒老怪",
                "specialty": "毒修蛊修",
                "territory": "万毒沼泽",
                "strength": "较弱",
                "philosophy": "以毒养身，以蛊控人",
                "relations": {"敌对": ["丹霞宗"], "同盟": ["血魔宗"]}
            },
            "万宝阁": {
                "type": "商业势力",
                "founder": "万宝真人",
                "specialty": "商贸情报",
                "territory": "各大城市",
                "strength": "财力雄厚",
                "philosophy": "无商不奸，利益至上",
                "relations": {"商业合作": ["器符门"], "复杂": ["各方势力"]}
            }
        }
        
    def _initialize_relations(self) -> Dict[Tuple[str, str], str]:
        """初始化势力关系"""
        relations = {}
        # 这里可以详细定义各势力间的具体关系
        return relations
        
    def get_faction_info(self, faction_name: str) -> Dict:
        """获取势力详细信息"""
        return self.factions.get(faction_name, {})
        
    def get_faction_relations(self, faction_name: str) -> Dict[str, List[str]]:
        """获取势力关系网"""
        faction = self.factions.get(faction_name, {})
        return faction.get("relations", {})

class WorldGeography:
    """世界地理系统"""
    
    def __init__(self):
        self.locations = self._initialize_locations()
        self.treasure_maps = self._initialize_treasure_maps()
        
    def _initialize_locations(self) -> Dict[str, Dict]:
        """初始化重要地点"""
        return {
            "青云山脉": {
                "type": "修炼圣地",
                "danger_level": "中等",
                "resources": ["灵石矿脉", "千年灵草", "剑气残留"],
                "special_features": ["剑冢遗址", "云海仙境"],
                "accessibility": "需要引荐",
                "controlled_by": "青云剑派"
            },
            "幽冥谷": {
                "type": "险地",
                "danger_level": "极高",
                "resources": ["阴属性材料", "鬼物内丹", "冥界气息"],
                "special_features": ["万魂幡", "幽冥泉", "白骨平原"],
                "accessibility": "极其危险",
                "controlled_by": "未知势力"
            },
            "天机城": {
                "type": "修仙都市",
                "danger_level": "低",
                "resources": ["修仙物资", "情报信息", "人脉关系"],
                "special_features": ["拍卖行", "坊市", "客栈酒楼"],
                "accessibility": "开放",
                "controlled_by": "天道盟"
            },
            "丹霞山": {
                "type": "丹修圣地",
                "danger_level": "中等",
                "resources": ["炼丹材料", "火焰精华", "药园"],
                "special_features": ["丹炉峰", "药王谷", "火焰池"],
                "accessibility": "需要丹道基础",
                "controlled_by": "丹霞宗"
            },
            "器符谷": {
                "type": "器修圣地",
                "danger_level": "中等",
                "resources": ["炼器材料", "符纸灵墨", "机关零件"],
                "special_features": ["炼器坊", "符箓塔", "机关密室"],
                "accessibility": "需要器道基础",
                "controlled_by": "器符门"
            },
            "血魔岭": {
                "type": "魔道禁地",
                "danger_level": "极高",
                "resources": ["魔晶", "血煞之气", "邪恶材料"],
                "special_features": ["血池", "魔殿废墟", "怨灵聚集地"],
                "accessibility": "极度危险",
                "controlled_by": "血魔宗"
            },
            "万毒沼泽": {
                "type": "毒瘴之地",
                "danger_level": "高",
                "resources": ["毒物", "蛊虫", "剧毒材料"],
                "special_features": ["毒龙潭", "蛊神庙", "万毒阵"],
                "accessibility": "需要防护措施",
                "controlled_by": "万毒门"
            },
            "蓬莱仙岛": {
                "type": "海外仙山",
                "danger_level": "未知",
                "resources": ["仙灵之气", "珍稀材料", "仙人遗迹"],
                "special_features": ["仙人居所", "时空裂缝", "海外秘境"],
                "accessibility": "传说之地",
                "controlled_by": "传说中的仙人"
            }
        }
        
    def _initialize_treasure_maps(self) -> List[Dict]:
        """初始化藏宝图系统"""
        return [
            {
                "name": "上古剑冢地图",
                "location": "青云山脉深处",
                "difficulty": "极高",
                "rewards": ["上古剑诀", "神器残片", "大量灵石"],
                "clues": ["剑气指引", "星辰定位", "古阵破解"]
            },
            {
                "name": "丹霞秘境图",
                "location": "丹霞山秘境",
                "difficulty": "中等",
                "rewards": ["千年丹方", "灵药种子", "丹火精粹"],
                "clues": ["药香追踪", "火焰印记", "丹道感悟"]
            },
            {
                "name": "器符传承图",
                "location": "器符谷地下",
                "difficulty": "中等",
                "rewards": ["上古炼器法", "符箓真传", "机关秘术"],
                "clues": ["金属共鸣", "符文显现", "机关启动"]
            },
            {
                "name": "幽冥宝藏图",
                "location": "幽冥谷核心",
                "difficulty": "致命",
                "rewards": ["冥界至宝", "鬼道真经", "阴属性神器"],
                "clues": ["阴气感应", "鬼哭狼嚎", "生死考验"]
            }
        ]
        
    def get_location_info(self, location_name: str) -> Dict:
        """获取地点详细信息"""
        return self.locations.get(location_name, {})
        
    def get_random_treasure_hunt(self) -> Dict:
        """随机获取一个寻宝任务"""
        return random.choice(self.treasure_maps)

class WorldBuildingSystem:
    """世界观构建主系统"""
    
    def __init__(self):
        self.history = WorldHistory()
        self.factions = MajorFactions()
        self.geography = WorldGeography()
        self.world_context = self._build_world_context()
        
    def _build_world_context(self) -> Dict[str, any]:
        """构建完整的世界背景"""
        context = {
            "history": self.history.get_current_context(),
            "major_factions": self.factions.factions,
            "key_locations": self.geography.locations,
            "current_events": self.history._get_recent_events(),
            "world_tension": self._calculate_world_tension()
        }
        return context
        
    def _calculate_world_tension(self) -> str:
        """计算当前世界紧张程度"""
        tensions = ["平静", "暗流涌动", "局势紧张", "剑拔弩张", "大战将起"]
        # 基于各种因素计算紧张程度
        base_tension = 2  # 默认暗流涌动
        modifiers = random.randint(-1, 2)
        final_index = max(0, min(len(tensions)-1, base_tension + modifiers))
        return tensions[final_index]
        
    def get_world_overview(self) -> str:
        """获取世界概况"""
        context = self.history.get_current_context()
        overview = f"""
=== 修仙世界概况 ===

时代背景：{context['era']}
时代特征：{context['era_details']['characteristics']}
灵气状况：{context['world_state']['灵气浓度']}%
修仙资源：{context['world_state']['修仙资源']}

主要势力格局：
{self._format_factions_overview()}

重要地理：
{self._format_locations_overview()}

当前局势：{self._calculate_world_tension()}
        """
        return overview.strip()
        
    def _format_factions_overview(self) -> str:
        """格式化势力概览"""
        overview = ""
        major_factions = ["天道盟", "青云剑派", "血魔宗", "丹霞宗"]
        for faction in major_factions:
            info = self.factions.get_faction_info(faction)
            if info:
                overview += f"  • {faction} - {info['type']} - {info['strength']}\n"
        return overview
        
    def _format_locations_overview(self) -> str:
        """格式化地点概览"""
        overview = ""
        key_locations = ["青云山脉", "天机城", "幽冥谷", "丹霞山"]
        for location in key_locations:
            info = self.geography.get_location_info(location)
            if info:
                overview += f"  • {location} - {info['type']} - 危险等级：{info['danger_level']}\n"
        return overview
        
    def get_dynamic_events(self) -> List[str]:
        """获取动态世界事件"""
        return self.history._get_recent_events()