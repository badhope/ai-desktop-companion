import socket
import subprocess
import requests
import json
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse
import ipaddress
from core.logger import logger_manager

class NetworkTools:
    def __init__(self):
        self.logger = logger_manager.get_logger('network_tools')
        self.session = requests.Session()
        self.session.timeout = 10
    
    def ping_host(self, host: str, count: int = 4) -> Dict[str, Any]:
        """Ping主机"""
        try:
            result = subprocess.run(
                ['ping', '-n', str(count), host],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout
            success = result.returncode == 0
            
            # 解析ping结果
            stats = {}
            lines = output.split('\n')
            for line in lines:
                if '平均' in line or 'Average' in line:
                    # 提取平均延迟
                    import re
                    match = re.search(r'(\d+)ms', line)
                    if match:
                        stats['average_latency'] = int(match.group(1))
                elif '丢失' in line or 'Lost' in line:
                    # 提取丢包率
                    import re
                    match = re.search(r'(\d+)%', line)
                    if match:
                        stats['packet_loss'] = int(match.group(1))
            
            return {
                'host': host,
                'success': success,
                'output': output,
                'statistics': stats
            }
            
        except subprocess.TimeoutExpired:
            return {'host': host, 'success': False, 'error': 'Ping超时'}
        except Exception as e:
            self.logger.error(f"Ping失败 {host}: {e}")
            return {'host': host, 'success': False, 'error': str(e)}
    
    def port_scan(self, host: str, ports: List[int] = None) -> Dict[str, Any]:
        """端口扫描"""
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 1723, 3306, 3389, 5432, 8080]
        
        try:
            open_ports = []
            closed_ports = []
            
            for port in ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    result = sock.connect_ex((host, port))
                    sock.close()
                    
                    if result == 0:
                        open_ports.append(port)
                        self.logger.info(f"发现开放端口: {host}:{port}")
                    else:
                        closed_ports.append(port)
                        
                except Exception as e:
                    self.logger.warning(f"扫描端口 {port} 失败: {e}")
                    closed_ports.append(port)
            
            return {
                'host': host,
                'open_ports': open_ports,
                'closed_ports': closed_ports,
                'total_scanned': len(ports)
            }
            
        except Exception as e:
            self.logger.error(f"端口扫描失败 {host}: {e}")
            return {'host': host, 'error': str(e)}
    
    def get_network_info(self) -> Dict[str, Any]:
        """获取网络信息"""
        try:
            # 获取本机IP信息
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # 获取网络接口信息
            interfaces = {}
            try:
                result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                interfaces['ipconfig'] = result.stdout
            except:
                pass
            
            # 测试外网连接
            external_ip = None
            try:
                response = self.session.get('https://api.ipify.org?format=json', timeout=5)
                if response.status_code == 200:
                    external_ip = response.json()['ip']
            except:
                pass
            
            return {
                'hostname': hostname,
                'local_ip': local_ip,
                'external_ip': external_ip,
                'interfaces': interfaces
            }
            
        except Exception as e:
            self.logger.error(f"获取网络信息失败: {e}")
            return {'error': str(e)}
    
    def http_request(self, url: str, method: str = 'GET', **kwargs) -> Dict[str, Any]:
        """发送HTTP请求"""
        try:
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                url = 'http://' + url
            
            response = self.session.request(method, url, **kwargs)
            
            return {
                'url': url,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content_length': len(response.content),
                'encoding': response.encoding,
                'elapsed': response.elapsed.total_seconds()
            }
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"HTTP请求失败 {url}: {e}")
            return {'url': url, 'error': str(e)}
        except Exception as e:
            self.logger.error(f"HTTP请求异常 {url}: {e}")
            return {'url': url, 'error': str(e)}
    
    def dns_lookup(self, hostname: str) -> Dict[str, Any]:
        """DNS查询"""
        try:
            # A记录查询
            ip_addresses = []
            try:
                addrinfo = socket.getaddrinfo(hostname, None)
                for addr in addrinfo:
                    ip = addr[4][0]
                    if ip not in ip_addresses:
                        ip_addresses.append(ip)
            except:
                pass
            
            # 使用nslookup
            nslookup_result = None
            try:
                result = subprocess.run(
                    ['nslookup', hostname],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                nslookup_result = result.stdout
            except:
                pass
            
            return {
                'hostname': hostname,
                'ip_addresses': ip_addresses,
                'nslookup_result': nslookup_result
            }
            
        except Exception as e:
            self.logger.error(f"DNS查询失败 {hostname}: {e}")
            return {'hostname': hostname, 'error': str(e)}
    
    def network_speed_test(self) -> Dict[str, Any]:
        """网络速度测试"""
        try:
            speeds = {}
            
            # 测试到不同服务器的延迟
            test_servers = [
                'google.com',
                'baidu.com',
                'github.com',
                '1.1.1.1'
            ]
            
            for server in test_servers:
                ping_result = self.ping_host(server, count=3)
                if ping_result['success'] and 'statistics' in ping_result:
                    speeds[server] = ping_result['statistics'].get('average_latency', 0)
            
            # 测试下载速度（简单测试）
            download_test_urls = [
                ('small_file', 'https://httpbin.org/bytes/1024'),  # 1KB
                ('medium_file', 'https://httpbin.org/bytes/102400')  # 100KB
            ]
            
            download_speeds = {}
            for name, url in download_test_urls:
                try:
                    response = self.session.get(url, timeout=30)
                    elapsed = response.elapsed.total_seconds()
                    size = len(response.content)
                    speed_mbps = (size * 8) / (elapsed * 1024 * 1024) if elapsed > 0 else 0
                    download_speeds[name] = round(speed_mbps, 2)
                except:
                    download_speeds[name] = 0
            
            return {
                'ping_latencies': speeds,
                'download_speeds': download_speeds,
                'timestamp': self._get_timestamp()
            }
            
        except Exception as e:
            self.logger.error(f"网络速度测试失败: {e}")
            return {'error': str(e)}
    
    def scan_local_network(self) -> List[Dict[str, Any]]:
        """扫描本地网络"""
        try:
            local_devices = []
            
            # 获取本机网络信息
            network_info = self.get_network_info()
            if 'local_ip' in network_info:
                local_ip = network_info['local_ip']
                
                # 确定网络范围
                try:
                    ip_obj = ipaddress.ip_address(local_ip)
                    if isinstance(ip_obj, ipaddress.IPv4Address):
                        # 简单的C类网络扫描
                        network_base = '.'.join(local_ip.split('.')[:-1])
                        
                        for i in range(1, 255):
                            target_ip = f"{network_base}.{i}"
                            if target_ip != local_ip:
                                # 快速ping检测
                                result = subprocess.run(
                                    ['ping', '-n', '1', '-w', '1000', target_ip],
                                    capture_output=True,
                                    text=True
                                )
                                
                                if result.returncode == 0:
                                    # 尝试获取主机名
                                    try:
                                        hostname = socket.getfqdn(target_ip)
                                    except:
                                        hostname = 'Unknown'
                                    
                                    local_devices.append({
                                        'ip': target_ip,
                                        'hostname': hostname,
                                        'status': 'online'
                                    })
                
                except Exception as e:
                    self.logger.error(f"网络扫描解析失败: {e}")
            
            return local_devices
            
        except Exception as e:
            self.logger.error(f"本地网络扫描失败: {e}")
            return []
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()

# 全局网络工具实例
network_tools = NetworkTools()