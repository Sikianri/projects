import json

# 给定的JSON数据
json_data = '[{"id":102597800,"createdAt":"2021-09-05T12:35:34.000Z","updatedAt":"2022-09-04T08:09:09.000Z","key":"0","original":"# The mnemonic medium may help scaffold prompt-writing through author-provided prompts","translation":"# 助记媒 介可能通过提供作者创作的卡片来辅助卡片编写","file":{"id":352060,"name":"andy/note/mnemonic-medium/The mnemonic medium may help scaffold prompt-writing through author-provided prompts.md.csv","project":3131},"stage":9,"project":3131,"uid":23431,"extra":null,"context":null,"words":11,"version":null,"importHistory":[{"id":128500662,"createdAt":"2021-09-05T12:35:34.000Z","field":"translation","uid":null,"tid":102597800,"project":3131,"key":"0","from":"","to":"#助记媒体可以通过作 者提供的提示帮助搭建提示书写的脚手架","type":"text","operation":"import"},{"id":128500661,"createdAt":"2021-09-05T12:35:34.000Z","field":"original","uid":null,"tid":102597800,"project":3131,"key":"0","from":"","to":"# The mnemonic medium may help scaffold prompt-writing through author-provided prompts","type":"text","operation":"import"}]}]'

# 将JSON数据解析为Python字典列表
data_list = json.loads(json_data)

# 将数据转换为TiddlyWiki格式
tiddlywiki_data = ""
for data in data_list:
    title = data["original"].strip("# ").strip()  # 获取标题，去除#和空格
    content = data["translation"]
    tiddlywiki_data += f"!!{title}\n{content}\n\n"

# 将结果打印输出或保存到文件
print(tiddlywiki_data)
