#!/usr/bin/env -S python
# SPDX-License-Identifier: MIT
# Copyright 2022-2023 hirmiura <https://github.com/hirmiura>
#
# Bitmap Font Generator Config Generator
from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from BMFC import BMFC

BMFCGEN_JSON_FILE = "bmfcgen.json"


@dataclass
class BmfGenConf(BMFC):
    outputfile: str = ""

    @property
    def bmfc_file(self):
        return self.outputfile + ".bmfc"

    @property
    def fnt_file(self):
        return self.outputfile + ".fnt"

    @property
    def png_file(self):
        return self.outputfile + "_0.png"


def read_jsonc(file: str) -> dict:
    """Cコメント付きJSONファイルを読み込む

    Args:
        file (str): JSONファイル

    Returns:
        dict: JOSNオブジェクト
    """
    with open(file, encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r"/\*[\s\S]*?\*/|//.*", "", text)
    return json.loads(text)


def init_config() -> list[BmfGenConf]:
    TEMP_KEY = "template"
    CONFIG_KEY = "config"

    # 設定リスト
    bmf_config_list = []

    # JSON設定ファイルを読み込む
    jobj = read_jsonc(BMFCGEN_JSON_FILE)

    # 全体用テンプレートを読み込む
    world_temp = BmfGenConf.load(jobj[TEMP_KEY]) if TEMP_KEY in jobj else BmfGenConf()

    # 設定リストを読み込む
    if CONFIG_KEY in jobj:
        for c in jobj[CONFIG_KEY]:
            cdict = c
            # 全体用テンプレートからコピーする
            citem = copy.copy(world_temp)
            if TEMP_KEY in cdict:
                # 個別テンプレートがあれば読み込む
                citem.load(c[TEMP_KEY])
                del cdict[TEMP_KEY]
            # 残りの設定を読み込む
            citem.apply_dict(cdict)
            # 設定リストに追加する
            bmf_config_list.append(citem)

    return bmf_config_list


def generate_bmfc(bmf_config_list: list[BmfGenConf]) -> None:
    print("bmfcファイルを生成中...", flush=True)
    count: int = 0
    for conf in bmf_config_list:
        count += 1
        # ファイルが既存か調べる
        bmfc_fp = Path(conf.bmfc_file)
        if bmfc_fp.exists():
            # 同一ファイルか調べる
            with tempfile.SpooledTemporaryFile(100_000, "wb", encoding="utf-8") as temp_fp:
                temp_fp.write(str(conf).encode())
                # ファイルサイズチェック
                temp_fp.seek(0, 2)
                temp_fp_size = temp_fp.tell()
                bmfc_fp_size = bmfc_fp.stat().st_size
                if bmfc_fp_size == temp_fp_size:
                    # ハッシュチェック
                    temp_fp.seek(0)
                    temp_hash = hashlib.file_digest(temp_fp, hashlib.sha1).hexdigest()
                    with bmfc_fp.open("rb") as fp:
                        bmfc_hash = hashlib.file_digest(fp, hashlib.sha1).hexdigest()
                    if temp_hash == bmfc_hash:
                        print(f"skip=> {conf.bmfc_file}", flush=True)
                        continue
        # 書き出し
        conf.save(conf.bmfc_file)
        print(f"Gen==> {conf.bmfc_file}", flush=True)

    print(f"{count} ファイル生成完了", flush=True)


def main() -> int:
    bmf_config_list = init_config()
    generate_bmfc(bmf_config_list)
    return 0


if __name__ == "__main__":
    sys.exit(main())
