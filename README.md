# WordPress ガジェットブログ自動投稿システム

GitHub Actionsを使用して、Amazonのガジェット商品レビュー記事を自動的にWordPressブログに投稿するシステムです。

## 機能

- PC周辺機器・PCパーツのレビュー記事を自動生成
- WordPress REST APIを使用した自動投稿
- GitHub Actionsによる定期実行（毎日午前10時）
- 手動実行にも対応
- カテゴリーとタグの自動管理

## セットアップ手順

### 1. WordPressの準備

#### Application Passwordの作成

1. WordPressの管理画面にログイン
2. `ユーザー` → `プロフィール` に移動
3. 下にスクロールして `アプリケーションパスワード` セクションを見つける
4. 新しいアプリケーションパスワード名を入力（例: "GitHub Actions"）
5. `新しいアプリケーションパスワードを追加` をクリック
6. 表示されたパスワードをコピー（スペースは除去してください）

#### REST APIの確認

以下のURLにアクセスして、REST APIが有効か確認してください：
```
https://wwnaoya.com/wp-json/wp/v2/posts
```

### 2. GitHubリポジトリの作成

```bash
cd wordpress-gadget-automation
git init
git add .
git commit -m "Initial commit: WordPress自動投稿システム"
git branch -M main
git remote add origin https://github.com/<あなたのユーザー名>/wordpress-gadget-automation.git
git push -u origin main
```

### 3. GitHub Secretsの設定

GitHubリポジトリの `Settings` → `Secrets and variables` → `Actions` → `New repository secret` で以下を設定：

| Secret名 | 値 |
|---------|---|
| `WP_SITE_URL` | `https://wwnaoya.com` |
| `WP_USERNAME` | WordPressのユーザー名 |
| `WP_APP_PASSWORD` | 作成したApplication Password（スペースなし） |

### 4. 商品データの追加

[data/products.json](data/products.json) に投稿したい商品情報を追加します。

```json
[
  {
    "name": "ロジクール ワイヤレスマウス MX Master 3S",
    "asin": "B0B4DQPH5K",
    "url": "https://www.amazon.co.jp/dp/B0B4DQPH5K",
    "price": "¥14,800",
    "category": "PC周辺機器",
    "description": "高精度センサーと快適なエルゴノミクスデザインを備えたプレミアムワイヤレスマウス",
    "features": [
      "8,000 DPI高精度センサー",
      "最大70日間のバッテリー寿命",
      "静音クリック設計",
      "複数デバイス対応"
    ]
  }
]
```

サンプルデータを生成するには：

```bash
python src/amazon_scraper.py
```

## 使用方法

### 自動実行

GitHub Actionsが毎日午前10時（JST）に自動実行されます。

スケジュールを変更する場合は、[.github/workflows/auto-post.yml](.github/workflows/auto-post.yml) の `cron` 設定を編集してください。

```yaml
schedule:
  - cron: '0 1 * * *'  # UTC 1:00 = JST 10:00
```

### 手動実行

1. GitHubリポジトリの `Actions` タブに移動
2. `WordPress Auto Post` ワークフローを選択
3. `Run workflow` をクリック
4. 投稿ステータス（`draft` または `publish`）を選択
5. `Run workflow` で実行

### ローカルでのテスト

```bash
# 環境変数を設定
export WP_SITE_URL="https://wwnaoya.com"
export WP_USERNAME="あなたのユーザー名"
export WP_APP_PASSWORD="あなたのアプリケーションパスワード"
export POST_STATUS="draft"

# 依存関係のインストール
pip install -r requirements.txt

# 商品データの初期化
python src/amazon_scraper.py

# 記事を投稿
python src/main.py
```

## プロジェクト構成

```
wordpress-gadget-automation/
├── .github/
│   └── workflows/
│       └── auto-post.yml          # GitHub Actionsワークフロー
├── src/
│   ├── wordpress_client.py        # WordPress REST APIクライアント
│   ├── amazon_scraper.py          # Amazon商品データ管理
│   ├── post_generator.py          # ブログ記事生成ロジック
│   └── main.py                    # メインスクリプト
├── data/
│   └── products.json              # 商品データ
├── requirements.txt               # Python依存関係
└── README.md                      # このファイル
```

## カスタマイズ

### 記事テンプレートの変更

[src/post_generator.py](src/post_generator.py) を編集して、記事の構成や文体をカスタマイズできます。

### 投稿頻度の変更

[.github/workflows/auto-post.yml](.github/workflows/auto-post.yml) の `schedule` セクションを編集してください。

例：
- 毎日2回（朝10時、夕方18時）
  ```yaml
  schedule:
    - cron: '0 1 * * *'   # JST 10:00
    - cron: '0 9 * * *'   # JST 18:00
  ```

- 週3回（月・水・金の10時）
  ```yaml
  schedule:
    - cron: '0 1 * * 1,3,5'
  ```

### カテゴリーの追加

商品データの `category` フィールドに新しいカテゴリー名を指定すると、自動的にWordPressに作成されます。

## トラブルシューティング

### 投稿が失敗する場合

1. WordPress REST APIが有効か確認
   ```
   https://wwnaoya.com/wp-json/wp/v2/posts
   ```

2. Application Passwordが正しいか確認
   - スペースが含まれていないか
   - コピーミスがないか

3. GitHub Actionsのログを確認
   - `Actions` タブから実行履歴を確認
   - エラーメッセージを確認

### パーマリンク設定

WordPressの `設定` → `パーマリンク` で、REST APIが正常に動作するように設定してください（デフォルトの `投稿名` 推奨）。

## セキュリティ注意事項

- Application Passwordは必ずGitHub Secretsに保存してください
- Personal Access Tokenをコードに直接書き込まないでください
- 定期的にApplication Passwordをローテーションしてください

## ライセンス

MIT License

## サポート

問題が発生した場合は、GitHubのIssuesで報告してください。
