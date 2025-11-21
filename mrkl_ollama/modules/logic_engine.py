# modules/logic_engine.py
import re

def run(text: str) -> str:
    """
    非形式化的小示例：识别“如果…那么…”句式并给出演绎结论。
    更严谨可接入 Prolog / SAT / 规则库。
    """
    m = re.search(r"如果(.+?)，?那么(.+?)[。\.]?$", text)
    if not m:
        return "【逻辑】未识别到‘如果…那么…’规则。"
    premise = m.group(1).strip()
    conclusion = m.group(2).strip()
    return f"【逻辑】规则：若 {premise} 则 {conclusion}\n推理结论：在已知 {premise} 条件下，应当 {conclusion}。"
