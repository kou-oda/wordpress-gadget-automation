#!/usr/bin/env python3
"""
WordPress ガジェットブログ自動投稿スクリプト
"""

import os
import sys
import time
from wordpress_client import WordPressClient
from amazon_scraper import AmazonProductManager, GadgetProduct
from post_generator import BlogPostGenerator


def main():
    """メイン処理"""

    # 環境変数から設定を取得
    wp_site_url = os.getenv('WP_SITE_URL', 'https://wwnaoya.com')
    wp_username = os.getenv('WP_USERNAME')
    wp_app_password = os.getenv('WP_APP_PASSWORD')
    post_status = os.getenv('POST_STATUS', 'draft')  # draft または publish

    # 必須環境変数のチェック
    if not wp_username or not wp_app_password:
        print("エラー: WP_USERNAME と WP_APP_PASSWORD の環境変数を設定してください。")
        sys.exit(1)

    print(f"WordPress サイト: {wp_site_url}")
    print(f"投稿ステータス: {post_status}")
    print("-" * 50)

    # WordPress クライアント初期化
    try:
        wp_client = WordPressClient(wp_site_url, wp_username, wp_app_password)
        print("✓ WordPress REST API クライアントを初期化しました。")

        # 接続と認証のテスト（エラーでも続行）
        try:
            wp_client.test_connection()
        except Exception as test_error:
            print(f"⚠ 接続テストに失敗しましたが続行します: {test_error}")
            print("実際の投稿で再度認証を試みます...")
    except Exception as e:
        print(f"エラー: WordPress初期化に失敗しました - {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 前回の投稿を取得（関連記事セクション用）
    previous_post = None
    try:
        previous_post = wp_client.get_latest_post()
        if previous_post:
            print(f"✓ 前回の投稿を取得しました: {previous_post['title']}")
        else:
            print("⚠ 前回の投稿が見つかりませんでした（初回投稿の可能性）")
    except Exception as e:
        print(f"⚠ 前回の投稿取得に失敗: {e}")

    # 商品マネージャーを初期化（50日経過チェックと自動リフレッシュを含む）
    products_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'products.json')
    product_manager = AmazonProductManager(products_file)

    # Amazon PA-APIを使用して商品を自動取得
    use_paapi = os.getenv('USE_AMAZON_PAAPI', 'true').lower() == 'true'
    product = None

    if use_paapi:
        # PA-APIから商品を取得
        try:
            from amazon_paapi_client import AmazonPAAPIClient
            print("Amazon PA-APIを使用して商品を検索中...")
            print("PA-API 5.0 レート制限: 10秒に1リクエスト（安全マージン込みで12秒）")
            paapi_client = AmazonPAAPIClient()

            # 投稿済みでない商品を取得するまでリトライ
            # PA-API 5.0のレート制限を考慮: 10秒に1リクエスト + 安全マージン2秒 = 12秒
            max_attempts = 10
            request_interval = 12.0  # 秒

            for attempt in range(max_attempts):
                # 2回目以降のリクエストでは12秒待機
                if attempt > 0:
                    print(f"PA-APIレート制限を考慮し、{request_interval}秒待機中...")
                    time.sleep(request_interval)

                candidate = paapi_client.get_random_product()
                if candidate and candidate.asin not in product_manager.posted_asins:
                    product = candidate
                    break
                elif candidate:
                    print(f"商品 {candidate.asin} は投稿済みです。別の商品を検索中... ({attempt + 1}/{max_attempts})")

            if not product:
                print("警告: PA-APIで未投稿の商品が見つかりませんでした。ローカルデータを使用します。")
                use_paapi = False
        except Exception as e:
            print(f"警告: PA-APIの使用中にエラーが発生しました - {e}")
            import traceback
            traceback.print_exc()
            print("ローカルの商品データを使用します。")
            use_paapi = False

    # 商品バリエーションを取得（同じ製品の仕様違いをまとめる）
    product_variants = []

    if not use_paapi:
        # ローカルの商品データを使用（フォールバック）
        if not product_manager.get_all_products():
            print("エラー: 商品データが見つかりません。")
            print(f"products.json ファイルを {products_file} に配置してください。")
            sys.exit(1)

        print(f"✓ {len(product_manager.get_all_products())}件のローカル商品データを読み込みました。")

        # 同一製品のバリエーションをすべて取得
        product_variants = product_manager.get_product_variants()
        if not product_variants:
            print("エラー: 投稿する商品が見つかりません。")
            sys.exit(1)
    else:
        # PA-APIから取得した場合は単一商品
        if product:
            product_variants = [product]

    # メイン商品（最初のバリエーション）
    product = product_variants[0]

    print(f"選択された商品: {product.name}")
    print(f"商品ASIN: {product.asin}")
    if len(product_variants) > 1:
        print(f"バリエーション: {len(product_variants)}個の仕様違いを1記事にまとめます")
    print("-" * 50)

    # ブログ記事生成（バリエーション対応、関連記事付き）
    generator = BlogPostGenerator()
    title = generator.generate_title(product)
    content = generator.generate_post_content(product, variants=product_variants, previous_post=previous_post)
    meta_description = generator.generate_meta_description(product)
    seo_title = generator.generate_seo_title(product, post_title=title)  # 投稿タイトルをSEOタイトルとして使用
    seo_keywords = generator.generate_seo_keywords(product)

    print(f"記事タイトル: {title}")
    print(f"メタディスクリプション: {meta_description}")
    print(f"SEOタイトル: {seo_title}")
    print(f"SEOキーワード: {seo_keywords}")
    print("-" * 50)

    # カテゴリーの準備
    try:
        # カテゴリーの取得または作成
        category_id = wp_client.get_or_create_category(product.category)
        print(f"✓ カテゴリー設定: {product.category} (ID: {category_id})")

    except Exception as e:
        print(f"警告: カテゴリーの設定中にエラーが発生しました - {e}")
        category_id = None

    # 記事を投稿
    try:
        post_data = wp_client.create_post(
            title=title,
            content=content,
            status=post_status,
            categories=[category_id] if category_id else None,
            tags=None,
            excerpt=meta_description,
            seo_title=seo_title,
            seo_description=meta_description,
            seo_keywords=seo_keywords
        )

        post_url = post_data.get('link', '')
        post_id = post_data.get('id', '')

        print("=" * 50)
        print("✓ 記事の投稿に成功しました!")
        print(f"投稿ID: {post_id}")
        print(f"URL: {post_url}")
        print(f"ステータス: {post_status}")
        print("=" * 50)

        # 投稿成功後、すべてのバリエーションを投稿済みとしてマーク
        for variant in product_variants:
            product_manager.mark_as_posted(variant.asin)

        # 投稿済み商品の統計を表示
        total_products = len(product_manager.get_all_products())
        posted_count = len(product_manager.posted_asins)
        remaining_count = total_products - posted_count

        print("\n商品投稿状況:")
        print(f"  総商品数: {total_products}個")
        print(f"  投稿済み: {posted_count}個")
        print(f"  残り: {remaining_count}個")

        if remaining_count == 0:
            print("  ⚠ 全商品の投稿が完了しました。次回実行時に履歴がリセットされます。")

        return 0

    except Exception as e:
        print(f"エラー: 記事の投稿に失敗しました - {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
