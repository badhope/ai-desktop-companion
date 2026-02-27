import pyautogui
import schedule
import time
import threading
from typing import Dict, List, Callable, Any
from datetime import datetime, timedelta
import json
import os
from core.logger import logger_manager

class AutomationManager:
    def __init__(self):
        self.logger = logger_manager.get_logger('automation')
        self.tasks = {}
        self.running = False
        self.scheduler_thread = None
        pyautogui.FAILSAFE = True  # 启用安全模式
    
    def create_click_task(self, name: str, x: int, y: int, clicks: int = 1, 
                         interval: float = 0.0, button: str = 'left') -> bool:
        """创建点击任务"""
        try:
            task = {
                'type': 'click',
                'x': x,
                'y': y,
                'clicks': clicks,
                'interval': interval,
                'button': button,
                'created_at': datetime.now().isoformat()
            }
            
            self.tasks[name] = task
            self.logger.info(f"点击任务创建成功: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"创建点击任务失败: {e}")
            return False
    
    def create_typing_task(self, name: str, text: str, interval: float = 0.1) -> bool:
        """创建打字任务"""
        try:
            task = {
                'type': 'typing',
                'text': text,
                'interval': interval,
                'created_at': datetime.now().isoformat()
            }
            
            self.tasks[name] = task
            self.logger.info(f"打字任务创建成功: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"创建打字任务失败: {e}")
            return False
    
    def create_screenshot_task(self, name: str, interval_minutes: int, 
                              save_path: str = None) -> bool:
        """创建定时截图任务"""
        try:
            task = {
                'type': 'screenshot',
                'interval_minutes': interval_minutes,
                'save_path': save_path or './screenshots',
                'created_at': datetime.now().isoformat()
            }
            
            # 确保保存目录存在
            os.makedirs(task['save_path'], exist_ok=True)
            
            self.tasks[name] = task
            self.logger.info(f"截图任务创建成功: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"创建截图任务失败: {e}")
            return False
    
    def create_custom_task(self, name: str, func: Callable, *args, **kwargs) -> bool:
        """创建自定义任务"""
        try:
            task = {
                'type': 'custom',
                'function': func,
                'args': args,
                'kwargs': kwargs,
                'created_at': datetime.now().isoformat()
            }
            
            self.tasks[name] = task
            self.logger.info(f"自定义任务创建成功: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"创建自定义任务失败: {e}")
            return False
    
    def execute_task(self, task_name: str) -> bool:
        """执行任务"""
        try:
            if task_name not in self.tasks:
                raise ValueError(f"任务不存在: {task_name}")
            
            task = self.tasks[task_name]
            task_type = task['type']
            
            if task_type == 'click':
                pyautogui.click(
                    x=task['x'], 
                    y=task['y'], 
                    clicks=task['clicks'],
                    interval=task['interval'],
                    button=task['button']
                )
                
            elif task_type == 'typing':
                pyautogui.typewrite(task['text'], interval=task['interval'])
                
            elif task_type == 'screenshot':
                import pyautogui
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                filepath = os.path.join(task['save_path'], filename)
                pyautogui.screenshot(filepath)
                
            elif task_type == 'custom':
                task['function'](*task['args'], **task['kwargs'])
            
            self.logger.info(f"任务执行成功: {task_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"任务执行失败 {task_name}: {e}")
            return False
    
    def schedule_task(self, task_name: str, schedule_type: str, **schedule_params) -> bool:
        """调度任务"""
        try:
            if task_name not in self.tasks:
                raise ValueError(f"任务不存在: {task_name}")
            
            def job():
                self.execute_task(task_name)
            
            # 根据调度类型设置计划
            if schedule_type == 'every':
                interval = schedule_params.get('interval', 1)
                unit = schedule_params.get('unit', 'minutes')
                
                if unit == 'seconds':
                    schedule.every(interval).seconds.do(job)
                elif unit == 'minutes':
                    schedule.every(interval).minutes.do(job)
                elif unit == 'hours':
                    schedule.every(interval).hours.do(job)
                elif unit == 'days':
                    schedule.every(interval).days.do(job)
                    
            elif schedule_type == 'daily':
                time_str = schedule_params.get('time', '09:00')
                schedule.every().day.at(time_str).do(job)
                
            elif schedule_type == 'weekly':
                day = schedule_params.get('day', 'monday')
                time_str = schedule_params.get('time', '09:00')
                getattr(schedule.every(), day).at(time_str).do(job)
            
            self.logger.info(f"任务调度设置成功: {task_name} - {schedule_type}")
            return True
            
        except Exception as e:
            self.logger.error(f"任务调度失败: {e}")
            return False
    
    def start_scheduler(self):
        """启动任务调度器"""
        if self.running:
            return
            
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        self.logger.info("任务调度器已启动")
    
    def stop_scheduler(self):
        """停止任务调度器"""
        self.running = False
        schedule.clear()
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        self.logger.info("任务调度器已停止")
    
    def _scheduler_loop(self):
        """调度器循环"""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"调度器循环错误: {e}")
                time.sleep(5)
    
    def get_scheduled_tasks(self) -> List[Dict[str, Any]]:
        """获取所有已调度的任务"""
        try:
            jobs = []
            for job in schedule.jobs:
                jobs.append({
                    'job': str(job),
                    'next_run': job.next_run.isoformat() if job.next_run else None,
                    'interval': str(job.interval),
                    'unit': getattr(job, 'unit', 'unknown')
                })
            return jobs
        except Exception as e:
            self.logger.error(f"获取调度任务失败: {e}")
            return []
    
    def remove_task(self, task_name: str) -> bool:
        """移除任务"""
        try:
            if task_name in self.tasks:
                del self.tasks[task_name]
                self.logger.info(f"任务已移除: {task_name}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"移除任务失败: {e}")
            return False
    
    def get_all_tasks(self) -> Dict[str, Any]:
        """获取所有任务信息"""
        return {
            'tasks': self.tasks,
            'scheduled_jobs': self.get_scheduled_tasks(),
            'running': self.running
        }
    
    def export_tasks(self, filepath: str) -> bool:
        """导出任务配置"""
        try:
            # 移除不可序列化的函数对象
            exportable_tasks = {}
            for name, task in self.tasks.items():
                if task['type'] != 'custom':  # 自定义任务可能包含函数引用
                    exportable_tasks[name] = task
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(exportable_tasks, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"任务配置已导出: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"导出任务配置失败: {e}")
            return False
    
    def import_tasks(self, filepath: str) -> bool:
        """导入任务配置"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                imported_tasks = json.load(f)
            
            self.tasks.update(imported_tasks)
            self.logger.info(f"任务配置已导入: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"导入任务配置失败: {e}")
            return False

# 全局自动化管理器实例
automation_manager = AutomationManager()