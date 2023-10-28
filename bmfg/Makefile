# SPDX-License-Identifier: MIT
# Copyright 2023 hirmiura (https://github.com/hirmiura)
#
SHELL := /bin/bash

# 各種ディレクトリ
D_BIN		:= ../bin
D_MOD		:= ../mod
D_FONTSDST	:= $(D_MOD)/graphics/fonts

# 実行ファイル
E_BMFONT		:= $(D_BIN)/bmfont64.exe
E_FIXFACE		:= $(D_BIN)/fixface.py
E_FIXHEIGHT		:= $(D_BIN)/fixheight.py

# 生成するフォント
FONTNAME := BIZUDPGothic
FONT_LIST := 12cond.fnt 20aa.fnt 20aab.fnt 20b.fnt 24aa.fnt 24aab.fnt 15aa.fnt 21aa.fnt 25aa.fnt
FONTS := $(addprefix $(FONTNAME),$(FONT_LIST))


#==============================================================================
# カラーコード
#==============================================================================
CC_Reset     := \033[0m
CC_BrRed     := \033[91m
CC_BrGreen   := \033[92m
CC_BrYellow  := \033[93m
CC_BrBlue    := \033[94m
CC_BrMagenta := \033[95m
CC_BrCyan    := \033[96m
CC_BrWhite   := \033[97m


#==============================================================================
# ヘルプ表示
#==============================================================================
define find.functions
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
endef

.PHONY: help
help:
	@echo '以下のコマンドが使用できます'
	@echo ''
	$(call find.functions)


#==============================================================================
# セットアップ
#==============================================================================
.PHONY: setup
setup: ## セットアップ - ビルドの前準備
setup: .setup-bmfcgen

.setup-bmfcgen: bmfcgen.json bmfc_template.txt
	@echo -e '$(CC_BrBlue)========== setup-bmfcgen ==========$(CC_Reset)'
	$(D_BIN)/bmfcgen.py
	touch .setup-bmfcgen


#==============================================================================
# ビルド
#==============================================================================
.PHONY: build build-fonts build-fonts-para copy-fonts fixheight
build: ## ビルドする
build: build-fonts copy-fonts fixheight

%.fnt: %.bmfc
	$(E_BMFONT) -c $< -o $@
	$(E_FIXFACE) $@

build-fonts:
	$(MAKE) -j 4 build-fonts-para

build-fonts-para: $(FONTS)

copy-fonts: $(FONTS) clean-mod-fonts
	@echo -e '$(CC_BrBlue)========== copy-fonts ==========$(CC_Reset)'
	@mkdir -p $(D_FONTSDST)
	cp $(FONTNAME)12cond.fnt $(D_FONTSDST)/orbitron12condensed.fnt
	cp $(FONTNAME)20aa.fnt $(D_FONTSDST)/orbitron20aa.fnt
	cp $(FONTNAME)20aab.fnt $(D_FONTSDST)/orbitron20aabold.fnt
	cp $(FONTNAME)20b.fnt $(D_FONTSDST)/orbitron20bold.fnt
	cp $(FONTNAME)24aa.fnt $(D_FONTSDST)/orbitron24aa.fnt
	cp $(FONTNAME)24aab.fnt $(D_FONTSDST)/orbitron24aabold.fnt
	cp $(FONTNAME)15aa.fnt $(D_FONTSDST)/insignia15LTaa.fnt
	cp $(FONTNAME)21aa.fnt $(D_FONTSDST)/insignia21LTaa.fnt
	cp $(FONTNAME)25aa.fnt $(D_FONTSDST)/insignia25LTaa.fnt
	cp *.png $(D_FONTSDST)

fixheight:
	# @echo -e '$(CC_BrBlue)========== fixheight ==========$(CC_Reset)'
	# $(E_FIXHEIGHT) -lh 15 -ba 12 -y 4 -t=-4 $(D_FONTSDST)/insignia15LTaa.fnt
	# $(E_FIXHEIGHT) -lh 21 -ba 17 -y 6 -t=-7 $(D_FONTSDST)/insignia21LTaa.fnt
	# $(E_FIXHEIGHT) -lh 24 -ba 20 -y 7 -t=-10 $(D_FONTSDST)/insignia25LTaa.fnt


#==============================================================================
# 全ての作業を一括で実施する
#==============================================================================
.PHONY: all
all: ## 全ての作業を一括で実施する
all: setup
	$(MAKE) build


#==============================================================================
# クリーンアップ
#==============================================================================
.PHONY: clean clean-all clean-bmfc clean-fnt clean-mod-fonts
clean: ## セットアップで生成したファイル以外を全て削除します
clean: clean-mod-fonts clean-fnt

clean-all: ## 生成した全てのファイルを削除します
clean-all: clean clean-bmfc

clean-bmfc:
	@echo -e '$(CC_BrMagenta)========== clean-bmfc ==========$(CC_Reset)'
	rm -f .setup-bmfcgen *.bmfc

clean-fnt:
	@echo -e '$(CC_BrMagenta)========== clean-fnt ==========$(CC_Reset)'
	rm -f *.{fnt,png}

clean-mod-fonts:
	@echo -e '$(CC_BrMagenta)========== clean-mod-fonts ==========$(CC_Reset)'
	rm -f $(D_FONTSDST)/*.fnt $(D_FONTSDST)/*.png
