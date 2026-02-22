#!/bin/bash
# 全球科技新闻自动化系统 - 运行脚本
# 每天早上8:30执行

# 设置工作目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 设置Python路径（如果需要）
# export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# ============================================
# 新闻API配置（必需，至少配置一个）
# ============================================

# NewsAPI密钥 - 从 https://newsapi.org/ 获取（推荐）
# 免费版：100请求/天，支持英文科技新闻
export NEWSAPI_KEY="b1b5dc1e64064cddb26ab4d984642ba3"

# GNews密钥 - 从 https://gnews.io/ 获取
# 免费版：100请求/天，每次10篇文章
export GNEWS_KEY="626d1ce5f0c532755f3952c362034952"

# 天行数据密钥 - 从 https://www.tianapi.com/ 获取
# 免费版：100请求/天，支持中文科技新闻
export TIANXING_KEY="your_tianxing_key_here"

# ============================================
# Get笔记配置（可选）
# ============================================

# Get笔记API密钥（可选）
# export GETNOTE_API_KEY="your_api_key_here"

# 设置Webhook地址（可选）
# export GETNOTE_WEBHOOK_URL="your_webhook_url_here"

# 创建日志目录
mkdir -p "$SCRIPT_DIR/logs"

# 获取当前日期
DATE=$(date +"%Y%m%d")
LOG_FILE="$SCRIPT_DIR/logs/tech-news-$DATE.log"

echo "========================================" >> "$LOG_FILE"
echo "🚀 全球科技新闻自动化系统" >> "$LOG_FILE"
echo "⏰ 启动时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 运行主程序
python3 "$SCRIPT_DIR/main.py" --send >> "$LOG_FILE" 2>&1

# 检查运行结果
EXIT_CODE=$?

echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ 执行成功" >> "$LOG_FILE"
else
    echo "❌ 执行失败 (退出码: $EXIT_CODE)" >> "$LOG_FILE"
fi
echo "结束时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

exit $EXIT_CODE
