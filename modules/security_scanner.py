import os
import hashlib
import subprocess
import win32api
import win32con
import win32security
from typing import Dict, List, Any, Optional
import threading
import time
from datetime import datetime
from core.logger import logger_manager
from core.permissions import permission_manager

class SecurityScanner:
    def __init__(self):
        self.logger = logger_manager.get_logger('security_scanner')
        self.scan_results = []
        self.scanning = False
        self.scan_thread = None
    
    def scan_for_malware_indicators(self) -> List[Dict[str, Any]]:
        """扫描恶意软件指标"""
        indicators = []
        
        try:
            # 检查可疑进程
            suspicious_processes = self._check_suspicious_processes()
            indicators.extend(suspicious_processes)
            
            # 检查启动项
            suspicious_startup = self._check_startup_items()
            indicators.extend(suspicious_startup)
            
            # 检查网络连接
            suspicious_connections = self._check_network_connections()
            indicators.extend(suspicious_connections)
            
            # 检查文件完整性
            integrity_issues = self._check_file_integrity()
            indicators.extend(integrity_issues)
            
        except Exception as e:
            self.logger.error(f"恶意软件扫描失败: {e}")
        
        return indicators
    
    def _check_suspicious_processes(self) -> List[Dict[str, Any]]:
        """检查可疑进程"""
        import psutil
        suspicious = []
        
        # 已知的恶意软件进程名
        malicious_names = [
            'malware.exe', 'trojan.exe', 'virus.exe', 'ransomware.exe',
            'miner.exe', 'botnet.exe', 'keylogger.exe', 'spyware.exe'
        ]
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
                try:
                    proc_info = proc.info
                    proc_name = proc_info['name'].lower()
                    
                    # 检查进程名
                    if any(malicious_name in proc_name for malicious_name in malicious_names):
                        suspicious.append({
                            'type': 'suspicious_process',
                            'severity': 'high',
                            'process_name': proc_info['name'],
                            'pid': proc_info['pid'],
                            'path': proc_info['exe'],
                            'description': '检测到可疑进程名'
                        })
                    
                    # 检查临时目录中的可执行文件
                    if proc_info['exe']:
                        exe_path = proc_info['exe'].lower()
                        if 'temp' in exe_path and exe_path.endswith('.exe'):
                            suspicious.append({
                                'type': 'suspicious_location',
                                'severity': 'medium',
                                'process_name': proc_info['name'],
                                'pid': proc_info['pid'],
                                'path': proc_info['exe'],
                                'description': '在临时目录中发现可执行文件'
                            })
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            self.logger.error(f"检查可疑进程失败: {e}")
        
        return suspicious
    
    def _check_startup_items(self) -> List[Dict[str, Any]]:
        """检查启动项"""
        suspicious = []
        
        try:
            # 检查注册表启动项
            startup_keys = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce",
                r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Run"
            ]
            
            import winreg
            for key_path in startup_keys:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            # 检查可疑的启动项
                            if any(suspicious_word in value.lower() for suspicious_word in 
                                 ['temp', 'appdata', 'downloads', 'malware']):
                                suspicious.append({
                                    'type': 'suspicious_startup',
                                    'severity': 'high',
                                    'name': name,
                                    'value': value,
                                    'location': f"HKLM\\{key_path}",
                                    'description': '检测到可疑启动项'
                                })
                            i += 1
                        except WindowsError:
                            break
                    winreg.CloseKey(key)
                except Exception as e:
                    self.logger.warning(f"检查注册表项失败 {key_path}: {e}")
                    
        except Exception as e:
            self.logger.error(f"检查启动项失败: {e}")
        
        return suspicious
    
    def _check_network_connections(self) -> List[Dict[str, Any]]:
        """检查网络连接"""
        import psutil
        suspicious = []
        
        try:
            connections = psutil.net_connections()
            for conn in connections:
                if conn.status == 'ESTABLISHED':
                    # 检查连接到可疑端口
                    suspicious_ports = [1337, 31337, 6667, 6668, 6669]  # 常见恶意软件端口
                    if conn.raddr and conn.raddr.port in suspicious_ports:
                        suspicious.append({
                            'type': 'suspicious_connection',
                            'severity': 'high',
                            'local_addr': f"{conn.laddr.ip}:{conn.laddr.port}",
                            'remote_addr': f"{conn.raddr.ip}:{conn.raddr.port}",
                            'description': f'连接到可疑端口 {conn.raddr.port}'
                        })
                        
        except Exception as e:
            self.logger.error(f"检查网络连接失败: {e}")
        
        return suspicious
    
    def _check_file_integrity(self) -> List[Dict[str, Any]]:
        """检查文件完整性"""
        suspicious = []
        
        # 关键系统文件路径
        critical_paths = [
            r"C:\Windows\System32",
            r"C:\Windows\SysWOW64",
            r"C:\Program Files",
            r"C:\Program Files (x86)"
        ]
        
        for path in critical_paths:
            try:
                if os.path.exists(path):
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            if file.endswith(('.exe', '.dll', '.sys')):
                                file_path = os.path.join(root, file)
                                try:
                                    # 检查文件权限
                                    if self._has_unusual_permissions(file_path):
                                        suspicious.append({
                                            'type': 'unusual_permissions',
                                            'severity': 'medium',
                                            'file_path': file_path,
                                            'description': '文件具有异常权限'
                                        })
                                        
                                    # 检查文件大小异常
                                    if self._has_unusual_size(file_path):
                                        suspicious.append({
                                            'type': 'unusual_size',
                                            'severity': 'low',
                                            'file_path': file_path,
                                            'description': '文件大小异常'
                                        })
                                        
                                except (PermissionError, OSError):
                                    continue
            except Exception as e:
                self.logger.warning(f"检查路径失败 {path}: {e}")
        
        return suspicious
    
    def _has_unusual_permissions(self, file_path: str) -> bool:
        """检查文件是否有异常权限"""
        try:
            # 获取文件安全信息
            sd = win32security.GetFileSecurity(file_path, win32security.DACL_SECURITY_INFORMATION)
            dacl = sd.GetSecurityDescriptorDacl()
            
            if dacl:
                for i in range(dacl.GetAceCount()):
                    ace = dacl.GetAce(i)
                    # 检查是否有Everyone完全控制权限等异常情况
                    if ace[0][1] & win32con.FILE_ALL_ACCESS:
                        trustee = ace[2]
                        if trustee == win32security.ConvertStringSidToSid('S-1-1-0'):  # Everyone
                            return True
            return False
        except:
            return False
    
    def _has_unusual_size(self, file_path: str) -> bool:
        """检查文件大小是否异常"""
        try:
            size = os.path.getsize(file_path)
            # 系统文件通常不会太大或太小
            return size < 1024 or size > 100 * 1024 * 1024  # 小于1KB或大于100MB
        except:
            return False
    
    def scan_system_vulnerabilities(self) -> Dict[str, Any]:
        """扫描系统漏洞"""
        vulnerabilities = {
            'missing_updates': [],
            'weak_passwords': [],
            'misconfigurations': [],
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # 检查Windows更新状态
            updates_status = self._check_windows_updates()
            vulnerabilities['missing_updates'] = updates_status
            
            # 检查密码策略
            password_policy = self._check_password_policy()
            vulnerabilities['weak_passwords'] = password_policy
            
            # 检查系统配置
            misconfigurations = self._check_system_configuration()
            vulnerabilities['misconfigurations'] = misconfigurations
            
        except Exception as e:
            self.logger.error(f"系统漏洞扫描失败: {e}")
            vulnerabilities['error'] = str(e)
        
        return vulnerabilities
    
    def _check_windows_updates(self) -> List[str]:
        """检查Windows更新状态"""
        missing_updates = []
        try:
            # 使用wmic检查更新状态
            result = subprocess.run([
                'wmic', 'qfe', 'get', 'Description,HotFixID,InstalledOn'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # 这里应该与最新的安全更新列表进行比较
                # 简化版本：检查是否有最近30天内的更新
                output_lines = result.stdout.strip().split('\n')[1:]  # 跳过标题行
                recent_updates = 0
                
                for line in output_lines:
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        try:
                            date_str = parts[-1]
                            # 简单的日期解析
                            if '/' in date_str:
                                recent_updates += 1
                        except:
                            continue
                
                if recent_updates < 5:  # 如果最近更新很少
                    missing_updates.append("系统缺少关键安全更新")
                    
        except Exception as e:
            self.logger.error(f"检查Windows更新失败: {e}")
        
        return missing_updates
    
    def _check_password_policy(self) -> List[str]:
        """检查密码策略"""
        weak_policies = []
        try:
            # 检查密码复杂性要求
            result = subprocess.run([
                'net', 'accounts'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                output = result.stdout.lower()
                if 'passwords must meet complexity requirements: no' in output:
                    weak_policies.append("密码复杂性要求未启用")
                
                # 检查最小密码长度
                if 'minimum password length:' in output:
                    lines = output.split('\n')
                    for line in lines:
                        if 'minimum password length:' in line:
                            try:
                                length = int(line.split(':')[-1].strip())
                                if length < 8:
                                    weak_policies.append(f"最小密码长度过短: {length}")
                            except:
                                pass
                                
        except Exception as e:
            self.logger.error(f"检查密码策略失败: {e}")
        
        return weak_policies
    
    def _check_system_configuration(self) -> List[str]:
        """检查系统配置问题"""
        issues = []
        try:
            # 检查防火墙状态
            firewall_result = subprocess.run([
                'netsh', 'advfirewall', 'show', 'allprofiles', 'state'
            ], capture_output=True, text=True, timeout=10)
            
            if firewall_result.returncode == 0:
                if 'off' in firewall_result.stdout.lower():
                    issues.append("Windows防火墙未启用")
            
            # 检查UAC设置
            import winreg
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                   r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System")
                consent_prompt_behavior, _ = winreg.QueryValueEx(key, "ConsentPromptBehaviorAdmin")
                if consent_prompt_behavior == 0:
                    issues.append("用户账户控制(UAC)已禁用")
                winreg.CloseKey(key)
            except:
                pass
                
        except Exception as e:
            self.logger.error(f"检查系统配置失败: {e}")
        
        return issues
    
    def start_continuous_monitoring(self):
        """开始持续监控"""
        if self.scanning:
            return
            
        self.scanning = True
        self.scan_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.scan_thread.start()
        self.logger.info("安全监控已启动")
    
    def stop_continuous_monitoring(self):
        """停止持续监控"""
        self.scanning = False
        if self.scan_thread:
            self.scan_thread.join(timeout=5)
        self.logger.info("安全监控已停止")
    
    def _monitoring_loop(self):
        """监控循环"""
        while self.scanning:
            try:
                # 执行定期安全检查
                results = self.scan_for_malware_indicators()
                if results:
                    self.scan_results.extend(results)
                    self.logger.warning(f"发现 {len(results)} 个安全威胁")
                
                # 每30分钟执行一次完整扫描
                time.sleep(1800)
                
            except Exception as e:
                self.logger.error(f"安全监控循环错误: {e}")
                time.sleep(60)
    
    def get_latest_threats(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最新威胁"""
        return self.scan_results[-limit:] if self.scan_results else []
    
    def clear_threat_history(self):
        """清除威胁历史"""
        self.scan_results.clear()
        self.logger.info("威胁历史已清除")

# 全局安全扫描器实例
security_scanner = SecurityScanner()