import requests
import zipfile
import os
import json
import shutil
from git import Repo

def download_translation_file(token, project_id):
    headers = {
        "Authorization": token
    }
    url = f"https://paratranz.cn/api/projects/{project_id}/artifacts/download"
    response = requests.get(url, headers=headers, allow_redirects=True)
    if response.status_code == 200:
        with open("translation.zip", "wb") as file:
            file.write(response.content)
        return "translation.zip"
    else:
        print(f"Error: {response.status_code}")
        return None

def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def clean_title(title):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '[', ']', '(', ')']
    for char in invalid_chars:
        title = title.replace(char, '')
    return title        

def process_json_files(cache_directory, output_directory):
    for root, dirs, files in os.walk(cache_directory):
        for file in files:
            if file.endswith(".json"):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 提取作者名
                    author = None
                    for entry in data:
                        if "著" in entry['translation'] or "作者" in entry['translation']:
                            author = clean_title(entry['translation'].split()[0])
                            break

                    # 如果没有找到作者名，跳过这个文件
                    if not author:
                        continue

                    author_dir = os.path.join(output_directory, author)
                    if not os.path.exists(author_dir):
                        os.makedirs(author_dir)
                    
                    # 提取文章标题并清理
                    title = clean_title(data[0]['translation'])
                    # 合并翻译的条目为一个文章
                    article = "\n".join([entry['translation'] for entry in data])
                    # 保存到作者的目录中
                    with open(os.path.join(author_dir, f"{title}.txt"), 'w', encoding='utf-8') as article_file:
                        article_file.write(article)

def push_to_github(repo_path):
    repo = Repo(repo_path)
    repo.git.add(update=True)
    repo.index.commit("Updated translation articles")
    origin = repo.remote(name='origin')
    try:
        origin.push()
    except:
        # 如果首次推送，设置上游分支并推送
        repo.git.push('--set-upstream', 'origin', 'main')

if __name__ == "__main__":
    TOKEN = "e113b723befac3023508a709d7444ce3"
    PROJECT_ID = 3131
    LOCAL_REPO_PATH = "c:/cs/repositories/memoFile"
    CACHE_DIR = os.path.join(LOCAL_REPO_PATH, "cache")
    
    zip_file = download_translation_file(TOKEN, PROJECT_ID)
    if zip_file:
        unzip_file(zip_file, CACHE_DIR)
        process_json_files(CACHE_DIR, LOCAL_REPO_PATH)
        # 删除缓存文件夹
        shutil.rmtree(CACHE_DIR)
        push_to_github(LOCAL_REPO_PATH)
        print("操作完成!")
    else:
        print("下载失败!")
