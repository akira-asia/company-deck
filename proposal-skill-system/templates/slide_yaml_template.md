# Slide YAML Template

```yaml
deck:
  title: "提案タイトル"
  client: "クライアント名"
  date: "YYYY-MM-DD"
  slides:
    - id: 1
      type: cover
      title: "表紙タイトル"
      message: "この提案で伝えたい一文"
      elements:
        - type: text
          content: "補足テキスト"

    - id: 2
      type: summary
      title: "エグゼクティブサマリー"
      message: "提案全体の要点"
      elements:
        - type: bullets
          items:
            - "課題"
            - "提案"
            - "期待成果"
```
