# 全球科技新闻自动化系统 - Docker镜像
FROM python:3.11-slim

LABEL maintainer="Tech News Automation"
LABEL description="Daily tech news automation with Xiaohongshu-style image generation"

# 设置时区（北京时间）
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    fonts-noto-cjk \
    cron \
    curl \
    tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && fc-cache -fv

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY requirements.txt .
COPY main.py .
COPY run.sh .
COPY install.sh .
COPY scripts/ ./scripts/
COPY systemd/ ./systemd/

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建必要的目录
RUN mkdir -p /app/output /app/logs

# 设置执行权限
RUN chmod +x run.sh install.sh

# 设置环境变量（这些会被运行时的环境变量覆盖）
ENV NEWSAPI_KEY=""
ENV GNEWS_KEY=""
ENV TIANXING_KEY=""
ENV GETNOTE_API_KEY=""
ENV PYTHONUNBUFFERED=1

# 添加定时任务
RUN echo "30 8 * * * cd /app && python3 main.py --send >> /var/log/cron.log 2>&1" | crontab -

# 创建日志文件
RUN touch /var/log/cron.log

# 暴露输出目录
VOLUME ["/app/output", "/app/logs"]

# 启动cron服务
CMD ["sh", "-c", "echo '容器启动成功' && cron && tail -f /var/log/cron.log"]
