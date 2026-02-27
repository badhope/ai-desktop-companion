#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
像素角色动画系统
支持字符动画、表情变化、动作序列等
"""

import time
import random
import threading
from typing import List, Dict, Callable

class PixelAnimator:
    def __init__(self):
        self.animations = {}
        self.current_animation = None
        self.is_animating = False
        self.animation_thread = None
        
        # 初始化预设动画
        self._init_default_animations()
    
    def _init_default_animations(self):
        """初始化默认动画"""
        # 表情动画
        self.animations['happy'] = [
            '😊', '😃', '😄', '😁', '😆', '😅', '😂', '🤣'
        ]
        
        self.animations['sad'] = [
            '😢', '😭', '😞', '😔', '😟', '🙁', '☹️', '😣'
        ]
        
        self.animations['angry'] = [
            '😠', '😡', '🤬', '😤', '💢', '🔥', '💣', '💥'
        ]
        
        self.animations['surprised'] = [
            '😮', '😯', '😲', '😳', '😵', '🤯', '😱', '🙀'
        ]
        
        self.animations['thinking'] = [
            '🤔', '💭', '💡', '🤓', '🧐', '👁️‍🗨️', '💭', '❓'
        ]
        
        # 动作动画
        self.animations['dance'] = [
            '💃', '🕺', '👯', '🎉', '🎊', '✨', '💫', '🌟'
        ]
        
        self.animations['sleep'] = [
            '😴', '😪', '😫', '🥱', '🛌', '🌙', '⭐', '💤'
        ]
        
        self.animations['excited'] = [
            '🤩', '🥳', '🎊', '🎉', '✨', '💫', '🔥', '💯'
        ]
        
        # 天气动画
        self.animations['sunny'] = [
            '☀️', '😎', '🕶️', '🏖️', '🌊', '🌞', '🌈', '🌤️'
        ]
        
        self.animations['rainy'] = [
            '🌧️', '☔', '⛈️', '🌩️', '💧', '💦', '☂️', '☔'
        ]
    
    def add_custom_animation(self, name: str, frames: List[str]):
        """添加自定义动画"""
        if len(frames) < 2:
            raise ValueError("动画至少需要2帧")
        self.animations[name] = frames
    
    def play_animation(self, animation_name: str, duration: float = 3.0, 
                      loop: bool = False, callback: Callable = None):
        """播放动画"""
        if animation_name not in self.animations:
            raise ValueError(f"动画 '{animation_name}' 不存在")
        
        if self.is_animating:
            self.stop_animation()
        
        self.current_animation = animation_name
        self.is_animating = True
        
        def animation_worker():
            frames = self.animations[animation_name]
            frame_duration = 0.3  # 每帧持续时间
            total_frames = int(duration / frame_duration)
            
            try:
                while self.is_animating and (loop or total_frames > 0):
                    for frame in frames:
                        if not self.is_animating:
                            break
                        print(f"\r{frame}", end='', flush=True)
                        time.sleep(frame_duration)
                        if not loop:
                            total_frames -= 1
                            if total_frames <= 0:
                                break
            except Exception as e:
                print(f"\n动画播放出错: {e}")
            finally:
                if callback:
                    callback()
                self.is_animating = False
        
        self.animation_thread = threading.Thread(target=animation_worker, daemon=True)
        self.animation_thread.start()
    
    def stop_animation(self):
        """停止当前动画"""
        self.is_animating = False
        if self.animation_thread:
            self.animation_thread.join(timeout=1)
    
    def get_available_animations(self) -> List[str]:
        """获取可用动画列表"""
        return list(self.animations.keys())
    
    def create_emotion_sequence(self, emotions: List[str], hold_time: float = 1.0):
        """创建情感序列动画"""
        def emotion_worker():
            for emotion in emotions:
                if emotion in self.animations:
                    frames = self.animations[emotion][:3]  # 只取前3帧
                    for frame in frames:
                        print(f"\r{frame}", end='', flush=True)
                        time.sleep(hold_time / 3)
            print()  # 换行
        
        thread = threading.Thread(target=emotion_worker, daemon=True)
        thread.start()
        return thread
    
    def random_emotion_animation(self):
        """随机播放情感动画"""
        emotions = ['happy', 'sad', 'angry', 'surprised', 'thinking']
        emotion = random.choice(emotions)
        self.play_animation(emotion, duration=2.0)

# 全局动画器实例
pixel_animator = PixelAnimator()