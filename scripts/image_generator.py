#!/usr/bin/env python3
"""
小红书风格图片生成模块
生成适合小红书分享的科技新闻图片
"""

from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
from typing import List, Dict
import textwrap

class XiaohongshuImageGenerator:
    def __init__(self):
        self.width = 1080
        self.height = 1920
        self.output_dir = "/mnt/okcomputer/output/tech-news-automation/output"
        
        # 小红书风格配色
        self.colors = {
            'bg_gradient_start': (255, 245, 250),  # 淡粉色
            'bg_gradient_end': (240, 248, 255),    # 淡蓝色
            'primary': (255, 107, 107),            # 珊瑚红
            'secondary': (78, 205, 196),           # 青绿色
            'accent': (255, 200, 87),              # 金黄色
            'text_dark': (45, 52, 70),             # 深灰蓝
            'text_light': (120, 120, 120),         # 浅灰
            'white': (255, 255, 255),
            'category_colors': {
                '人工智能': (147, 112, 219),      # 紫色
                '硬件设备': (255, 140, 66),       # 橙色
                '自动驾驶': (50, 205, 50),        # 绿色
                '芯片': (30, 144, 255),           # 蓝色
                '元宇宙': (255, 105, 180),        # 粉红
                '航天': (70, 130, 180),           # 钢蓝
            }
        }
        
    def create_gradient_background(self) -> Image:
        """创建渐变背景"""
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        
        for y in range(self.height):
            r = int(self.colors['bg_gradient_start'][0] + 
                   (self.colors['bg_gradient_end'][0] - self.colors['bg_gradient_start'][0]) * y / self.height)
            g = int(self.colors['bg_gradient_start'][1] + 
                   (self.colors['bg_gradient_end'][1] - self.colors['bg_gradient_start'][1]) * y / self.height)
            b = int(self.colors['bg_gradient_start'][2] + 
                   (self.colors['bg_gradient_end'][2] - self.colors['bg_gradient_start'][2]) * y / self.height)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        
        return img
    
    def draw_rounded_rectangle(self, draw, xy, radius, fill, outline=None):
        """绘制圆角矩形"""
        x1, y1, x2, y2 = xy
        
        # 绘制主体矩形
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
        
        # 绘制四个圆角
        draw.ellipse([x1, y1, x1 + radius * 2, y1 + radius * 2], fill=fill)
        draw.ellipse([x2 - radius * 2, y1, x2, y1 + radius * 2], fill=fill)
        draw.ellipse([x1, y2 - radius * 2, x1 + radius * 2, y2], fill=fill)
        draw.ellipse([x2 - radius * 2, y2 - radius * 2, x2, y2], fill=fill)
    
    def get_font(self, size: int, bold: bool = False):
        """获取字体"""
        try:
            # 使用系统Noto字体
            if bold:
                return ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", size)
            return ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", size)
        except:
            try:
                return ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc", size)
            except:
                return ImageFont.load_default()
    
    def replace_emoji_with_text(self, text: str) -> str:
        """将emoji替换为文字符号"""
        emoji_map = {
            '🚀': '▶',
            '📋': '◆',
            '💡': '★',
            '🤖': 'AI',
            '🚗': '●',
            '💻': '■',
            '🥽': '◎',
            '🔥': 'HOT',
            '📰': '•',
            '👇': '↓',
            '📌': '#',
            '💬': '"',
            '📅': '●',
            '🎙️': '▶',
            '🎉': '★',
            '💖': '♥',
            '🙏': '✓',
            '🌟': '★',
            '📈': '↑',
            '📊': '◆',
            '🎯': '◎',
            '⚠️': '!',
            '✅': '√',
            '❌': '×',
            '⏰': 'T',
            '📱': '■',
            '📚': '≡',
            '🏝️': '○',
            '🎧': '♪',
            '📷': '○',
            '🎬': '▶',
            '📎': '∞',
            '🔗': '~',
            '🏷️': '#',
            '📍': '●',
            '✨': '*',
            '📮': '@',
            '📨': '→',
        }
        for emoji, replacement in emoji_map.items():
            text = text.replace(emoji, replacement)
        return text
    
    def generate_cover_image(self, news_list: List[Dict]) -> str:
        """生成封面图片"""
        img = self.create_gradient_background()
        draw = ImageDraw.Draw(img)
        
        # 标题区域
        title_y = 80
        
        # 绘制装饰元素
        self.draw_rounded_rectangle(draw, [60, title_y, 1020, title_y + 200], 30, self.colors['white'])
        
        # 主标题
        title_font = self.get_font(72, bold=True)
        title_text = self.replace_emoji_with_text("🚀 全球科技早报")
        draw.text((self.width//2, title_y + 60), title_text, 
                 fill=self.colors['text_dark'], font=title_font, anchor="mm")
        
        # 日期
        date_font = self.get_font(40)
        today = datetime.now().strftime("%Y年%m月%d日")
        draw.text((self.width//2, title_y + 140), today, 
                 fill=self.colors['text_light'], font=date_font, anchor="mm")
        
        # 热门新闻卡片
        card_y = title_y + 280
        card_margin = 40
        card_width = (self.width - card_margin * 3) // 2
        
        for i, news in enumerate(news_list[:4]):
            row = i // 2
            col = i % 2
            x = card_margin + col * (card_width + card_margin)
            y = card_y + row * 320
            
            # 卡片背景
            self.draw_rounded_rectangle(draw, [x, y, x + card_width, y + 280], 20, self.colors['white'])
            
            # 类别标签
            cat = news.get('category', '科技')
            cat_color = self.colors['category_colors'].get(cat, self.colors['primary'])
            self.draw_rounded_rectangle(draw, [x + 20, y + 20, x + 120, y + 55], 15, cat_color)
            
            cat_font = self.get_font(22)
            draw.text((x + 70, y + 37), cat, fill=self.colors['white'], font=cat_font, anchor="mm")
            
            # 热度标识
            hot_font = self.get_font(20)
            draw.text((x + card_width - 20, y + 37), f"🔥{news['hot_score']}", 
                     fill=self.colors['primary'], font=hot_font, anchor="rm")
            
            # 标题
            title_font = self.get_font(28, bold=True)
            title_text = news['title'][:18] + "..." if len(news['title']) > 18 else news['title']
            draw.text((x + 20, y + 80), title_text, fill=self.colors['text_dark'], font=title_font)
            
            # 摘要
            summary_font = self.get_font(22)
            summary = news['summary'][:35] + "..."
            draw.text((x + 20, y + 130), summary, fill=self.colors['text_light'], font=summary_font)
            
            # 来源
            source_font = self.get_font(20)
            draw.text((x + 20, y + 240), f"📰 {news['source']}", 
                     fill=self.colors['text_light'], font=source_font)
        
        # 底部提示
        bottom_y = self.height - 120
        tip_font = self.get_font(28)
        tip_text = self.replace_emoji_with_text("👇 滑动查看更多科技资讯")
        draw.text((self.width//2, bottom_y), tip_text, 
                 fill=self.colors['text_light'], font=tip_font, anchor="mm")
        
        # 保存图片
        output_path = os.path.join(self.output_dir, "tech_news_cover.jpg")
        img.save(output_path, "JPEG", quality=95)
        return output_path
    
    def generate_detail_image(self, news_list: List[Dict]) -> str:
        """生成详情图片"""
        img = self.create_gradient_background()
        draw = ImageDraw.Draw(img)
        
        # 标题
        title_y = 60
        title_font = self.get_font(56, bold=True)
        title_text = self.replace_emoji_with_text("📋 今日科技详情")
        draw.text((self.width//2, title_y), title_text, 
                 fill=self.colors['text_dark'], font=title_font, anchor="mm")
        
        # 新闻列表
        y_offset = 140
        item_height = 200
        margin = 40
        
        for i, news in enumerate(news_list[:6]):
            # 序号圆圈
            num_color = self.colors['primary'] if i < 3 else self.colors['secondary']
            draw.ellipse([margin, y_offset, margin + 50, y_offset + 50], fill=num_color)
            
            num_font = self.get_font(28, bold=True)
            draw.text((margin + 25, y_offset + 25), str(i + 1), 
                     fill=self.colors['white'], font=num_font, anchor="mm")
            
            # 内容卡片
            card_x = margin + 70
            card_width = self.width - card_x - margin
            self.draw_rounded_rectangle(draw, 
                [card_x, y_offset, card_x + card_width, y_offset + item_height], 
                15, self.colors['white'])
            
            # 类别标签
            cat = news.get('category', '科技')
            cat_color = self.colors['category_colors'].get(cat, self.colors['primary'])
            self.draw_rounded_rectangle(draw, 
                [card_x + 15, y_offset + 15, card_x + 100, y_offset + 45], 
                12, cat_color)
            
            cat_font = self.get_font(20)
            draw.text((card_x + 57, y_offset + 30), cat, 
                     fill=self.colors['white'], font=cat_font, anchor="mm")
            
            # 热度
            hot_font = self.get_font(20)
            hot_text = self.replace_emoji_with_text(f"🔥 {news['hot_score']}")
            draw.text((card_x + card_width - 15, y_offset + 30), 
                     hot_text, 
                     fill=self.colors['primary'], font=hot_font, anchor="rm")
            
            # 标题
            title_font = self.get_font(30, bold=True)
            draw.text((card_x + 15, y_offset + 65), news['title'], 
                     fill=self.colors['text_dark'], font=title_font)
            
            # 摘要（多行）
            summary_font = self.get_font(24)
            summary_lines = textwrap.wrap(news['summary'], width=32)
            for j, line in enumerate(summary_lines[:2]):
                draw.text((card_x + 15, y_offset + 110 + j * 35), line, 
                         fill=self.colors['text_light'], font=summary_font)
            
            # 来源
            source_font = self.get_font(20)
            source_text = self.replace_emoji_with_text(f"📰 {news['source']}")
            draw.text((card_x + 15, y_offset + item_height - 30), 
                     source_text, 
                     fill=self.colors['text_light'], font=source_font)
            
            y_offset += item_height + 20
        
        # 保存图片
        output_path = os.path.join(self.output_dir, "tech_news_detail.jpg")
        img.save(output_path, "JPEG", quality=95)
        return output_path
    
    def generate_summary_image(self) -> str:
        """生成总结图片"""
        img = self.create_gradient_background()
        draw = ImageDraw.Draw(img)
        
        # 标题
        title_y = 100
        title_font = self.get_font(64, bold=True)
        title_text = self.replace_emoji_with_text("💡 科技趋势洞察")
        draw.text((self.width//2, title_y), title_text, 
                 fill=self.colors['text_dark'], font=title_font, anchor="mm")
        
        # 主要内容区域
        content_y = 250
        
        # 绘制趋势卡片
        trends = [
            (self.replace_emoji_with_text("🤖 AI革命"), "大模型能力持续突破，多模态成为标配", self.colors['category_colors']['人工智能']),
            (self.replace_emoji_with_text("🚗 智能驾驶"), "自动驾驶技术加速落地，L4级即将商用", self.colors['category_colors']['自动驾驶']),
            (self.replace_emoji_with_text("💻 芯片战争"), "AI芯片算力竞赛白热化，3nm成主流", self.colors['category_colors']['芯片']),
            (self.replace_emoji_with_text("🥽 AR/VR"), "空间计算时代来临，头显设备轻量化", self.colors['category_colors']['硬件设备']),
        ]
        
        card_height = 180
        card_margin = 50
        
        for i, (title, desc, color) in enumerate(trends):
            y = content_y + i * (card_height + card_margin)
            
            # 卡片背景
            self.draw_rounded_rectangle(draw, 
                [80, y, self.width - 80, y + card_height], 
                25, self.colors['white'])
            
            # 左侧色条
            draw.rectangle([80, y, 100, y + card_height], fill=color)
            
            # 标题
            trend_title_font = self.get_font(40, bold=True)
            draw.text((130, y + 40), title, fill=self.colors['text_dark'], font=trend_title_font)
            
            # 描述
            trend_desc_font = self.get_font(28)
            draw.text((130, y + 100), desc, fill=self.colors['text_light'], font=trend_desc_font)
        
        # 底部语录
        quote_y = self.height - 200
        self.draw_rounded_rectangle(draw, [80, quote_y, self.width - 80, quote_y + 150], 20, 
                                   (255, 250, 240))
        
        quote_font = self.get_font(32)
        draw.text((self.width//2, quote_y + 40), 
                 "\"科技改变世界，创新引领未来\"", 
                 fill=self.colors['text_dark'], font=quote_font, anchor="mm")
        
        sub_font = self.get_font(24)
        sub_text = self.replace_emoji_with_text("每天3分钟，掌握全球科技动态 🚀")
        draw.text((self.width//2, quote_y + 100), 
                 sub_text, 
                 fill=self.colors['text_light'], font=sub_font, anchor="mm")
        
        # 保存图片
        output_path = os.path.join(self.output_dir, "tech_news_summary.jpg")
        img.save(output_path, "JPEG", quality=95)
        return output_path
    
    def generate_all_images(self, news_list: List[Dict]) -> List[str]:
        """生成所有图片"""
        images = []
        
        # 生成封面
        cover_path = self.generate_cover_image(news_list)
        images.append(cover_path)
        print(f"✅ 封面图片已生成: {cover_path}")
        
        # 生成详情页
        detail_path = self.generate_detail_image(news_list)
        images.append(detail_path)
        print(f"✅ 详情图片已生成: {detail_path}")
        
        # 生成总结页
        summary_path = self.generate_summary_image()
        images.append(summary_path)
        print(f"✅ 总结图片已生成: {summary_path}")
        
        return images

if __name__ == "__main__":
    # 测试
    from news_fetcher import TechNewsFetcher
    
    fetcher = TechNewsFetcher()
    news = fetcher.fetch_news()
    
    generator = XiaohongshuImageGenerator()
    images = generator.generate_all_images(news)
    
    print(f"\n🎉 共生成 {len(images)} 张图片")
