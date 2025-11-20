# eval_toolqa.py
import os, json, time, math, csv, glob
from typing import Dict, Any, List, Tuple, Optional

from llm_ollama import OllamaLLM
from router import route
from modules import calculator, logic_engine, wiki_search

# ====== 配置区 ======
TOOLQA_DIR = r"D:\Desktop\ToolQA-main"   # <- 改成你的路径
# 常见题目目录名（如不一致，脚本也会递归扫描）
CAND_SUBDIRS = ["data", "questions", "dataset", "data/questions"]

MODEL_NAME = "qwen2.5:7b-instruct"
TEMPERATURE = 0.2
MAX_SAMPLES = None          # 设为整数可只跑前 N 条，调试用
SAVE_CSV = "toolqa_eval_results.csv"

# 数值题的误差阈值
NUM_TOL = 1e-6

# 分类映射（根据文件路径/字段猜测类别，便于分项统计）
def guess_category(sample: Dict[str, Any], path: str) -> str:
    # 优先读取字段
    for k in ["category", "task", "domain", "type"]:
        if k in sample and isinstance(sample[k], str):
            return sample[k].lower()
    lowerp = path.lower()
    if "math" in lowerp or "calc" in lowerp:
        return "math"
    if "text" in lowerp or "retrieval" in lowerp or "wiki" in lowerp:
        return "text"
    if "db" in lowerp or "sql" in lowerp:
        return "db"
    if "graph" in lowerp:
        return "graph"
    return "general"

# 标准答案/预测 文本归一化
def norm_text(s: str) -> str:
    return str(s).strip().replace("\u3000"," ").replace("　"," ").replace("\n"," ").replace("\r"," ").strip()

def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except:
        return False

def match_answer(pred: str, gold: str, category: str) -> bool:
    p, g = norm_text(pred), norm_text(gold)
    # 数值优先数值比较
    if is_number(p) and is_number(g):
        try:
            return abs(float(p) - float(g)) < NUM_TOL
        except:
            pass
    # 一般文本 Exact Match（可按需扩展：大小写、标点、同义词）
    return p == g

def load_toolqa_samples(root: str) -> List[Dict[str, Any]]:
    # 递归找 json/jsonl
    files = []
    for sub in CAND_SUBDIRS:
        p = os.path.join(root, sub)
        if os.path.isdir(p):
            files += glob.glob(os.path.join(p, "**", "*.json"), recursive=True)
            files += glob.glob(os.path.join(p, "**", "*.jsonl"), recursive=True)

    if not files:
        # 兜底：直接在根目录递归
        files = glob.glob(os.path.join(root, "**", "*.json"), recursive=True)
        files += glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True)

    samples = []
    for fp in files:
        try:
            if fp.endswith(".jsonl"):
                with open(fp, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f):
                        line = line.strip()
                        if not line: continue
                        obj = json.loads(line)
                        q,a = extract_qa(obj)
                        if q is None or a is None: continue
                        samples.append({
                            "id": obj.get("id", f"{os.path.basename(fp)}#{i}"),
                            "question": q,
                            "gold": a,
                            "path": fp,
                            "category": guess_category(obj, fp),
                            "required_tools": obj.get("required_tools") or obj.get("tools") or []
                        })
            else:
                with open(fp, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # 可能是列表或字典
                if isinstance(data, list):
                    it = enumerate(data)
                    get_id = lambda i, o: o.get("id", f"{os.path.basename(fp)}#{i}")
                elif isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
                    it = enumerate(data["data"])
                    get_id = lambda i, o: o.get("id", f"{os.path.basename(fp)}#{i}")
                else:
                    # 单条 or 未知结构
                    it = [(0, data)]
                    get_id = lambda i, o: o.get("id", f"{os.path.basename(fp)}#{i}")

                for i, obj in it:
                    q,a = extract_qa(obj)
                    if q is None or a is None: continue
                    samples.append({
                        "id": get_id(i, obj),
                        "question": q,
                        "gold": a,
                        "path": fp,
                        "category": guess_category(obj, fp),
                        "required_tools": obj.get("required_tools") or obj.get("tools") or []
                    })
        except Exception as e:
            print(f"[WARN] load failed: {fp} -> {e}")
            continue

    # 去重（按 question+gold）
    uniq = {}
    for s in samples:
        key = (norm_text(s["question"]), norm_text(s["gold"]))
        if key not in uniq:
            uniq[key] = s
    samples = list(uniq.values())
    print(f"[INFO] loaded {len(samples)} samples from {root}")
    return samples

def extract_qa(obj: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    # 自适配：尝试多个常用字段名
    q = obj.get("question") or obj.get("query") or obj.get("input") or obj.get("Q")
    a = obj.get("answer") or obj.get("gold") or obj.get("A") or obj.get("label")
    if isinstance(q, dict) and "text" in q: q = q["text"]
    if isinstance(a, dict) and "text" in a: a = a["text"]
    # 答案可能是数组/对象，尽量取主要字段
    if isinstance(a, list) and a:
        a = a[0]
    if isinstance(a, (dict,)):
        a = a.get("value") or a.get("text") or a.get("answer")
    if q is None or a is None:
        return None, None
    return str(q), str(a)

# ====== 你的两条答题线 ======
def answer_baseline(llm: OllamaLLM, q: str) -> Dict[str, Any]:
    t0 = time.time()
    resp = llm.generate(q, temperature=TEMPERATURE)
    dt = time.time() - t0
    return {
        "answer": resp,
        "latency_s": dt,
        "trace": [{"type":"llm","content_len":len(resp)}],
        "tool_called": False,
        "route": "llm"
    }

def dispatch_module(mod: str, text: str, llm: OllamaLLM) -> str:
    if mod == "calculator":
        return calculator.run(text)
    if mod == "logic":
        return logic_engine.run(text)
    if mod == "search":
        q = text
        for prefix in ("查找","搜索","百科","查一下"):
            q = q.replace(prefix, "").strip()
        return wiki_search.run(q)
    # 默认走 LLM
    return llm.generate(text, temperature=TEMPERATURE)

def postprocess_mrkl_output(output: str) -> str:
    """
    从模块返回格式中尽量抽取“最终答案”。
    这里给简单启发式：取最后一行的数字/句子；你可按需要优化。
    """
    s = output.strip()
    # 优先抽数值
    tokens = s.replace("\n"," ").split()
    nums = [t for t in tokens if is_number(t)]
    if nums:
        return nums[-1]
    return s

def answer_mrkl(llm: OllamaLLM, q: str) -> Dict[str, Any]:
    t0 = time.time()
    r = route(q)  # 你的 router
    out = dispatch_module(r, q, llm)
    final = postprocess_mrkl_output(out)
    dt = time.time() - t0
    tool_called = (r != "llm")
    return {
        "answer": final,
        "latency_s": dt,
        "trace": [{"type":"route","route":r},{"type":"result","len":len(out)}],
        "tool_called": tool_called,
        "route": r
    }

def main():
    llm = OllamaLLM(model=MODEL_NAME)
    samples = load_toolqa_samples(TOOLQA_DIR)
    if MAX_SAMPLES:
        samples = samples[:MAX_SAMPLES]

    totals = {
        "A": {"n":0,"ok":0,"lat":[], "by_cat":{}},
        "B": {"n":0,"ok":0,"lat":[], "by_cat":{}, "tool_calls":0}
    }

    rows = []
    for i, s in enumerate(samples, 1):
        q, gold, cat = s["question"], s["gold"], s["category"]

        outA = answer_baseline(llm, q)
        okA = match_answer(outA["answer"], gold, cat)
        totals["A"]["n"] += 1
        totals["A"]["ok"] += int(okA)
        totals["A"]["lat"].append(outA["latency_s"])
        totals["A"]["by_cat"].setdefault(cat, {"n":0,"ok":0,"lat":[]})
        cA = totals["A"]["by_cat"][cat]
        cA["n"]+=1; cA["ok"]+=int(okA); cA["lat"].append(outA["latency_s"])

        outB = answer_mrkl(llm, q)
        okB = match_answer(outB["answer"], gold, cat)
        totals["B"]["n"] += 1
        totals["B"]["ok"] += int(okB)
        totals["B"]["lat"].append(outB["latency_s"])
        totals["B"]["by_cat"].setdefault(cat, {"n":0,"ok":0,"lat":[],"tool":0})
        cB = totals["B"]["by_cat"][cat]
        cB["n"]+=1; cB["ok"]+=int(okB); cB["lat"].append(outB["latency_s"])
        if outB["tool_called"]:
            totals["B"]["tool_calls"] += 1
            cB["tool"] += 1

        rows.append({
            "id": s["id"],
            "category": cat,
            "question": q,
            "gold": gold,
            "A_pred": outA["answer"],
            "A_ok": okA,
            "A_ms": int(outA["latency_s"]*1000),
            "B_route": outB["route"],
            "B_pred": outB["answer"],
            "B_ok": okB,
            "B_ms": int(outB["latency_s"]*1000),
            "B_tool_called": outB["tool_called"],
            "path": s["path"]
        })

        if i % 20 == 0:
            print(f"[{i}/{len(samples)}] last: A_ok={okA} B_ok={okB} route={outB['route']}")

    # 导出明细
    with open(SAVE_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    # 汇总输出
    def pct(x,y): return 0.0 if y==0 else 100.0*x/y
    A_acc = pct(totals["A"]["ok"], totals["A"]["n"])
    B_acc = pct(totals["B"]["ok"], totals["B"]["n"])
    A_ms = sum(totals["A"]["lat"])/len(totals["A"]["lat"]) * 1000 if totals["A"]["lat"] else 0
    B_ms = sum(totals["B"]["lat"])/len(totals["B"]["lat"]) * 1000 if totals["B"]["lat"] else 0
    tool_rate = pct(totals["B"]["tool_calls"], totals["B"]["n"])

    print("\n==== Overall ====")
    print(f"A (纯LLM) : Acc={A_acc:.2f}%  Avg Lat={A_ms:.0f} ms")
    print(f"B (MRKL ) : Acc={B_acc:.2f}%  Avg Lat={B_ms:.0f} ms  ToolRate={tool_rate:.1f}%")
    print(f"明细已保存：{SAVE_CSV}")

    print("\n==== By Category ====")
    cats = set(list(totals["A"]["by_cat"].keys()) + list(totals["B"]["by_cat"].keys()))
    for cat in sorted(cats):
        a = totals["A"]["by_cat"].get(cat, {"n":0,"ok":0,"lat":[]})
        b = totals["B"]["by_cat"].get(cat, {"n":0,"ok":0,"lat":[],"tool":0})
        a_acc = pct(a["ok"], a["n"]) if a["n"] else 0
        b_acc = pct(b["ok"], b["n"]) if b["n"] else 0
        a_ms = (sum(a["lat"])/len(a["lat"]))*1000 if a["lat"] else 0
        b_ms = (sum(b["lat"])/len(b["lat"]))*1000 if b["lat"] else 0
        b_tr = pct(b.get("tool",0), b["n"]) if b["n"] else 0
        print(f"[{cat}]  A:Acc={a_acc:.1f}%@{a_ms:.0f}ms   B:Acc={b_acc:.1f}%@{b_ms:.0f}ms  ToolRate={b_tr:.1f}%")

if __name__ == "__main__":
    main()
# eval_toolqa.py