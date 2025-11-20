# main.py
from llm_ollama import OllamaLLM
from router import route
from modules import calculator, logic_engine, wiki_search

BANNER = """\
==== MRKL (Qwen + 外部推理模块) ====
输入 'exit' 退出
示例：
  12345 * 6789
  如果下雨，那么我需要带伞。
  查找 牛顿第二定律
  帮我写一段秋天的诗
------------------------------------
"""

def dispatch(module: str, text: str, llm: OllamaLLM) -> str:
    if module == "calculator":
        return calculator.run(text)
    if module == "logic":
        return logic_engine.run(text)
    if module == "search":
        # 允许 "查找 xxx" 或直接 "牛顿第二定律"
        q = text
        for prefix in ("查找", "搜索", "百科", "查一下"):
            q = q.replace(prefix, "").strip()
        return wiki_search.run(q)
    # 默认走 LLM
    return llm.generate(text, temperature=0.2)

def main():
    llm = OllamaLLM(model="qwen2.5:7b-instruct")
    print(BANNER)
    while True:
        try:
            user = input("你：").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye")
            break
        if user.lower() in ("exit", "/bye"):
            print("Bye")
            break
        m = route(user)
        result = dispatch(m, user, llm)
        print(f"\n[路由 → {m}]\n{result}\n")

if __name__ == "__main__":
    main()
