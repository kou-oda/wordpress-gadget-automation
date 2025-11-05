#!/usr/bin/env python3
"""
Ping送信スクリプト
ブログ検索エンジンに新着記事を通知
"""
import xmlrpc.client
import sys

# 日本の主要Pingサーバー
PING_SERVERS = [
    'http://blog.goo.ne.jp/XMLRPC',
    'http://blogsearch.google.co.jp/ping/RPC2',
    'http://blogsearch.google.com/ping/RPC2',
    'http://ping.blogranking.net/cgi-bin/xmlrpc',
    'http://ping.fc2.com/',
    'http://ping.feedburner.com',
    'http://ping.rss.drecom.jp/',
    'http://rpc.weblogs.com/RPC2',
    'http://rpc.pingomatic.com/',
    'http://www.blogpeople.net/servlet/weblogUpdates',
    'http://ping.blo.gs/',
    'http://api.my.yahoo.com/RPC2',
]


def send_ping(blog_name: str, blog_url: str, post_url: str = None) -> dict:
    """
    Ping送信を実行

    Args:
        blog_name: ブログ名
        blog_url: ブログURL
        post_url: 記事URL（オプション）

    Returns:
        送信結果の辞書
    """
    results = {
        'success': [],
        'failed': []
    }

    for server in PING_SERVERS:
        try:
            print(f"Ping送信中: {server}")

            # XML-RPC クライアント作成
            client = xmlrpc.client.ServerProxy(server)

            # Ping送信（weblogUpdates.ping メソッド）
            if post_url:
                response = client.weblogUpdates.extendedPing(
                    blog_name,
                    blog_url,
                    post_url,
                    ''  # RSS URL（オプション）
                )
            else:
                response = client.weblogUpdates.ping(blog_name, blog_url)

            print(f"✓ 成功: {server}")
            results['success'].append(server)

        except Exception as e:
            print(f"✗ 失敗: {server} - {e}")
            results['failed'].append(server)

    return results


def main():
    """メイン処理"""
    import os

    # 環境変数から設定を取得
    blog_name = os.getenv('BLOG_NAME', 'ガジェットレビューブログ')
    blog_url = os.getenv('WP_SITE_URL', 'https://wwnaoya.com')

    # 最新記事URLを取得（WordPress REST API）
    try:
        import requests
        response = requests.get(f"{blog_url}/wp-json/wp/v2/posts?per_page=1&orderby=date")
        posts = response.json()

        if posts and len(posts) > 0:
            post_url = posts[0]['link']
            post_title = posts[0]['title']['rendered']
            print(f"最新記事: {post_title}")
            print(f"URL: {post_url}")
        else:
            post_url = None
    except Exception as e:
        print(f"警告: 最新記事の取得に失敗: {e}")
        post_url = None

    # Ping送信
    print("=" * 50)
    print("Ping送信を開始します...")
    print("=" * 50)

    results = send_ping(blog_name, blog_url, post_url)

    # 結果表示
    print("\n" + "=" * 50)
    print("Ping送信結果")
    print("=" * 50)
    print(f"✓ 成功: {len(results['success'])}件")
    print(f"✗ 失敗: {len(results['failed'])}件")

    if results['success']:
        print("\n成功したサーバー:")
        for server in results['success']:
            print(f"  - {server}")

    if results['failed']:
        print("\n失敗したサーバー:")
        for server in results['failed']:
            print(f"  - {server}")

    return 0 if len(results['success']) > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
