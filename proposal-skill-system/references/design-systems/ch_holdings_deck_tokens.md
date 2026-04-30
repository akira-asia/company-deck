---
# ============================================================
# LAYER 2: Design Tokens（deck-md-builder Skill 出力範囲）
# Source: CH_Holdings_11th_Company_Pitch_ver1_1.pdf
# Generated: 2026-04-30
# ============================================================
design_tokens:
  colors:
    main: "#1A1A1A"          # テキスト・ダーク背景・タイトルスライド
    accent: "#0EBAB5"        # タイトル・強調・フッター帯・カードヘッダー
    warning: "#E04E49"       # 課題・リスク・機会損失強調
    sub: "#F2F2F2"           # 背景カード・グレーヘッダー
    text_secondary: "#555555"
    border: "#C0C0C0"
  
  typography:
    font_family: "'Hiragino Sans', 'Yu Gothic UI', 'Noto Sans JP', sans-serif"
    base_size: "11px"
    title_size: "26px"
    subtitle_size: "15px"
    title_weight: "700"      # 太字傾向（ゴシック）
  
  layout:
    header_style: "white_with_teal_title"   # 白背景＋ティール色のスライドタイトル
    title_slide_style: "black_band"          # 表紙等は黒背景＋白文字
    accent_shape: "rounded_4px"              # カード・ボタン
    icon_shape: "circle"                      # ステップアイコン・バッジは真円
    background: "plain"                       # 無地基調
    logo_position: "footer_center"
  
  footer:
    text: "CH Holdings / 2026"
    page_format: "{page} / {total}"
    band_color: "accent"                      # フッター帯はaccent色のソリッド帯
    band_height: "8px"

# ============================================================
# LAYER 1, 3 はこのSkillの対象外
# 別途 consulting-slide-builder などでコンテンツを追記してください
# ============================================================
---

<!-- このdeck.mdはデザイントークンのみが定義されています。
     スライドコンテンツ（LAYER 1: メタ情報, LAYER 3: スライド本文）は
     consulting-slide-builder Skill などで追記してください。
     
     抽出元: CH_Holdings_11th_Company_Pitch_ver1_1.pdf
     主要な視覚的特徴:
     - ティール（#0EBAB5）を全編アクセントとして統一使用
     - フッター帯（ソリッド）でブランド一貫性を担保
     - 課題セクションは赤（#E04E49）で警告色を明示
     - 表紙・章扉は黒背景、本文ページは白背景の2系統 -->
