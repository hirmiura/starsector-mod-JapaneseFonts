# SPDX-License-Identifier: MIT
# Copyright 2023 hirmiura (https://github.com/hirmiura)
#
SHELL := /bin/bash

# このパッケージのバージョン
# V_VERSION := $(shell tomlq -r '.tool.poetry.version' pyproject.toml)

# 各種ディレクトリ
D_BIN		:= bin
D_TMP		:= tmp
D_FONTS		:= fonts
D_MOD		:= mod
D_ID		:= $(shell jq -r '.id' $(D_MOD)/mod_info.json)

# URL
URL_BMFG	:= https://www.angelcode.com/products/bmfont/bmfont64_1.14b_beta.zip
URL_FONT	:= https://raw.githubusercontent.com/googlefonts/morisawa-biz-ud-gothic/main/fonts/ttf

#==============================================================================
# カラーコード
# ヘルプ表示
#==============================================================================
include ColorCode.mk
include Help.mk


#==============================================================================
# セットアップ
#==============================================================================
.PHONY: setup setup-bfg setup-fonts setup-bmfg
setup: ## セットアップ - ビルドの前準備
setup: setup-bfg setup-fonts setup-bmfg

setup-bfg:
	@echo -e '$(CC_BrBlue)========== setup-bfg ==========$(CC_Reset)'
	@mkdir -p $(D_TMP)
	wget -nc -P $(D_TMP) $(URL_BMFG)
	unzip -n $(D_TMP)/bmfont64_1.14b_beta.zip -d $(D_BIN)
	chmod 755 $(D_BIN)/bmfont64.exe

setup-fonts:
	@echo -e '$(CC_BrBlue)========== setup-fonts ==========$(CC_Reset)'
	@mkdir -p $(D_FONTS)
	wget -nc -P $(D_FONTS) $(URL_FONT)/BIZUDGothic-Regular.ttf
	wget -nc -P $(D_FONTS) $(URL_FONT)/BIZUDGothic-Bold.ttf
	wget -nc -P $(D_FONTS) $(URL_FONT)/BIZUDPGothic-Regular.ttf
	wget -nc -P $(D_FONTS) $(URL_FONT)/BIZUDPGothic-Bold.ttf

setup-bmfg:
	@echo -e '$(CC_BrBlue)========== setup-bmfg ==========$(CC_Reset)'
	$(MAKE) -C bmfg setup


#==============================================================================
# ビルド
#==============================================================================
.PHONY: build build-bmfg
build: ## ビルドする
build: setup build-bmfg $(FONTS)

build-bmfg:
	@echo -e '$(CC_BrBlue)========== build-bmfg ==========$(CC_Reset)'
	$(MAKE) -C bmfg build


#==============================================================================
# パッケージング
#==============================================================================
.PHONY: packaging
packaging: ## パッケージ化する
packaging: build clean-package $(D_ID).zip

$(D_ID).zip:
	@echo -e '$(CC_BrBlue)========== $(D_ID).zip ==========$(CC_Reset)'
	cp -r $(D_MOD) $(D_ID)
	zip -r $(D_ID).zip $(D_ID)
	rm -fr $(D_ID)


#==============================================================================
# 全ての作業を一括で実施する
#==============================================================================
.PHONY: all
all: ## 全ての作業を一括で実施する
all: setup build packaging


#==============================================================================
# クリーンアップ
#==============================================================================
.PHONY: clean clean-all clean-fonts clean-tmp clean-package
clean: ## セットアップで生成したファイル以外を全て削除します
clean: clean-package
	$(MAKE) -C bmfg clean

clean-all: ## 生成した全てのファイルを削除します
clean-all: clean clean-fonts clean-tmp
	$(MAKE) -C bmfg clean-all

clean-fonts:
	@echo -e '$(CC_BrMagenta)========== clean-fonts ==========$(CC_Reset)'
	rm -fr $(D_FONTS)

clean-tmp:
	@echo -e '$(CC_BrMagenta)========== clean-tmp ==========$(CC_Reset)'
	rm -fr $(D_TMP)

clean-package:
	@echo -e '$(CC_BrMagenta)========== clean-package ==========$(CC_Reset)'
	rm -fr $(D_ID).zip $(D_ID)
