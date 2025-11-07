import requests
import base64
import json
from typing import Dict, List, Optional
import os


class WordPressClient:
    """WordPress REST API クライアント"""

    def __init__(self, site_url: str, username: str, app_password: str):
        """
        初期化

        Args:
            site_url: WordPressサイトのURL（例: https://wwnaoya.com）
            username: WordPressユーザー名
            app_password: WordPress Application Password
        """
        self.site_url = site_url.rstrip('/')
        self.api_url = f"{self.site_url}/wp-json/wp/v2"
        self.username = username
        self.app_password = app_password

        # Basic認証のヘッダー作成
        credentials = f"{username}:{app_password}"
        token = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            'Authorization': f'Basic {token}',
            'Content-Type': 'application/json'
        }

    def test_connection(self) -> Dict:
        """REST API接続とユーザー権限をテスト"""
        print("\n=== WordPress REST API 診断 ===")

        # Step 1: REST API自体が有効かチェック
        try:
            print("1. REST APIの可用性をチェック中...")
            base_endpoint = f"{self.site_url}/wp-json"
            base_response = requests.get(base_endpoint)

            if base_response.status_code == 200:
                print("   ✓ REST APIは有効です")
            else:
                print(f"   ✗ REST APIが無効または制限されています (HTTP {base_response.status_code})")
                print("   対処: REST APIを有効にするか、セキュリティプラグインの設定を確認してください")
                return {}
        except Exception as e:
            print(f"   ✗ REST APIに接続できません: {e}")
            return {}

        # Step 2: 認証をテスト
        try:
            print("2. 認証をテスト中...")
            endpoint = f"{self.site_url}/wp-json/wp/v2/users/me"
            response = requests.get(endpoint, headers=self.headers)

            # レスポンス詳細を表示
            print(f"   リクエストURL: {endpoint}")
            print(f"   レスポンスコード: {response.status_code}")

            if response.status_code == 200:
                user_data = response.json()
                print(f"   ✓ 認証成功: ユーザー '{user_data.get('name')}' (ID: {user_data.get('id')})")

                # 権限の詳細チェック
                caps = user_data.get('capabilities', {})
                important_caps = ['edit_posts', 'publish_posts', 'edit_categories']
                print(f"   重要な権限:")
                for cap in important_caps:
                    status = "✓" if caps.get(cap) else "✗"
                    print(f"     {status} {cap}: {caps.get(cap, False)}")

                return user_data
            elif response.status_code == 403:
                print("   ✗ 認証エラー: 403 Forbidden")
                try:
                    error_data = response.json()
                    print(f"   エラーコード: {error_data.get('code', 'unknown')}")
                    print(f"   エラーメッセージ: {error_data.get('message', 'No message')}")
                except:
                    print(f"   エラー詳細: {response.text[:200]}")

                print("\n   考えられる原因:")
                print("   1. Application Passwordの形式が間違っている")
                print("      → スペースを削除してください（例: 'xxxx yyyy zzzz' → 'xxxxyyyyyyzzzz'）")
                print("   2. WordPressのApplication Password機能が無効")
                print("      → functions.phpに以下を追加: add_filter('wp_is_application_passwords_available', '__return_true');")
                print("   3. セキュリティプラグインがREST APIをブロックしている")
                print("      → Wordfence、iThemes Security等の設定を確認")
                print("   4. .htaccessで認証ヘッダーが削除されている")
                print("      → .htaccessに以下を追加: SetEnvIf Authorization \"(.*)\" HTTP_AUTHORIZATION=$1")
                raise requests.exceptions.HTTPError(f"403 Forbidden: {response.text[:200]}")
            else:
                print(f"   ✗ 予期しないレスポンス: HTTP {response.status_code}")
                print(f"   レスポンス: {response.text[:200]}")
                response.raise_for_status()

        except requests.exceptions.HTTPError:
            raise
        except Exception as e:
            print(f"   ✗ 接続テストエラー: {e}")
            raise

    def create_post(
        self,
        title: str,
        content: str,
        status: str = 'draft',
        categories: Optional[List[int]] = None,
        tags: Optional[List[int]] = None,
        excerpt: Optional[str] = None,
        seo_title: Optional[str] = None,
        seo_description: Optional[str] = None,
        seo_keywords: Optional[str] = None
    ) -> Dict:
        """
        新しい投稿を作成

        Args:
            title: 投稿タイトル
            content: 投稿内容（HTML）
            status: 投稿ステータス（draft, publish, private）
            categories: カテゴリーIDのリスト
            tags: タグIDのリスト
            excerpt: 抜粋（メタディスクリプション用）
            seo_title: SEOタイトル（Yoast/Rank Math/AIOSEO対応）
            seo_description: SEOメタディスクリプション
            seo_keywords: SEOメタキーワード

        Returns:
            作成された投稿の情報
        """
        endpoint = f"{self.api_url}/posts"

        data = {
            'title': title,
            'content': content,
            'status': status
        }

        if categories:
            data['categories'] = categories
        if tags:
            data['tags'] = tags
        if excerpt:
            data['excerpt'] = excerpt

        # SEO情報の設定（meta フィールドに追加）
        # Yoast SEO, Rank Math, All in One SEO に対応
        if seo_title or seo_description or seo_keywords:
            meta = {}

            # Yoast SEO
            if seo_title:
                meta['_yoast_wpseo_title'] = seo_title
            if seo_description:
                meta['_yoast_wpseo_metadesc'] = seo_description
            if seo_keywords:
                meta['_yoast_wpseo_focuskw'] = seo_keywords

            # Rank Math
            if seo_title:
                meta['rank_math_title'] = seo_title
            if seo_description:
                meta['rank_math_description'] = seo_description
            if seo_keywords:
                meta['rank_math_focus_keyword'] = seo_keywords

            # All in One SEO (AIOSEO)
            if seo_title:
                meta['_aioseo_title'] = seo_title
            if seo_description:
                meta['_aioseo_description'] = seo_description
            if seo_keywords:
                meta['_aioseo_keywords'] = seo_keywords

            data['meta'] = meta

        response = requests.post(
            endpoint,
            headers=self.headers,
            json=data
        )
        response.raise_for_status()

        post_data = response.json()

        # SEO情報を別途更新（メタフィールドとして保存）
        if seo_title or seo_description or seo_keywords:
            post_id = post_data.get('id')
            if post_id:
                self._update_seo_meta(post_id, seo_title, seo_description, seo_keywords)

        return post_data

    def _update_seo_meta(self, post_id: int, seo_title: str = None, seo_description: str = None, seo_keywords: str = None):
        """投稿のSEOメタデータを更新（Yoast SEO, Rank Math, AIOSEO対応）"""
        try:
            # Yoast SEO用のメタデータ更新
            if seo_title:
                self._update_post_meta(post_id, '_yoast_wpseo_title', seo_title)
            if seo_description:
                self._update_post_meta(post_id, '_yoast_wpseo_metadesc', seo_description)
            if seo_keywords:
                self._update_post_meta(post_id, '_yoast_wpseo_focuskw', seo_keywords)

            # Rank Math用のメタデータ更新
            if seo_title:
                self._update_post_meta(post_id, 'rank_math_title', seo_title)
            if seo_description:
                self._update_post_meta(post_id, 'rank_math_description', seo_description)
            if seo_keywords:
                self._update_post_meta(post_id, 'rank_math_focus_keyword', seo_keywords)

            # AIOSEO用のメタデータ更新
            if seo_title:
                self._update_post_meta(post_id, '_aioseo_title', seo_title)
            if seo_description:
                self._update_post_meta(post_id, '_aioseo_description', seo_description)
            if seo_keywords:
                self._update_post_meta(post_id, '_aioseo_keywords', seo_keywords)

        except Exception as e:
            print(f"警告: SEOメタデータの更新に失敗しました - {e}")

    def _update_post_meta(self, post_id: int, meta_key: str, meta_value: str):
        """投稿メタデータを更新"""
        # WordPress REST APIのPUTメソッドを使用して投稿を更新
        endpoint = f"{self.api_url}/posts/{post_id}"
        data = {
            'meta': {
                meta_key: meta_value
            }
        }

        try:
            # PUTメソッドを使用
            response = requests.put(
                endpoint,
                headers=self.headers,
                json=data
            )
            # 成功した場合のみログ出力
            if response.status_code in [200, 201]:
                print(f"  ✓ SEOメタフィールド {meta_key} を更新しました")
            else:
                # エラーレスポンスの詳細を表示
                print(f"  ⚠ メタフィールド {meta_key} の更新に失敗: HTTP {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"    詳細: {error_detail.get('message', 'Unknown error')}")
                except:
                    pass
        except Exception as e:
            print(f"  ✗ メタフィールド {meta_key} の更新エラー: {e}")

    def upload_media(self, image_url: str, filename: str) -> Dict:
        """
        メディアライブラリに画像をアップロード

        Args:
            image_url: 画像のURL
            filename: ファイル名

        Returns:
            アップロードされたメディアの情報
        """
        # 画像をダウンロード
        img_response = requests.get(image_url)
        img_response.raise_for_status()

        endpoint = f"{self.api_url}/media"

        # Content-Typeを適切に設定
        content_type = img_response.headers.get('Content-Type', 'image/jpeg')

        headers = {
            'Authorization': self.headers['Authorization'],
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-Type': content_type
        }

        response = requests.post(
            endpoint,
            headers=headers,
            data=img_response.content
        )
        response.raise_for_status()

        return response.json()

    def get_categories(self) -> List[Dict]:
        """カテゴリー一覧を取得"""
        endpoint = f"{self.api_url}/categories"
        response = requests.get(endpoint, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_category(self, name: str, description: str = "") -> Dict:
        """
        新しいカテゴリーを作成

        Args:
            name: カテゴリー名
            description: カテゴリーの説明

        Returns:
            作成されたカテゴリーの情報
        """
        endpoint = f"{self.api_url}/categories"
        data = {
            'name': name,
            'description': description
        }

        response = requests.post(
            endpoint,
            headers=self.headers,
            json=data
        )
        response.raise_for_status()

        return response.json()

    def get_or_create_category(self, name: str) -> int:
        """カテゴリーを取得または作成してIDを返す"""
        categories = self.get_categories()

        for cat in categories:
            if cat['name'].lower() == name.lower():
                return cat['id']

        # カテゴリーが存在しない場合は作成
        new_cat = self.create_category(name)
        return new_cat['id']

    def get_tags(self) -> List[Dict]:
        """タグ一覧を取得"""
        endpoint = f"{self.api_url}/tags"
        response = requests.get(endpoint, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_tag(self, name: str) -> Dict:
        """新しいタグを作成"""
        endpoint = f"{self.api_url}/tags"
        data = {'name': name}

        response = requests.post(
            endpoint,
            headers=self.headers,
            json=data
        )
        response.raise_for_status()

        return response.json()

    def get_or_create_tags(self, tag_names: List[str]) -> List[int]:
        """タグを取得または作成してIDリストを返す"""
        existing_tags = self.get_tags()
        tag_ids = []

        for tag_name in tag_names:
            found = False
            for tag in existing_tags:
                if tag['name'].lower() == tag_name.lower():
                    tag_ids.append(tag['id'])
                    found = True
                    break

            if not found:
                new_tag = self.create_tag(tag_name)
                tag_ids.append(new_tag['id'])

        return tag_ids

    def get_latest_post(self) -> Optional[Dict]:
        """
        最新の投稿を1件取得

        Returns:
            最新投稿の情報（title, link, featured_media）、取得できない場合はNone
        """
        try:
            url = f"{self.api_url}/posts"
            params = {
                'per_page': 1,
                'orderby': 'date',
                'order': 'desc',
                'status': 'publish'
            }
            response = requests.get(url, params=params)
            response.raise_for_status()

            posts = response.json()
            if posts and len(posts) > 0:
                post = posts[0]
                result = {
                    'title': post.get('title', {}).get('rendered', ''),
                    'link': post.get('link', ''),
                    'featured_media': post.get('featured_media', 0)
                }

                # アイキャッチ画像のURLを取得
                if result['featured_media'] > 0:
                    media_url = f"{self.api_url}/media/{result['featured_media']}"
                    media_response = requests.get(media_url)
                    if media_response.status_code == 200:
                        media_data = media_response.json()
                        result['featured_image_url'] = media_data.get('source_url', '')
                    else:
                        result['featured_image_url'] = ''
                else:
                    result['featured_image_url'] = ''

                return result

            return None

        except Exception as e:
            print(f"最新投稿の取得に失敗: {e}")
            return None
