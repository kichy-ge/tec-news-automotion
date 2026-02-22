#!/usr/bin/env python3
"""
Get笔记发送模块
将生成的内容发送到Get笔记
"""

import requests
import json
import os
from datetime import datetime
from typing import List, Dict

class GetNoteSender:
    def __init__(self, api_key: str = None):
        """
        初始化Get笔记发送器
        
        Args:
            api_key: Get笔记API密钥，可从 https://www.biji.com/subject 获取
        """
        self.api_key = api_key or os.getenv('GETNOTE_API_KEY', '')
        self.base_url = "https://open-api.biji.com/getnote/openapi"
        self.headers = {
            'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Authorization': f'Bearer {self.api_key}',
            'X-OAuth-Version': '1'
        }
    
    def send_to_knowledge_base(self, topic_id: str, question: str, 
                               deep_seek: bool = True, refs: bool = False) -> Dict:
        """
        向Get笔记知识库发送查询（用于测试API连接）
        
        Args:
            topic_id: 知识库ID
            question: 查询问题
            deep_seek: 是否启用深度思考
            refs: 是否需要引用
            
        Returns:
            API响应结果
        """
        url = f"{self.base_url}/knowledge/search"
        
        payload = {
            "question": question,
            "topic_ids": [topic_id],
            "deep_seek": deep_seek,
            "refs": refs
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            return {
                'success': True,
                'data': response.json()
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_note_via_webhook(self, title: str, content: str, 
                                images: List[str] = None) -> Dict:
        """
        通过Webhook方式创建笔记（需要配置Get笔记的Webhook）
        
        Args:
            title: 笔记标题
            content: 笔记内容
            images: 图片路径列表
            
        Returns:
            发送结果
        """
        # 注意：Get笔记目前主要通过APP和网页端创建笔记
        # 这里提供模拟实现，实际使用时需要配置相应的集成方式
        
        webhook_url = os.getenv('GETNOTE_WEBHOOK_URL', '')
        
        if not webhook_url:
            return {
                'success': False,
                'error': '未配置Get笔记Webhook地址',
                'message': '请先在Get笔记APP中配置Webhook集成'
            }
        
        payload = {
            'title': title,
            'content': content,
            'created_at': datetime.now().isoformat(),
            'source': '科技新闻自动化'
        }
        
        try:
            response = requests.post(webhook_url, json=payload, timeout=30)
            response.raise_for_status()
            return {
                'success': True,
                'message': '笔记已成功发送到Get笔记'
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def save_note_locally(self, title: str, content: str, 
                         images: List[str], output_dir: str = None) -> str:
        """
        将笔记保存到本地，用户可以手动导入Get笔记
        
        Args:
            title: 笔记标题
            content: 笔记内容
            images: 图片路径列表
            output_dir: 输出目录
            
        Returns:
            保存的文件路径
        """
        if output_dir is None:
            output_dir = "/mnt/okcomputer/output/tech-news-automation/output"
        
        # 创建笔记目录
        note_dir = os.path.join(output_dir, datetime.now().strftime("%Y%m%d"))
        os.makedirs(note_dir, exist_ok=True)
        
        # 保存文本内容
        note_path = os.path.join(note_dir, "note.txt")
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(f"标题: {title}\n")
            f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            f.write(content)
        
        # 复制图片
        import shutil
        image_list = []
        for i, img_path in enumerate(images):
            if os.path.exists(img_path):
                ext = os.path.splitext(img_path)[1]
                new_name = f"image_{i+1}{ext}"
                new_path = os.path.join(note_dir, new_name)
                shutil.copy(img_path, new_path)
                image_list.append(new_path)
        
        # 生成导入指南
        guide_path = os.path.join(note_dir, "导入指南.txt")
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write("Get笔记导入指南\n")
            f.write("=" * 50 + "\n\n")
            f.write("1. 打开Get笔记APP或网页版\n")
            f.write("2. 点击新建笔记\n")
            f.write("3. 复制note.txt中的内容\n")
            f.write("4. 添加图片（按顺序选择image_1, image_2, image_3）\n")
            f.write("5. 保存笔记\n\n")
            f.write("图片文件:\n")
            for img in image_list:
                f.write(f"  - {os.path.basename(img)}\n")
        
        return note_dir
    
    def send_note(self, title: str, content: str, images: List[str] = None) -> Dict:
        """
        发送笔记到Get笔记（主入口）
        
        由于Get笔记API目前主要提供知识库查询功能，
        创建笔记需要通过以下方式之一：
        1. 配置Webhook集成
        2. 使用Get笔记APP的分享功能
        3. 保存到本地后手动导入
        
        本方法默认使用本地保存方式，确保内容不会丢失
        """
        
        # 首先尝试Webhook方式
        if os.getenv('GETNOTE_WEBHOOK_URL'):
            result = self.create_note_via_webhook(title, content, images)
            if result['success']:
                return result
        
        # 回退到本地保存方式
        note_dir = self.save_note_locally(title, content, images)
        
        return {
            'success': True,
            'method': 'local_save',
            'message': f'笔记已保存到本地: {note_dir}',
            'note_dir': note_dir,
            'instructions': '请按照导入指南.txt中的步骤手动导入Get笔记'
        }

def send_daily_tech_news(news_list: List[Dict], images: List[str], 
                         api_key: str = None) -> Dict:
    """
    发送每日科技新闻到Get笔记
    
    Args:
        news_list: 新闻列表
        images: 生成的图片路径列表
        api_key: Get笔记API密钥
        
    Returns:
        发送结果
    """
    from news_fetcher import TechNewsFetcher
    
    # 格式化内容
    fetcher = TechNewsFetcher()
    content = fetcher.format_for_xiaohongshu(news_list)
    
    # 生成标题
    today = datetime.now().strftime("%m月%d日")
    title = f"🚀 全球科技早报 | {today}"
    
    # 发送笔记
    sender = GetNoteSender(api_key)
    result = sender.send_note(title, content, images)
    
    return result

if __name__ == "__main__":
    # 测试
    sender = GetNoteSender()
    
    # 测试本地保存功能
    test_title = "测试笔记"
    test_content = "这是测试内容\n第二行内容"
    test_images = []
    
    result = sender.send_note(test_title, test_content, test_images)
    print(json.dumps(result, ensure_ascii=False, indent=2))
