#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统一错误处理和日志系统
"""

import logging
import traceback
import sys
from datetime import datetime
from pathlib import Path

class ErrorHandler:
    def __init__(self, log_file="app_errors.log"):
        self.log_file = Path(log_file)
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志系统"""
        # 创建日志目录
        log_dir = self.log_file.parent
        log_dir.mkdir(exist_ok=True)
        
        # 配置日志格式
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger("AI_Companion")
    
    def log_error(self, error, context=""):
        """记录错误信息"""
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'traceback': traceback.format_exc()
        }
        
        self.logger.error(f"错误发生在 {context}: {error}")
        return error_info
    
    def log_warning(self, message, context=""):
        """记录警告信息"""
        self.logger.warning(f"警告在 {context}: {message}")
    
    def log_info(self, message, context=""):
        """记录一般信息"""
        self.logger.info(f"信息来自 {context}: {message}")
    
    def handle_exception(self, func, *args, **kwargs):
        """装饰器式的异常处理"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_info = self.log_error(e, func.__name__)
            return None, error_info

# 全局错误处理器实例
error_handler = ErrorHandler()

def safe_execute(func, *args, default_return=None, **kwargs):
    """安全执行函数，捕获异常"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        error_handler.log_error(e, func.__name__)
        return default_return

def retry_on_failure(func, max_retries=3, delay=1, *args, **kwargs):
    """失败重试机制"""
    import time
    
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_handler.log_warning(f"第{attempt + 1}次尝试失败: {e}", func.__name__)
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                error_handler.log_error(e, f"{func.__name__} 最终失败")
                return None