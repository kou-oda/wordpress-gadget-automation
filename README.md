# WordPress ガジェットブログ自動投稿システム

GitHub Actionsを使用して、Amazonのガジェット商品レビュー記事を自動的にWordPressブログに投稿するシステムです。

## 機能

### コンテンツ生成
- PC周辺機器・PCパーツのレビュー記事を自動生成
- WordPress REST APIを使用した自動投稿
- GitHub Actionsによる定期実行（毎日午前10時・午後8時）
- 手動実行にも対応
- カテゴリーとタグの自動管理
- **投稿済み商品の追跡機能**（同じ商品の重複投稿を防止）
- **商品データ自動更新**（PA-APIから12秒間隔で安全に取得）
- **記事末尾に商品購入リンク表示**（PA-APIリクエスト上限増加に貢献）

### トラフィック増加施策 ⭐NEW
- **X (Twitter)自動投稿**（記事公開後に即座にツイート）
- **Google Indexing API連携**（検索結果への即時反映）
- **Ping送信**（ブログ検索エンジンへの自動通知）
- **SNSマルチ投稿対応**（Zapier/IFTTT連携可能）

詳細は [TRAFFIC_STRATEGY.md](TRAFFIC_STRATEGY.md) を参照してください。

### AI支援のワークフロー修正 🤖NEW
- **Claude Code Bot**（IssueコメントでAIがコード修正）
- **GitHub Actions統合**（自動プッシュ・自動テスト対応）
- **簡単なセットアップ**（4ステップで導入完了）

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

### 3. Amazon PA-APIの設定

Amazon Associate（アソシエイト）アカウントでPA-APIの認証情報を取得します：

1. [Amazon Associate Central](https://affiliate.amazon.co.jp/)にログイン
2. `ツール` → `Product Advertising API` に移動
3. Access KeyとSecret Keyを取得
4. Associate Tag（トラッキングID）を確認

### 4. GitHub Secretsの設定

GitHubリポジトリの `Settings` → `Secrets and variables` → `Actions` → `New repository secret` で以下を設定：

| Secret名 | 値 |
|---------|---|
| `WP_SITE_URL` | `https://wwnaoya.com` |
| `WP_USERNAME` | WordPressのユーザー名 |
| `WP_APP_PASSWORD` | 作成したApplication Password（スペースなし） |
| `AMAZON_ACCESS_KEY` | Amazon PA-APIのAccess Key |
| `AMAZON_SECRET_KEY` | Amazon PA-APIのSecret Key |
| `AMAZON_ASSOCIATE_TAG` | AmazonアソシエイトのトラッキングID |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Google Service AccountのJSONキー（Google Indexing API用） |

### 5. 動作確認

**PA-APIを使用する場合**（推奨）：
- 毎日自動的にAmazonから大手メーカーの商品を検索して投稿
- 手動でのデータ追加は不要

**ローカルデータを使用する場合**（フォールバック）：
- PA-APIが利用できない場合は、[data/products.json](data/products.json)のデータを使用
- サンプルデータを生成: `python src/amazon_scraper.py`

### 6. 商品データ更新機能

#### 自動更新（推奨）

GitHub Actionsで商品データを自動更新できます：

1. GitHubリポジトリの「Actions」タブを開く
2. 「商品データ自動更新（レート制限対応）」を選択
3. 「Run workflow」→「Run workflow」をクリック

**特徴:**
- PA-APIから12秒間隔でリクエスト送信（PA-API 5.0: 10秒 + 安全マージン2秒）
- 100個の最新商品を自動取得（所要時間: 約20-25分）
- 既存データを自動バックアップ
- カテゴリー別の集計表示

**レート制限について:**
- PA-API 5.0の制限: 10秒に1リクエスト
- 安全のため12秒間隔に設定（2秒のマージン）
- リクエスト上限は商品購入により増加

詳細は [PRODUCT_UPDATE_GUIDE.md](PRODUCT_UPDATE_GUIDE.md) を参照してください。

### 7. Google Indexing APIの設定（オプション）

Google Indexing APIを使用すると、記事公開後すぐにGoogleにクロールをリクエストできます。

#### Google Cloud Platformでの設定

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. 新しいプロジェクトを作成（またはg既存のプロジェクトを選択）
3. **APIとサービス** → **ライブラリ** に移動
4. 「Indexing API」を検索して有効化
5. **認証情報** → **認証情報を作成** → **サービスアカウント** を選択
6. サービスアカウント名を入力（例：`wordpress-indexing-bot`）
7. 作成したサービスアカウントをクリック
8. **キー** タブ → **鍵を追加** → **新しい鍵を作成** → **JSON** を選択
9. ダウンロードされたJSONファイルの内容をコピー

#### Search Consoleでの設定

1. [Google Search Console](https://search.google.com/search-console)にアクセス
2. 対象のプロパティを選択
3. **設定** → **ユーザーと権限** に移動
4. **ユーザーを追加** をクリック
5. サービスアカウントのメールアドレス（`xxxxx@xxxxx.iam.gserviceaccount.com`）を入力
6. 権限を「所有者」に設定して追加

#### GitHub Secretsに追加

GitHubリポジトリの `Settings` → `Secrets and variables` → `Actions` で以下を追加：

| Secret名 | 値 |
|---------|---|
| `GOOGLE_SERVICE_ACCOUNT_JSON` | ダウンロードしたJSONファイルの内容全体 |

#### 動作確認

1. GitHubリポジトリの `Actions` タブを開く
2. `Scheduled Google Indexing` ワークフローを選択
3. `Run workflow` をクリックして手動実行
4. ワークフローが成功すれば、設定完了です

**機能:**
- 毎日JST 9:00に自動実行
- 最新10件の公開済み記事をGoogle Indexing APIに送信
- レート制限対策：2秒間隔で送信（1日200リクエスト制限）
- 成功・失敗の詳細なログ出力

#### データファイル

- `data/products.json`: 商品データ（100個）
- `data/posted_products.json`: 投稿済み商品のASINリスト（ローカルのみ）
- `data/products_metadata.json`: 最終更新日とリフレッシュ回数

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
│       ├── auto-post.yml                      # WordPress自動投稿
│       ├── scheduled-google-indexing.yml      # Google Indexing API
│       ├── scheduled-twitter-post.yml         # X(Twitter)自動投稿
│       ├── ping-submit.yml                    # Ping送信
│       ├── bulk-twitter-post.yml              # 一括Twitter投稿
│       ├── refresh-products-slow.yml          # 商品データ更新
│       └── claude-code-bot.yml                # Claude Code Bot（AI支援）
├── src/
│   ├── wordpress_client.py        # WordPress REST APIクライアント
│   ├── amazon_scraper.py          # Amazon商品データ管理
│   ├── post_generator.py          # ブログ記事生成ロジック
│   └── main.py                    # メインスクリプト
├── data/
│   └── products.json              # 商品データ
├── scripts/                       # 各種スクリプト
├── requirements.txt               # Python依存関係
├── README.md                      # このファイル
├── SETUP.md                       # 詳細なセットアップガイド
├── TRAFFIC_STRATEGY.md            # トラフィック増加戦略
└── PRODUCT_UPDATE_GUIDE.md        # 商品データ更新ガイド
```

## Claude Code Botによるワークフロー修正 🤖

IssueコメントでAIにワークフローを修正してもらう機能です。Claude Code（Maxプラン）を使用します。

### 導入に必要な4つのステップ

#### ステップ1：認証トークンの生成（手元のPCで実行）

まず、GitHub Actions（無人のロボット）に「あなたのアカウントですよ」と証明させるための「合鍵（OAuthトークン）」を、手元のPCで発行します。

**前提条件：**
- 手元のPCに `claude-code` CLI がインストールされていること
- `claude-code` CLIで、Maxプランのアカウントにログイン済みであること

**手順：**

1. 手元のPCでターミナル（コマンドプロンプトやPowerShellなど）を開きます

2. 以下のコマンドを実行します：
   ```bash
   claude setup-token
   ```

3. ブラウザが自動で開き、Anthropicの認証画面が表示されます。ログインと承認を求められるので、許可してください

4. 認証が完了すると、ターミナルに `claudecode_oauth_...` から始まる非常に長い文字列（これが認証トークン）が表示されます

5. この文字列（トークン）をすべてコピーし、安全な場所に一時的にメモします

#### ステップ2：GitHubリポジトリに「合鍵」を登録

次に、自動化したいGitHubリポジトリに、発行した「合鍵（トークン）」を安全に登録します。

1. 自動化したいプライベートリポジトリをGitHubで開きます

2. `Settings` タブ → `Secrets and variables` → `Actions` を選択します

3. `Repository secrets` のセクションにある `New repository secret` ボタンをクリックします

4. 以下の2項目を入力します：
   - **Name**: `CLAUDE_CODE_OAUTH_TOKEN`
     （この名前は後でYAMLファイルが参照するので、一字一句正確に）
   - **Secret**: ステップ1でコピーした長いトークン文字列 (`claudecode_oauth_...`) を貼り付けます

5. `Add secret` ボタンを押して保存します

#### ステップ3：ワークフローファイル (.yml) の作成

このリポジトリには既に `.github/workflows/claude-code-bot.yml` が含まれています。

このファイルがGitHubにプッシュされていることを確認してください。

**ワークフローの動作:**
- Issueにコメントが作成されたら起動
- コメントが `@claude` で始まる場合のみ実行
- AIがコードを修正して自動的にコミット＆プッシュ
- Issue に結果を報告

#### ステップ4：動作確認

1. このリポジトリで、テスト用のIssueを作成します（例：「テストIssue」）

2. 作成したIssueのコメント欄に、以下のように書き込んで送信します：
   ```
   @claude README.mdに「こんにちは、世界！」と追記してください。
   ```

3. リポジトリの `Actions` タブを開きます

4. `Claude Code Issue Bot (Max Plan)` というワークフローが実行中（または実行完了）になっていることを確認します

5. ワークフローがエラーなく完了すると、数分後に「Claude Code Bot」という名前で新しいコミットがプッシュされ、README.mdが書き換わっているはずです

### 使用例

**ワークフローを修正する場合：**
```
@claude scheduled-google-indexing.ymlのcron設定を毎日午後6時（JST）に変更してください。
```

**新しい機能を追加する場合：**
```
@claude WordPress投稿後にSlackに通知を送る機能を追加してください。
```

**バグ修正：**
```
@claude main.pyのエラーハンドリングを改善してください。例外が発生した場合にログを出力するようにしてください。
```

### 注意事項

- Claude Code Botは**Maxプラン**が必要です
- プライベートリポジトリでの使用を推奨します（トークン漏洩防止）
- AIによる変更は自動的にコミットされますが、必ず内容を確認してください
- 大規模な変更の場合は、段階的に指示を出すことをおすすめします

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
