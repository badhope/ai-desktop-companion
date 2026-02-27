import ctypes
import os
import sys
import win32api
import win32security
import win32con
from typing import List, Dict, Any
from core.logger import logger_manager

class PermissionManager:
    def __init__(self):
        self.logger = logger_manager.get_logger('permissions')
        self.required_privileges = [
            'SeDebugPrivilege',
            'SeBackupPrivilege', 
            'SeRestorePrivilege',
            'SeSecurityPrivilege',
            'SeTakeOwnershipPrivilege',
            'SeShutdownPrivilege'
        ]
        self.current_privileges = []
        self.check_admin_status()
        
    def check_admin_status(self) -> bool:
        """检查是否具有管理员权限"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception as e:
            self.logger.error(f"检查管理员权限失败: {e}")
            return False
    
    def request_admin_privileges(self) -> bool:
        """请求管理员权限"""
        if self.check_admin_status():
            return True
            
        try:
            # 重新以管理员身份运行程序
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            return True
        except Exception as e:
            self.logger.error(f"请求管理员权限失败: {e}")
            return False
    
    def enable_privileges(self, privileges: List[str]) -> bool:
        """启用系统特权"""
        try:
            # 获取当前进程令牌
            token = win32security.OpenProcessToken(
                win32api.GetCurrentProcess(), 
                win32con.TOKEN_ADJUST_PRIVILEGES | win32con.TOKEN_QUERY
            )
            
            for privilege_name in privileges:
                try:
                    # 查找特权值
                    privilege_value = win32security.LookupPrivilegeValue(None, privilege_name)
                    
                    # 启用特权
                    win32security.AdjustTokenPrivileges(
                        token, 
                        0, 
                        [(privilege_value, win32con.SE_PRIVILEGE_ENABLED)]
                    )
                    
                    self.current_privileges.append(privilege_name)
                    self.logger.info(f"已启用特权: {privilege_name}")
                    
                except Exception as e:
                    self.logger.warning(f"启用特权 {privilege_name} 失败: {e}")
            
            win32api.CloseHandle(token)
            return len(self.current_privileges) > 0
            
        except Exception as e:
            self.logger.error(f"启用特权失败: {e}")
            return False
    
    def get_system_privileges(self) -> List[str]:
        """获取当前拥有的系统特权"""
        return self.current_privileges.copy()
    
    def check_file_permissions(self, filepath: str, permissions: List[str]) -> Dict[str, bool]:
        """检查文件权限"""
        results = {}
        try:
            # 检查文件是否存在
            if not os.path.exists(filepath):
                results['exists'] = False
                return results
                
            results['exists'] = True
            
            # 检查各种权限
            checks = {
                'read': os.R_OK,
                'write': os.W_OK, 
                'execute': os.X_OK
            }
            
            for perm_name, perm_flag in checks.items():
                if perm_name in permissions:
                    results[perm_name] = os.access(filepath, perm_flag)
                    
        except Exception as e:
            self.logger.error(f"检查文件权限失败 {filepath}: {e}")
            results['error'] = str(e)
            
        return results
    
    def grant_file_permissions(self, filepath: str, user: str = None) -> bool:
        """授予文件完全控制权限"""
        try:
            if user is None:
                user = os.getenv('USERNAME')
                
            # 使用icacls命令授予权限
            cmd = f'icacls "{filepath}" /grant "{user}:(F)" /T'
            result = os.system(cmd)
            
            if result == 0:
                self.logger.info(f"已授予 {user} 对 {filepath} 的完全控制权限")
                return True
            else:
                self.logger.error(f"授予权限失败: {result}")
                return False
                
        except Exception as e:
            self.logger.error(f"授予文件权限失败: {e}")
            return False
    
    def monitor_privilege_changes(self):
        """监控特权变化"""
        def privilege_watcher():
            import time
            last_privileges = set(self.current_privileges)
            
            while True:
                current_privileges = set(self.get_system_privileges())
                if current_privileges != last_privileges:
                    removed = last_privileges - current_privileges
                    added = current_privileges - last_privileges
                    
                    if removed:
                        self.logger.warning(f"特权被移除: {removed}")
                    if added:
                        self.logger.info(f"新获得特权: {added}")
                        
                    last_privileges = current_privileges
                
                time.sleep(5)  # 每5秒检查一次
        
        import threading
        watcher_thread = threading.Thread(target=privilege_watcher, daemon=True)
        watcher_thread.start()

# 全局权限管理器实例
permission_manager = PermissionManager()