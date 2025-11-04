#!/usr/bin/env python3
"""
WordPress ガジェットブログ自動投稿スクリプト
"""

import os
import sys
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
        print("✓ WordPress REST API に接続しました。")
    except Exception as e:
        print(f"エラー: WordPress接続に失敗しました - {e}")
        sys.exit(1)

    # Amazon 商品マネージャー初期化
    products_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'products.json')
    product_manager = AmazonProductManager(products_file)

    if not product_manager.get_all_products():
        print("エラー: 商品データが見つかりません。")
        print(f"products.json ファイルを {products_file} に配置してください。")
        sys.exit(1)

    print(f"✓ {len(product_manager.get_all_products())}件の商品データを読み込みました。")

    # ランダムに商品を選択
    product = product_manager.get_random_product()
    if not product:
        print("エラー: 投稿する商品が見つかりません。")
        sys.exit(1)

    print(f"選択された商品: {product.name}")
    print("-" * 50)

    # ブログ記事生成
    generator = BlogPostGenerator()
    title = generator.generate_title(product)
    content = generator.generate_post_content(product)
    tags = generator.generate_tags(product)

    print(f"記事タイトル: {title}")
    print(f"タグ: {', '.join(tags)}")
    print("-" * 50)

    # カテゴリーとタグの準備
    try:
        # カテゴリーの取得または作成
        category_id = wp_client.get_or_create_category(product.category)
        print(f"✓ カテゴリー設定: {product.category} (ID: {category_id})")

        # タグの取得または作成
        tag_ids = wp_client.get_or_create_tags(tags)
        print(f"✓ タグ設定: {len(tag_ids)}個のタグを設定しました。")

    except Exception as e:
        print(f"警告: カテゴリー/タグの設定中にエラーが発生しました - {e}")
        category_id = None
        tag_ids = []

    # 記事を投稿
    try:
        post_data = wp_client.create_post(
            title=title,
            content=content,
            status=post_status,
            categories=[category_id] if category_id else None,
            tags=tag_ids if tag_ids else None
        )

        post_url = post_data.get('link', '')
        post_id = post_data.get('id', '')

        print("=" * 50)
        print("✓ 記事の投稿に成功しました!")
        print(f"投稿ID: {post_id}")
        print(f"URL: {post_url}")
        print(f"ステータス: {post_status}")
        print("=" * 50)

        return 0

    except Exception as e:
        print(f"エラー: 記事の投稿に失敗しました - {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
