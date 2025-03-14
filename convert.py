import csv

def extract_titles_from_csv(csv_file_path, txt_file_path):
    # 读取CSV文件并提取标题
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as csv_file:  # 使用 utf-8-sig 来处理 BOM
        reader = csv.DictReader(csv_file)
        # 打印列名以便调试
        print("CSV文件的列名:", reader.fieldnames)
        
        # 将所有列名转换为小写以便比较，同时去除可能的BOM标记
        fieldnames_lower = [f.strip('\ufeff').lower() for f in reader.fieldnames]
        if 'title' in fieldnames_lower:
            title_column = reader.fieldnames[fieldnames_lower.index('title')]
        else:
            raise ValueError(f"CSV文件中没有找到'title'列。可用的列名: {', '.join(reader.fieldnames)}")
            
        titles = [row[title_column] for row in reader]
    
    # 将标题写入TXT文件，每个标题一行
    with open(txt_file_path, mode='w', encoding='utf-8') as txt_file:
        txt_file.write('\n'.join(titles))

if __name__ == "__main__":
    csv_file_path = 'd:\\python\\bili_crawler\\bilibili_favorites39.txt'
    txt_file_path = 'd:\\python\\bili_crawler\\bilibili_titles.txt'
    extract_titles_from_csv(csv_file_path, txt_file_path)
