#!/usr/bin/env -S python
# SPDX-License-Identifier: MIT
# Copyright 2022-2023 hirmiura (https://github.com/hirmiura)
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

args: Any = None


def pargs() -> None:
    global args
    parser = argparse.ArgumentParser(description="fntファイル1行目のfaceの中の空白を除去する")
    parser.add_argument("files", nargs="+", help="1つ以上の入力ファイル")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    args = parser.parse_args()


def process() -> None:
    for file in args.files:
        fp = Path(file)
        text = fp.read_text(encoding="utf-8")
        lines = text.splitlines()
        # 1行目だけ処理する
        m = re.search(r' face="(.*?)" ', lines[0])
        if not m:
            raise ValueError("Face not found.")
        face = m.group(1)
        face_wo_space = re.sub(r"\s+", "", face)
        lines[0] = re.sub(rf' face="{face}" ', f' face="{face_wo_space}" ', lines[0])
        text = "\n".join(lines)
        fp.write_text(text, encoding="utf-8")


def main() -> int:
    pargs()
    process()
    return 0


if __name__ == "__main__":
    sys.exit(main())
