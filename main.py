#!/usr/bin/env python3
"""
全球高科技新闻自动化系统 - 主调度脚本
每天早上8:30自动获取科技新闻，生成小红书风格图片，发送到Get笔记
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from news_fetcher import TechNewsFetcher
from image_generator import XiaohongshuImageGenerator
from getnote_sender import send_daily_tech_news

class TechNewsAutomation:
    def __init__(self):
        self.output_dir = "/mnt/okcomputer/output/tech-news-automation/output"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 初始化模块
        self.news_fetcher = TechNewsFetcher()
        self.image_generator = XiaohongshuImageGenerator()
        
    def run(self, skip_send: bool = False) -> dict:
        """
        运行完整的自动化流程
        
        Args:
            skip_send: 是否跳过发送到Get笔记（用于测试）
            
        Returns:
            运行结果报告
        """
        print("=" * 60)
        print("🚀 全球科技新闻自动化系统")
        print(f"⏰ 运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print()
        
        result = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'steps': {}
        }
        
        # 步骤1: 获取新闻
        print("📰 步骤1: 获取高科技新闻...")
        try:
            news = self.news_fetcher.fetch_news(num_results=10)
            result['steps']['fetch_news'] = {
                'success': True,
                'count': len(news)
            }
            print(f"✅ 成功获取 {len(news)} 条新闻")
            
            # 打印新闻摘要
            for i, item in enumerate(news[:5], 1):
                print(f"   {i}. [{item['category']}] {item['title'][:40]}...")
        except Exception as e:
            result['steps']['fetch_news'] = {
                'success': False,
                'error': str(e)
            }
            print(f"❌ 获取新闻失败: {e}")
            return result
        
        print()
        
        # 步骤2: 生成小红书风格图片
        print("🎨 步骤2: 生成小红书风格图片...")
        try:
            images = self.image_generator.generate_all_images(news)
            result['steps']['generate_images'] = {
                'success': True,
                'images': images
            }
            print(f"✅ 成功生成 {len(images)} 张图片")
        except Exception as e:
            result['steps']['generate_images'] = {
                'success': False,
                'error': str(e)
            }
            print(f"❌ 生成图片失败: {e}")
            return result
        
        print()
        
        # 步骤3: 发送到Get笔记
        if not skip_send:
            print("📤 步骤3: 发送到Get笔记...")
            try:
                api_key = os.getenv('GETNOTE_API_KEY', '')
                send_result = send_daily_tech_news(news, images, api_key)
                result['steps']['send_to_getnote'] = send_result
                
                if send_result['success']:
                    print(f"✅ 发送成功")
                    if 'message' in send_result:
                        print(f"   {send_result['message']}")
                else:
                    print(f"⚠️ 发送未完成: {send_result.get('message', '')}")
            except Exception as e:
                result['steps']['send_to_getnote'] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"⚠️ 发送过程出现问题: {e}")
        else:
            print("📤 步骤3: 跳过发送（测试模式）")
            result['steps']['send_to_getnote'] = {
                'success': True,
                'skipped': True
            }
        
        print()
        print("=" * 60)
        print("✨ 自动化流程完成!")
        print("=" * 60)
        
        # 保存运行报告
        report_path = os.path.join(self.output_dir, 
                                   f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"📊 运行报告已保存: {report_path}")
        
        return result

def setup_cron_job():
    """设置定时任务（每天早上8:30运行）"""
    import subprocess
    
    # 获取当前脚本的绝对路径
    script_path = os.path.abspath(__file__)
    python_path = sys.executable
    
    # 创建cron任务
    cron_line = f"30 8 * * * cd {os.path.dirname(script_path)} && {python_path} {script_path} --send >> /var/log/tech-news.log 2>&1"
    
    print("📅 定时任务设置指南:")
    print("=" * 60)
    print("方法1: 使用crontab（Linux/Mac）")
    print(f"  1. 运行: crontab -e")
    print(f"  2. 添加以下行:")
    print(f"     {cron_line}")
    print()
    print("方法2: 使用systemd timer（Linux）")
    print("  1. 创建服务文件: /etc/systemd/system/tech-news.service")
    print("  2. 创建定时器: /etc/systemd/system/tech-news.timer")
    print("  3. 启用定时器: systemctl enable tech-news.timer")
    print()
    print("方法3: 使用Windows任务计划程序")
    print("  1. 打开任务计划程序")
    print("  2. 创建基本任务")
    print(f"  3. 设置程序: {python_path}")
    print(f"  4. 设置参数: {script_path} --send")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description='全球科技新闻自动化系统')
    parser.add_argument('--send', action='store_true', 
                       help='发送到Get笔记（默认只生成不发送）')
    parser.add_argument('--setup-cron', action='store_true',
                       help='显示定时任务设置指南')
    parser.add_argument('--test', action='store_true',
                       help='测试模式（不发送）')
    
    args = parser.parse_args()
    
    if args.setup_cron:
        setup_cron_job()
        return
    
    # 运行自动化流程
    automation = TechNewsAutomation()
    skip_send = not args.send or args.test
    
    result = automation.run(skip_send=skip_send)
    
    # 返回退出码
    sys.exit(0 if result['success'] else 1)

if __name__ == "__main__":
    main()
