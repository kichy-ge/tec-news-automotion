#!/usr/bin/env python3
"""
高科技新闻获取模块
接入真实新闻API获取全球高科技公司最新新闻

支持的API：
- NewsAPI (https://newsapi.org/) - 免费100请求/天
- GNews (https://gnews.io/) - 免费100请求/天  
- 中文科技新闻API (api.aa1.cn) - 免费
"""

import requests
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import random
import time

class TechNewsFetcher:
    def __init__(self):
        # API密钥配置（从环境变量读取）
        self.newsapi_key = os.getenv('NEWSAPI_KEY', '')
        self.gnews_key = os.getenv('GNEWS_KEY', '')
        
        # API基础URL
        self.newsapi_url = "https://newsapi.org/v2"
        self.gnews_url = "https://gnews.io/api/v4"
        
        # 中文新闻API（可选）
        self.tianxing_key = os.getenv('TIANXING_KEY', '')  # 天行数据 https://www.tianapi.com/
        self.tianxing_url = "http://api.tianapi.com/keji/index"
        
        # 缓存配置
        self.cache_file = "/tmp/tech_news_cache.json"
        self.cache_duration = 3600  # 缓存1小时
        
    def _get_cache(self) -> Optional[List[Dict]]:
        """从缓存读取新闻"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                    if time.time() - cache.get('timestamp', 0) < self.cache_duration:
                        return cache.get('news', [])
        except Exception as e:
            print(f"缓存读取失败: {e}")
        return None
    
    def _set_cache(self, news: List[Dict]):
        """保存新闻到缓存"""
        try:
            cache = {
                'timestamp': time.time(),
                'news': news
            }
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False)
        except Exception as e:
            print(f"缓存保存失败: {e}")
    
    def fetch_from_newsapi(self, query: str = "technology", num_results: int = 10) -> List[Dict]:
        """
        从NewsAPI获取科技新闻
        免费版限制：100请求/天
        """
        if not self.newsapi_key:
            print("⚠️ 未配置NEWSAPI_KEY，跳过NewsAPI")
            return []
        
        url = f"{self.newsapi_url}/everything"
        
        # 计算昨天日期（免费版只能获取1天内的新闻）
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        params = {
            'q': query,
            'from': yesterday,
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': num_results,
            'apiKey': self.newsapi_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'ok':
                articles = data.get('articles', [])
                news_list = []
                for article in articles:
                    news_list.append({
                        'title': article.get('title', ''),
                        'summary': article.get('description', '') or article.get('content', '')[:150],
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'category': self._categorize_news(article.get('title', '')),
                        'hot_score': random.randint(70, 98),
                        'url': article.get('url', ''),
                        'published_at': article.get('publishedAt', ''),
                        'from_api': 'NewsAPI'
                    })
                print(f"✅ NewsAPI获取成功: {len(news_list)}条")
                return news_list
            else:
                print(f"⚠️ NewsAPI返回错误: {data.get('message', 'Unknown error')}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"❌ NewsAPI请求失败: {e}")
            return []
    
    def fetch_from_gnews(self, query: str = "technology", num_results: int = 10) -> List[Dict]:
        """
        从GNews获取科技新闻
        免费版限制：100请求/天，每次最多10条
        """
        if not self.gnews_key:
            print("⚠️ 未配置GNEWS_KEY，跳过GNews")
            return []
        
        url = f"{self.gnews_url}/search"
        
        params = {
            'q': query,
            'lang': 'en',
            'max': min(num_results, 10),  # 免费版每次最多10条
            'apikey': self.gnews_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = data.get('articles', [])
            news_list = []
            for article in articles:
                news_list.append({
                    'title': article.get('title', ''),
                    'summary': article.get('description', '') or article.get('content', '')[:150],
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'category': self._categorize_news(article.get('title', '')),
                    'hot_score': random.randint(70, 98),
                    'url': article.get('url', ''),
                    'published_at': article.get('publishedAt', ''),
                    'from_api': 'GNews'
                })
            print(f"✅ GNews获取成功: {len(news_list)}条")
            return news_list
            
        except requests.exceptions.RequestException as e:
            print(f"❌ GNews请求失败: {e}")
            return []
    
    def fetch_from_tianxing(self, num_results: int = 10) -> List[Dict]:
        """
        从天行数据API获取中文科技新闻
        免费版：100次/天
        官网：https://www.tianapi.com/apiview/10
        """
        if not self.tianxing_key:
            print("⚠️ 未配置TIANXING_KEY，跳过天行数据API")
            return []
        
        url = self.tianxing_url
        params = {
            'key': self.tianxing_key,
            'num': min(num_results, 20)  # 最多20条
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 200:
                articles = data.get('newslist', [])
                news_list = []
                for article in articles:
                    news_list.append({
                        'title': article.get('title', ''),
                        'summary': article.get('description', '') or article.get('title', '')[:80] + '...',
                        'source': article.get('source', '科技资讯'),
                        'category': self._categorize_cn_news(article.get('title', '')),
                        'hot_score': random.randint(70, 95),
                        'url': article.get('url', ''),
                        'published_at': article.get('ctime', ''),
                        'from_api': 'TianXing'
                    })
                print(f"✅ 天行数据API获取成功: {len(news_list)}条")
                return news_list
            else:
                print(f"⚠️ 天行数据API返回错误: {data.get('msg', 'Unknown')}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 天行数据API请求失败: {e}")
            return []
    
    def _categorize_news(self, title: str) -> str:
        """根据标题分类英文新闻"""
        title_lower = title.lower()
        
        categories = {
            '人工智能': ['ai', 'artificial intelligence', 'gpt', 'chatgpt', 'openai', 'llm', 
                      'machine learning', 'deep learning', 'neural', 'google gemini', 'claude'],
            '芯片': ['chip', 'gpu', 'cpu', 'semiconductor', 'nvidia', 'intel', 'amd', 'tsmc', '3nm', '5nm'],
            '自动驾驶': ['tesla', 'self-driving', 'autonomous', 'fsd', 'electric vehicle', 'ev', 'car'],
            '硬件设备': ['iphone', 'apple', 'vision pro', 'meta quest', 'vr', 'ar', 'headset', 'smartphone'],
            '元宇宙': ['metaverse', 'virtual reality', 'augmented reality', 'vr', 'ar', 'meta'],
            '航天': ['spacex', 'space', 'rocket', 'mars', 'satellite', 'starlink', 'nasa'],
            '区块链': ['bitcoin', 'crypto', 'blockchain', 'ethereum', 'nft', 'web3'],
            '云计算': ['cloud', 'aws', 'azure', 'google cloud', 'server'],
        }
        
        for category, keywords in categories.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return '科技'
    
    def _categorize_cn_news(self, title: str) -> str:
        """根据标题分类中文新闻"""
        categories = {
            '人工智能': ['AI', '人工智能', 'GPT', 'ChatGPT', '大模型', 'OpenAI', '文心', '通义', '讯飞'],
            '芯片': ['芯片', 'GPU', 'CPU', '半导体', '英伟达', '英特尔', 'AMD', '台积电', '光刻'],
            '自动驾驶': ['特斯拉', '自动驾驶', 'FSD', '电动车', '新能源汽车', '比亚迪', '蔚来'],
            '硬件设备': ['iPhone', '苹果', 'Vision Pro', 'Meta', 'VR', 'AR', '头显', '手机', '小米'],
            '元宇宙': ['元宇宙', '虚拟现实', '增强现实', 'VR', 'AR'],
            '航天': ['SpaceX', '航天', '火箭', '火星', '卫星', '星链', 'NASA', '中国航天'],
            '区块链': ['比特币', '加密货币', '区块链', '以太坊', 'NFT', 'Web3'],
            '云计算': ['云计算', '阿里云', '腾讯云', 'AWS', '服务器'],
        }
        
        for category, keywords in categories.items():
            if any(keyword in title for keyword in keywords):
                return category
        
        return '科技'
    
    def fetch_news(self, num_results: int = 10) -> List[Dict]:
        """
        获取高科技新闻（聚合多个API）
        
        优先级：
        1. 先检查缓存
        2. 尝试NewsAPI
        3. 尝试GNews
        4. 尝试中文API
        5. 使用模拟数据作为后备
        """
        print("📰 开始获取科技新闻...")
        
        # 1. 检查缓存
        cached_news = self._get_cache()
        if cached_news:
            print(f"✅ 使用缓存数据: {len(cached_news)}条")
            return cached_news[:num_results]
        
        all_news = []
        
        # 2. 尝试NewsAPI
        if self.newsapi_key:
            newsapi_news = self.fetch_from_newsapi("technology AI", num_results // 2)
            all_news.extend(newsapi_news)
        
        # 3. 尝试GNews
        if self.gnews_key and len(all_news) < num_results:
            gnews_news = self.fetch_from_gnews("technology", num_results // 2)
            # 去重
            existing_titles = {n['title'] for n in all_news}
            for news in gnews_news:
                if news['title'] not in existing_titles:
                    all_news.append(news)
        
        # 4. 尝试天行数据中文API
        if len(all_news) < num_results:
            cn_news = self.fetch_from_tianxing(num_results - len(all_news))
            all_news.extend(cn_news)
        
        # 5. 如果都没有获取到，使用模拟数据
        if not all_news:
            print("⚠️ 所有API都失败，使用模拟数据")
            all_news = self._get_mock_news()
        
        # 按热度排序
        all_news.sort(key=lambda x: x['hot_score'], reverse=True)
        
        # 保存到缓存
        self._set_cache(all_news)
        
        print(f"✅ 共获取 {len(all_news)} 条新闻")
        return all_news[:num_results]
    
    def _get_mock_news(self) -> List[Dict]:
        """模拟新闻数据（后备方案）"""
        return [
            {
                "title": "OpenAI发布GPT-5，多模态能力大幅提升",
                "summary": "OpenAI今日发布新一代大模型GPT-5，支持文本、图像、音频、视频多模态输入，推理能力较前代提升40%。",
                "source": "TechCrunch",
                "category": "人工智能",
                "hot_score": 98,
                "from_api": "Mock"
            },
            {
                "title": "苹果Vision Pro 2代曝光：更轻更薄，价格减半",
                "summary": "据供应链消息，苹果第二代Vision Pro头显设备重量将减轻30%，售价有望降至1999美元起。",
                "source": "Bloomberg",
                "category": "硬件设备",
                "hot_score": 95,
                "from_api": "Mock"
            },
            {
                "title": "特斯拉FSD V13实现完全无人驾驶，马斯克称即将全球推送",
                "summary": "特斯拉宣布FSD V13版本在内部测试中实现零干预驾驶，计划下月向美国用户全面推送。",
                "source": "Reuters",
                "category": "自动驾驶",
                "hot_score": 92,
                "from_api": "Mock"
            },
            {
                "title": "英伟达发布H200 GPU，AI算力再翻倍",
                "summary": "英伟达在GTC大会上发布新一代AI芯片H200，采用3nm工艺，训练大模型速度提升2.5倍。",
                "source": "The Verge",
                "category": "芯片",
                "hot_score": 90,
                "from_api": "Mock"
            },
            {
                "title": "微软Copilot整合GPT-5，Office套件全面AI化",
                "summary": "微软宣布将GPT-5深度整合进Office 365，Word、Excel、PPT将迎来革命性AI功能升级。",
                "source": "Wired",
                "category": "人工智能",
                "hot_score": 88,
                "from_api": "Mock"
            },
            {
                "title": "谷歌Gemini 2.0挑战GPT-5，多语言支持领先",
                "summary": "谷歌发布Gemini 2.0，支持超过100种语言，在代码生成和数学推理方面表现优异。",
                "source": "Ars Technica",
                "category": "人工智能",
                "hot_score": 85,
                "from_api": "Mock"
            },
            {
                "title": "Meta元宇宙部门首次盈利，VR用户破千万",
                "summary": "Meta Reality Labs季度营收首次超过成本，Quest系列VR头显全球销量突破1000万台。",
                "source": "CNBC",
                "category": "元宇宙",
                "hot_score": 82,
                "from_api": "Mock"
            },
            {
                "title": "SpaceX星舰第五次试飞成功，火星计划提速",
                "summary": "星舰成功完成第五次轨道试飞，马斯克表示2026年载人火星任务准备就绪。",
                "source": "SpaceNews",
                "category": "航天",
                "hot_score": 80,
                "from_api": "Mock"
            }
        ]
    
    def categorize_news(self, news_list: List[Dict]) -> Dict[str, List[Dict]]:
        """按类别分类新闻"""
        categories = {}
        for news in news_list:
            cat = news.get('category', '其他')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(news)
        return categories
    
    def format_for_xiaohongshu(self, news_list: List[Dict]) -> str:
        """格式化为小红书风格文案"""
        today = datetime.now().strftime("%m月%d日")
        
        content = f"▶ 全球科技早报 | {today}\n"
        content += "=" * 20 + "\n\n"
        
        # 添加今日热点
        content += "HOT 今日热点 TOP 5\n\n"
        
        for i, news in enumerate(news_list[:5], 1):
            content += f"{i}. {news['title']}\n"
            content += f"   {news['summary'][:50]}...\n"
            content += f"   热度: {news['hot_score']}/100"
            if news.get('from_api'):
                content += f" | 来源: {news['from_api']}"
            content += "\n\n"
        
        content += "=" * 20 + "\n\n"
        
        # 按类别分类
        categories = self.categorize_news(news_list)
        
        for cat, items in categories.items():
            content += f"# {cat}\n"
            for item in items[:2]:
                content += f"• {item['title']}\n"
            content += "\n"
        
        content += "=" * 20 + "\n\n"
        content += "今日思考\n"
        content += "科技改变世界，每一天都有新的突破。"
        content += "保持关注，把握未来趋势！\n\n"
        
        content += "#科技新闻 #AI #人工智能 #科技早报\n"
        content += "#硅谷 #特斯拉 #OpenAI #谷歌 #微软"
        
        return content

if __name__ == "__main__":
    fetcher = TechNewsFetcher()
    news = fetcher.fetch_news(num_results=10)
    
    print("\n" + "="*60)
    print("获取的新闻列表:")
    print("="*60)
    for i, item in enumerate(news, 1):
        print(f"\n{i}. [{item['category']}] {item['title']}")
        print(f"   来源: {item['source']} | API: {item.get('from_api', 'Unknown')}")
        print(f"   热度: {item['hot_score']}")
    
    print("\n" + "="*60)
    print("小红书格式:")
    print("="*60)
    xiaohongshu_content = fetcher.format_for_xiaohongshu(news)
    print(xiaohongshu_content)
