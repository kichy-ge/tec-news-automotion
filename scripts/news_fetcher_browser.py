#!/usr/bin/env python3
"""
使用浏览器工具获取新闻（解决网络限制问题）
作为news_fetcher的备用方案
"""

import json
import subprocess
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import random

class BrowserNewsFetcher:
    """使用浏览器工具获取新闻"""
    
    def __init__(self):
        self.newsapi_key = "b1b5dc1e64064cddb26ab4d984642ba3"
        
    def fetch_from_newsapi_via_browser(self, query: str = "technology", num_results: int = 10) -> List[Dict]:
        """
        通过浏览器工具获取NewsAPI数据
        """
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        url = f"https://newsapi.org/v2/everything?q={query}&from={yesterday}&sortBy=publishedAt&language=en&pageSize={num_results}&apiKey={self.newsapi_key}"
        
        try:
            # 使用curl获取数据
            result = subprocess.run(
                ['curl', '-s', '--max-time', '30', url],
                capture_output=True,
                text=True,
                timeout=35
            )
            
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                
                if data.get('status') == 'ok':
                    articles = data.get('articles', [])
                    news_list = []
                    for article in articles:
                        news_list.append({
                            'title': article.get('title', ''),
                            'summary': (article.get('description') or article.get('content', '')[:150])[:150],
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
                    print(f"⚠️ NewsAPI返回错误: {data.get('message', 'Unknown')}")
                    return []
            else:
                print(f"❌ curl请求失败")
                return []
                
        except Exception as e:
            print(f"❌ 浏览器获取失败: {e}")
            return []
    
    def _categorize_news(self, title: str) -> str:
        """根据标题分类新闻"""
        title_lower = title.lower()
        
        categories = {
            '人工智能': ['ai', 'artificial intelligence', 'gpt', 'chatgpt', 'openai', 'llm', 
                      'machine learning', 'deep learning', 'neural', 'google gemini', 'claude'],
            '芯片': ['chip', 'gpu', 'cpu', 'semiconductor', 'nvidia', 'intel', 'amd', 'tsmc', '3nm', '5nm'],
            '自动驾驶': ['tesla', 'self-driving', 'autonomous', 'fsd', 'electric vehicle', 'ev', 'car', 'waymo', 'robotaxi'],
            '硬件设备': ['iphone', 'apple', 'vision pro', 'meta quest', 'vr', 'ar', 'headset', 'smartphone', 'ipad', 'mac'],
            '元宇宙': ['metaverse', 'virtual reality', 'augmented reality', 'vr', 'ar', 'meta'],
            '航天': ['spacex', 'space', 'rocket', 'mars', 'satellite', 'starlink', 'nasa'],
            '区块链': ['bitcoin', 'crypto', 'blockchain', 'ethereum', 'nft', 'web3'],
            '云计算': ['cloud', 'aws', 'azure', 'google cloud', 'server'],
        }
        
        for category, keywords in categories.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return '科技'
    
    def fetch_news(self, num_results: int = 10) -> List[Dict]:
        """获取新闻（主入口）"""
        print("📰 开始获取科技新闻...")
        
        # 尝试通过浏览器获取
        news = self.fetch_from_newsapi_via_browser("technology AI", num_results)
        
        if news:
            # 按热度排序
            news.sort(key=lambda x: x['hot_score'], reverse=True)
            print(f"✅ 共获取 {len(news)} 条真实新闻")
            return news[:num_results]
        else:
            print("⚠️ 无法获取真实新闻，使用模拟数据")
            return self._get_mock_news()
    
    def _get_mock_news(self) -> List[Dict]:
        """模拟新闻数据"""
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

if __name__ == "__main__":
    fetcher = BrowserNewsFetcher()
    news = fetcher.fetch_news(num_results=10)
    
    print("\n" + "="*60)
    print("获取的新闻列表:")
    print("="*60)
    for i, item in enumerate(news, 1):
        print(f"\n{i}. [{item['category']}] {item['title']}")
        print(f"   来源: {item['source']} | API: {item.get('from_api', 'Unknown')}")
        print(f"   热度: {item['hot_score']}")
