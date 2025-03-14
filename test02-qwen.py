import requests

def fetch_bilibili_favorites(fid):
    base_url = "https://api.bilibili.com/x/v3/fav/resource/list"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": f"https://space.bilibili.com/432142408/favlist?fid={fid}&ftype=create&ctype=21"
    }
    params = {
        "media_id": fid,
        "pn": 1,
        "ps": 20,
        "keyword": "",
        "order": "mtime",
        "type": 0,
        "tid": 0,
        "platform": "web",
        "jsonp": "jsonp"
    }

    all_videos = []
    page_number = 1

    while True:
        params["pn"] = page_number
        response = requests.get(base_url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Failed to retrieve data: {response.status_code}")
            print(response.text)
            break
        
        try:
            data = response.json()
        except ValueError as e:
            print("Response content is not valid JSON")
            print(response.text)
            break
        
        if 'code' in data and data['code'] != 0:
            print(f"Error from Bilibili API: {data['message']}")
            break
        
        if 'data' in data and 'medias' in data['data']:
            medias = data['data']['medias']
            if medias is None:
                print("No more media items found.")
                break
            
            for video in medias:
                title = video['title']
                up_name = video['upper']['name']
                all_videos.append((title, up_name))
        else:
            print("Unexpected data structure:", data)
            break

        page_number += 1

    return all_videos

if __name__ == "__main__":
    fid = 464620808
    videos = fetch_bilibili_favorites(fid)

    for i, (title, up_name) in enumerate(videos, start=1):
        print(f"{i}. 视频标题: {title}, UP主: {up_name}")



