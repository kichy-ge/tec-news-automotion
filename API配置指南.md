# 🔑 新闻API配置指南

本系统支持多个新闻API，至少配置一个即可开始使用真实新闻数据。

## 📋 支持的API

| API | 语言 | 免费额度 | 特点 |
|-----|------|---------|------|
| NewsAPI | 英文 | 100请求/天 | 全球新闻源，支持分类筛选 |
| GNews | 英文 | 100请求/天 | 简洁快速，每次最多10条 |
| 天行数据 | 中文 | 100请求/天 | 国内科技新闻 |

## 🚀 快速配置（推荐NewsAPI）

### 1. 注册NewsAPI账号

1. 访问 https://newsapi.org/
2. 点击 "Get API Key" 按钮
3. 使用邮箱注册账号
4. 登录后复制API密钥

### 2. 配置API密钥

编辑 `run.sh` 文件：

```bash
nano run.sh
```

找到以下行并填入你的API密钥：

```bash
export NEWSAPI_KEY="your_newsapi_key_here"
```

改为：

```bash
export NEWSAPI_KEY="1234567890abcdef1234567890abcdef"
```

### 3. 测试运行

```bash
python3 main.py --test
```

如果看到 `✅ NewsAPI获取成功: X条`，说明配置成功！

---

## 📰 NewsAPI 详细配置

### 获取API密钥

1. 访问 https://newsapi.org/
2. 点击 "Get API Key"
3. 填写邮箱和密码注册
4. 查看邮箱验证邮件并点击验证链接
5. 登录后，API密钥会显示在首页

### 免费版限制

- 100请求/天
- 只能获取1天内的新闻
- 不支持HTTPS（开发环境需要处理）

### 升级付费版

如果需要更多请求量，可以升级到付费版：
- 开发者版：$449/月，100,000请求/天
- 商业版：自定义价格

---

## 📰 GNews 配置（备选）

### 获取API密钥

1. 访问 https://gnews.io/
2. 点击 "Get API Key"
3. 使用Google账号或邮箱注册
4. 在Dashboard中复制API密钥

### 配置方法

编辑 `run.sh`：

```bash
export GNEWS_KEY="your_gnews_api_key_here"
```

### 免费版限制

- 100请求/天
- 每次请求最多10篇文章
- 总共可获取1000篇文章/天

---

## 🇨🇳 天行数据配置（中文新闻）

### 获取API密钥

1. 访问 https://www.tianapi.com/apiview/10
2. 点击 "立即申请"
3. 注册账号并登录
4. 在"我的API"页面找到"科技新闻"接口
5. 复制API密钥

### 配置方法

编辑 `run.sh`：

```bash
export TIANXING_KEY="your_tianxing_api_key_here"
```

### 免费版限制

- 100请求/天
- 每次最多20条新闻

---

## 🔧 高级配置

### 使用 .env 文件

可以创建 `.env` 文件管理API密钥：

```bash
cp .env.example .env
nano .env
```

填写你的API密钥：

```bash
NEWSAPI_KEY=your_newsapi_key_here
GNEWS_KEY=your_gnews_key_here
TIANXING_KEY=your_tianxing_key_here
```

加载环境变量：

```bash
source .env
```

### 配置多个API

系统会按以下优先级使用API：
1. NewsAPI（英文）
2. GNews（英文）
3. 天行数据（中文）

如果配置了多个API，系统会自动聚合新闻并去重。

### 只使用中文新闻

如果只配置了 `TIANXING_KEY`，系统将只获取中文科技新闻。

### 只使用英文新闻

如果只配置了 `NEWSAPI_KEY` 或 `GNEWS_KEY`，系统将只获取英文科技新闻。

---

## 🧪 测试API连接

### 测试NewsAPI

```bash
curl "https://newsapi.org/v2/everything?q=technology&apiKey=YOUR_API_KEY"
```

### 测试GNews

```bash
curl "https://gnews.io/api/v4/search?q=technology&apikey=YOUR_API_KEY"
```

### 测试天行数据

```bash
curl "http://api.tianapi.com/keji/index?key=YOUR_API_KEY&num=5"
```

---

## ❌ 常见问题

### "未配置NEWSAPI_KEY，跳过NewsAPI"

**原因**：没有配置API密钥

**解决**：
1. 按照上述步骤获取API密钥
2. 编辑 `run.sh` 填入密钥
3. 重新运行

### "NewsAPI请求失败"

**原因**：
- API密钥错误
- 网络连接问题
- 超过免费版限制

**解决**：
1. 检查API密钥是否正确
2. 测试API连接（见上文）
3. 检查是否超过100请求/天限制

### "所有API都失败，使用模拟数据"

**原因**：所有配置的API都无法连接

**解决**：
1. 检查网络连接
2. 检查API密钥
3. 暂时使用模拟数据，稍后再试

---

## 📊 API使用统计

### 查看NewsAPI使用量

登录 https://newsapi.org/ 查看Dashboard

### 查看GNews使用量

登录 https://gnews.io/ 查看Dashboard

### 查看天行数据使用量

登录 https://www.tianapi.com/ 查看"我的API"

---

## 💡 最佳实践

1. **至少配置一个API**：推荐NewsAPI，稳定可靠
2. **配置多个API**：可以提高新闻覆盖率和系统稳定性
3. **监控使用量**：避免超过免费版限制
4. **使用缓存**：系统会自动缓存1小时，减少API调用

---

## 📞 获取帮助

- NewsAPI文档：https://newsapi.org/docs
- GNews文档：https://gnews.io/docs
- 天行数据文档：https://www.tianapi.com/apiview/10
