# modules/wiki_search.py
import requests

def run(query: str) -> str:
    if not query:
        return "【搜索】请输入关键词。"
    url = "https://zh.wikipedia.org/api/rest_v1/page/summary/" + query
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            extract = data.get("extract")
            if extract:
                return f"【搜索】{query}\n{extract}"
        return f"【搜索】未找到：{query}"
    except Exception as e:
        return f"【搜索】失败：{e}"
