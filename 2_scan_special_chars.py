#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描当前脚本所在目录的所有文件和文件夹，
检测名称中是否包含：
  1. 表情符号
  2. 空格
  3. / \ : * ? " < > |
并将所有“有问题”路径以结构化 Markdown 输出到 issues.md。
"""

import os
import re
import sys
from pathlib import Path

try:
    import emoji
    EMOJI_PATTERN = emoji.get_emoji_regexp()
except ImportError:
    # 如果未安装 emoji 包，则只检测常见 emoji 区段
    EMOJI_PATTERN = re.compile(
        "[\U0001F300-\U0001F6FF\U0001F900-\U0001F9FF\U0001FA70-\U0001FAFF]"
    )

# 要检测的九个特殊字符加空格
SPECIAL_CHARS = set(' /\\:*?"<>|')

def has_bad_chars(name: str) -> bool:
    if any(c in SPECIAL_CHARS for c in name):
        return True
    if EMOJI_PATTERN.search(name):
        return True
    return False

def scan_and_report(root: Path):
    md_lines = ["# 检测报告", "", f"扫描目录：`{root}`", ""]
    for dirpath, dirnames, filenames in os.walk(root):
        rel = Path(dirpath).relative_to(root)
        indent = "  " * len(rel.parts)
        # 先检查当前目录名（除最顶层）
        if rel and has_bad_chars(rel.name):
            md_lines.append(f"{indent}- 📁 **{rel.name}** （目录）")
        # 再检查子目录
        for d in dirnames:
            if has_bad_chars(d):
                md_lines.append(f"{indent}  - 📁 {d}")
        # 检查文件
        for f in filenames:
            if has_bad_chars(f):
                md_lines.append(f"{indent}  - 📄 {f}")
    out = root / "issues.md"
    with out.open("w", encoding="utf-8") as fp:
        fp.write("\n".join(md_lines))
    print(f"检测完成，结果已保存到 {out}")

if __name__ == "__main__":
    base = Path(__file__).parent.resolve()
    scan_and_report(base)
