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
    parser = argparse.ArgumentParser(description="fntファイルの高さのパラメータを変更する")
    parser.add_argument("-lh", type=int, default=None, help="lineHeightの値 - 元フォントに合わせると良い")
    parser.add_argument("-ba", type=int, default=None, help="baseの変更値 - 元フォントに合わせると良い")
    parser.add_argument("-y", type=int, default=0, help="yの変更値 - オフセット指定")
    parser.add_argument("-t", type=int, default=0, help="heightの変更値 - オフセット指定")
    parser.add_argument("files", nargs="+", help="1つ以上の入力ファイル")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    args = parser.parse_args()


def process() -> None:
    for file in args.files:
        fp = Path(file)
        text = fp.read_text(encoding="utf-8")
        lines = text.splitlines()
        # 2行目を処理する
        if args.lh:
            lines[1] = re.sub(r" lineHeight=(\d+) ", f" lineHeight={args.lh} ", lines[1])
        if args.ba:
            lines[1] = re.sub(r" base=(\d+) ", f" base={args.ba} ", lines[1])
        # 3行目から処理する
        i: int = 2
        iMax: int = len(lines)
        while i < iMax:
            m = re.search(r"^(.+\sy=)(\d+)(\s.+\sheight=)(\d+)(\s.+)$", lines[i])
            if m:
                y = int(m.group(2)) + args.y
                h = int(m.group(4)) + args.t
                lines[i] = "".join([m.group(1), str(y), m.group(3), str(h), m.group(5)])
            i += 1
        text = "\n".join(lines)
        fp.write_text(text, encoding="utf-8")


def main() -> int:
    pargs()
    process()
    return 0


if __name__ == "__main__":
    sys.exit(main())
