# 故障排除指南

## 🚨 常见问题及解决方案

### 环境配置问题

#### 1. Python版本问题

**症状**：
```
ModuleNotFoundError: No module named 'xxx'
SyntaxError: invalid syntax
```

**解决方案**：
1. 检查Python版本：`python --version`
2. 确保版本 ≥ 3.8
3. 重新安装Python，勾选"Add Python to PATH"

#### 2. 依赖包缺失

**症状**：
```
ImportError: No module named 'customtkinter'
ImportError: No module named 'psutil'
```

**解决方案**：
```bash
# 自动检查并安装
python setup_checker.py

# 或手动安装
pip install -r requirements.txt
```

#### 3. 权限问题

**症状**：
```
PermissionError: [Errno 13] Permission denied
```

**解决方案**：
- Windows：以管理员身份运行命令提示符
- Linux/macOS：使用 `sudo` 或检查文件权限

### 游戏运行问题

#### 1. 启动失败

**症状**：
- 程序闪退
- 黑屏无响应
- 报错信息不明确

**排查步骤**：
1. 运行环境检查：`python setup_checker.py`
2. 查看日志文件：`logs/` 目录
3. 启用调试模式：设置环境变量 `DEBUG_MODE=True`

#### 2. 存档问题

**症状**：
- 存档无法读取
- 存档文件损坏
- 存档丢失

**解决方案**：
```bash
# 检查存档目录
ls saves/

# 备份存档
cp saves/ saves_backup/

# 清理损坏存档
rm saves/corrupted_save.json
```

#### 3. 性能问题

**症状**：
- 游戏运行缓慢
- 内存占用过高
- CPU使用率异常

**优化建议**：
1. 关闭其他程序释放资源
2. 降低游戏复杂度设置
3. 检查是否有无限循环

### 开发相关问题

#### 1. 代码调试

**启用调试模式**：
```python
# 在代码开头添加
import os
os.environ['DEBUG_MODE'] = 'True'

# 或运行时设置
DEBUG_MODE=True python enhanced_game.py
```

**查看详细日志**：
```bash
# 实时查看日志
tail -f logs/game_*.log

# 搜索特定错误
grep "ERROR" logs/game_*.log
```

#### 2. 模块导入问题

**常见错误**：
```
ModuleNotFoundError: No module named 'game_core'
ImportError: attempted relative import with no known parent package
```

**解决方案**：
```python
# 确保正确的工作目录
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 或使用绝对导入
from game_core.game_engine import GameEngine
```

#### 3. 编码问题

**症状**：
```
UnicodeDecodeError: 'gbk' codec can't decode byte
```

**解决方案**：
```python
# 在文件开头添加编码声明
# -*- coding: utf-8 -*-

# 或在打开文件时指定编码
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()
```

## 🛠️ 高级故障排除

### 系统诊断脚本

```python
# diagnose.py
import sys
import os
import platform

def diagnose():
    print("系统诊断报告")
    print("=" * 40)
    
    # Python信息
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    
    # 系统信息
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"架构: {platform.architecture()}")
    
    # 环境变量
    print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")
    print(f"DEBUG_MODE: {os.environ.get('DEBUG_MODE', 'False')}")
    
    # 当前工作目录
    print(f"工作目录: {os.getcwd()}")
    
    # 检查关键文件
    required_files = [
        'enhanced_game.py',
        'game_core/',
        'game_modules/',
        'requirements.txt'
    ]
    
    print("\n文件检查:")
    for file in required_files:
        status = "✓" if os.path.exists(file) else "✗"
        print(f"  {status} {file}")

if __name__ == "__main__":
    diagnose()
```

### 性能分析工具

```python
import cProfile
import pstats

def profile_game():
    """性能分析"""
    profiler = cProfile.Profile()
    profiler.enable()
    
    # 运行游戏代码
    from enhanced_game import enhanced_main
    enhanced_main()
    
    profiler.disable()
    
    # 输出分析结果
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # 显示前20个最耗时的函数

# 使用方式
# python -m cProfile -o profile_output.prof your_script.py
```

## 📞 获取帮助

### 社区支持

1. **GitHub Issues**：提交bug报告和功能请求
2. **QQ群**：实时交流和技术支持
3. **论坛**：详细讨论和经验分享

### 提交Bug报告

请包含以下信息：
- 错误信息和堆栈跟踪
- 系统环境信息
- 复现步骤
- 相关日志文件

### 日志文件位置

```
logs/
├── game_20240101.log    # 按日期分割的日志
├── error.log           # 错误专用日志
└── debug.log           # 调试信息日志
```

## 🔧 应急处理

### 快速恢复方案

1. **重置游戏状态**：
```bash
# 备份当前状态
cp -r saves/ saves_backup/

# 清理缓存
rm -rf __pycache__/
rm -rf *.pyc
```

2. **重新安装**：
```bash
# 备份重要文件
cp saves/*.json ~/backup/

# 重新克隆项目
git clone <repository-url>
```

3. **最小化运行**：
```bash
# 只运行核心功能
python -c "
from game_core.game_engine import GameEngine
from game_core.player import Player
# 简化初始化
"
```

### 环境重建脚本

```bash
#!/bin/bash
# rebuild_env.sh

echo "重建游戏环境..."

# 清理旧环境
rm -rf __pycache__/
rm -rf */__pycache__/
find . -name "*.pyc" -delete

# 重新安装依赖
pip install --upgrade pip
pip install -r requirements.txt

# 运行检查
python setup_checker.py

echo "环境重建完成！"
```

记住：遇到问题时不要慌张，按照步骤逐一排查，大部分问题都能得到解决！