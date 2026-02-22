#!/bin/bash
# GitHub部署辅助脚本
# 一键完成GitHub仓库创建、代码推送、配置Secrets

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo "========================================"
echo "  🚀 GitHub部署助手"
echo "========================================"
echo ""

# 检查git
if ! command -v git &> /dev/null; then
    print_error "未找到Git，请先安装Git"
    exit 1
fi

# 获取GitHub用户名
read -p "请输入你的GitHub用户名: " GITHUB_USERNAME
if [ -z "$GITHUB_USERNAME" ]; then
    print_error "用户名不能为空"
    exit 1
fi

# 获取仓库名
read -p "请输入仓库名 (默认: tech-news-automation): " REPO_NAME
REPO_NAME=${REPO_NAME:-tech-news-automation}

print_info "配置信息:"
echo "  GitHub用户名: $GITHUB_USERNAME"
echo "  仓库名: $REPO_NAME"
echo ""

# 检查是否在项目目录
if [ ! -f "main.py" ]; then
    print_error "请在项目根目录运行此脚本"
    exit 1
fi

# 步骤1: 初始化Git
print_info "步骤1: 初始化Git仓库..."
if [ ! -d ".git" ]; then
    git init
    print_success "Git仓库初始化完成"
else
    print_warning "Git仓库已存在"
fi

# 步骤2: 配置Git
print_info "步骤2: 配置Git..."
read -p "请输入你的Git邮箱: " GIT_EMAIL
read -p "请输入你的Git用户名: " GIT_USER_NAME

git config user.email "$GIT_EMAIL"
git config user.name "$GIT_USER_NAME"
print_success "Git配置完成"

# 步骤3: 添加文件
print_info "步骤3: 添加文件到Git..."
git add .
print_success "文件已添加"

# 步骤4: 提交
print_info "步骤4: 提交代码..."
git commit -m "Initial commit: Tech News Automation System" || print_warning "没有新文件需要提交"
print_success "代码已提交"

# 步骤5: 添加远程仓库
print_info "步骤5: 配置远程仓库..."
REMOTE_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# 检查是否已有远程仓库
if git remote | grep -q "origin"; then
    print_warning "远程仓库已存在，更新URL..."
    git remote set-url origin "$REMOTE_URL"
else
    git remote add origin "$REMOTE_URL"
fi
print_success "远程仓库配置完成: $REMOTE_URL"

# 步骤6: 推送代码
print_info "步骤6: 推送代码到GitHub..."
print_warning "请确保你已经在GitHub上创建了仓库: $REMOTE_URL"
read -p "按回车键继续推送，或按Ctrl+C取消..."

git branch -M main
git push -u origin main || {
    print_error "推送失败，请检查:"
    echo "  1. GitHub仓库是否已创建"
    echo "  2. 是否有推送权限"
    echo "  3. 网络连接是否正常"
    exit 1
}
print_success "代码已推送到GitHub"

# 步骤7: 提示配置Secrets
echo ""
echo "========================================"
print_success "代码推送完成！"
echo "========================================"
echo ""
print_info "下一步：配置GitHub Secrets"
echo ""
echo "请访问: https://github.com/$GITHUB_USERNAME/$REPO_NAME/settings/secrets/actions"
echo ""
echo "添加以下Secrets:"
echo ""
echo "  1. NEWSAPI_KEY"
echo "     值: b1b5dc1e64064cddb26ab4d984642ba3"
echo "     获取: https://newsapi.org/"
echo ""
echo "  2. GNEWS_KEY"
echo "     值: 626d1ce5f0c532755f3952c362034952"
echo "     获取: https://gnews.io/"
echo ""
echo "========================================"
echo ""
print_info "配置完成后，可以手动触发Actions测试:"
echo "  1. 访问: https://github.com/$GITHUB_USERNAME/$REPO_NAME/actions"
echo "  2. 点击 'Daily Tech News'"
echo "  3. 点击 'Run workflow'"
echo ""
print_success "部署完成！"
