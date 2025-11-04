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

    def create_post(
        self,
        title: str,
        content: str,
        status: str = 'draft',
        categories: Optional[List[int]] = None,
        tags: Optional[List[int]] = None,
        featured_media: Optional[int] = None
    ) -> Dict:
        """
        新しい投稿を作成

        Args:
            title: 投稿タイトル
            content: 投稿内容（HTML）
            status: 投稿ステータス（draft, publish, private）
            categories: カテゴリーIDのリスト
            tags: タグIDのリスト
            featured_media: アイキャッチ画像のメディアID

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
        if featured_media:
            data['featured_media'] = featured_media

        response = requests.post(
            endpoint,
            headers=self.headers,
            json=data
        )
        response.raise_for_status()

        return response.json()

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

        headers = {
            'Authorization': self.headers['Authorization'],
            'Content-Disposition': f'attachment; filename="{filename}"',
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
