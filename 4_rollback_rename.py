#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
读取 rename_special_chars.py 生成的 rename_log.json，
按相反顺序将所有重命名操作一次撤回，恢复原始文件/文件夹名称。
"""

import os
import json
import sys
from pathlib import Path

def rollback(root: Path):
    log_file = root / "rename_log.json"
    if not log_file.exists():
        print(f"未找到重命名日志：{log_file}")
        sys.exit(1)

    with log_file.open("r", encoding="utf-8") as fp:
        log = json.load(fp)

    # 倒序执行，保证嵌套目录能正确恢复
    for entry in reversed(log):
        old = root / entry["old"]
        new = root / entry["new"]
        if new.exists():
            os.rename(new, old)
            print(f"回滚：{new} -> {old}")
        else:
            print(f"跳过（目标不存在）：{new}")
    print("所有操作已回滚完成。")

if __name__ == "__main__":
    base = Path(__file__).parent.resolve()
    rollback(base)
