import os
import shutil
import hashlib
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from core.logger import logger_manager
from core.permissions import permission_manager

class FileManager:
    def __init__(self):
        self.logger = logger_manager.get_logger('file_manager')
        self.recent_files = []
        self.max_recent_files = 100
    
    def list_directory(self, path: str, recursive: bool = False) -> List[Dict[str, Any]]:
        """列出目录内容"""
        try:
            path_obj = Path(path)
            if not path_obj.exists():
                raise FileNotFoundError(f"路径不存在: {path}")
            
            items = []
            if recursive:
                pattern = "**/*"
                paths = path_obj.glob(pattern)
            else:
                paths = path_obj.iterdir()
            
            for item_path in paths:
                try:
                    stat = item_path.stat()
                    item_info = {
                        'name': item_path.name,
                        'path': str(item_path),
                        'is_directory': item_path.is_dir(),
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'permissions': oct(stat.st_mode)[-3:]
                    }
                    items.append(item_info)
                except (PermissionError, OSError) as e:
                    self.logger.warning(f"无法访问 {item_path}: {e}")
                    continue
            
            return sorted(items, key=lambda x: (not x['is_directory'], x['name'].lower()))
            
        except Exception as e:
            self.logger.error(f"列出目录失败 {path}: {e}")
            raise
    
    def search_files(self, search_term: str, search_path: str = ".", 
                    file_types: List[str] = None, case_sensitive: bool = False) -> List[Dict]:
        """搜索文件"""
        try:
            results = []
            search_path_obj = Path(search_path)
            
            # 构建搜索模式
            if file_types:
                patterns = [f"*.{ext}" for ext in file_types]
            else:
                patterns = ["*"]
            
            for pattern in patterns:
                for file_path in search_path_obj.rglob(pattern):
                    if search_term in (file_path.name if case_sensitive else file_path.name.lower()):
                        try:
                            stat = file_path.stat()
                            results.append({
                                'name': file_path.name,
                                'path': str(file_path),
                                'size': stat.st_size,
                                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                            })
                        except (PermissionError, OSError):
                            continue
            
            return sorted(results, key=lambda x: x['name'])
            
        except Exception as e:
            self.logger.error(f"文件搜索失败: {e}")
            return []
    
    def copy_file(self, source: str, destination: str, overwrite: bool = False) -> bool:
        """复制文件"""
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            
            if not source_path.exists():
                raise FileNotFoundError(f"源文件不存在: {source}")
            
            if dest_path.exists() and not overwrite:
                raise FileExistsError(f"目标文件已存在: {destination}")
            
            # 确保目标目录存在
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            if source_path.is_dir():
                shutil.copytree(source, destination, dirs_exist_ok=overwrite)
            else:
                shutil.copy2(source, destination)
            
            self.logger.info(f"文件复制成功: {source} -> {destination}")
            self._add_to_recent(destination)
            return True
            
        except Exception as e:
            self.logger.error(f"文件复制失败: {e}")
            return False
    
    def move_file(self, source: str, destination: str, overwrite: bool = False) -> bool:
        """移动文件"""
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            
            if not source_path.exists():
                raise FileNotFoundError(f"源文件不存在: {source}")
            
            if dest_path.exists() and not overwrite:
                raise FileExistsError(f"目标文件已存在: {destination}")
            
            # 确保目标目录存在
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.move(source, destination)
            self.logger.info(f"文件移动成功: {source} -> {destination}")
            self._add_to_recent(destination)
            return True
            
        except Exception as e:
            self.logger.error(f"文件移动失败: {e}")
            return False
    
    def delete_file(self, path: str, recursive: bool = False) -> bool:
        """删除文件或目录"""
        try:
            path_obj = Path(path)
            
            if not path_obj.exists():
                raise FileNotFoundError(f"文件不存在: {path}")
            
            if path_obj.is_dir() and recursive:
                shutil.rmtree(path)
            elif path_obj.is_dir():
                path_obj.rmdir()
            else:
                path_obj.unlink()
            
            self.logger.info(f"文件删除成功: {path}")
            return True
            
        except Exception as e:
            self.logger.error(f"文件删除失败: {e}")
            return False
    
    def create_directory(self, path: str) -> bool:
        """创建目录"""
        try:
            path_obj = Path(path)
            path_obj.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"目录创建成功: {path}")
            return True
        except Exception as e:
            self.logger.error(f"目录创建失败: {e}")
            return False
    
    def get_file_hash(self, path: str, algorithm: str = 'md5') -> Optional[str]:
        """计算文件哈希值"""
        try:
            hash_func = getattr(hashlib, algorithm)()
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception as e:
            self.logger.error(f"计算文件哈希失败: {e}")
            return None
    
    def get_file_info(self, path: str) -> Dict[str, Any]:
        """获取详细文件信息"""
        try:
            path_obj = Path(path)
            if not path_obj.exists():
                raise FileNotFoundError(f"文件不存在: {path}")
            
            stat = path_obj.stat()
            
            info = {
                'name': path_obj.name,
                'path': str(path_obj),
                'size': stat.st_size,
                'is_directory': path_obj.is_dir(),
                'extension': path_obj.suffix,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'accessed': datetime.fromtimestamp(stat.st_atime).isoformat(),
                'permissions': oct(stat.st_mode)[-3:],
                'owner': stat.st_uid if hasattr(stat, 'st_uid') else None
            }
            
            # 计算哈希值（仅对小文件）
            if not path_obj.is_dir() and stat.st_size < 100 * 1024 * 1024:  # 100MB
                info['md5_hash'] = self.get_file_hash(path, 'md5')
                info['sha256_hash'] = self.get_file_hash(path, 'sha256')
            
            return info
            
        except Exception as e:
            self.logger.error(f"获取文件信息失败: {e}")
            return {'error': str(e)}
    
    def batch_operation(self, operation: str, paths: List[str], **kwargs) -> Dict[str, int]:
        """批量操作文件"""
        results = {'success': 0, 'failed': 0, 'errors': []}
        
        operations = {
            'copy': self.copy_file,
            'move': self.move_file,
            'delete': self.delete_file
        }
        
        if operation not in operations:
            raise ValueError(f"不支持的操作: {operation}")
        
        func = operations[operation]
        
        for path in paths:
            try:
                if func(path, **kwargs):
                    results['success'] += 1
                else:
                    results['failed'] += 1
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"{path}: {str(e)}")
        
        self.logger.info(f"批量操作完成 - 成功: {results['success']}, 失败: {results['failed']}")
        return results
    
    def _add_to_recent(self, path: str):
        """添加到最近文件列表"""
        if path not in self.recent_files:
            self.recent_files.insert(0, path)
            if len(self.recent_files) > self.max_recent_files:
                self.recent_files = self.recent_files[:self.max_recent_files]
    
    def get_recent_files(self, count: int = 10) -> List[str]:
        """获取最近访问的文件"""
        return self.recent_files[:count]
    
    def clear_recent_files(self):
        """清空最近文件列表"""
        self.recent_files.clear()
        self.logger.info("最近文件列表已清空")

# 全局文件管理器实例
file_manager = FileManager()