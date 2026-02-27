#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
音频系统模块
支持音效播放、背景音乐、语音合成等功能
"""

import os
import sys
import time
import random
import threading
from pathlib import Path
from typing import Dict, List, Optional

class AudioSystem:
    def __init__(self):
        self.pygame_available = False
        self.pyttsx3_available = False
        self.sound_effects = {}
        self.background_music = {}
        self.current_music = None
        self.music_volume = 0.7
        self.sfx_volume = 1.0
        
        # 初始化音频库
        self._init_audio_libraries()
        # 加载默认音效
        self._load_default_sounds()
    
    def _init_audio_libraries(self):
        """初始化音频库"""
        try:
            import pygame
            pygame.mixer.init()
            self.pygame_available = True
            print("✅ Pygame音频系统初始化成功")
        except ImportError:
            print("⚠️  Pygame不可用，音频功能受限")
        
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self.pyttsx3_available = True
            print("✅ 文字转语音系统初始化成功")
        except ImportError:
            print("⚠️  pyttsx3不可用，语音功能受限")
    
    def _load_default_sounds(self):
        """加载默认音效"""
        # 定义默认音效（使用系统声音或生成简单音效）
        self.default_sounds = {
            'startup': self._generate_beep_sound(523, 0.2),  # C5
            'notification': self._generate_beep_sound(659, 0.1),  # E5
            'error': self._generate_beep_sound(261, 0.3),  # C4
            'success': self._generate_chime_sound(),
            'typing': self._generate_soft_click(),
            'menu_select': self._generate_menu_sound()
        }
    
    def _generate_beep_sound(self, frequency: int, duration: float):
        """生成蜂鸣声"""
        if not self.pygame_available:
            return lambda: print("🔔 beep")
        
        try:
            import numpy as np
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = np.zeros((frames, 2))
            
            for i in range(frames):
                wave = np.sin(2 * np.pi * frequency * i / sample_rate)
                arr[i][0] = wave * 0.1  # 左声道
                arr[i][1] = wave * 0.1  # 右声道
            
            return lambda: self._play_array_sound(arr, sample_rate)
        except:
            return lambda: print(f"🎵 频率: {frequency}Hz")
    
    def _generate_chime_sound(self):
        """生成钟声"""
        frequencies = [523, 659, 784]  # C-E-G 和弦
        if not self.pygame_available:
            return lambda: print("🎵 chime")
        
        try:
            import numpy as np
            sample_rate = 22050
            duration = 0.8
            frames = int(duration * sample_rate)
            arr = np.zeros((frames, 2))
            
            for freq in frequencies:
                for i in range(frames):
                    wave = np.sin(2 * np.pi * freq * i / sample_rate)
                    envelope = np.exp(-i / (sample_rate * 0.3))  # 淡出效果
                    arr[i][0] += wave * envelope * 0.05
                    arr[i][1] += wave * envelope * 0.05
            
            return lambda: self._play_array_sound(arr, sample_rate)
        except:
            return lambda: print("🎵 chime")
    
    def _generate_soft_click(self):
        """生成软点击声"""
        return lambda: print("🖱️ click")
    
    def _generate_menu_sound(self):
        """生成菜单选择声"""
        return lambda: print("🎵 select")
    
    def _play_array_sound(self, array, sample_rate):
        """播放numpy数组声音"""
        if not self.pygame_available:
            return
        
        try:
            import pygame
            import numpy as np
            sound = pygame.sndarray.make_sound((array * 32767).astype(np.int16))
            sound.set_volume(self.sfx_volume)
            sound.play()
        except Exception as e:
            print(f"播放声音失败: {e}")
    
    def play_sound(self, sound_name: str):
        """播放音效"""
        if sound_name in self.default_sounds:
            try:
                self.default_sounds[sound_name]()
            except Exception as e:
                print(f"播放音效 {sound_name} 失败: {e}")
        else:
            print(f"🎵 {sound_name}")
    
    def speak_text(self, text: str, rate: int = 200, volume: float = 0.9):
        """文字转语音"""
        if not self.pyttsx3_available:
            print(f"🗣️  {text}")
            return
        
        try:
            def tts_worker():
                self.tts_engine.setProperty('rate', rate)
                self.tts_engine.setProperty('volume', volume)
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            
            tts_thread = threading.Thread(target=tts_worker, daemon=True)
            tts_thread.start()
            
        except Exception as e:
            print(f"语音合成失败: {e}")
            print(f"🗣️  {text}")
    
    def play_background_music(self, music_type: str = "ambient"):
        """播放背景音乐"""
        if not self.pygame_available:
            print(f"🎵 播放背景音乐: {music_type}")
            return
        
        # 简单的音乐生成
        try:
            import numpy as np
            import pygame
            
            # 生成简单的环境音乐
            sample_rate = 22050
            duration = 30  # 30秒循环
            frames = int(duration * sample_rate)
            arr = np.zeros((frames, 2))
            
            # 基础频率
            base_freqs = [261, 329, 392]  # C-E-G
            
            for i, freq in enumerate(base_freqs):
                for j in range(frames):
                    # 添加一些变化
                    mod_freq = freq + 2 * np.sin(2 * np.pi * 0.1 * j / sample_rate)
                    wave = np.sin(2 * np.pi * mod_freq * j / sample_rate)
                    envelope = 0.3 * np.exp(-j / (sample_rate * 5))  # 长淡出
                    arr[j][0] += wave * envelope * 0.1
                    arr[j][1] += wave * envelope * 0.1
            
            # 创建循环播放
            music_array = (arr * 32767).astype(np.int16)
            sound = pygame.sndarray.make_sound(music_array)
            sound.set_volume(self.music_volume)
            sound.play(-1)  # -1表示无限循环
            self.current_music = sound
            
        except Exception as e:
            print(f"背景音乐播放失败: {e}")
    
    def stop_background_music(self):
        """停止背景音乐"""
        if self.current_music:
            try:
                self.current_music.stop()
                self.current_music = None
            except:
                pass
    
    def set_volume(self, music_vol: float = None, sfx_vol: float = None):
        """设置音量"""
        if music_vol is not None:
            self.music_volume = max(0, min(1, music_vol))
        if sfx_vol is not None:
            self.sfx_volume = max(0, min(1, sfx_vol))

# 全局音频系统实例
audio_system = AudioSystem()