@echo off
title 妖怪道模拟器 - 用户友好版
color 0A

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    妖怪道模拟器                              ║
echo ║                                                              ║
echo ║           新手友好的修仙游戏启动器                           ║
echo ║                                                              ║
echo ║  🌟 自动环境检查  🎮 简单一键启动  🆘 详细帮助              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔍 正在检查运行环境...
python -c "import sys; exit(0 if sys.version_info >= (3,8) else 1)" 2>nul
if errorlevel 1 (
    echo ❌ 错误：需要Python 3.8或更高版本
    echo 💡 请访问 python.org 下载最新Python
    echo.
    pause
    exit /b 1
)

echo ✓ Python环境检查通过
echo.

echo 🚀 正在启动游戏...
echo.

python user_friendly_launcher.py

if errorlevel 1 (
    echo.
    echo ❌ 游戏启动失败
    echo 💡 建议：
    echo    1. 运行 python setup_checker.py 检查环境
    echo    2. 确保已安装所有必需依赖
    echo    3. 查看 README_USER.md 获取帮助
    echo.
    pause
)