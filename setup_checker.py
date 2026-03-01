#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境配置检查器
自动检测和配置游戏运行环境，对新手友好
"""

import sys
import os
import subprocess
import platform
from typing import Dict, List, Tuple

class EnvironmentChecker:
    """环境检查器"""
    
    def __init__(self):
        self.required_packages = [
            'customtkinter>=5.2.0',
            'psutil>=5.9.0',
            'pillow>=9.0.0'
        ]
        self.optional_packages = [
            'pygame>=2.1.0',
            'opencv-python>=4.6.0',
            'numpy>=1.21.0'
        ]
        self.system_info = self._get_system_info()
        
    def _get_system_info(self) -> Dict[str, str]:
        """获取系统信息"""
        return {
            'platform': platform.system(),
            'version': platform.version(),
            'python_version': sys.version,
            'architecture': platform.architecture()[0]
        }
        
    def check_python_version(self) -> Tuple[bool, str]:
        """检查Python版本"""
        version_info = sys.version_info
        if version_info.major >= 3 and version_info.minor >= 8:
            return True, f"✓ Python版本合格: {version_info.major}.{version_info.minor}.{version_info.micro}"
        else:
            return False, f"✗ Python版本过低: {version_info.major}.{version_info.minor}.{version_info.micro} (需要3.8+)"
            
    def check_required_packages(self) -> Tuple[List[str], List[str]]:
        """检查必需包"""
        installed = []
        missing = []
        
        for package in self.required_packages:
            package_name = package.split('>=')[0]
            try:
                __import__(package_name.replace('-', '_'))
                installed.append(package)
            except ImportError:
                missing.append(package)
                
        return installed, missing
        
    def check_optional_packages(self) -> Tuple[List[str], List[str]]:
        """检查可选包"""
        installed = []
        missing = []
        
        for package in self.optional_packages:
            package_name = package.split('>=')[0]
            try:
                __import__(package_name.replace('-', '_'))
                installed.append(package)
            except ImportError:
                missing.append(package)
                
        return installed, missing
        
    def check_directories(self) -> List[str]:
        """检查必要目录"""
        required_dirs = ['saves', 'assets', 'logs']
        missing_dirs = []
        
        for dir_name in required_dirs:
            if not os.path.exists(dir_name):
                missing_dirs.append(dir_name)
                
        return missing_dirs
        
    def create_missing_directories(self, missing_dirs: List[str]) -> bool:
        """创建缺失的目录"""
        try:
            for dir_name in missing_dirs:
                os.makedirs(dir_name, exist_ok=True)
                print(f"✓ 创建目录: {dir_name}")
            return True
        except Exception as e:
            print(f"✗ 创建目录失败: {e}")
            return False
            
    def install_missing_packages(self, packages: List[str]) -> bool:
        """安装缺失的包"""
        if not packages:
            return True
            
        print("正在安装缺失的依赖包...")
        success_count = 0
        
        for package in packages:
            try:
                print(f"安装 {package}...")
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', package
                ])
                success_count += 1
                print(f"✓ {package} 安装成功")
            except subprocess.CalledProcessError as e:
                print(f"✗ {package} 安装失败: {e}")
            except Exception as e:
                print(f"✗ 安装过程中出错: {e}")
                
        return success_count == len(packages)
        
    def run_comprehensive_check(self) -> Dict[str, any]:
        """运行全面检查"""
        print("=" * 60)
        print("道士职业模拟器 - 环境配置检查")
        print("=" * 60)
        
        results = {
            'system_check': {},
            'python_check': {},
            'package_check': {},
            'directory_check': {}
        }
        
        # 系统信息检查
        print("\n🖥️  系统信息检查:")
        print(f"  操作系统: {self.system_info['platform']} {self.system_info['version']}")
        print(f"  Python版本: {self.system_info['python_version']}")
        print(f"  系统架构: {self.system_info['architecture']}")
        results['system_check'] = self.system_info
        
        # Python版本检查
        print("\n🐍 Python版本检查:")
        version_ok, version_msg = self.check_python_version()
        print(f"  {version_msg}")
        results['python_check'] = {
            'ok': version_ok,
            'message': version_msg
        }
        
        # 必需包检查
        print("\n📦 必需依赖包检查:")
        installed_req, missing_req = self.check_required_packages()
        
        if installed_req:
            print("  已安装的包:")
            for pkg in installed_req:
                print(f"    ✓ {pkg}")
                
        if missing_req:
            print("  缺失的包:")
            for pkg in missing_req:
                print(f"    ✗ {pkg}")
                
        results['package_check']['required'] = {
            'installed': installed_req,
            'missing': missing_req
        }
        
        # 可选包检查
        print("\n🔧 可选依赖包检查:")
        installed_opt, missing_opt = self.check_optional_packages()
        
        if installed_opt:
            print("  已安装的可选包:")
            for pkg in installed_opt:
                print(f"    ✓ {pkg}")
                
        if missing_opt:
            print("  未安装的可选包（不影响基本功能）:")
            for pkg in missing_opt:
                print(f"    ○ {pkg}")
                
        results['package_check']['optional'] = {
            'installed': installed_opt,
            'missing': missing_opt
        }
        
        # 目录检查
        print("\n📁 必要目录检查:")
        missing_dirs = self.check_directories()
        
        if missing_dirs:
            print("  缺失的目录:")
            for dir_name in missing_dirs:
                print(f"    ✗ {dir_name}")
            print("  正在创建缺失目录...")
            if self.create_missing_directories(missing_dirs):
                print("  ✓ 目录创建完成")
            else:
                print("  ✗ 目录创建失败")
        else:
            print("  ✓ 所有必需目录都已存在")
            
        results['directory_check'] = {
            'missing': missing_dirs,
            'all_exist': len(missing_dirs) == 0
        }
        
        # 总体评估
        print("\n" + "=" * 60)
        print("📊 检查结果总结:")
        
        can_run = True
        issues = []
        
        if not version_ok:
            can_run = False
            issues.append("Python版本不符合要求")
            
        if missing_req:
            can_run = False
            issues.append(f"缺少{len(missing_req)}个必需依赖包")
            
        if not results['directory_check']['all_exist']:
            issues.append("目录结构不完整")
            
        if can_run:
            print("🎉 环境检查通过！可以正常运行游戏")
            if missing_opt:
                print(f"💡 提示：还有{len(missing_opt)}个可选包未安装，建议安装以获得完整体验")
        else:
            print("❌ 环境检查未通过，存在问题：")
            for issue in issues:
                print(f"  • {issue}")
                
        results['can_run'] = can_run
        results['issues'] = issues
        
        print("=" * 60)
        return results
        
    def auto_fix_issues(self, results: Dict[str, any]) -> bool:
        """自动修复问题"""
        print("\n🔧 自动修复检测到的问题...")
        
        fixes_applied = []
        
        # 修复缺失的必需包
        missing_required = results['package_check']['required']['missing']
        if missing_required:
            print("正在安装必需的依赖包...")
            if self.install_missing_packages(missing_required):
                fixes_applied.append("必需依赖包安装完成")
            else:
                print("✗ 必需依赖包安装失败")
                return False
                
        # 修复缺失目录
        missing_dirs = results['directory_check']['missing']
        if missing_dirs:
            print("正在创建缺失目录...")
            if self.create_missing_directories(missing_dirs):
                fixes_applied.append("目录结构修复完成")
            else:
                print("✗ 目录创建失败")
                return False
                
        if fixes_applied:
            print("\n✓ 修复完成:")
            for fix in fixes_applied:
                print(f"  • {fix}")
            return True
        else:
            print("✓ 没有发现问题需要修复")
            return True

def main():
    """主函数"""
    checker = EnvironmentChecker()
    
    # 运行检查
    results = checker.run_comprehensive_check()
    
    # 如果有问题，询问是否自动修复
    if not results['can_run']:
        print("\n🔧 检测到环境问题，是否尝试自动修复？")
        choice = input("输入 y 确认自动修复，或按回车跳过: ").strip().lower()
        
        if choice == 'y':
            if checker.auto_fix_issues(results):
                print("\n🔄 修复完成，重新检查环境...")
                # 重新检查
                new_results = checker.run_comprehensive_check()
                if new_results['can_run']:
                    print("\n🎉 环境已准备就绪，可以开始游戏了！")
                else:
                    print("\n❌ 仍有问题未能解决，请手动处理")
            else:
                print("\n❌ 自动修复失败，请手动解决环境问题")
        else:
            print("\n💡 您可以选择手动解决上述问题，或寻求技术支持")
    else:
        print("\n🎮 环境一切就绪，随时可以开始修仙之旅！")
        
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()