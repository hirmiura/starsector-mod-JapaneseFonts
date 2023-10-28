# starsector-mod-JapaneseFonts

これは [Starsector] で日本語を表示するための、フォント差し替え Mod です。  
現在は、森澤の [BIZ UDPGothic] を使用して一部のフォントのみ置き換えています。

## 注意

- 表示を変更するだけなので、別途日本語化ファイルが必要になります。
- IMEによる日本語入力は出来ません。
- コピー&ペーストは出来ます。船名の日本語化等が可能です。

## ビルド

### 開発環境

Debian(unstable) on WSL + Poetry + GNU make + ネット環境

フォントの生成に、AngelCodeさんの [Bitmap Font Generator] を使用しているので、  
Windows環境を前提としています。Wine等で動くかは試していないので分かりません。  
[Bitmap Font Generator] と [BIZ UDPGothic] をダウンロードするため、ネット環境も必要です。

### make

`make all` でいけると思います。

## ライセンス

生成されたフォントは、オリジナルから [SIL Open Font License (OFL)] を引き継いでいます。  
その他の配布物については [MIT License] としています。

## 過去の遺物

- [starsector-mod-Font_Replacement_for_Orbitron](https://github.com/hirmiura/starsector-mod-Font_Replacement_for_Orbitron)
- [starsector-mod-Font_Replacement_for_Insignia](https://github.com/hirmiura/starsector-mod-Font_Replacement_for_Insignia)
- [starsector-mod-JapaneseTranslation](https://github.com/hirmiura/starsector-mod-JapaneseTranslation)
- [starsector-mod-Font_Sika](https://github.com/hirmiura/starsector-mod-Font_Sika)
- [bfg_scripts](https://github.com/hirmiura/bfg_scripts)

---

[starsector]: https://fractalsoftworks.com/
[biz udpgothic]: https://fonts.google.com/specimen/BIZ+UDPGothic
[SIL Open Font License (OFL)]: https://scripts.sil.org/ofl
[MIT License]: https://opensource.org/license/mit/
[Bitmap Font Generator]: https://www.angelcode.com/products/bmfont/
