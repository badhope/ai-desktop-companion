#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试和日志系统
为开发者提供详细的调试信息和日志记录
"""

import os
import sys
import logging
from datetime import datetime
from typing import Any, Dict, List
import traceback

class DebugLogger:
    """调试日志管理器"""
    
    def __init__(self, log_level: str = "INFO"):
        self.log_level = getattr(logging, log_level.upper())
        self.logger = self._setup_logger()
        self.debug_mode = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
        
    def _setup_logger(self) -> logging.Logger:
        """设置日志系统"""
        # 确保日志目录存在
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # 创建logger
        logger = logging.getLogger('cultivation_game')
        logger.setLevel(self.log_level)
        
        # 避免重复添加handler
        if logger.handlers:
            return logger
            
        # 文件处理器
        log_file = f"logs/game_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(self.log_level)
        
        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO if not self.debug_mode else logging.DEBUG)
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
        
    def debug(self, message: str, *args, **kwargs):
        """调试级别日志"""
        self.logger.debug(message, *args, **kwargs)
        
    def info(self, message: str, *args, **kwargs):
        """信息级别日志"""
        self.logger.info(message, *args, **kwargs)
        
    def warning(self, message: str, *args, **kwargs):
        """警告级别日志"""
        self.logger.warning(message, *args, **kwargs)
        
    def error(self, message: str, *args, **kwargs):
        """错误级别日志"""
        self.logger.error(message, *args, **kwargs)
        
    def critical(self, message: str, *args, **kwargs):
        """严重错误级别日志"""
        self.logger.critical(message, *args, **kwargs)
        
    def exception(self, message: str, *args, **kwargs):
        """记录异常信息"""
        self.logger.exception(message, *args, **kwargs)
        
    def log_performance(self, operation: str, duration: float):
        """记录性能信息"""
        self.info(f"性能监控 - {operation}: {duration:.4f}秒")
        
    def log_game_state(self, state_info: Dict[str, Any]):
        """记录游戏状态"""
        if self.debug_mode:
            self.debug(f"游戏状态: {state_info}")
            
    def log_player_action(self, player_name: str, action: str, result: str = None):
        """记录玩家操作"""
        message = f"玩家操作 - {player_name}: {action}"
        if result:
            message += f" (结果: {result})"
        self.info(message)
        
    def log_system_event(self, event_type: str, details: Dict[str, Any]):
        """记录系统事件"""
        self.info(f"系统事件 - {event_type}: {details}")

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self, logger: DebugLogger):
        self.logger = logger
        self.timings = {}
        
    def start_timing(self, operation: str):
        """开始计时"""
        self.timings[operation] = datetime.now()
        
    def end_timing(self, operation: str) -> float:
        """结束计时并记录"""
        if operation in self.timings:
            duration = (datetime.now() - self.timings[operation]).total_seconds()
            self.logger.log_performance(operation, duration)
            del self.timings[operation]
            return duration
        return 0.0
        
    def benchmark_function(self, func, *args, **kwargs):
        """基准测试函数"""
        func_name = func.__name__
        self.start_timing(func_name)
        try:
            result = func(*args, **kwargs)
            duration = self.end_timing(func_name)
            return result, duration
        except Exception as e:
            self.logger.exception(f"函数 {func_name} 执行出错")
            raise

class ErrorTracker:
    """错误追踪器"""
    
    def __init__(self, logger: DebugLogger):
        self.logger = logger
        self.error_count = 0
        self.error_history = []
        
    def track_error(self, error_type: str, message: str, traceback_info: str = None):
        """追踪错误"""
        self.error_count += 1
        error_info = {
            'timestamp': datetime.now(),
            'type': error_type,
            'message': message,
            'traceback': traceback_info,
            'count': self.error_count
        }
        self.error_history.append(error_info)
        
        # 记录到日志
        self.logger.error(f"错误 #{self.error_count}: [{error_type}] {message}")
        if traceback_info:
            self.logger.debug(f"Traceback: {traceback_info}")
            
    def get_error_summary(self) -> Dict[str, Any]:
        """获取错误摘要"""
        error_types = {}
        for error in self.error_history:
            error_type = error['type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
            
        return {
            'total_errors': self.error_count,
            'error_types': error_types,
            'recent_errors': self.error_history[-10:]  # 最近10个错误
        }
        
    def clear_history(self):
        """清空错误历史"""
        self.error_history.clear()
        self.error_count = 0

# 全局实例
debug_logger = DebugLogger()
performance_monitor = PerformanceMonitor(debug_logger)
error_tracker = ErrorTracker(debug_logger)

def handle_exception(exc_type, exc_value, exc_traceback):
    """全局异常处理"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
        
    # 记录异常信息
    error_msg = f"{exc_type.__name__}: {exc_value}"
    tb_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    error_tracker.track_error("UnhandledException", error_msg, tb_str)
    debug_logger.critical(f"未处理的异常: {error_msg}")
    debug_logger.debug(f"完整Traceback:\n{tb_str}")

# 设置全局异常处理
sys.excepthook = handle_exception

def setup_developer_environment():
    """设置开发者环境"""
    # 启用调试模式
    os.environ['DEBUG_MODE'] = 'True'
    
    # 设置详细日志级别
    debug_logger.logger.setLevel(logging.DEBUG)
    
    print("🔧 开发者环境已启用")
    print("   • 调试日志已开启")
    print("   • 详细错误信息显示")
    print("   • 性能监控已激活")
    
def get_system_info() -> Dict[str, Any]:
    """获取系统信息用于调试"""
    import platform
    import psutil
    
    return {
        'platform': platform.platform(),
        'python_version': sys.version,
        'cpu_count': psutil.cpu_count(),
        'memory_total': psutil.virtual_memory().total,
        'memory_available': psutil.virtual_memory().available,
        'disk_usage': psutil.disk_usage('.').free,
        'debug_mode': debug_logger.debug_mode
    }

if __name__ == "__main__":
    # 测试调试系统
    print("🧪 调试系统测试")
    
    # 基本日志测试
    debug_logger.info("这是信息日志")
    debug_logger.warning("这是警告日志")
    debug_logger.error("这是错误日志")
    
    # 性能监控测试
    performance_monitor.start_timing("test_operation")
    import time
    time.sleep(0.1)  # 模拟操作
    performance_monitor.end_timing("test_operation")
    
    # 错误追踪测试
    try:
        raise ValueError("测试异常")
    except Exception as e:
        error_tracker.track_error("TestError", str(e))
        
    # 显示错误摘要
    summary = error_tracker.get_error_summary()
    print(f"错误统计: {summary}")
    
    print("✅ 调试系统测试完成")