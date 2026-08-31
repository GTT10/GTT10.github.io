# 岡山大学大学院入試アーカイブ

数学・材料力学・流体力学・熱力学の2003〜2024年度を整理した静的学習サイトです。

## 収録状況

- 4科目 × 22年度 = 88年度ページ
- 問題PDF 88件、解答PDF 88件
- 解説付き 75年度分、PDF資料のみ 13年度分

年度一覧では「解説」と「PDF資料」を区別して表示します。

## 内容を編集するときの原則

1. 問題PDFを一次資料とし、科目・年度・大問・小問を固定する。
2. 問題文にない条件は仮定として明記する。
3. 条件不足や物性指定の不整合がある場合は「一意に定まらない」を主結論にする。
4. 条件付きの数値解は、採用した経路・物性モデル・浮力・分圧などと分けて示す。
5. 年度ページと公開PDFの結論を一致させる。

## ローカル確認

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
node tools/audit-site.mjs
.venv/bin/python tools/audit-pdfs.py
python3 -m http.server 8000
```

`audit-site.mjs` は88年度ページ、サイト内リンク、重複ID、画像alt、主要な訂正内容を検査します。`audit-pdfs.py` は176PDFの構造、年度・科目ごとの配置、主要な改訂PDFの本文を検査します。

## 改訂PDFの生成

```bash
.venv/bin/python tools/generate_math_2003_pdf.py
.venv/bin/python tools/generate_fluid_2003_pdf.py
.venv/bin/python tools/generate_thermo_2003_2008.py 2003 2007
```

ReportLab用の日本語フォントが標準候補にない環境では、`GTT10_JAPANESE_FONT` に埋め込み可能な日本語TrueTypeフォントを指定してください。`tools/generate_fluid_answers.py` の2004〜2008年度版は別途LuaLaTeXを必要とします。
同じReportLab・フォント・入力を使う再生成では、PDFのメタデータを固定して同一ハッシュになるようにしています。

## 誤りの報告

対象の科目・年度・設問と、問題原本に基づく根拠を添えて[GitHub Issues](https://github.com/GTT10/GTT10.github.io/issues)へ報告してください。
