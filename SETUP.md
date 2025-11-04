# セットアップ手順

WordPressガジェットブログ自動投稿システムのセットアップ手順です。

## 前提条件

- WordPressサイト: https://wwnaoya.com
- GitHubアカウント
- Python 3.11以上（ローカルテスト用）

## ステップ1: WordPressの設定

### 1.1 WordPress REST APIの有効化確認

ブラウザで以下のURLにアクセスして、JSONレスポンスが返ってくることを確認：

```
https://wwnaoya.com/wp-json/wp/v2/posts
```

### 1.2 Application Passwordの作成

1. WordPressにログイン: https://wwnaoya.com/wp-admin
2. 左メニューから `ユーザー` → `プロフィール` をクリック
3. ページを下にスクロールして `アプリケーションパスワード` セクションを探す
4. 「新しいアプリケーションパスワード名」に `GitHub Actions` と入力
5. `新しいアプリケーションパスワードを追加` ボタンをクリック
6. 表示されたパスワードをコピー（**スペースを削除してください**）
   - 例: `abcd efgh ijkl mnop qrst uvwx` → `abcdefghijklmnopqrstuvwx`

**重要:** このパスワードは一度しか表示されないので、必ず保存してください。

## ステップ2: GitHubリポジトリの作成

### 2.1 新しいリポジトリを作成

1. https://github.com/new にアクセス
2. Repository name: `wordpress-gadget-automation`
3. Description: `WordPressガジェットブログ自動投稿システム`
4. Public/Private を選択
5. `Create repository` をクリック

### 2.2 ローカルリポジトリをプッシュ

以下のコマンドを実行（GitHubユーザー名を置き換えてください）：

```bash
cd wordpress-gadget-automation
git branch -M main
git remote add origin https://github.com/<あなたのユーザー名>/wordpress-gadget-automation.git
git push -u origin main
```

認証が求められたら、GitHubのユーザー名とPersonal Access Tokenを入力してください。

## ステップ3: GitHub Secretsの設定

### 3.1 Secretsページに移動

1. GitHubリポジトリページに移動
2. `Settings` タブをクリック
3. 左サイドバーの `Secrets and variables` → `Actions` をクリック
4. `New repository secret` をクリック

### 3.2 以下の3つのSecretを作成

#### Secret 1: WP_SITE_URL
- Name: `WP_SITE_URL`
- Value: `https://wwnaoya.com`

#### Secret 2: WP_USERNAME
- Name: `WP_USERNAME`
- Value: `WordPressのユーザー名`（管理者権限を持つユーザー）

#### Secret 3: WP_APP_PASSWORD
- Name: `WP_APP_PASSWORD`
- Value: `ステップ1.2で作成したApplication Password（スペースなし）`

## ステップ4: 商品データの準備

### 4.1 商品データファイルの確認

`data/products.json` ファイルには、サンプルのガジェット商品データが既に含まれています。

### 4.2 独自の商品を追加（オプション）

商品を追加する場合は、以下の形式でJSONファイルに追加してください：

```json
{
  "name": "商品名",
  "asin": "AmazonのASINコード",
  "url": "https://www.amazon.co.jp/dp/ASIN",
  "price": "¥価格",
  "category": "PC周辺機器またはPCパーツ",
  "description": "商品の簡単な説明",
  "features": [
    "特徴1",
    "特徴2",
    "特徴3"
  ]
}
```

### 4.3 変更をコミット＆プッシュ

```bash
git add data/products.json
git commit -m "商品データを追加"
git push
```

## ステップ5: GitHub Actionsの有効化とテスト

### 5.1 Actionsタブを確認

1. GitHubリポジトリの `Actions` タブをクリック
2. ワークフローが表示されることを確認

### 5.2 手動で実行してテスト

1. `WordPress Auto Post` ワークフローをクリック
2. 右上の `Run workflow` ボタンをクリック
3. `post_status` で `draft` を選択（下書きとして投稿）
4. `Run workflow` をクリック

### 5.3 実行結果を確認

1. ワークフローの実行が開始されます
2. 完了したら、WordPressの管理画面 → `投稿` → `投稿一覧` で下書きが作成されているか確認
3. 問題なければ、記事を確認して公開できます

## ステップ6: 自動実行の設定

### 6.1 スケジュールの確認

デフォルトでは、毎日午前10時（日本時間）に自動実行されます。

### 6.2 スケジュールの変更（オプション）

実行頻度を変更する場合は、`.github/workflows/auto-post.yml` を編集：

```yaml
schedule:
  - cron: '0 1 * * *'  # UTC 1:00 = JST 10:00
```

cron式の例：
- 毎日正午: `0 3 * * *`
- 週3回（月水金の10時）: `0 1 * * 1,3,5`
- 毎日2回（朝10時、夕方18時）: `0 1,9 * * *`

変更後、コミット＆プッシュ：

```bash
git add .github/workflows/auto-post.yml
git commit -m "スケジュールを変更"
git push
```

## ステップ7: 投稿ステータスの変更

### 下書きから自動公開に変更

デフォルトでは `draft`（下書き）で投稿されます。自動的に公開したい場合は、`.github/workflows/auto-post.yml` を編集：

```yaml
POST_STATUS: ${{ github.event.inputs.post_status || 'publish' }}
```

`'draft'` を `'publish'` に変更します。

**注意:** 自動公開は慎重に行ってください。まずは下書きで運用して、問題ないことを確認してから変更することをおすすめします。

## トラブルシューティング

### エラー: "WordPress接続に失敗しました"

- WP_SITE_URLが正しいか確認
- WP_USERNAMEが正しいか確認
- WP_APP_PASSWORDにスペースが含まれていないか確認
- Application Passwordが有効か確認（WordPressで再生成を試す）

### エラー: "商品データが見つかりません"

- `data/products.json` ファイルが存在するか確認
- JSONファイルの形式が正しいか確認（JSONバリデーターを使用）

### Actions が実行されない

- リポジトリの Settings → Actions → General で、Actionsが有効になっているか確認
- ワークフローファイルのcron式が正しいか確認

### REST APIが無効

- WordPressの設定 → パーマリンク設定 で、パーマリンクが設定されているか確認
- セキュリティプラグインがREST APIをブロックしていないか確認

## 次のステップ

1. 初回は下書きで投稿して、記事の品質を確認
2. 記事テンプレートをカスタマイズ（`src/post_generator.py`）
3. 商品データベースを充実させる
4. 投稿頻度を調整
5. 自動公開を有効化（推奨は下書きで運用）

## サポート

問題が発生した場合は、GitHubリポジトリのIssuesで報告してください。
