# HTML → 編集可能PPTX 変換手順（ネイティブシェイプ方式）

STEP 3 で HTMLDeck から **編集可能なPPTX** を生成する手順。

---

## 設計原則（ユーザー要件由来 / 絶対要件）

このSKILLのPPTX生成は以下2点を **絶対要件** として遵守する：

1. **編集可能なPPT**：すべての要素は PPTXネイティブシェイプ／テキストフレームとして配置する。背景画像（PNG焼き込み）は使わない。
2. **オブジェクトに直接文字を書く**：rect等のシェイプの上にテキストを重ねるのではなく、シェイプの `text_frame` にテキストを直接埋め込む。テキストボックスを別レイヤーで重ねる旧方式は禁止。

これにより、PowerPoint で開いた時にすべてのテキスト・色・サイズが編集可能になる。

---

## 入出力

| 種類 | パス |
|---|---|
| 入力 | `/mnt/user-data/outputs/proposal_v[N]_19pages.html` |
| 出力 | `/mnt/user-data/outputs/proposal_v[N]_19pages.pptx` |
| 中間 | `/home/claude/extracted/slide_XX.json` (19ファイル) |

---

## アーキテクチャ

```
HTMLDeck (.html)
    │
    ├─► [STEP A] scripts/extract_layout.py
    │   Playwright で HTML を 1280×720 でレンダリング
    │   getBoundingClientRect() で全要素の絶対座標・色・テキスト・フォントを抽出
    │   → /home/claude/extracted/slide_XX.json
    │
    └─► [STEP B] scripts/build_native_pptx.py
        各JSONを読み、python-pptxで16:9のPPTXを生成
        ・HTML <div> → 矩形シェイプ + text_frame
        ・SVG <rect> → 矩形シェイプ
        ・SVG <text> → 親rectのtext_frameに統合（textの中心点でrect内判定）
        ・SVG <line> → 直線シェイプ
        ・SVG <polygon> → 三角形シェイプ（矢印先端）
        ・SVG <circle> → 楕円シェイプ
        → proposal_v[N]_19pages.pptx
```

---

## STEP A: レイアウト抽出 (extract_layout.py)

```bash
cd /home/claude
python3 /path/to/skill/scripts/extract_layout.py
```

**スクリプトの動作**：

1. Playwright で chromium を起動、HTMLをロード
2. CSS注入で各 `.slide` を 1280×720 固定サイズにレンダリング
3. JS evaluate で全 HTML要素 + SVG内要素の bbox・スタイル情報を取得
4. 1スライドにつき1JSONとして `extracted/slide_XX.json` に保存

**抽出データ**：

| 要素 | 抽出データ |
|---|---|
| HTML要素 (div, span等) | x, y, w, h（slide相対）, text, bg, color, fontSize, fontWeight, textAlign, borderRadius, border系, padding系 |
| SVG `<rect>` | bbox(transform反映), fill, stroke, strokeWidth, rx, strokeDasharray |
| SVG `<text>` | bbox + center点 (cx, cy), text, fill, fontSize, fontWeight, textAnchor |
| SVG `<line>` | x1,y1,x2,y2（bboxから復元）, stroke, strokeWidth, strokeDasharray |
| SVG `<polygon>` | bbox, points, fill |
| SVG `<circle>` | bbox + center (cx, cy), r, fill, stroke |
| スライドルート | slideBackground (root の background-color) |

**重要な実装ポイント**：

- `.slide-subtitle` は子の `<span>` を含めた `textContent` を一括取得し、子へは降りない（二重表示防止）
- `<br>` は `\n` として directText に含める
- SVG内要素は `getBoundingClientRect()` を使って `<g transform>` を反映した絶対位置で取得
- HTML要素の `directText` がある場合は `isLeaf` でなくても登録（spanを含む親div対応）

---

## STEP B: ネイティブPPTX生成 (build_native_pptx.py)

```bash
python3 /path/to/skill/scripts/build_native_pptx.py
```

スライドは 16:9 (13.33in × 7.5in)。1px = 13.33/1280 inch でEMU変換。

### 変換ルール

#### 1. スライドルート背景

`slideBackground` が白以外なら、スライド全面に背景矩形を最初に配置（黒背景の表紙対応）。

#### 2. HTML要素

| 条件 | 処理 |
|---|---|
| 背景色あり or 罫線あり | 矩形シェイプを作成、`text_frame` にテキスト埋め込み |
| 背景なし、罫線なし、テキストあり | テキストボックス単独配置（小フォント<13pxは `word_wrap=False`、幅1.15倍） |
| `cls == "slide"` または スライド全体サイズ | スキップ（背景はSTEP 0で塗り済み） |

`borderLeftWidth > 0` だけの場合は、左に細い縦線シェイプを別途追加（引用ボックス対応）。

#### 3. SVG `<rect>` → 矩形シェイプ

- `rx > 1` なら `MSO_SHAPE.ROUNDED_RECTANGLE`、それ以外は `MSO_SHAPE.RECTANGLE`
- 塗り・枠線・dash を適用
- `rect_to_shape` 辞書に保存（後でテキスト統合時に参照）

#### 4. SVG `<text>` → 親rectのtext_frameに統合（要件の核）

**判定ロジック**：textの中心点 (cx, cy) が rect の境界内にある場合、その rect の text_frame に paragraph として追加。

```python
# textの中心点でrect内判定（text-anchor補正不要）
candidates = []
for rect in rects:
    if rect.x <= text.cx <= rect.x + rect.w and \
       rect.y <= text.cy <= rect.y + rect.h:
        candidates.append((rect.area, rect))

if candidates:
    # 最も小さいrect（最も内側）を選択 → text_frameに統合
    smallest_rect = min(candidates, key=lambda c: c[0])
    add_paragraph_to_shape(smallest_rect, text)
else:
    # どのrectにも含まれない → 独立textboxとして配置
    add_textbox(slide, text)
```

これにより「シェイプにテキストを直接書く」原則が達成される。テキストボックスを別レイヤーで重ねない。

#### 5. SVG `<line>` → 直線シェイプ

`MSO_CONNECTOR.STRAIGHT` で配置。dash対応（`dash_style = 7`）。

#### 6. SVG `<polygon>` → 三角形シェイプ（矢印先端）

`MSO_SHAPE.RIGHT_TRIANGLE` で bbox に配置。

#### 7. SVG `<circle>` → 楕円シェイプ

`MSO_SHAPE.OVAL` で配置。`rect_to_shape` にも登録（中心テキストを内包できる）。

---

## 自己チェック（生成後）

```python
from pptx import Presentation

prs = Presentation(output_pptx_path)
assert len(prs.slides) == 19, "スライド枚数不一致"
assert abs(prs.slide_width.inches - 13.33) < 0.05, "16:9でない"

total_shapes = 0
total_text = 0
for slide in prs.slides:
    total_shapes += len(slide.shapes)
    total_text += sum(1 for s in slide.shapes if s.has_text_frame and s.text_frame.text.strip())

assert total_shapes >= 500, f"シェイプ数が少なすぎる ({total_shapes})"
assert total_text / total_shapes > 0.5, "テキスト付きシェイプ比率が低い（要件違反の可能性）"
```

参考実績（Booking.com 19枚 + CH Holdings デザイン）：
- 合計シェイプ数: 626
- テキスト付きシェイプ: 450（約72%）

---

## 視覚QA（pptx skill 推奨フロー）

```bash
python3 /mnt/skills/public/pptx/scripts/office/soffice.py \
    --headless --convert-to pdf $PPTX --outdir /home/claude/
pdftoppm -jpeg -r 100 /home/claude/$BASENAME.pdf /home/claude/slide
ls /home/claude/slide-*.jpg
```

`view` ツールで視覚確認：

- [ ] スライドレベルの背景色が出ている（特に表紙の黒背景）
- [ ] タイトル・メインメッセージが見える
- [ ] アクセント色（CH Holdings ティール等）が正しく適用
- [ ] フッター帯（ティール6px等）がある
- [ ] テキストが折り返しで切れていない
- [ ] シェイプとテキストが重ならない（オブジェクト内統合済み）
- [ ] 矢印先端（polygon）の位置が正しい

問題があれば、修正は **HTML側** で行い、再度 STEP A → STEP B を実行する。

---

## 既知の制約

| 制約 | 対処 |
|---|---|
| グラデーション・シャドウは再現不可 | フラットデザインに統一済（02-content-rules.md） |
| SVGの複雑なpath/curve | rect/text/line/polygon/circle のみサポート。pathは無視 |
| `transform="rotate(N)"` の回転 | 現状未対応。回転矢印は使わない |
| 一部のSVG内textが座標判定で消失 | PowerPointで開いて手動補正 |
| ベクトルアイコン（lucide等） | 絵文字 + テキストで代替 |
| フォントの完全一致 | 'Hiragino Sans' を指定。環境にない場合はOSデフォルトに |

---

## scripts/ に同梱されているもの

このSKILLには動作確認済みの2つのスクリプトが同梱されている：

```
proposal-deck-from-analysis/
└── scripts/
    ├── extract_layout.py      # Playwrightで HTML → JSON抽出
    └── build_native_pptx.py   # JSON → 編集可能PPTX 生成
```

両者とも Booking.com 19枚提案書 + CH Holdings デザインで動作実証済み（19枚で 626ネイティブシェイプ、450テキスト付き）。新規案件でも同じスクリプトで動く。

入出力パスはスクリプト先頭の定数で指定：

```python
# extract_layout.py
HTML_PATH = "/home/claude/booking_v9_chholdings.html"  # ← 案件ごとに変更
OUTPUT_DIR = Path("/home/claude/extracted")

# build_native_pptx.py
EXTRACTED_DIR = Path("/home/claude/extracted")
OUTPUT_PPTX = "/mnt/user-data/outputs/booking_v9_chholdings_19pages.pptx"  # ← 案件ごとに変更
```

---

## 旧方式（PNG背景貼り付け）は使用禁止

過去の提案書ビルダーで使われていた「スライド全体をPNGで背景貼り付け、ノートに編集メモを書く」方式は **使用禁止**。

理由：
- PNG焼き込みのテキストは編集不可
- ユーザー要望「編集可能なpptにして欲しい」「オブジェクトに直接文字を書く」に違反

過去にこの方式で作ったPPTXがあれば、必ず本SKILLのネイティブ方式で作り直すこと。
