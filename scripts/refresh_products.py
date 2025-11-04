#!/usr/bin/env python3
"""
現在販売中の商品を100個取得してローカルデータに保存するスクリプト
"""
import os
import sys
import json

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from amazon_paapi_client import AmazonPAAPIClient
from amazon_scraper import AmazonProductManager


def main():
    """メイン処理"""
    print("=" * 60)
    print("現在販売中の商品を100個取得します")
    print("=" * 60)

    # 環境変数チェック
    required_vars = ['AMAZON_ACCESS_KEY', 'AMAZON_SECRET_KEY', 'AMAZON_ASSOCIATE_TAG']
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        print(f"エラー: 以下の環境変数が設定されていません:")
        for var in missing:
            print(f"  - {var}")
        print("\n.envファイルを作成するか、環境変数を設定してください。")
        sys.exit(1)

    print("✓ PA-API認証情報が設定されています\n")

    try:
        # PA-APIクライアント初期化
        paapi_client = AmazonPAAPIClient()
        print("✓ PA-APIクライアントの初期化に成功しました\n")

        # 商品を取得
        print("商品検索を開始します...")
        new_products = []
        categories = list(paapi_client.SEARCH_KEYWORDS.keys())

        for category in categories:
            keywords = paapi_client.SEARCH_KEYWORDS[category]
            print(f"\nカテゴリー: {category}")

            for keyword in keywords:
                if len(new_products) >= 100:
                    break

                print(f"  検索キーワード: {keyword}", end=" ... ")
                products = paapi_client.search_products(keyword, category, max_results=3)

                if products:
                    new_products.extend(products)
                    print(f"✓ {len(products)}個取得 (合計: {len(new_products)}個)")
                else:
                    print("商品なし")

            if len(new_products) >= 100:
                break

        # 重複を削除（ASINベース）
        print("\n重複を削除中...")
        seen_asins = set()
        unique_products = []
        for p in new_products:
            if p.asin not in seen_asins:
                seen_asins.add(p.asin)
                unique_products.append(p)

        # 100個に制限
        final_products = unique_products[:100]

        print(f"✓ 重複削除後: {len(final_products)}個の商品")

        # 商品データを保存
        products_file = os.path.join(
            os.path.dirname(__file__),
            '..',
            'data',
            'products.json'
        )

        product_manager = AmazonProductManager(products_file)
        product_manager.products = final_products
        product_manager.save_products()

        print(f"\n✓ {len(final_products)}個の商品を保存しました: {products_file}")

        # メタデータを更新
        from datetime import datetime
        metadata = {
            'last_refresh_date': datetime.now().isoformat(),
            'refresh_count': product_manager.load_metadata().get('refresh_count', 0) + 1,
            'manual_refresh': True
        }
        product_manager.save_metadata(metadata)
        print("✓ メタデータを更新しました")

        # 投稿済み商品履歴をクリア
        product_manager.posted_asins = []
        product_manager.save_posted_asins()
        print("✓ 投稿済み商品履歴をクリアしました")

        print("\n" + "=" * 60)
        print("商品データの更新が完了しました！")
        print("=" * 60)
        print(f"\n商品の内訳:")

        # カテゴリー別に集計
        category_counts = {}
        for p in final_products:
            category_counts[p.category] = category_counts.get(p.category, 0) + 1

        for category, count in sorted(category_counts.items()):
            print(f"  {category}: {count}個")

        print(f"\n総計: {len(final_products)}個")

        return 0

    except Exception as e:
        print(f"\nエラー: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
