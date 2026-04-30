"""
HTMLDeck の各スライドから、全要素の座標・色・テキスト・フォント情報を抽出する。
出力: 各スライドごとのJSONファイル（要素リスト）
"""
import asyncio
import json
import re
from pathlib import Path
from playwright.async_api import async_playwright

HTML_PATH = "/home/claude/booking_v9_chholdings.html"
OUTPUT_DIR = Path("/home/claude/extracted")
OUTPUT_DIR.mkdir(exist_ok=True)

# スライドの基準サイズ (16:9, 1280×720)
SLIDE_W = 1280
SLIDE_H = 720

EXTRACT_JS = """
() => {
  const slides = document.querySelectorAll('.slide');
  const result = [];
  
  slides.forEach((slide, idx) => {
    const slideRect = slide.getBoundingClientRect();
    const elements = [];
    
    // 全子孫要素を走査
    function walk(node, depth=0) {
      if (node.nodeType === Node.TEXT_NODE) return;
      if (node === slide) {
        Array.from(node.children).forEach(c => walk(c, depth+1));
        return;
      }
      
      const rect = node.getBoundingClientRect();
      const styles = getComputedStyle(node);
      
      // スライド相対座標
      const x = rect.x - slideRect.x;
      const y = rect.y - slideRect.y;
      const w = rect.width;
      const h = rect.height;
      
      // SVG内要素は別ロジック（スライドのSVGから直接取得するため、ここではdivのみ）
      if (node.tagName === 'svg' || node.closest('svg')) {
        // SVGはスキップ（後で別関数で処理）
        return;
      }
      
      // スキップ条件
      if (w <= 1 || h <= 1) return;
      
      // slide-subtitle は子のspanも統合した一つのテキストとして扱う
      const isSubtitle = node.classList && node.classList.contains('slide-subtitle');
      if (isSubtitle) {
        const fullText = node.textContent.trim();
        if (fullText) {
          elements.push({
            tag: node.tagName,
            cls: node.className,
            x, y, w, h,
            text: fullText,
            isLeaf: true,
            isSubtitle: true,
            bg: styles.backgroundColor,
            color: styles.color,
            fontSize: styles.fontSize,
            fontWeight: styles.fontWeight,
            textAlign: styles.textAlign,
            lineHeight: styles.lineHeight,
            paddingTop: styles.paddingTop,
            paddingLeft: styles.paddingLeft,
            paddingRight: styles.paddingRight,
            paddingBottom: styles.paddingBottom,
            borderRadius: styles.borderRadius,
            borderTopWidth: styles.borderTopWidth,
            borderTopColor: styles.borderTopColor,
            borderLeftWidth: styles.borderLeftWidth,
            borderLeftColor: styles.borderLeftColor,
          });
        }
        return; // 子要素へ降りない
      }
      
      // テキスト（直接の子テキストノード, brは改行に）
      let directText = '';
      Array.from(node.childNodes).forEach(n => {
        if (n.nodeType === Node.TEXT_NODE) {
          const t = n.textContent.trim();
          if (t) directText += (directText ? ' ' : '') + t;
        } else if (n.nodeType === Node.ELEMENT_NODE && n.tagName === 'BR') {
          directText += '\\n';
        }
      });
      directText = directText.trim();
      
      // 子要素にテキスト要素がない場合はリーフテキスト
      const hasChildElement = Array.from(node.children).length > 0;
      
      const bg = styles.backgroundColor;
      const hasBg = bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent';
      const hasBorder = parseFloat(styles.borderTopWidth) + parseFloat(styles.borderRightWidth) + parseFloat(styles.borderBottomWidth) + parseFloat(styles.borderLeftWidth) > 0;
      
      // 記録すべき要素：背景色がある or 罫線がある or 直接テキストがある
      if (hasBg || hasBorder || directText) {
        elements.push({
          tag: node.tagName,
          cls: node.className && typeof node.className === 'string' ? node.className : '',
          x, y, w, h,
          text: directText,
          isLeaf: !hasChildElement,
          bg: bg,
          color: styles.color,
          fontSize: styles.fontSize,
          fontWeight: styles.fontWeight,
          textAlign: styles.textAlign,
          borderRadius: styles.borderRadius,
          borderTopWidth: styles.borderTopWidth,
          borderTopColor: styles.borderTopColor,
          borderLeftWidth: styles.borderLeftWidth,
          borderLeftColor: styles.borderLeftColor,
          paddingTop: styles.paddingTop,
          paddingLeft: styles.paddingLeft,
          paddingRight: styles.paddingRight,
          paddingBottom: styles.paddingBottom,
          lineHeight: styles.lineHeight,
        });
      }
      
      // 再帰
      Array.from(node.children).forEach(c => walk(c, depth+1));
    }
    
    walk(slide);
    
    // SVG内の要素を別途取得
    const svgs = slide.querySelectorAll('svg');
    const svgElements = [];
    svgs.forEach(svg => {
      const svgRect = svg.getBoundingClientRect();
      const svgX = svgRect.x - slideRect.x;
      const svgY = svgRect.y - slideRect.y;
      const svgW = svgRect.width;
      const svgH = svgRect.height;
      const viewBox = svg.getAttribute('viewBox');
      const [vbx, vby, vbw, vbh] = (viewBox || '0 0 1 1').split(/\\s+/).map(Number);
      
      // SVG内座標 → スライド相対座標への変換係数
      const sx = svgW / vbw;
      const sy = svgH / vbh;
      
      // 全rect, text, line, polygon を取得 (getBoundingClientRectで絶対位置)
      svg.querySelectorAll('rect, text, line, polygon, circle').forEach(el => {
        const tag = el.tagName.toLowerCase();
        const item = { tag, svgX: svgX, svgY: svgY, sx: sx, sy: sy };
        const bb = el.getBoundingClientRect();
        const absX = bb.x - slideRect.x;
        const absY = bb.y - slideRect.y;
        
        if (tag === 'rect') {
          item.x = absX;
          item.y = absY;
          item.w = bb.width;
          item.h = bb.height;
          item.fill = el.getAttribute('fill') || 'none';
          item.stroke = el.getAttribute('stroke') || 'none';
          item.strokeWidth = parseFloat(el.getAttribute('stroke-width') || 0);
          item.rx = parseFloat(el.getAttribute('rx') || 0) * sx;
          item.strokeDasharray = el.getAttribute('stroke-dasharray') || '';
        } else if (tag === 'text') {
          // textは中心点を使う
          item.x = absX;
          item.y = absY;
          item.w = bb.width;
          item.h = bb.height;
          item.cx = absX + bb.width / 2;
          item.cy = absY + bb.height / 2;
          item.text = el.textContent;
          item.fill = el.getAttribute('fill') || '#000';
          item.fontSize = parseFloat(el.getAttribute('font-size') || 11) * Math.min(sx, sy);
          item.fontWeight = el.getAttribute('font-weight') || '400';
          item.textAnchor = el.getAttribute('text-anchor') || 'start';
        } else if (tag === 'line') {
          // lineは bb から推定 (transform済み)
          // ただし対角線かも知れないので元の x1,y1,x2,y2 を transformで補正
          // 簡易: bbの2隅を使う (近似)
          // line自体のtransform後の座標を取得するのは難しいので、bb左上→右下で線を引く
          // SVGのlineは水平/垂直/対角しかないので bb から再現可能
          const x1raw = parseFloat(el.getAttribute('x1') || 0);
          const x2raw = parseFloat(el.getAttribute('x2') || 0);
          const y1raw = parseFloat(el.getAttribute('y1') || 0);
          const y2raw = parseFloat(el.getAttribute('y2') || 0);
          // bb から両端を推定:
          // x方向の関係を保つ
          if (x1raw < x2raw) {
            item.x1 = absX;
            item.x2 = absX + bb.width;
          } else if (x1raw > x2raw) {
            item.x1 = absX + bb.width;
            item.x2 = absX;
          } else {
            item.x1 = absX + bb.width / 2;
            item.x2 = absX + bb.width / 2;
          }
          if (y1raw < y2raw) {
            item.y1 = absY;
            item.y2 = absY + bb.height;
          } else if (y1raw > y2raw) {
            item.y1 = absY + bb.height;
            item.y2 = absY;
          } else {
            item.y1 = absY + bb.height / 2;
            item.y2 = absY + bb.height / 2;
          }
          item.stroke = el.getAttribute('stroke') || '#000';
          item.strokeWidth = parseFloat(el.getAttribute('stroke-width') || 1);
          item.strokeDasharray = el.getAttribute('stroke-dasharray') || '';
        } else if (tag === 'polygon') {
          // polygonはbbから矩形領域を推定
          item.x = absX;
          item.y = absY;
          item.w = bb.width;
          item.h = bb.height;
          item.points = el.getAttribute('points') || '';
          item.fill = el.getAttribute('fill') || 'none';
        } else if (tag === 'circle') {
          item.x = absX;
          item.y = absY;
          item.w = bb.width;
          item.h = bb.height;
          item.cx = absX + bb.width / 2;
          item.cy = absY + bb.height / 2;
          item.r = bb.width / 2;
          item.fill = el.getAttribute('fill') || 'none';
          item.stroke = el.getAttribute('stroke') || 'none';
        }
        svgElements.push(item);
      });
    });
    
    const slideStyles = getComputedStyle(slide);
    result.push({
      index: idx,
      slideWidth: slideRect.width,
      slideHeight: slideRect.height,
      slideBackground: slideStyles.backgroundColor,
      htmlElements: elements,
      svgElements: svgElements,
    });
  });
  
  return result;
};
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 1320, "height": 4000})
        page = await context.new_page()
        await page.goto(f"file://{HTML_PATH}")
        await page.wait_for_load_state("networkidle")
        
        # 各スライドを 1280px 幅でレンダリングするため、bodyを直接調整
        await page.add_style_tag(content="""
            body { padding: 0 !important; max-width: 1280px !important; margin: 0 !important; background: #fff !important; }
            .deck-header, .layout-label { display: none !important; }
            .layout-section { margin: 0 !important; padding: 0 !important; }
            .slide { width: 1280px !important; height: 720px !important; aspect-ratio: unset !important; }
        """)
        await page.wait_for_timeout(500)
        
        data = await page.evaluate(EXTRACT_JS)
        await browser.close()
        
        # 各スライドごとに保存
        for slide_data in data:
            idx = slide_data["index"]
            out_path = OUTPUT_DIR / f"slide_{idx:02d}.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(slide_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 抽出完了: {len(data)}枚")
        # サンプル統計
        for sd in data[:3]:
            html_n = len(sd["htmlElements"])
            svg_n = len(sd["svgElements"])
            print(f"  Slide {sd['index']+1}: HTML要素 {html_n}, SVG要素 {svg_n}")

asyncio.run(main())
