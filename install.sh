#!/bin/bash
# 全球科技新闻自动化系统 - 安装脚本
# 用于设置定时任务和初始化环境

set -e

echo "========================================"
echo "🚀 全球科技新闻自动化系统 - 安装"
echo "========================================"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查Python版本
echo "📋 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.8或更高版本"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python版本: $PYTHON_VERSION"

# 安装依赖
echo ""
echo "📦 安装Python依赖..."
pip3 install -r requirements.txt -q

# 创建必要的目录
echo ""
echo "📁 创建目录结构..."
mkdir -p "$SCRIPT_DIR/logs"
mkdir -p "$SCRIPT_DIR/output"

# 设置执行权限
chmod +x "$SCRIPT_DIR/run.sh"
chmod +x "$SCRIPT_DIR/main.py"

echo ""
echo "========================================"
echo "✅ 安装完成！"
echo "========================================"
echo ""
echo "使用指南:"
echo ""
echo "1. 测试运行（不发送）:"
echo "   python3 main.py --test"
echo ""
echo "2. 完整运行（包含发送）:"
echo "   python3 main.py --send"
echo ""
echo "3. 设置定时任务:"
echo ""
echo "   方法1 - Crontab:"
echo "   crontab -e"
echo "   添加: 30 8 * * * cd $SCRIPT_DIR && ./run.sh"
echo ""
echo "   方法2 - Systemd:"
echo "   sudo cp systemd/tech-news.service /etc/systemd/system/"
echo "   sudo cp systemd/tech-news.timer /etc/systemd/system/"
echo "   sudo systemctl daemon-reload"
echo "   sudo systemctl enable tech-news.timer"
echo "   sudo systemctl start tech-news.timer"
echo ""
echo "4. 查看定时任务设置指南:"
echo "   python3 main.py --setup-cron"
echo ""
echo "配置文件:"
echo "  - run.sh: 设置环境变量（GETNOTE_API_KEY等）"
echo "  - crontab.txt: Crontab配置示例"
echo ""
echo "输出目录: $SCRIPT_DIR/output/"
echo "日志目录: $SCRIPT_DIR/logs/"
echo ""
