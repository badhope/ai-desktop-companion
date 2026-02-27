#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI桌面伴侣主程序
功能极其丰富，权限非常大的智能助手系统
"""

import sys
import os
import asyncio
import threading
from datetime import datetime

# 添加项目路径到系统路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from core.logger import logger_manager, main_logger
from core.permissions import permission_manager
from core.ai_engine import ai_engine
from modules.system_monitor import system_monitor
from modules.file_manager import file_manager
from modules.network_tools import network_tools
from modules.media_control import media_controller
from modules.automation import automation_manager
from modules.security_scanner import security_scanner

class AIDesktopCompanion:
    def __init__(self):
        self.logger = main_logger
        self.running = False
        self.modules = {}
        
    def initialize_system(self):
        """初始化系统"""
        self.logger.info("=" * 50)
        self.logger.info(f"启动 {config.APP_NAME} v{config.VERSION}")
        self.logger.info("=" * 50)
        
        # 检查管理员权限
        if config.ADMIN_REQUIRED and not permission_manager.check_admin_status():
            self.logger.warning("程序需要管理员权限才能发挥全部功能")
            # 可以选择请求提升权限
            # permission_manager.request_admin_privileges()
        
        # 启用系统特权
        if config.SYSTEM_ACCESS:
            permission_manager.enable_privileges(permission_manager.required_privileges)
        
        # 初始化各模块
        self._initialize_modules()
        
        # 启动后台服务
        self._start_background_services()
        
        self.logger.info("系统初始化完成")
    
    def _initialize_modules(self):
        """初始化各个功能模块"""
        self.modules = {
            'ai_engine': ai_engine,
            'system_monitor': system_monitor,
            'file_manager': file_manager,
            'network_tools': network_tools,
            'media_controller': media_controller,
            'automation_manager': automation_manager,
            'security_scanner': security_scanner
        }
        
        self.logger.info(f"已加载 {len(self.modules)} 个功能模块")
    
    def _start_background_services(self):
        """启动后台服务"""
        try:
            # 启动系统监控
            if config.ENABLE_SYSTEM_MONITOR:
                system_monitor.start_monitoring()
                self.logger.info("系统监控服务已启动")
            
            # 启动安全扫描
            if config.ENABLE_SECURITY_SCAN:
                security_scanner.start_continuous_monitoring()
                self.logger.info("安全扫描服务已启动")
            
            # 启动自动化调度器
            automation_manager.start_scheduler()
            self.logger.info("自动化调度器已启动")
            
        except Exception as e:
            self.logger.error(f"启动后台服务失败: {e}")
    
    def process_command(self, command: str) -> str:
        """处理用户命令"""
        try:
            self.logger.info(f"收到命令: {command}")
            
            # 让AI引擎处理命令
            response = asyncio.run(ai_engine.process_user_input(command))
            
            # 根据响应执行相应操作
            self._execute_response_actions(response, command)
            
            return response
            
        except Exception as e:
            self.logger.error(f"处理命令失败: {e}")
            return f"处理命令时发生错误: {str(e)}"
    
    def _execute_response_actions(self, response: str, original_command: str):
        """根据AI响应执行相应的系统操作"""
        # 这里可以实现更复杂的命令解析和执行逻辑
        # 例如识别特定的系统操作指令并直接执行
        
        action_keywords = {
            '系统监控': lambda: self._handle_system_monitor_commands(original_command),
            '文件管理': lambda: self._handle_file_commands(original_command),
            '网络工具': lambda: self._handle_network_commands(original_command),
            '媒体控制': lambda: self._handle_media_commands(original_command),
            '安全扫描': lambda: self._handle_security_commands(original_command)
        }
        
        for keyword, handler in action_keywords.items():
            if keyword in response:
                try:
                    handler()
                except Exception as e:
                    self.logger.error(f"执行{keyword}操作失败: {e}")
    
    def _handle_system_monitor_commands(self, command: str):
        """处理系统监控相关命令"""
        if '状态' in command or 'status' in command.lower():
            status = system_monitor.get_current_status()
            self.logger.info(f"系统状态: {status}")
    
    def _handle_file_commands(self, command: str):
        """处理文件管理相关命令"""
        # 实现文件操作逻辑
        pass
    
    def _handle_network_commands(self, command: str):
        """处理网络工具相关命令"""
        # 实现网络操作逻辑
        pass
    
    def _handle_media_commands(self, command: str):
        """处理媒体控制相关命令"""
        # 实现媒体操作逻辑
        pass
    
    def _handle_security_commands(self, command: str):
        """处理安全扫描相关命令"""
        if '扫描' in command or 'scan' in command.lower():
            threats = security_scanner.scan_for_malware_indicators()
            if threats:
                self.logger.warning(f"发现安全威胁: {len(threats)} 个")
    
    def get_system_overview(self) -> dict:
        """获取系统概览信息"""
        try:
            overview = {
                'timestamp': datetime.now().isoformat(),
                'app_info': {
                    'name': config.APP_NAME,
                    'version': config.VERSION,
                    'developer': config.DEVELOPER
                },
                'system_status': system_monitor.get_current_status(),
                'security_status': {
                    'active_threats': len(security_scanner.get_latest_threats()),
                    'monitoring_enabled': security_scanner.scanning
                },
                'modules_loaded': list(self.modules.keys()),
                'permissions': {
                    'admin': permission_manager.check_admin_status(),
                    'current_privileges': permission_manager.get_system_privileges()
                }
            }
            return overview
        except Exception as e:
            self.logger.error(f"获取系统概览失败: {e}")
            return {'error': str(e)}
    
    def shutdown(self):
        """关闭系统"""
        self.logger.info("正在关闭AI桌面伴侣...")
        
        # 停止后台服务
        try:
            system_monitor.stop_monitoring()
            security_scanner.stop_continuous_monitoring()
            automation_manager.stop_scheduler()
            media_controller.close_camera()
        except Exception as e:
            self.logger.error(f"关闭服务时出错: {e}")
        
        self.running = False
        self.logger.info("AI桌面伴侣已关闭")

def main():
    """主函数"""
    app = AIDesktopCompanion()
    
    try:
        # 初始化系统
        app.initialize_system()
        app.running = True
        
        # 显示欢迎信息
        print("\n" + "="*60)
        print(f"🤖 {config.APP_NAME} v{config.VERSION}")
        print(f"🚀 开发者: {config.DEVELOPER}")
        print("="*60)
        print("系统功能:")
        print("  🖥️  系统监控与管理")
        print("  📁 文件操作与管理") 
        print("  🌐 网络诊断与工具")
        print("  🎵 多媒体控制")
        print("  ⚡ 自动化任务")
        print("  🔒 安全扫描与防护")
        print("="*60)
        
        # 获取系统概览
        overview = app.get_system_overview()
        print(f"\n📊 系统状态:")
        print(f"   管理员权限: {'✅' if overview['permissions']['admin'] else '❌'}")
        print(f"   加载模块数: {len(overview['modules_loaded'])}")
        print(f"   安全威胁数: {overview['security_status']['active_threats']}")
        
        print(f"\n💡 提示: 输入 'help' 查看帮助，'quit' 退出程序")
        
        # 主循环
        while app.running:
            try:
                user_input = input("\n👤 您说: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    break
                elif user_input.lower() in ['help', '帮助']:
                    print_help()
                    continue
                elif user_input.lower() in ['status', '状态']:
                    overview = app.get_system_overview()
                    print(f"系统概览: {overview}")
                    continue
                
                # 处理用户命令
                response = app.process_command(user_input)
                print(f"🤖 助手: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 收到中断信号，正在退出...")
                break
            except EOFError:
                print("\n\n👋 输入结束，正在退出...")
                break
            except Exception as e:
                print(f"❌ 发生错误: {e}")
                main_logger.error(f"主循环错误: {e}")
    
    except Exception as e:
        print(f"❌ 程序启动失败: {e}")
        main_logger.error(f"程序启动失败: {e}")
    
    finally:
        app.shutdown()

def print_help():
    """打印帮助信息"""
    help_text = """
🤖 AI桌面伴侣 - 帮助文档

📋 基本命令:
  • status/状态    - 查看系统状态
  • help/帮助      - 显示此帮助信息  
  • quit/exit/退出 - 退出程序

🔧 系统功能:
  • 系统监控 - 实时监控CPU、内存、磁盘等
  • 文件管理 - 文件浏览、搜索、操作
  • 网络工具 - 网络诊断、端口扫描
  • 媒体控制 - 音量调节、截图、录像
  • 自动化   - 任务调度、自动操作
  • 安全扫描 - 恶意软件检测、漏洞扫描

📝 使用示例:
  • "帮我监控系统状态"
  • "扫描D盘的所有pdf文件"
  • "截取当前屏幕"
  • "检查网络连接"
  • "设置每小时自动备份"

⚠️  注意事项:
  • 部分功能需要管理员权限
  • 敏感操作会要求确认
  • 建议定期查看安全扫描结果
    """
    print(help_text)

if __name__ == "__main__":
    main()