# 商品データ更新ガイド

## 概要

このガイドでは、`data/products.json`の商品データを更新する方法を説明します。

## 更新方法の選択

### 方法A: 自動更新（推奨）

PA-APIから10秒間隔でリクエストを送信し、安全に100個の商品を自動取得します。

**特徴:**
- ✅ 完全自動化
- ✅ レート制限を考慮（PA-API 5.0: 10秒に1リクエスト）
- ✅ GitHub Actionsで実行
- ⏱️ 所要時間: 約17-20分

**実行方法:**
1. GitHubリポジトリの「Actions」タブを開く
2. 「商品データ自動更新（レート制限対応）」を選択
3. 「Run workflow」→「Run workflow」をクリック
4. 完了を待つ（約17-20分）

**注意:**
- PA-API 5.0のレート制限により、100個の商品取得に約17-20分かかります
- GitHub Actionsは30分でタイムアウトするため、十分余裕があります

### 方法B: ローカル実行

ローカル環境でスクリプトを実行して更新します。

**前提条件:**
- Python 3.10以上
- 環境変数の設定（`.env`ファイル）

```bash
# .envファイルの例
AMAZON_ACCESS_KEY=your_access_key
AMAZON_SECRET_KEY=your_secret_key
AMAZON_ASSOCIATE_TAG=your_associate_tag
AMAZON_REGION=jp
```

**実行コマンド:**
```bash
python scripts/refresh_products_slow.py
```

### 方法C: 手動編集

個別の商品を手動で更新する場合に使用します。

## 更新手順

### 方法1: 既存データの一部を更新

既存の100個の商品データから、販売終了や在庫切れの商品のみを最新商品に置き換えます。

1. `data/products.json`を開く
2. 販売終了した商品のASINを確認
3. Amazonで最新の人気商品を検索
4. 新しい商品情報で置き換え

```json
{
  "name": "商品名",
  "asin": "ASIN番号",
  "url": "https://www.amazon.co.jp/dp/ASIN番号",
  "price": "¥XX,XXX",
  "image_url": "商品画像URL",
  "description": "商品説明",
  "category": "PC周辺機器 または PCパーツ",
  "features": [
    "特徴1",
    "特徴2",
    "特徴3"
  ],
  "rating": 4.5
}
```

### 方法2: 全商品データを一括更新

50日ごとに全商品を最新のものに置き換える場合：

1. `scripts/create_curated_products.py`を編集
2. 最新の人気商品100個のデータを記載
3. スクリプトを実行:
   ```bash
   python scripts/create_curated_products.py
   ```
4. 生成されたデータを確認
5. Gitにコミット:
   ```bash
   git add data/products.json data/products_metadata.json
   git commit -m "商品データを更新（2024年XX月版）"
   git push origin main
   ```

## 商品選定のポイント

### 推奨カテゴリー

- **PC周辺機器（60個）**:
  - マウス: 15個
  - キーボード: 15個
  - モニター: 10個
  - ヘッドセット: 5個
  - Webカメラ: 3個
  - スピーカー: 3個
  - その他周辺機器: 9個

- **PCパーツ（40個）**:
  - SSD: 15個
  - メモリ: 10個
  - CPUクーラー: 5個
  - 電源ユニット: 5個
  - PCケース: 3個
  - グラフィックボード: 2個

### 選定基準

1. **大手メーカー製品を優先**:
   - Logicool, Microsoft, Razer, ASUS, Dell, HP
   - Samsung, Crucial, Western Digital, Corsair
   - Intel, AMD, NVIDIA

2. **現在販売中の商品**:
   - Amazonで「在庫あり」の商品
   - 発売から2年以内の製品を推奨

3. **高評価商品**:
   - 評価4.0以上
   - レビュー数100件以上

4. **価格帯のバランス**:
   - 低価格帯（〜¥10,000）: 30%
   - 中価格帯（¥10,000〜¥30,000）: 50%
   - 高価格帯（¥30,000〜）: 20%

## 自動更新の仕組み

### 50日サイクル

システムは以下のように動作します：

1. `data/products_metadata.json`の`last_refresh_date`を確認
2. 50日経過していれば、PA-APIから新商品を自動取得（GitHub Actions実行時）
3. 取得失敗時はローカルデータを維持

### 手動での更新タイミング

以下の場合は手動更新を推奨：

- 季節の変わり目（3月、6月、9月、12月）
- 新製品の大型リリース後
- Amazon Prime Day やブラックフライデー前
- 商品の在庫切れが目立つとき

## トラブルシューティング

### Q: 商品が投稿されない

A: `data/posted_products.json`に全ASINが記録されている可能性があります。
   このファイルを削除するか、空の配列`[]`に上書きしてください。

### Q: 古い商品が投稿される

A: `data/products.json`を最新のものに更新し、コミット・プッシュしてください。

### Q: メタデータをリセットしたい

A: `data/products_metadata.json`を削除するか、以下の内容で上書き:
```json
{
  "last_refresh_date": "2025-01-01T00:00:00.000000"
}
```

## 参考リンク

- [Amazon.co.jp ベストセラー - PC周辺機器](https://www.amazon.co.jp/gp/bestsellers/computers/2127209051)
- [Amazon.co.jp ベストセラー - PCパーツ](https://www.amazon.co.jp/gp/bestsellers/computers/2151981051)
- [価格.com - PC周辺機器](https://kakaku.com/pc/)
