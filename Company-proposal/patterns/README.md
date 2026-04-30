# patterns/

横串で抽出した勝ち筋・負け筋の台帳。

## ファイル構成

- `by-bm-type/` … ビジネスモデル型別パターン
- `by-industry/` … 業界別パターン
- `by-deal-size/` … 案件規模別パターン

## 昇格ルール

`_meta/scoring-rubric.md` 参照。

サマリ：

- BM型ベース：同BM型で **2件以上Score4以上の受注** → `by-bm-type/`
- 業界ベース：同業界で **3件以上Score3以上の提案実績** → `by-industry/`
- 規模ベース：同deal_sizeで **3件以上の受注実績** → `by-deal-size/`

## ファイル命名

- BM型：`d2c-brand-cocreation.md`（小文字+ハイフン）
- 業界：`cosmetics-haircare.md`
- 規模：`size-L.md`

## 推奨フォーマット（テンプレ）

各パターン.mdは以下の構成で書くこと：

```markdown
# [型名] 勝ちパターン v1.0

## 受注実績：X/Y件（XX%）

## 必勝アセット
- ...

## 失注時の不足アセット
- ...

## 推奨スライド構成
1. ...

## 価格レンジ
- 受注帯：...
- 失注帯：...

## 関連案件
- proposals/...
```

## 月次更新フロー

1. 過去30日のmeta.yml集計をClaudeに依頼
2. 昇格基準を満たす型を判定
3. 該当パターン.mdを新規作成 or バージョンアップ
4. `templates/deck-skeletons/` への反映可否を判断
