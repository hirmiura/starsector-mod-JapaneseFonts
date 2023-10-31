#!/usr/bin/env -S python
# SPDX-License-Identifier: MIT
# Copyright 2022-2023 hirmiura <https://github.com/hirmiura>
#
# Bitmap Font Generator Configuration file class
from __future__ import annotations

import inspect
import re
import sys
from dataclasses import dataclass, field
from functools import total_ordering


@total_ordering
class NumRange:
    """charsで使う数字の範囲を表すクラス"""

    def __init__(self, begin, end=None):
        assert begin is not None
        if end is None:
            end = begin
        if begin < end:
            self._begin = begin
            self._end = end
        else:
            self._begin = end
            self._end = begin

    def __eq__(self, other):
        if not isinstance(other, NumRange):
            return NotImplemented
        return self._begin == other._begin and self._end == other._end

    def __lt__(self, other):
        if not isinstance(other, NumRange):
            return NotImplemented
        if self._begin != other._begin:
            return self._begin < other._begin
        else:
            return self._end < other._end

    @property
    def is_single(self) -> bool:
        return self._begin == self._end

    @property
    def is_range(self) -> bool:
        return not self.is_single

    @property
    def begin(self):
        return self._begin

    @property
    def end(self):
        return self._end

    def __str__(self):
        if self.is_single:
            return str(self._begin)
        else:
            return str(self._begin) + "-" + str(self._end)


@dataclass
class BMFC:
    fileVersion: int = 1
    fontName: str = ""
    fontFile: str = ""
    charSet: int = 0
    fontSize: int = 10
    aa: int = 1
    scaleH: int = 100
    useSmoothing: int = 1
    isBold: int = 0
    isItalic: int = 0
    useUnicode: int = 1
    disableBoxChars: int = 1
    outputInvalidCharGlyph: int = 0
    dontIncludeKerningPairs: int = 0
    useHinting: int = 1
    renderFromOutline: int = 1
    useClearType: int = 1
    autoFitNumPages: int = 0
    autoFitFontSizeMin: int = 0
    autoFitFontSizeMax: int = 0

    paddingDown: int = 0
    paddingUp: int = 0
    paddingRight: int = 0
    paddingLeft: int = 0
    spacingHoriz: int = 1
    spacingVert: int = 1
    useFixedHeight: int = 0
    forceZero: int = 0
    widthPaddingFactor: float = 0.00

    outWidth: int = 256
    outHeight: int = 256
    outBitDepth: int = 32
    fontDescFormat: int = 0
    fourChnlPacked: int = 0
    textureFormat: str = "png"
    textureCompression: int = 0
    alphaChnl: int = 1
    redChnl: int = 0
    greenChnl: int = 0
    blueChnl: int = 0
    invA: int = 0
    invR: int = 0
    invG: int = 0
    invB: int = 0

    outlineThickness: int = 0

    chars: list[NumRange] = field(default_factory=list)

    @property
    def textureSize(self):
        return (self.outWidth, self.outHeight)

    @textureSize.setter
    def textureSize(self, size):
        try:
            w, h = size
        except ValueError:
            raise ValueError("Pass an iterable with two items")
        else:
            self.outWidth = w
            self.outHeight = h

    @classmethod
    def read(cls, text: str):
        result = cls()
        tli = text.splitlines()
        attrs = dict(inspect.getmembers(result, lambda x: not callable(x)))
        for line in tli:
            # コメントと空行
            if re.match(r"\s*#|\s*$", line):
                continue

            # chars=
            m = re.match(r"chars=(\S+)", line)
            if m:
                numlist = m.group(1).split(",")
                for nums in numlist:
                    n1, *n2 = nums.split("-")
                    n1 = int(n1)
                    n2 = int(n2[0]) if n2 else None
                    result.chars.append(NumRange(n1, n2))
                continue

            # その他
            m = re.match(r"(\w+)=(.+)", line)
            if m:
                k = m.group(1)
                if k not in attrs:
                    continue
                var = attrs[k]
                ty = type(var)
                v = m.group(2)
                if ty is int:
                    setattr(result, k, int(v))
                elif ty is float:
                    setattr(result, k, float(v))
                elif ty is str:
                    setattr(result, k, str(v))
        return result

    @classmethod
    def load(cls, file):
        with open(file, encoding="utf-8") as f:
            return cls.read(f.read())

    def _make_chars(self) -> str:
        i = 0
        i_max = len(self.chars)
        result = []
        do_loop = True
        while do_loop:
            line = ["chars="]
            cur_len = 0
            while True:
                if i >= i_max:
                    do_loop = False
                    break
                next_len = len(str(self.chars[i]))
                if cur_len + next_len > 99:
                    break
                if cur_len != 0:
                    line.append(",")
                    cur_len += 1
                line.append(str(self.chars[i]))
                cur_len += next_len
                i += 1
            if cur_len > 0:
                result.extend(line)
                result.append("\n")
        return "".join(result)

    def __str__(self):
        tli = []
        tli.append(
            f"""\
# AngelCode Bitmap Font Generator configuration file
fileVersion={self.fileVersion}

# font settings
fontName={self.fontName}
fontFile={self.fontFile}
charSet={self.charSet}
fontSize={self.fontSize}
aa={self.aa}
scaleH={self.scaleH}
useSmoothing={self.useSmoothing}
isBold={self.isBold}
isItalic={self.isItalic}
useUnicode={self.useUnicode}
disableBoxChars={self.disableBoxChars}
outputInvalidCharGlyph={self.outputInvalidCharGlyph}
dontIncludeKerningPairs={self.dontIncludeKerningPairs}
useHinting={self.useHinting}
renderFromOutline={self.renderFromOutline}
useClearType={self.useClearType}
autoFitNumPages={self.autoFitNumPages}
autoFitFontSizeMin={self.autoFitFontSizeMin}
autoFitFontSizeMax={self.autoFitFontSizeMax}

# character alignment
paddingDown={self.paddingDown}
paddingUp={self.paddingUp}
paddingRight={self.paddingRight}
paddingLeft={self.paddingLeft}
spacingHoriz={self.spacingHoriz}
spacingVert={self.spacingVert}
useFixedHeight={self.useFixedHeight}
forceZero={self.forceZero}
widthPaddingFactor={self.widthPaddingFactor}

# output file
outWidth={self.outWidth}
outHeight={self.outHeight}
outBitDepth={self.outBitDepth}
fontDescFormat={self.fontDescFormat}
fourChnlPacked={self.fourChnlPacked}
textureFormat={self.textureFormat}
textureCompression={self.textureCompression}
alphaChnl={self.alphaChnl}
redChnl={self.redChnl}
greenChnl={self.greenChnl}
blueChnl={self.blueChnl}
invA={self.invA}
invR={self.invR}
invG={self.invG}
invB={self.invB}

# outline
outlineThickness={self.outlineThickness}

# selected chars
"""
        )

        tli.append(self._make_chars())
        tli.append(
            """
# imported icon images
"""
        )
        return "".join(tli)

    def save(self, file) -> None:
        with open(file, "w", encoding="utf-8") as f:
            f.write(str(self))

    def apply_dict(self, d: dict) -> None:
        assert d is not None
        attrs = dict(inspect.getmembers(self, lambda x: not callable(x)))
        for k, v in d.items():
            if k not in attrs:
                continue
            var = attrs[k]
            ty = type(var)
            if ty is int:
                setattr(self, k, int(v))
            elif ty is float:
                setattr(self, k, float(v))
            elif ty is str:
                setattr(self, k, str(v))
            elif k == "chars":
                numlist = v.split(",")
                for nums in numlist:
                    n1, *n2 = nums.split("-")
                    n1 = int(n1)
                    n2 = int(n2[0]) if n2 else None
                    self.chars.append(NumRange(n1, n2))


def test():
    obj = BMFC.load("test.bmfc")
    print(obj)


if __name__ == "__main__":
    sys.exit(test())
