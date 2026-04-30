# 案件テンプレート

このフォルダをコピーして新規案件を始めること。

```bash
cp -r proposals/_template proposals/2026-QX_クライアント名
```

## ファイル構成

- `meta.yml` ★必須 … 案件のメタデータ（クライアント名・BM型・予算など）
- `result.md` ★必須 … 結果と決定要因の言語化（提案完了後・結果確定後に更新）
- `deck/` … 最終提案書（PPTX/PDF/HTML等）

## 命名規則

- フォルダ名：`YYYY-QX_クライアント名`
  - 例：`2026-Q2_Lucido-L`
  - 例：`2026-Q3_Hokkaido-Gyoren`
- 内部ファイル：英数字推奨（日本語可）

## 運用

1. **提案時（5分）**：このフォルダをコピー → meta.yml記入 → deck/に資料配置
2. **結果確定時（10分）**：result.md記入 → meta.ymlのphase更新
3. **月次（30分）**：Claudeに集計依頼 → patterns/に昇格判定
