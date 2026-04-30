# templates/

再利用可能なテンプレート・パーツの集約フォルダ。

## ファイル構成

- `deck-skeletons/` … スライド骨子の雛形（PPTX/HTML/MD）
- `analysis-snippets/` … 分析ドキュメントの再利用パーツ

## 運用

`patterns/` で勝ち筋として確立したものを `templates/deck-skeletons/` に反映。
新規案件はここから出発し、案件特性に応じてカスタマイズ。

## 命名規則

- BM型ベース：`d2c-brand-cocreation_v1.pptx`
- 業界ベース：`cosmetics-haircare_v1.md`
- バージョンは `_vX` で管理（v1, v1.1, v2 等）

## 月次更新

`patterns/` の更新に伴い、対応する `templates/` も更新する：

1. `patterns/by-bm-type/d2c-cocreation.md` v1.2 で「LTV/CAC試算スライド必須化」が追加された
2. `templates/deck-skeletons/d2c-cocreation_v1.2.pptx` にLTV/CAC試算スライドを追加
3. 次回の同型案件はこのv1.2から出発
