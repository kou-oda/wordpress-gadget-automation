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

    # SEOメタデータ生成
    seo_title = title  # SEOタイトルは記事タイトルと同じ
    meta_description = generator.generate_meta_description(product)
    meta_keywords = generator.generate_meta_keywords(product)

    print(f"記事タイトル: {title}")
    print(f"SEOタイトル: {seo_title}")
    print(f"メタディスクリプション: {meta_description}")
    print(f"メタキーワード: {meta_keywords}")
    print("-" * 50)

    # カテゴリーの準備
    try:
        # カテゴリーの取得または作成
        category_id = wp_client.get_or_create_category(product.category)
        print(f"✓ カテゴリー設定: {product.category} (ID: {category_id})")

    except Exception as e:
        print(f"警告: カテゴリーの設定中にエラーが発生しました - {e}")
        category_id = None

    # アイキャッチ画像のアップロード
    featured_media_id = None
    if product.image_url:
        try:
            print("アイキャッチ画像をアップロード中...")
            # ファイル名を生成（商品名から安全なファイル名を作成）
            import re
            safe_name = re.sub(r'[^\w\s-]', '', product.name)
            safe_name = re.sub(r'[-\s]+', '-', safe_name)
            filename = f"{safe_name}.jpg"

            media_data = wp_client.upload_media(product.image_url, filename)
            featured_media_id = media_data.get('id')
            print(f"✓ アイキャッチ画像をアップロードしました (ID: {featured_media_id})")
        except Exception as e:
            print(f"警告: アイキャッチ画像のアップロードに失敗しました - {e}")
            # 画像アップロードに失敗しても記事投稿は続行

    # 記事を投稿
    try:
        post_data = wp_client.create_post(
            title=title,
            content=content,
            status=post_status,
            categories=[category_id] if category_id else None,
            tags=None,
            featured_media=featured_media_id,
            seo_title=seo_title,
            meta_description=meta_description,
            meta_keywords=meta_keywords
        )

        post_url = post_data.get('link', '')
        post_id = post_data.get('id', '')

        print("=" * 50)
        print("✓ 記事の投稿に成功しました!")
        print(f"投稿ID: {post_id}")
        print(f"URL: {post_url}")
        print(f"ステータス: {post_status}")
        if featured_media_id:
            print(f"アイキャッチ画像: 設定済み")
        print("=" * 50)

        return 0

    except Exception as e:
        print(f"エラー: 記事の投稿に失敗しました - {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
