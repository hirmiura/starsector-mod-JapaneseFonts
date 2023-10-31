# SPDX-License-Identifier: MIT
# Copyright 2023 hirmiura (https://github.com/hirmiura)
#
SHELL := /bin/bash

# 各種ディレクトリ
D_BIN		:= bin
D_TMP		:= tmp
D_FONTS		:= fonts
D_MOD		:= mod

# このパッケージのバージョン
V_ID		:= $(shell jq -r '.id' $(D_MOD)/mod_info.json)
V_VERSION	:= $(shell jq -r '.version' $(D_MOD)/mod_info.json)
F_PACKAGE	:= $(V_ID)-$(V_VERSION)

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
packaging: build clean-package $(F_PACKAGE).zip

$(F_PACKAGE).zip:
	@echo -e '$(CC_BrBlue)========== $(F_PACKAGE).zip ==========$(CC_Reset)'
	cp -r $(D_MOD) $(V_ID)
	zip -r $(F_PACKAGE).zip $(V_ID)
	rm -fr $(V_ID)


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
clean-all: clean clean-fonts clean-tmp clean-exe
	$(MAKE) -C bmfg clean-all

clean-fonts:
	@echo -e '$(CC_BrMagenta)========== clean-fonts ==========$(CC_Reset)'
	rm -fr $(D_FONTS)

clean-tmp:
	@echo -e '$(CC_BrMagenta)========== clean-tmp ==========$(CC_Reset)'
	rm -fr $(D_TMP)

clean-exe:
	@echo -e '$(CC_BrMagenta)========== clean-exe ==========$(CC_Reset)'
	rm -f $(D_BIN)/bmfont64.exe

clean-package:
	@echo -e '$(CC_BrMagenta)========== clean-package ==========$(CC_Reset)'
	rm -fr $(F_PACKAGE).zip $(V_ID)
