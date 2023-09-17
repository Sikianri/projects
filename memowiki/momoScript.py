import requests
import zipfile
import os
import csv
import shutil
from git import Repo

# 使用token和project_id从paratranz.cn下载翻译文件
def download_translation_file(token, project_id):
    headers = {
        "Authorization": token  # 设置授权头
    }
    url = f"https://paratranz.cn/api/projects/{project_id}/artifacts/download"
    response = requests.get(url, headers=headers, allow_redirects=True)
    if response.status_code == 200:
        with open("translation.zip", "wb") as file:
            file.write(response.content)  # 将响应内容写入文件
        return "translation.zip"
    else:
        print(f"Error: {response.status_code}")
        return None

# 解压文件功能
def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)  # 解压所有文件到指定目录

# 清理标题中的无效字符
def clean_title(title):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '[', ']', '(', ')', '#']
    for char in invalid_chars:
        title = title.replace(char, '')  # 替换标题中的无效字符
    return title.strip()

# 处理CSV文件并保存到输出目录
def process_csv_files(cache_directory, output_directory):
    for root, dirs, files in os.walk(cache_directory):  # 遍历缓存目录
        for file in files:
            if file.endswith(".csv"):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    first_row = next(reader, None)
                    if not first_row or len(first_row) < 3:
                        print(f"Skipping {file} due to missing or incomplete data")  # 如果数据不完整则跳过该文件
                        continue
                    title = clean_title(first_row[2])  # 清理标题
                    translations = [row[2] for row in reader if len(row) >= 3]  # 提取翻译内容
                    # 去除"utf8"并创建相对路径
                    relative_path = os.path.relpath(root, cache_directory).replace("utf8" + os.sep, "")
                    file_path = os.path.join(output_directory, relative_path, f"{title}.md")
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # 确保目录存在
                    with open(file_path, 'w', encoding='utf-8') as article_file:
                        article_file.write(title + '\n\n' + '\n\n'.join(translations))  # 将翻译内容写入markdown文件
# 将本地更改推送到GitHub
def push_to_github(repo_path):
    repo = Repo(repo_path)  # 初始化仓库路径
    repo.git.add(update=True)  # 添加所有更改
    repo.index.commit("Updated translation articles")  # 提交更改
    origin = repo.remote(name='origin')  # 设置远程仓库
    try:
        origin.push()  # 尝试推送更改
    except:
        repo.git.push('--set-upstream', 'origin', 'main')  # 如果失败，则设置上游并重试

if __name__ == "__main__":
    TOKEN = "e113b723befac3023508a709d7444ce3"  # 你的token
    PROJECT_ID = 3131  # 项目ID
    LOCAL_REPO_PATH = "c:/cs/repositories/memoFile"  # 本地仓库路径
    CACHE_DIR = "c:/cs/cache"  # 缓存目录
    
    zip_file = download_translation_file(TOKEN, PROJECT_ID)  # 下载翻译文件
    if zip_file:
        unzip_file(zip_file, CACHE_DIR)  # 解压文件
        process_csv_files(CACHE_DIR, LOCAL_REPO_PATH)  # 处理CSV文件
        # 删除缓存文件夹
        #shutil.rmtree(CACHE_DIR)
        push_to_github(LOCAL_REPO_PATH)  # 推送更改到GitHub
        print("操作完成!")
    else:
        print("下载失败!")
