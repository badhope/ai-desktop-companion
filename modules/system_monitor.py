import psutil
import time
import threading
from typing import Dict, List, Any
from datetime import datetime
from core.logger import logger_manager

class SystemMonitor:
    def __init__(self):
        self.logger = logger_manager.get_logger('system_monitor')
        self.monitoring = False
        self.monitor_thread = None
        self.alerts = []
        self.thresholds = {
            'cpu_usage': 80,      # CPU使用率阈值
            'memory_usage': 85,   # 内存使用率阈值
            'disk_usage': 90,     # 磁盘使用率阈值
            'temperature': 80,    # 温度阈值（如果可用）
            'network_activity': 1000000  # 网络活动阈值（字节/秒）
        }
    
    def start_monitoring(self):
        """开始系统监控"""
        if self.monitoring:
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("系统监控已启动")
    
    def stop_monitoring(self):
        """停止系统监控"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.logger.info("系统监控已停止")
    
    def _monitor_loop(self):
        """监控循环"""
        while self.monitoring:
            try:
                self._check_system_metrics()
                self._check_processes()
                self._check_network()
                time.sleep(5)  # 每5秒检查一次
            except Exception as e:
                self.logger.error(f"监控过程中出错: {e}")
                time.sleep(10)
    
    def _check_system_metrics(self):
        """检查系统指标"""
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > self.thresholds['cpu_usage']:
                self._add_alert('high_cpu', f"CPU使用率过高: {cpu_percent}%")
            
            # 内存使用率
            memory = psutil.virtual_memory()
            if memory.percent > self.thresholds['memory_usage']:
                self._add_alert('high_memory', f"内存使用率过高: {memory.percent}%")
            
            # 磁盘使用率
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            if disk_percent > self.thresholds['disk_usage']:
                self._add_alert('high_disk', f"磁盘使用率过高: {disk_percent:.1f}%")
            
            # 网络IO
            net_io = psutil.net_io_counters()
            bytes_sent_per_sec = net_io.bytes_sent
            bytes_recv_per_sec = net_io.bytes_recv
            
            if (bytes_sent_per_sec + bytes_recv_per_sec) > self.thresholds['network_activity']:
                self._add_alert('high_network', f"网络活动异常: {bytes_sent_per_sec + bytes_recv_per_sec} bytes/sec")
                
        except Exception as e:
            self.logger.error(f"检查系统指标失败: {e}")
    
    def _check_processes(self):
        """检查进程状态"""
        try:
            # 检查高CPU使用率的进程
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    cpu_percent = proc.info['cpu_percent']
                    if cpu_percent and cpu_percent > 50:
                        self._add_alert('high_process_cpu', 
                                      f"进程 {proc.info['name']} (PID: {proc.info['pid']}) CPU使用率过高: {cpu_percent}%")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            self.logger.error(f"检查进程失败: {e}")
    
    def _check_network(self):
        """检查网络连接"""
        try:
            connections = psutil.net_connections()
            established_count = len([conn for conn in connections if conn.status == 'ESTABLISHED'])
            
            if established_count > 100:  # 连接数过多警报
                self._add_alert('many_connections', f"建立的网络连接过多: {established_count}")
                
        except Exception as e:
            self.logger.error(f"检查网络失败: {e}")
    
    def _add_alert(self, alert_type: str, message: str):
        """添加警报"""
        alert = {
            'type': alert_type,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'handled': False
        }
        self.alerts.append(alert)
        self.logger.warning(f"系统警报 [{alert_type}]: {message}")
    
    def get_current_status(self) -> Dict[str, Any]:
        """获取当前系统状态"""
        try:
            return {
                'cpu': {
                    'percent': psutil.cpu_percent(),
                    'count': psutil.cpu_count(),
                    'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
                },
                'memory': psutil.virtual_memory()._asdict(),
                'disk': psutil.disk_usage('/')._asdict(),
                'network': psutil.net_io_counters()._asdict(),
                'boot_time': psutil.boot_time(),
                'process_count': len(psutil.pids()),
                'alerts': [alert for alert in self.alerts if not alert['handled']]
            }
        except Exception as e:
            self.logger.error(f"获取系统状态失败: {e}")
            return {'error': str(e)}
    
    def get_top_processes(self, count: int = 10) -> List[Dict]:
        """获取资源消耗最高的进程"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu_percent': proc.info['cpu_percent'] or 0,
                        'memory_percent': proc.info['memory_percent'] or 0,
                        'status': proc.info['status']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # 按CPU使用率排序
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            return processes[:count]
            
        except Exception as e:
            self.logger.error(f"获取进程列表失败: {e}")
            return []
    
    def handle_alert(self, alert_index: int):
        """标记警报为已处理"""
        if 0 <= alert_index < len(self.alerts):
            self.alerts[alert_index]['handled'] = True
            self.logger.info(f"警报已处理: {self.alerts[alert_index]['message']}")
    
    def clear_handled_alerts(self):
        """清除已处理的警报"""
        self.alerts = [alert for alert in self.alerts if not alert['handled']]
        self.logger.info("已清理已处理的警报")

# 全局系统监控实例
system_monitor = SystemMonitor()