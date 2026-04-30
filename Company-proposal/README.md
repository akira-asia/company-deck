# Company-proposal

提案書ナレッジを「記録 → 抽出 → 適用」の3ステップで資産化するリポジトリ。

> 関連スライド：`docs/提案学習ループ構築_編集可能版.pptx`

---

## ディレクトリ構成

```
Company-proposal/
├── _meta/                        # マスタ定義（タグ辞書・評価ルーブリック）
│   ├── tags.yml
│   └── scoring-rubric.md
├── proposals/                    # 案件ごと（1案件 = 1ディレクトリ）
│   ├── _template/                # 新規案件のテンプレ（ここをコピーして使う）
│   ├── 2026-Q2_案件A/
│   ├── 2026-Q2_案件B/
│   └── 2026-Q2_案件C/
├── patterns/                     # 横串で抽出した勝ち筋
│   ├── by-bm-type/
│   ├── by-industry/
│   └── by-deal-size/
├── templates/                    # 再利用パーツ
│   ├── deck-skeletons/
│   └── analysis-snippets/
└── docs/                         # 運用ドキュメント・スライド
```

---

## 運用フロー（5分・10分・30分の3アクション）

### ① 提案時（5分）

```bash
# 1. テンプレから案件フォルダを作成
cp -r proposals/_template proposals/2026-QX_クライアント名

# 2. meta.yml の基本情報を記入（クライアント名・業界・BM型・予算など）
# 3. 最終提案書を deck/ に格納

git add .
git commit -m "feat: クライアント名 提案完了"
git push
```

### ② 結果確定時（10分）

```bash
# 1. result.md を3行で記入
#    - 結果（受注/失注/保留）
#    - 決定要因（相手が何で決めたか）
#    - 次回への申し送り（流用可能パーツ・追加すべき要素）
# 2. meta.yml の phase / decision_date / score を更新

git add .
git commit -m "feat: クライアント名 受注/失注 記録"
git push
```

### ③ 月次レビュー（30分・毎月1日）

1. 過去30日の `meta.yml` 群を Claude に投入し、BM型・業界別の勝率を集計
2. 受注3件以上の型を `patterns/by-bm-type/` に昇格
3. `templates/deck-skeletons/` を最新版にバージョンアップ

---

## 必須ファイル（2つだけ）

各案件フォルダに必須なのは以下の2ファイルのみ。これ以上のルールは設けない。

- `meta.yml` … クライアント情報・BM型・予算・結果のメタデータ
- `result.md` … 結果と意思決定要因の言語化

---

## ブランチ戦略

- `main` … 確定済み案件（受注/失注確定後）
- `develop` … 進行中案件
- `feature/proposal-XXX` … 個別案件作業ブランチ

PR運用でレビュアーが目を通す運用を推奨。

---

## 関連リンク

- 学習ループ構築スライド： `docs/提案学習ループ構築_編集可能版.pptx`
- タグ辞書：`_meta/tags.yml`
- 評価ルーブリック：`_meta/scoring-rubric.md`
