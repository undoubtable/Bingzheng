# router.py
import re

def route(user_input: str) -> str:
    """
    返回要调用的模块名：'calculator' | 'logic' | 'search' | 'llm'
    """
    t = user_input.strip()

    # 粗略判断：包含算术符号或“等于多少”
    if re.search(r"[0-9\+\-\*/\^\(\)]", t) or ("等于多少" in t) or ("结果是多少" in t):
        return "calculator"

    # 简单逻辑：如果…那么…
    if "如果" in t and "那么" in t:
        return "logic"

    # 搜索：以“查找/搜索/百科/是谁/是什么”开头或包含“查一下”
    if t.startswith(("查找","搜索","百科")) or ("查一下" in t) or ("是谁" in t) or ("是什么" in t):
        return "search"

    # 其他交给 LLM
    return "llm"
