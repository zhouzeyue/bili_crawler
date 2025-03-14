import requests
from bs4 import BeautifulSoup
import re

# 目标URL
url = "https://space.bilibili.com/432142408/favlist?fid=464620808"

# 发送HTTP请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url, headers=headers)

# 检查请求是否成功
if response.status_code == 200:
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 查找所有视频项
    video_items = soup.find_all('div', class_='bili-video-card')
    
    # 存储结果
    videos = []
    
    for item in video_items:
        # 提取标题
        title_tag = item.find('div', class_='bili-video-card__title')
        title = title_tag.a.text.strip() if title_tag and title_tag.a else 'N/A'
        
        # 提取BV号
        href = title_tag.a['href'] if title_tag and title_tag.a else ''
        bv_number = re.search(r'BV\w+', href).group() if re.search(r'BV\w+', href) else 'N/A'
        
        # 提取UP主名称
        author_tag = item.find('a', class_='bili-video-card__author')
        author = author_tag.find('span', title=True).text.split(' · ')[0] if author_tag and author_tag.find('span', title=True) else 'N/A'
        
        # 存储信息
        videos.append({
            'title': title,
            'bv_number': bv_number,
            'author': author
        })
    
    # 打印结果
    for video in videos:
        print(f"标题: {video['title']}")
        print(f"BV号: {video['bv_number']}")
        print(f"UP主名称: {video['author']}")
        print('-' * 40)
else:
    print(f"请求失败，状态码: {response.status_code}")