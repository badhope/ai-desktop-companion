import pygame
import pyautogui
import cv2
import numpy as np
from PIL import Image
import time
from typing import Dict, Any, Optional
from core.logger import logger_manager

class MediaController:
    def __init__(self):
        self.logger = logger_manager.get_logger('media_controller')
        self.pygame_initialized = False
        self.camera = None
        self.initialize_pygame()
    
    def initialize_pygame(self):
        """初始化Pygame"""
        try:
            pygame.init()
            pygame.mixer.init()
            self.pygame_initialized = True
            self.logger.info("Pygame初始化成功")
        except Exception as e:
            self.logger.error(f"Pygame初始化失败: {e}")
    
    def volume_control(self, action: str, amount: int = 10) -> bool:
        """音量控制"""
        try:
            if action == 'up':
                pyautogui.press('volumeup', presses=amount//2)
            elif action == 'down':
                pyautogui.press('volumedown', presses=amount//2)
            elif action == 'mute':
                pyautogui.press('volumemute')
            else:
                return False
            
            self.logger.info(f"音量控制: {action}")
            return True
            
        except Exception as e:
            self.logger.error(f"音量控制失败: {e}")
            return False
    
    def media_control(self, action: str) -> bool:
        """媒体播放控制"""
        try:
            actions = {
                'play_pause': 'playpause',
                'next': 'nexttrack',
                'previous': 'prevtrack',
                'stop': 'stop'
            }
            
            if action in actions:
                pyautogui.press(actions[action])
                self.logger.info(f"媒体控制: {action}")
                return True
            else:
                self.logger.warning(f"未知的媒体控制动作: {action}")
                return False
                
        except Exception as e:
            self.logger.error(f"媒体控制失败: {e}")
            return False
    
    def screen_capture(self, region: tuple = None) -> Optional[Image.Image]:
        """屏幕截图"""
        try:
            if region:
                screenshot = pyautogui.screenshot(region=region)
            else:
                screenshot = pyautogui.screenshot()
            
            self.logger.info("屏幕截图完成")
            return screenshot
            
        except Exception as e:
            self.logger.error(f"屏幕截图失败: {e}")
            return None
    
    def record_screen(self, duration: int = 10, fps: int = 10) -> Optional[str]:
        """录制屏幕"""
        try:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screen_recording_{timestamp}.mp4"
            
            # 初始化视频写入器
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            screen_size = pyautogui.size()
            out = cv2.VideoWriter(filename, fourcc, fps, screen_size)
            
            frames_captured = 0
            start_time = time.time()
            
            while time.time() - start_time < duration:
                # 截图并转换为OpenCV格式
                screenshot = pyautogui.screenshot()
                frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                out.write(frame)
                frames_captured += 1
                
                # 控制帧率
                time.sleep(1/fps)
            
            out.release()
            self.logger.info(f"屏幕录制完成: {filename}, 帧数: {frames_captured}")
            return filename
            
        except Exception as e:
            self.logger.error(f"屏幕录制失败: {e}")
            return None
    
    def camera_capture(self, device_id: int = 0) -> Optional[Image.Image]:
        """摄像头拍照"""
        try:
            if self.camera is None:
                self.camera = cv2.VideoCapture(device_id)
            
            if not self.camera.isOpened():
                self.camera.open(device_id)
            
            ret, frame = self.camera.read()
            if ret:
                # 转换为PIL图像
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(rgb_frame)
                self.logger.info("摄像头拍照完成")
                return image
            else:
                self.logger.error("摄像头读取失败")
                return None
                
        except Exception as e:
            self.logger.error(f"摄像头拍照失败: {e}")
            return None
    
    def close_camera(self):
        """关闭摄像头"""
        if self.camera and self.camera.isOpened():
            self.camera.release()
            self.camera = None
            self.logger.info("摄像头已关闭")
    
    def play_audio(self, file_path: str) -> bool:
        """播放音频文件"""
        try:
            if not self.pygame_initialized:
                self.initialize_pygame()
            
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            self.logger.info(f"开始播放音频: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"播放音频失败: {e}")
            return False
    
    def stop_audio(self) -> bool:
        """停止音频播放"""
        try:
            if self.pygame_initialized:
                pygame.mixer.music.stop()
                self.logger.info("音频播放已停止")
                return True
            return False
        except Exception as e:
            self.logger.error(f"停止音频失败: {e}")
            return False
    
    def get_audio_status(self) -> Dict[str, Any]:
        """获取音频状态"""
        try:
            return {
                'is_playing': pygame.mixer.music.get_busy() if self.pygame_initialized else False,
                'volume': pygame.mixer.music.get_volume() if self.pygame_initialized else 0
            }
        except Exception as e:
            self.logger.error(f"获取音频状态失败: {e}")
            return {'error': str(e)}
    
    def brightness_control(self, action: str, amount: int = 10) -> bool:
        """屏幕亮度控制"""
        try:
            # Windows系统亮度控制
            if action == 'up':
                for _ in range(amount//10):
                    pyautogui.hotkey('fn', 'f3')  # 常见的亮度增加快捷键
            elif action == 'down':
                for _ in range(amount//10):
                    pyautogui.hotkey('fn', 'f2')  # 常见的亮度降低快捷键
            
            self.logger.info(f"亮度控制: {action}")
            return True
            
        except Exception as e:
            self.logger.error(f"亮度控制失败: {e}")
            return False
    
    def display_info(self) -> Dict[str, Any]:
        """获取显示信息"""
        try:
            screen_size = pyautogui.size()
            screenshot = pyautogui.screenshot()
            
            return {
                'screen_width': screen_size.width,
                'screen_height': screen_size.height,
                'color_depth': screenshot.mode,
                'screenshot_size': len(screenshot.tobytes())
            }
        except Exception as e:
            self.logger.error(f"获取显示信息失败: {e}")
            return {'error': str(e)}
    
    def __del__(self):
        """析构函数，清理资源"""
        try:
            self.close_camera()
            if self.pygame_initialized:
                pygame.quit()
        except:
            pass

# 全局媒体控制器实例
media_controller = MediaController()