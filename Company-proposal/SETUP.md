# セットアップ手順

このリポジトリをローカル展開してGitHubにpushするまでの手順。

---

## 前提

- Git がインストール済み（`git --version` で確認）
- GitHubアカウントを保有
- ターミナル（Mac: Terminal / Windows: Git Bash等）が使える

---

## 手順

### Step 1：zipを解凍してフォルダに移動

```bash
# ダウンロードした zip を任意の場所で解凍
unzip Company-proposal.zip
cd Company-proposal
```

### Step 2：GitHubで空のリポジトリを作成

1. GitHubにログイン
2. 右上 [+] → [New repository] をクリック
3. 以下を設定：
   - **Repository name**: `Company-proposal`
   - **Description**: 提案学習ループ構築リポジトリ（任意）
   - **Visibility**: **Private**（クライアント情報を含むため強く推奨）
   - **Initialize options**: ⚠️ README/`.gitignore`/Licenseは **チェックせず空のまま**（既に同梱済み）
4. [Create repository] をクリック

### Step 3：ローカルリポジトリを初期化してpush

GitHubから表示される「…or push an existing repository from the command line」のコマンドを使う。
あきらさんのGitHubユーザー名を `<USERNAME>` に置き換えて実行：

```bash
# Gitリポジトリ初期化
git init
git add .
git commit -m "feat: 初期構成セットアップ"

# ブランチをmainに設定
git branch -M main

# リモート追加（HTTPSの場合）
git remote add origin https://github.com/<USERNAME>/Company-proposal.git

# pushする（SSHを使う場合は git@github.com: 形式で）
git push -u origin main
```

### Step 4：developブランチを作成（推奨）

```bash
git checkout -b develop
git push -u origin develop
```

---

## 認証で躓いたら

### HTTPSでpush時に認証エラーが出る場合

GitHubは2021年からパスワード認証を廃止済み。**Personal Access Token (PAT)** を使用：

1. GitHub → 右上アイコン → Settings → Developer settings
2. Personal access tokens → Tokens (classic) → Generate new token
3. Scope: `repo` にチェック → Generate
4. 表示されたトークンをコピー（**一度きりしか表示されない**）
5. push時にパスワードの代わりにこのトークンを入力

### SSH鍵を使う場合（推奨）

```bash
# SSH鍵がない場合は作成
ssh-keygen -t ed25519 -C "your_email@example.com"

# 公開鍵をコピー
cat ~/.ssh/id_ed25519.pub
```

GitHubの Settings → SSH and GPG keys → New SSH key で公開鍵を登録。

---

## 動作確認

```bash
# ステータス確認
git status

# リモート確認
git remote -v

# ログ確認
git log --oneline
```

GitHubのリポジトリページで全ファイルが見えればセットアップ完了。

---

## 次のステップ

1. README.md を読んで運用ルールを把握
2. 直近3案件を `proposals/` 配下に移行
3. 月次レビュー（毎月1日）をカレンダー登録
