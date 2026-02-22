#!/bin/bash
# 全球科技新闻自动化系统 - 一键部署脚本
# 支持多种部署方式

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的信息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示菜单
show_menu() {
    clear
    echo "========================================"
    echo "  🚀 全球科技新闻自动化系统 - 部署工具"
    echo "========================================"
    echo ""
    echo "请选择部署方式:"
    echo ""
    echo "  1) 本地部署 (Linux服务器/VPS)"
    echo "  2) Docker部署"
    echo "  3) Docker Compose部署"
    echo "  4) GitHub Actions配置"
    echo "  5) 仅安装依赖"
    echo "  6) 测试运行"
    echo "  0) 退出"
    echo ""
    echo "========================================"
}

# 本地部署
local_deploy() {
    print_info "开始本地部署..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        print_error "未找到Python3，请先安装Python 3.8或更高版本"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_info "Python版本: $PYTHON_VERSION"
    
    # 安装依赖
    print_info "安装Python依赖..."
    pip3 install -r requirements.txt -q
    
    # 安装中文字体
    print_info "安装中文字体..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update -qq
        sudo apt-get install -y -qq fonts-noto-cjk
    elif command -v yum &> /dev/null; then
        sudo yum install -y google-noto-cjk-fonts
    else
        print_warning "无法自动安装字体，请手动安装中文字体"
    fi
    
    # 创建目录
    mkdir -p output logs
    
    # 配置API密钥
    print_info "配置API密钥..."
    if [ ! -f .env ]; then
        cp .env.example .env
        print_warning "请编辑 .env 文件，填入你的API密钥"
        nano .env 2>/dev/null || vi .env 2>/dev/null || print_warning "请手动编辑 .env 文件"
    fi
    
    # 设置定时任务
    print_info "设置定时任务..."
    read -p "是否设置每天8:30自动运行? (y/n): " setup_cron
    if [ "$setup_cron" = "y" ] || [ "$setup_cron" = "Y" ]; then
        CRON_JOB="30 8 * * * cd $(pwd) && ./run.sh"
        (crontab -l 2>/dev/null | grep -v "tech-news"; echo "$CRON_JOB") | crontab -
        print_success "定时任务已设置"
        crontab -l | grep "tech-news"
    fi
    
    # 测试运行
    print_info "测试运行..."
    python3 main.py --test
    
    print_success "本地部署完成!"
    print_info "生成的图片保存在 output/ 目录"
    print_info "日志保存在 logs/ 目录"
}

# Docker部署
docker_deploy() {
    print_info "开始Docker部署..."
    
    # 检查Docker
    if ! command -v docker &> /dev/null; then
        print_error "未找到Docker，请先安装Docker"
        echo "安装指南: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    # 配置API密钥
    if [ ! -f .env ]; then
        cp .env.example .env
        print_warning "请编辑 .env 文件，填入你的API密钥"
    fi
    
    # 构建镜像
    print_info "构建Docker镜像..."
    docker build -t tech-news-automation:latest .
    
    # 运行容器
    print_info "运行Docker容器..."
    docker run -d \
        --name tech-news-automation \
        --env-file .env \
        -v $(pwd)/output:/app/output \
        -v $(pwd)/logs:/app/logs \
        --restart unless-stopped \
        tech-news-automation:latest
    
    print_success "Docker部署完成!"
    print_info "查看日志: docker logs -f tech-news-automation"
    print_info "停止容器: docker stop tech-news-automation"
}

# Docker Compose部署
docker_compose_deploy() {
    print_info "开始Docker Compose部署..."
    
    # 检查Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "未找到Docker Compose，请先安装"
        echo "安装指南: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    # 配置API密钥
    if [ ! -f .env ]; then
        cp .env.example .env
        print_warning "请编辑 .env 文件，填入你的API密钥"
        nano .env 2>/dev/null || vi .env 2>/dev/null || print_warning "请手动编辑 .env 文件"
    fi
    
    # 启动服务
    print_info "启动Docker Compose服务..."
    if command -v docker-compose &> /dev/null; then
        docker-compose up -d
    else
        docker compose up -d
    fi
    
    print_success "Docker Compose部署完成!"
    print_info "查看日志: docker-compose logs -f"
    print_info "停止服务: docker-compose down"
}

# GitHub Actions配置
github_actions_setup() {
    print_info "GitHub Actions配置指南"
    echo ""
    echo "1. 在GitHub上创建新仓库"
    echo "2. 将代码推送到仓库:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/tech-news-automation.git"
    echo "   git push -u origin main"
    echo ""
    echo "3. 在仓库设置中添加Secrets:"
    echo "   - NEWSAPI_KEY: 你的NewsAPI密钥"
    echo "   - GNEWS_KEY: 你的GNews密钥"
    echo ""
    echo "4. GitHub Actions将自动每天8:30运行"
    echo "   也可以手动触发: Actions > Daily Tech News > Run workflow"
    echo ""
    print_success "配置完成!"
}

# 安装依赖
install_deps() {
    print_info "安装依赖..."
    
    # Python依赖
    pip3 install -r requirements.txt
    
    # 中文字体
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y fonts-noto-cjk
    elif command -v yum &> /dev/null; then
        sudo yum install -y google-noto-cjk-fonts
    fi
    
    print_success "依赖安装完成!"
}

# 测试运行
test_run() {
    print_info "测试运行..."
    
    # 加载环境变量
    if [ -f .env ]; then
        export $(cat .env | grep -v '^#' | xargs)
    fi
    
    python3 main.py --test
    
    print_success "测试完成!"
    print_info "查看生成的图片: ls -la output/"
}

# 主程序
main() {
    # 获取脚本所在目录
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    cd "$SCRIPT_DIR"
    
    while true; do
        show_menu
        read -p "请输入选项 [0-6]: " choice
        
        case $choice in
            1)
                local_deploy
                read -p "按回车键继续..."
                ;;
            2)
                docker_deploy
                read -p "按回车键继续..."
                ;;
            3)
                docker_compose_deploy
                read -p "按回车键继续..."
                ;;
            4)
                github_actions_setup
                read -p "按回车键继续..."
                ;;
            5)
                install_deps
                read -p "按回车键继续..."
                ;;
            6)
                test_run
                read -p "按回车键继续..."
                ;;
            0)
                print_info "感谢使用，再见!"
                exit 0
                ;;
            *)
                print_error "无效选项，请重新选择"
                sleep 2
                ;;
        esac
    done
}

# 运行主程序
main
