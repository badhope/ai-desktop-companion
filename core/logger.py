import logging
import logging.handlers
from datetime import datetime
from pathlib import Path
from config import config

class LoggerManager:
    def __init__(self):
        self.loggers = {}
        self.setup_main_logger()
    
    def setup_main_logger(self):
        """设置主日志记录器"""
        log_file = config.LOGS_DIR / f"ai_companion_{datetime.now().strftime('%Y%m%d')}.log"
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        
        # 文件处理器（轮转）
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # 主日志记录器
        self.main_logger = logging.getLogger('AI_Companion')
        self.main_logger.setLevel(getattr(logging, config.LOG_LEVEL))
        self.main_logger.addHandler(file_handler)
        self.main_logger.addHandler(console_handler)
        
        self.loggers['main'] = self.main_logger
    
    def get_logger(self, name):
        """获取指定名称的日志记录器"""
        if name not in self.loggers:
            logger = logging.getLogger(f'AI_Companion.{name}')
            logger.setLevel(getattr(logging, config.LOG_LEVEL))
            self.loggers[name] = logger
        return self.loggers[name]
    
    def log_system_event(self, event_type, message, level='INFO'):
        """记录系统事件"""
        logger = self.get_logger('system')
        getattr(logger, level.lower())(f"[{event_type}] {message}")
    
    def log_security_event(self, event_type, message, level='WARNING'):
        """记录安全事件"""
        logger = self.get_logger('security')
        getattr(logger, level.lower())(f"[SECURITY-{event_type}] {message}")
    
    def log_user_action(self, user, action, details="", level='INFO'):
        """记录用户操作"""
        logger = self.get_logger('user_actions')
        getattr(logger, level.lower())(f"[USER:{user}] {action} - {details}")

# 全局日志管理器实例
logger_manager = LoggerManager()
main_logger = logger_manager.main_logger