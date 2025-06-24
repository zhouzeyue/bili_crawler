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

def parse_bilibili_favorites(json_data):
    videos = []
    if not json_data['data']['medias']:
        return None
    
    for item in json_data['data']['medias']:
        video = {
            'title': item['title'],
            'up_name': item['upper']['name'],
            'bvid': item['bvid']
        }
        videos.append(video)
    return videos

def save_to_csv(data, filename='bilibili_favorites.csv'):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f'数据已保存到 {filename}')

def main():
    # 从URL中提取media_id (收藏夹ID)
    media_id = '464620808'  # 从您的URL中提取的收藏夹ID
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
        time.sleep(0.15)  # 添加延迟，避免请求过快
    
    print(f'共爬取到 {len(all_videos)} 个视频')
    save_to_csv(all_videos)

if __name__ == '__main__':
    main()