# 🚀 GitHub部署完整指南

使用GitHub Actions免费实现每天自动获取科技新闻并生成图片。

## 📋 部署流程

```
1. 创建GitHub仓库 → 2. 推送代码 → 3. 配置Secrets → 4. 运行测试 → 5. 完成
```

---

## 步骤1：创建GitHub仓库

### 1.1 登录GitHub

访问 https://github.com/login 并登录你的账号

### 1.2 创建新仓库

1. 点击右上角 **+** 号 → **New repository**
2. 填写仓库信息：
   - **Repository name**: `tech-news-automation`（或你喜欢的名字）
   - **Description**: 全球科技新闻自动化系统 - 每日生成小红书风格科技早报
   - **Visibility**: 选择 **Private**（保护API密钥）
   - ✅ 勾选 **Add a README file**
3. 点击 **Create repository**

![创建仓库](https://docs.github.com/assets/images/help/repository/repo-create.png)

---

## 步骤2：推送代码到GitHub

### 2.1 初始化本地仓库

在项目目录中执行：

```bash
# 进入项目目录
cd /mnt/okcomputer/output/tech-news-automation

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Tech News Automation System"
```

### 2.2 连接远程仓库

```bash
# 添加远程仓库（替换YOUR_USERNAME为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/tech-news-automation.git

# 推送代码
git branch -M main
git push -u origin main
```

### 2.3 验证推送

访问 `https://github.com/YOUR_USERNAME/tech-news-automation` 查看代码是否已上传

---

## 步骤3：配置GitHub Secrets

### 3.1 进入Settings

1. 打开你的GitHub仓库页面
2. 点击顶部 **Settings** 标签
3. 左侧菜单选择 **Secrets and variables** → **Actions**

### 3.2 添加API密钥

点击 **New repository secret** 按钮，依次添加：

#### Secret 1: NEWSAPI_KEY
- **Name**: `NEWSAPI_KEY`
- **Secret**: `b1b5dc1e64064cddb26ab4d984642ba3`
- 点击 **Add secret**

#### Secret 2: GNEWS_KEY
- **Name**: `GNEWS_KEY`
- **Secret**: `626d1ce5f0c532755f3952c362034952`
- 点击 **Add secret**

![添加Secret](https://docs.github.com/assets/images/help/repository/actions-secrets.png)

### 3.3 验证Secrets

添加完成后，你应该看到：

| Name | Updated |
|------|---------|
| NEWSAPI_KEY | just now |
| GNEWS_KEY | just now |

---

## 步骤4：运行GitHub Actions

### 4.1 查看Actions

1. 点击仓库顶部 **Actions** 标签
2. 你会看到 **Daily Tech News** 工作流

### 4.2 手动触发测试

1. 点击 **Daily Tech News**
2. 点击右侧 **Run workflow** 按钮
3. 选择分支（main）
4. 点击 **Run workflow**

![运行Workflow](https://docs.github.com/assets/images/help/actions/workflow-dispatch.png)

### 4.3 查看运行结果

1. 点击正在运行的工作流
2. 查看每个步骤的执行日志
3. 等待执行完成

---

## 步骤5：获取生成的图片

### 5.1 方式1：下载Artifacts

1. 工作流运行完成后，点击 **Artifacts**
2. 下载 `tech-news-images` 文件
3. 解压后查看生成的图片

### 5.2 方式2：查看Release

1. 点击仓库右侧 **Releases**
2. 查看最新发布的Release
3. 下载附件中的图片

### 5.3 方式3：查看Commit

1. 工作流会自动提交生成的文件
2. 点击 **Code** → 查看最新的commit
3. 在 `output/` 目录中查看图片

---

## ⏰ 定时任务说明

GitHub Actions已配置为每天自动运行：

```yaml
schedule:
  - cron: '30 0 * * *'  # UTC 00:30 = 北京时间 8:30
```

### 查看下次运行时间

1. 打开 Actions 页面
2. 查看 **Daily Tech News** 工作流
3. 右侧会显示下次计划运行时间

---

## 🐛 故障排除

### 问题1：Actions没有运行

**检查清单：**
- [ ] `.github/workflows/daily-news.yml` 文件存在
- [ ] 文件在 `main` 分支上
- [ ] Secrets 已正确配置

**解决方案：**
```bash
# 检查文件是否存在
ls -la .github/workflows/

# 确保文件已推送
git status
git push origin main
```

### 问题2：API请求失败

**错误信息：**
```
NewsAPI request failed: 401 Unauthorized
```

**解决方案：**
1. 检查 Secrets 是否正确设置
2. 验证 API 密钥是否有效
3. 重新添加 Secrets

### 问题3：图片生成失败

**错误信息：**
```
OSError: cannot open resource
```

**解决方案：**
GitHub Actions 环境中已配置中文字体，如果仍有问题，检查 `daily-news.yml` 中的字体安装步骤。

### 问题4：Artifacts下载失败

**解决方案：**
- Artifacts 默认保存 30 天
- 可以在工作流中调整 `retention-days`

---

## 📊 使用限制

### GitHub Actions 免费额度

| 类型 | 免费额度 |
|------|---------|
| 存储空间 | 500MB |
| 运行时间 | 2000分钟/月 |
| 并发任务 | 20个 |

### 本系统资源消耗

| 项目 | 消耗 |
|------|------|
| 每次运行时间 | ~2-3分钟 |
| 每月运行次数 | ~30次 |
| 每月总耗时 | ~90分钟 |
| 存储占用 | ~50MB/月 |

**结论：免费额度完全够用！**

---

## 🎨 自定义配置

### 修改运行时间

编辑 `.github/workflows/daily-news.yml`：

```yaml
on:
  schedule:
    # 北京时间 7:30 (UTC 23:30)
    - cron: '30 23 * * *'
    
    # 或每天运行两次
    - cron: '30 0 * * *'   # 8:30
    - cron: '30 12 * * *'  # 20:30
```

### 修改新闻数量

编辑 `main.py`：

```python
news = self.news_fetcher.fetch_news(num_results=15)  # 默认10条
```

### 添加邮件通知

在 `.github/workflows/daily-news.yml` 中添加：

```yaml
- name: Send email
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 587
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: Tech News ${{ github.run_date }}
    to: your-email@example.com
    from: GitHub Actions
    attachments: output/*.jpg
```

---

## 📱 接收通知

### 方式1：GitHub App

安装 GitHub App，Actions 完成后会收到推送通知

### 方式2：邮件通知

配置邮件通知：
1. 点击仓库 **Settings** → **Notifications**
2. 勾选 **Actions** 通知

### 方式3：Webhook

配置 webhook 发送到企业微信/钉钉/飞书：

```yaml
- name: Send notification
  run: |
    curl -X POST "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"msgtype": "text", "text": {"content": "科技早报已生成"}}'
```

---

## 🔒 安全建议

1. **使用Private仓库**：保护API密钥不被泄露
2. **定期更换密钥**：建议每3个月更换一次API密钥
3. **限制Actions权限**：在仓库设置中限制Actions的权限

---

## ✅ 部署检查清单

- [ ] GitHub仓库已创建
- [ ] 代码已推送到GitHub
- [ ] NEWSAPI_KEY 已添加到Secrets
- [ ] GNEWS_KEY 已添加到Secrets
- [ ] Actions工作流已运行
- [ ] 生成的图片已下载
- [ ] 定时任务正常工作

---

## 🎉 完成！

部署完成后，系统将在每天北京时间 **8:30** 自动：
1. 获取最新科技新闻
2. 生成3张小红书风格图片
3. 保存到Artifacts和Release

**明天早上8:30，你将收到第一份自动生成的科技新闻早报！**

---

## 📞 需要帮助？

- GitHub Actions文档：https://docs.github.com/cn/actions
- 查看Actions日志排查问题
- 参考 `部署指南.md` 获取更多部署方式
