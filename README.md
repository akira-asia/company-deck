# company-deck

提案資料作成のSkill、プロンプト、テンプレート、参照ルール、変換スクリプトを管理するリポジトリです。

## 目的

- 提案資料作成の品質を安定させる
- AIに渡す指示と判断基準を再利用可能にする
- 実案件から得た学びをSkill・Prompt・Designへ反映する
- 分析資料から骨子、HTMLDeck、編集可能なPPTXまでを段階的に作成できる状態にする

## ディレクトリ構成

```text
proposal-skill-system/
├── SKILL.md
├── DESIGN.md
├── prompts/
│   ├── proposal_creation.md
│   └── proposal_review.md
├── templates/
│   ├── proposal_outline.md
│   └── slide_yaml_template.md
├── references/
│   ├── 01-deck-structure.md
│   ├── 02-content-rules.md
│   ├── 03-widget-flow.md
│   ├── 04-design-system.md
│   ├── 05-pptx-conversion.md
│   ├── 06-pdca-learnings.md
│   └── design-systems/
├── scripts/
│   ├── build_native_pptx.py
│   └── extract_layout.py
├── cases/
└── changelog/
```

## 使い方

1. `proposal-skill-system/SKILL.md` で提案デッキ生成の基本プロセスを確認する
2. `proposal-skill-system/references/` でデッキ構成、コンテンツルール、デザイン、PPTX変換ルールを確認する
3. `proposal-skill-system/prompts/` のプロンプトで骨子作成やレビューを行う
4. `proposal-skill-system/templates/` の型をベースに資料構成を作る
5. `proposal-skill-system/scripts/` でレイアウト抽出やPPTX生成を行う
6. 実案件の入力・出力・レビュー・学びは `proposal-skill-system/cases/` に残す
7. 横断で再利用できる学びは `proposal-skill-system/references/06-pdca-learnings.md` に昇格する

## 更新ルール

- 実案件で再利用価値が確認できた改善のみ共通ルールへ反映する
- `SKILL.md`、`DESIGN.md`、`prompts/`、`references/`、`scripts/` を変更した場合は `proposal-skill-system/changelog/` に記録する
- 案件固有の判断はまず `cases/` に残し、共通化するかは後で判断する
