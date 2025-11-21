# modules/calculator.py
import sympy as sp

def run(expr_text: str) -> str:
    """
    接收纯表达式或含中文乘除号的字符串，返回计算结果和可解释过程。
    """
    try:
        expr = (expr_text.replace("×", "*")
                        .replace("÷", "/")
                        .replace("（", "(")
                        .replace("）", ")"))
        sym_expr = sp.sympify(expr)
        val = sp.N(sym_expr)
        return f"【计算器】表达式：{sym_expr}\n结果：{val}"
    except Exception as e:
        return f"【计算器】解析/计算失败：{e}"
