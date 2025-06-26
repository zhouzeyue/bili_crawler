import requests
import pandas as pd
import time

def fetch_bilibili_favorites(media_id, pn=1, ps=20):
    url = f'https://api.bilibili.com/x/v3/fav/resource/list'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://space.bilibili.com'
    }
    params = {
        'media_id': media_id,
        'pn': pn,
        'ps': ps,
        'keyword': '',
        'order': 'mtime',
        'type': 0,
        'tid': 0,
        'platform': 'web'
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# 在parse_bilibili_favorites函数中添加markdown_link列
def parse_bilibili_favorites(json_data):
    videos = []
    if not json_data['data']['medias']:
        return None
    
    for item in json_data['data']['medias']:
        # 生成Markdown格式链接 [标题_UP主](URL)
        markdown_link = f"[{item['title']}_{item['upper']['name']}](https://www.bilibili.com/video/{item['bvid']})"
        
        video = {
            'title': item['title'],
            'up_name': item['upper']['name'],
            'bvid': item['bvid'],
            'markdown_link': markdown_link  # 新增列
        }
        videos.append(video)
    return videos

# 无需修改save_to_csv函数，它会自动处理新增的列

def save_to_csv(data, filename='bilibili_favorites.csv'):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f'数据已保存到 {filename}')

import re  # 添加正则表达式模块用于URL解析

def main():
    # 提示用户输入收藏夹ID或URL
    user_input = input("请输入B站收藏夹ID或收藏夹网址: ").strip()
    
    # 尝试从URL中提取media_id
    if 'http' in user_input:
        # 匹配URL中的fid参数值
        match = re.search(r'(?:fid|media_id)=(\d+)', user_input)
        if match:
            media_id = match.group(1)
        else:
            # 尝试匹配URL末尾的数字ID
            match = re.search(r'/(\d+)/favlist', user_input)
            media_id = match.group(1) if match else None
    else:
        # 直接使用输入的数字作为media_id
        media_id = user_input if user_input.isdigit() else None
    
    # 验证media_id是否有效
    if not media_id or not media_id.isdigit():
        print("错误：无法识别有效的收藏夹ID，请确保输入的是数字ID或正确的收藏夹URL")
        return
    
    print(f"开始爬取收藏夹ID: {media_id}")
    page = 1
    all_videos = []
    
    while True:
        print(f'正在爬取第 {page} 页...')
        json_data = fetch_bilibili_favorites(media_id, page)
        videos = parse_bilibili_favorites(json_data)
        
        if not videos:
            break
            
        all_videos.extend(videos)
        page += 1
        time.sleep(0.15)
    
    print(f'共爬取到 {len(all_videos)} 个视频')
    save_to_csv(all_videos)

if __name__ == '__main__':
    main()