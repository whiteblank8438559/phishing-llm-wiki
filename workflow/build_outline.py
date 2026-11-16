#!/usr/bin/env python3
"""Read the local LLM Wiki, validate provenance, and emit a slide plan.

This script is the retrieval/check gate. It does not call an LLM or claim to
generate the final HTML; the AI uses the checked plan in the next step.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "sources"
TOPIC_DIR = ROOT / "topics"

SLIDES = [
    ("what-is-phishing.md", "什麼是網路釣魚？", "說出釣魚訊息的目的與常見媒介"),
    ("warning-signs.md", "辨認五類警訊", "找出催促、冒名、索取資料與可疑連結等警訊"),
    ("verify-before-click.md", "暫停、查看、獨立查證", "不用訊息內的管道，改從官網或官方 App 確認"),
    ("government-text-case.md", "案例練習：假冒資安機關", "把查證流程用於官方公布的案例"),
    ("respond-and-report.md", "收到或誤點後怎麼辦？", "依是否點擊或提供資料分流處理"),
]

SOURCE_LINK = re.compile(r"\[S(0[1-9][0-9]*)\]\(([^)]+)\)")
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def read_text(path: Path, issues: list[str]) -> str:
    if not path.is_file():
        issues.append(f"缺少檔案：{path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def check_local_links(path: Path, body: str, issues: list[str]) -> None:
    for target in MARKDOWN_LINK.findall(body):
        if target.startswith(("https://", "http://", "#")):
            continue
        resolved = (path.parent / target.split("#", 1)[0]).resolve()
        if not resolved.is_relative_to(ROOT.resolve()) or not resolved.is_file():
            issues.append(f"連結無效：{path.relative_to(ROOT)} → {target}")


def main() -> int:
    issues: list[str] = []
    source_files = sorted(SOURCE_DIR.glob("S*.md"))
    if len(source_files) < 5:
        issues.append(f"來源筆記不足五篇：目前 {len(source_files)} 篇")

    source_ids: set[str] = set()
    for path in source_files:
        match = re.match(r"S(\d+)-", path.name)
        if not match:
            issues.append(f"來源檔名沒有編號：{path.name}")
            continue
        source_ids.add(match.group(1))
        body = read_text(path, issues)
        if not re.search(r"https://[^)\s]+", body):
            issues.append(f"來源筆記缺原始網址：{path.name}")
        check_local_links(path, body, issues)

    planned: list[dict] = []
    cited_across_topics: set[str] = set()
    for filename, title, objective in SLIDES:
        path = TOPIC_DIR / filename
        body = read_text(path, issues)
        if not body:
            continue
        check_local_links(path, body, issues)
        references = []
        for source_id, target in SOURCE_LINK.findall(body):
            cited_across_topics.add(source_id)
            if source_id not in source_ids:
                issues.append(f"{filename} 引用不存在的來源 S{source_id}")
            if not (path.parent / target).resolve().is_file():
                issues.append(f"{filename} 的 S{source_id} 連結無效")
            if source_id not in references:
                references.append(source_id)
        if not references:
            issues.append(f"{filename} 沒有來源引用")
        planned.append({
            "title": title,
            "learning_objective": objective,
            "wiki_page": str(path.relative_to(ROOT)).replace("\\", "/"),
            "source_ids": [f"S{x}" for x in references],
            "wiki_markdown": body.strip(),
        })

    for source_id in sorted(source_ids - cited_across_topics):
        issues.append(f"來源 S{source_id} 未被任何主題頁引用")

    response = read_text(TOPIC_DIR / "respond-and-report.md", issues)
    if "美國專用" not in response or "臺灣" not in response:
        issues.append("事後處理頁缺少美國／臺灣通報方式的區分")
    case = read_text(TOPIC_DIR / "government-text-case.md", issues)
    if "官方公布案例" not in case or "逐字轉錄" not in case:
        issues.append("案例頁缺少來源與改寫標示")

    report = {
        "checked_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "status": "pass" if not issues else "needs_revision",
        "source_count": len(source_files),
        "topic_count": len(planned),
        "issues": sorted(set(issues)),
        "next_step": "generate_html" if not issues else "revise_wiki_then_rerun",
    }
    (OUT / "check_result.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if issues:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    plan = {
        "title": "如何辨識網路釣魚訊息",
        "audience": "沒有資安背景的初學者",
        "source_of_truth": "本專案的 LLM Wiki；若與原始資料不一致，回原始資料查證",
        "slides": [
            {"title": "開場與學習目標", "learning_objective": "理解本次要學會辨識、查證與處理", "wiki_page": "PLAN.md", "source_ids": [], "wiki_markdown": ""},
            *planned,
            {"title": "練習與重點回顧", "learning_objective": "將三步查證法套用於可疑訊息", "wiki_page": "AUDIT_LOG.md", "source_ids": ["S01", "S02", "S03", "S04", "S05"], "wiki_markdown": ""},
        ],
    }
    (OUT / "slide_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {report['source_count']} sources, {report['topic_count']} topics, {len(plan['slides'])} planned slides")
    return 0


if __name__ == "__main__":
    sys.exit(main())
