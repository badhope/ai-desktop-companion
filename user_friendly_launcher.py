#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户友好启动器
带有环境检查和清晰提示的新手友好启动脚本
"""

import sys
import os
import time
from datetime import datetime

def show_welcome():
    """显示欢迎界面"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    妖怪道模拟器                              ║
║                                                              ║
║           一个完整的修仙世界等你探索                         ║
║                                                              ║
║  🌟 新手友好  🎮 内容丰富  🚀 系统完善                      ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
def check_environment():
    """检查运行环境"""
    print("🔍 正在检查运行环境...")
    
    # 检查Python版本
    version_info = sys.version_info
    if version_info.major < 3 or version_info.minor < 8:
        print("❌ Python版本过低！")
        print(f"   当前版本: {version_info.major}.{version_info.minor}.{version_info.micro}")
        print("   需要版本: Python 3.8 或更高")
        print("\n💡 解决方案:")
        print("   1. 访问 python.org 下载最新Python")
        print("   2. 安装时勾选 'Add Python to PATH'")
        return False
        
    print(f"✓ Python版本检查通过: {version_info.major}.{version_info.minor}.{version_info.micro}")
    
    # 检查必需模块
    required_modules = ['os', 'sys', 'time', 'datetime']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
            
    if missing_modules:
        print(f"❌ 缺少必需模块: {', '.join(missing_modules)}")
        return False
        
    print("✓ 核心模块检查通过")
    return True

def show_game_modes():
    """显示游戏模式选择"""
    print("\n🎮 请选择游戏模式:")
    print("   1. 🎯 完整游戏体验 (推荐)")
    print("   2. 🎓 功能演示模式")
    print("   3. ⚙️  环境配置检查")
    print("   4. 🆘 帮助和支持")
    print("   5. 🚪 退出程序")
    
def launch_full_game():
    """启动完整游戏"""
    print("\n🚀 正在启动完整游戏...")
    print("   加载中，请稍候...")
    
    try:
        # 导入并启动主游戏
        from enhanced_game import enhanced_main
        enhanced_main()
    except ImportError as e:
        print(f"❌ 游戏模块导入失败: {e}")
        print("💡 可能需要运行环境检查")
        return False
    except Exception as e:
        print(f"❌ 游戏启动失败: {e}")
        return False
        
    return True

def launch_demo():
    """启动演示模式"""
    print("\n🎥 正在启动功能演示...")
    
    try:
        from complete_demo import complete_demo
        complete_demo()
    except ImportError as e:
        print(f"❌ 演示模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 演示启动失败: {e}")
        return False
        
    return True

def run_setup_check():
    """运行环境配置检查"""
    print("\n🔧 正在运行环境配置检查...")
    
    try:
        from setup_checker import main as setup_main
        setup_main()
    except ImportError as e:
        print(f"❌ 检查器模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 检查器运行失败: {e}")
        return False
        
    return True

def show_help():
    """显示帮助信息"""
    print("\n📖 帮助信息:")
    print("\n常见问题解答:")
    print("❓ Q: 游戏启动失败怎么办？")
    print("   A: 运行环境配置检查，确保Python版本>=3.8")
    
    print("\n❓ Q: 缺少依赖包怎么办？")
    print("   A: 选择环境配置检查，系统会自动安装缺失的包")
    
    print("\n❓ Q: 游戏运行缓慢怎么办？")
    print("   A: 确保电脑配置满足最低要求，关闭其他占用资源的程序")
    
    print("\n❓ Q: 存档丢失了怎么办？")
    print("   A: 存档文件位于 saves/ 目录下，注意定期备份")
    
    print("\n联系方式:")
    print("   📧 Email: support@xiuxian-game.com")
    print("   🌐 官网: www.xiuxian-game.com")
    print("   📱 QQ群: 123456789")
    
    print("\n💡 小贴士:")
    print("   • 首次运行建议先进行环境检查")
    print("   • 可以先体验演示模式熟悉操作")
    print("   • 定期保存游戏进度")
    print("   • 关注官方更新获取新内容")

def main():
    """主启动函数"""
    # 显示欢迎界面
    show_welcome()
    
    # 检查基础环境
    if not check_environment():
        print("\n❌ 环境检查未通过，请解决上述问题后再试")
        input("按回车键退出...")
        return
        
    print("✓ 环境检查通过！\n")
    
    # 主循环
    while True:
        show_game_modes()
        
        try:
            choice = input("\n请输入选择 (1-5): ").strip()
            
            if choice == "1":
                if launch_full_game():
                    break
                else:
                    print("\n⚠️  游戏启动失败，建议先运行环境检查")
                    
            elif choice == "2":
                if launch_demo():
                    break
                    
            elif choice == "3":
                run_setup_check()
                
            elif choice == "4":
                show_help()
                
            elif choice == "5":
                print("\n👋 感谢使用道士职业模拟器！")
                print("   愿你在修仙路上一帆风顺！")
                break
                
            else:
                print("❌ 无效选择，请输入 1-5 之间的数字")
                
        except KeyboardInterrupt:
            print("\n\n👋 程序被用户中断，再见！")
            break
        except Exception as e:
            print(f"\n❌ 发生未知错误: {e}")
            print("   建议联系技术支持或重新启动程序")
            
        # 每次操作后暂停，让用户阅读信息
        if choice != "5":
            input("\n按回车键继续...")

if __name__ == "__main__":
    main()