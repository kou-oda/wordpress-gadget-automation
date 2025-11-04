#!/usr/bin/env python3
"""
PA-APIレート制限を考慮した商品データ更新スクリプト
10秒間隔でリクエストを送信し、安全に100個の商品を取得
（PA-API 5.0の制限: 10秒に1リクエスト）
"""
import os
import sys
import json
import time
from datetime import datetime

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from amazon_paapi_client import AmazonPAAPIClient
from amazon_scraper import AmazonProductManager


def main():
    """メイン処理"""
    print("=" * 70)
    print("PA-APIから現在販売中の商品を100個取得します")
    print("レート制限を考慮し、10秒間隔でリクエストを送信します")
    print("（PA-API 5.0の制限: 10秒に1リクエスト）")
    print("=" * 70)

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
        print("PA-APIクライアントを初期化中...")
        paapi_client = AmazonPAAPIClient()
        print("✓ PA-APIクライアントの初期化に成功しました\n")

        # 商品を取得（レート制限を考慮）
        print("商品検索を開始します（10秒間隔）...")
        print("推定所要時間: 約17-20分\n")

        new_products = []
        categories = list(paapi_client.SEARCH_KEYWORDS.keys())
        total_requests = 0
        start_time = time.time()

        for category_idx, category in enumerate(categories):
            keywords = paapi_client.SEARCH_KEYWORDS[category]
            print(f"\n[{category_idx + 1}/{len(categories)}] カテゴリー: {category}")

            for keyword_idx, keyword in enumerate(keywords):
                if len(new_products) >= 100:
                    print(f"\n✓ 目標の100個に到達しました")
                    break

                # リクエスト前に待機（最初のリクエストは待機不要）
                if total_requests > 0:
                    wait_time = 10.0  # PA-API 5.0の制限: 10秒に1リクエスト
                    elapsed = time.time() - start_time
                    expected_time = total_requests * wait_time
                    if elapsed < expected_time:
                        sleep_time = expected_time - elapsed
                        print(f"  ⏳ {sleep_time:.1f}秒待機中...", end='\r')
                        time.sleep(sleep_time)

                # 商品検索実行
                print(f"  [{keyword_idx + 1:2d}/{len(keywords):2d}] '{keyword}' を検索中...", end=' ')

                try:
                    products = paapi_client.search_products(
                        keyword=keyword,
                        category=category,
                        max_results=5  # 各キーワードから5個まで取得
                    )
                    total_requests += 1

                    if products:
                        # 重複チェックしながら追加
                        existing_asins = {p.asin for p in new_products}
                        unique_new = [p for p in products if p.asin not in existing_asins]
                        new_products.extend(unique_new)

                        print(f"✓ {len(unique_new)}個取得 (合計: {len(new_products)}個)")
                    else:
                        print("商品なし")

                except Exception as e:
                    print(f"✗ エラー: {str(e)[:50]}")
                    # エラー後も続行
                    continue

            if len(new_products) >= 100:
                break

        elapsed_time = time.time() - start_time
        print(f"\n" + "=" * 70)
        print(f"検索完了: {total_requests}回のリクエスト、{elapsed_time:.1f}秒経過")
        print("=" * 70)

        if len(new_products) == 0:
            print("エラー: 商品を取得できませんでした。")
            sys.exit(1)

        # 100個に制限
        final_products = new_products[:100]
        print(f"\n✓ {len(final_products)}個の商品を取得しました")

        # 商品データを保存
        products_file = os.path.join(
            os.path.dirname(__file__),
            '..',
            'data',
            'products.json'
        )

        product_manager = AmazonProductManager(products_file)

        # 既存の商品データをバックアップ
        backup_file = products_file + '.backup'
        if os.path.exists(products_file):
            import shutil
            shutil.copy(products_file, backup_file)
            print(f"✓ 既存データをバックアップしました: {backup_file}")

        # 新しい商品データを保存
        product_manager.products = final_products
        product_manager.save_products()
        print(f"✓ 商品データを保存しました: {products_file}")

        # メタデータを更新
        metadata = {
            'last_refresh_date': datetime.now().isoformat(),
            'refresh_count': product_manager.load_metadata().get('refresh_count', 0) + 1,
            'auto_refresh': True,
            'total_requests': total_requests,
            'elapsed_seconds': int(elapsed_time)
        }
        product_manager.save_metadata(metadata)
        print("✓ メタデータを更新しました")

        # 投稿済み商品履歴をクリア
        product_manager.posted_asins = []
        product_manager.save_posted_asins()
        print("✓ 投稿済み商品履歴をクリアしました")

        print("\n" + "=" * 70)
        print("商品データの更新が完了しました！")
        print("=" * 70)

        # カテゴリー別に集計
        category_counts = {}
        for p in final_products:
            category_counts[p.category] = category_counts.get(p.category, 0) + 1

        print(f"\n商品の内訳:")
        for category, count in sorted(category_counts.items()):
            print(f"  {category}: {count}個")
        print(f"\n総計: {len(final_products)}個")

        # 統計情報
        print(f"\n統計情報:")
        print(f"  総リクエスト数: {total_requests}回")
        print(f"  所要時間: {elapsed_time:.1f}秒 ({elapsed_time/60:.1f}分)")
        print(f"  平均間隔: {elapsed_time/total_requests:.2f}秒/リクエスト")

        return 0

    except KeyboardInterrupt:
        print("\n\n中断されました。")
        print("部分的に取得した商品データは保存されていません。")
        sys.exit(1)

    except Exception as e:
        print(f"\nエラー: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
