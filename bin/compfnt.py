#!/usr/bin/env -S python
# SPDX-License-Identifier: MIT
# Copyright 2023 hirmiura (https://github.com/hirmiura)
"""指定ディレクトリにあるfntファイルのパラメータを比較する"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CRE_INFO = re.compile(
    r'^info face="(?P<face>.*)" size=(?P<size>-?\d+(\.\d*)?) bold=(?P<bold>\d)'
    r' italic=(?P<italic>\d) charset="(?P<charset>.*)" unicode=(?P<unicode>\d)'
    r" stretchH=(?P<stretchH>-?\d+) smooth=(?P<smooth>\d) aa=(?P<aa>\d)"
    r" padding=(?P<padding>.+) spacing=(?P<spacing>.+) outline=(?P<outline>\d)"
)
CRE_COMMON = re.compile(
    r"^common lineHeight=(?P<lineHeight>-?\d+(\.\d*)?) base=(?P<base>-?\d+(\.\d*)?)"
    r" scaleW=(?P<scaleW>-?\d+(\.\d*)?) scaleH=(?P<scaleH>-?\d+(\.\d*)?)"
    r" pages=(?P<pages>\d+) packed=(?P<packed>\d) alphaChnl=(?P<alphaChnl>\d)"
    r" redChnl=(?P<redChnl>\d) greenChnl=(?P<greenChnl>\d) blueChnl=(?P<blueChnl>\d)"
)

GN_INFO_LIST = [
    "face",
    "size",
    "bold",
    "italic",
    "charset",
    "unicode",
    "stretchH",
    "smooth",
    "aa",
    "padding",
    "spacing",
    "outline",
]
GN_COMMON_LIST = [
    "lineHeight",
    "base",
    "scaleW",
    "scaleH",
    "pages",
    "packed",
    "alphaChnl",
    "redChnl",
    "greenChnl",
    "blueChnl",
]


def pargs() -> argparse.Namespace:
    """コマンドライン引数を処理する

    Returns:
        argparse.Namespace: 処理した引数
    """
    parser = argparse.ArgumentParser(description="指定ディレクトリにあるfntファイルのパラメータを比較する")
    parser.add_argument("dirs", nargs="+", help="調査するディレクトリ")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    args = parser.parse_args()
    return args


def process(args: argparse.Namespace) -> None:
    assert args
    params_list = []

    # ディレクトリをチェックする
    for fdir in args.dirs:
        fnt_dir = Path(fdir)
        if not fnt_dir.exists():
            raise FileNotFoundError
        if not fnt_dir.is_dir():
            raise NotADirectoryError

        # fntファイルの一覧を取得する
        fnt_list = sorted(fnt_dir.glob("*.fnt"))

        # 各fntファイルを処理する
        for fnt_file in fnt_list:
            with fnt_file.open(encoding="utf-8") as fp:
                # infoとcommonのある先頭2行のみ読み込む
                line1 = fp.readline()
                line2 = fp.readline()

            # パラメータを抽出する
            mat_info = CRE_INFO.match(line1)
            assert mat_info is not None
            mat_common = CRE_COMMON.match(line2)
            assert mat_common is not None

            # 抽出したパラメータを辞書に保管する
            params = {}
            params["filename"] = fnt_file.name
            for gn_info in GN_INFO_LIST:
                params[gn_info] = mat_info.group(gn_info)
            for gn_common in GN_COMMON_LIST:
                params[gn_common] = mat_common.group(gn_common)
            params_list.append(params)

    output(params_list)


def output(params_list: list) -> None:
    """結果を出力する

    Args:
        params_list (list): パラメータのリスト
    """
    # ヘッダを出力する
    len4loop = len(params_list[0]) - 1
    for i, gn in enumerate(params_list[0].keys()):
        print(f"| {gn} ", end="")
        if i == len4loop:
            print("|")
    # 幅寄せルールを出力する
    for i in range(len4loop + 1):
        lcr = ":---" if i < 2 else "---:"
        print(f"| {lcr} ", end="")
        if i == len4loop:
            print("|")
    # パラメータを出力する
    for para in params_list:
        for i, gn in enumerate(para):
            print(f"| {para[gn]} ", end="")
            if i == len4loop:
                print("|")


def main() -> int:
    args = pargs()
    process(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
