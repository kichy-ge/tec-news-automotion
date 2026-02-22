# 🚀 一键部署到GitHub

## 方式1：使用部署脚本（推荐）

```bash
# 1. 进入项目目录
cd tech-news-automation

# 2. 运行GitHub部署脚本
bash github-deploy.sh

# 3. 按提示输入GitHub用户名、邮箱等信息

# 4. 在GitHub上配置Secrets
```

## 方式2：手动部署

### 步骤1：创建GitHub仓库

1. 访问 https://github.com/new
2. 填写仓库名：`tech-news-automation`
3. 选择 **Private**（保护API密钥）
4. 点击 **Create repository**

### 步骤2：推送代码

```bash
# 进入项目目录
cd tech-news-automation

# 初始化Git
git init
git add .
git commit -m "Initial commit"

# 添加远程仓库（替换YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/tech-news-automation.git

# 推送代码
git branch -M main
git push -u origin main
```

### 步骤3：配置Secrets

1. 打开仓库页面
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加两个Secrets：

| Name | Value |
|------|-------|
| `NEWSAPI_KEY` | `b1b5dc1e64064cddb26ab4d984642ba3` |
| `GNEWS_KEY` | `626d1ce5f0c532755f3952c362034952` |

### 步骤4：运行测试

1. 点击仓库顶部的 **Actions**
2. 选择 **Daily Tech News**
3. 点击 **Run workflow** → **Run workflow**
4. 等待执行完成

### 步骤5：下载图片

- 在Actions运行结果页面，点击 **Artifacts** 下载图片

---

## ✅ 部署验证

部署成功后：

1. ✅ 代码已推送到GitHub
2. ✅ Secrets已配置
3. ✅ Actions工作流正常运行
4. ✅ 生成的图片可下载

---

## ⏰ 定时任务

GitHub Actions已配置为每天 **8:30（北京时间）** 自动运行。

---

## 📚 详细文档

- [GitHub部署指南](GitHub部署指南.md) - 完整部署说明
- [API配置指南](API配置指南.md) - 获取API密钥
- [使用指南](使用指南.md) - 系统使用说明
