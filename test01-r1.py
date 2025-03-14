import requests
import csv
import time

def get_favlist_items(fid, pn=1):
    api_url = "https://api.bilibili.com/x/v3/fav/resource/list"
    params = {
        "media_id": fid,    # 收藏夹ID
        "pn": pn,          # 页码
        "ps": 20,          # 每页数量
        "keyword": "",
        "order": "mtime",
        "type": "0",
        "tid": "0",
        "platform": "web"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.bilibili.com/"
    }
    
    try:
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def parse_data(json_data):
    items = []
    if json_data and json_data["code"] == 0:
        for item in json_data["data"]["medias"]:
            title = item["title"]
            up_name = item["upper"]["name"]
            items.append((title, up_name))
    return items

def main():
    fid = "464620808"  # 收藏夹ID
    page = 1
    all_items = []
    
    with open("bilibili_fav.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["标题", "UP主"])
        
        while True:
            print(f"正在抓取第 {page} 页...")
            data = get_favlist_items(fid, pn=page)
            if not data:
                break
            
            page_items = parse_data(data)
            if not page_items:
                break
                
            all_items.extend(page_items)
            writer.writerows(page_items)
            
            # 判断是否还有下一页
            if data["data"]["has_more"] != 1:
                break
                
            page += 1
            # time.sleep(1)  # 礼貌性等待
    
    print(f"抓取完成，共获取到 {len(all_items)} 条数据")

if __name__ == "__main__":
    main()