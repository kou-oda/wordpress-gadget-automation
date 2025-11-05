"""
Amazon PA-API クライアント
大手メーカーの商品を自動取得
"""
import os
import random
import time
from typing import List, Optional

try:
    from amazon_paapi import AmazonApi
except ImportError:
    # フォールバック: 古いバージョンの場合
    from amazon.paapi import AmazonAPI as AmazonApi

from amazon_scraper import GadgetProduct


class AmazonPAAPIClient:
    """Amazon PA-API クライアント"""

    # 大手メーカーリスト
    MAJOR_BRANDS = [
        "Logitech", "ロジクール",
        "Microsoft", "マイクロソフト",
        "Samsung", "サムスン",
        "Crucial", "クルーシャル",
        "Anker", "アンカー",
        "BenQ", "ベンキュー",
        "HHKB", "Happy Hacking Keyboard",
        "Corsair", "コルセア",
        "Razer", "レイザー",
        "ASUS", "エイスース",
        "Dell", "デル",
        "HP", "ヒューレット・パッカード",
        "Lenovo", "レノボ",
        "SanDisk", "サンディスク",
        "Western Digital", "WD", "ウエスタンデジタル",
        "Kingston", "キングストン",
        "Intel", "インテル",
        "AMD",
        "NVIDIA", "エヌビディア",
        "Sony", "ソニー",
        "Panasonic", "パナソニック",
        "Canon", "キヤノン",
        "Epson", "エプソン",
        "Buffalo", "バッファロー",
        "Elecom", "エレコム",
        "Seagate", "シーゲート",
        "Transcend", "トランセンド",
        "Philips", "フィリップス",
        "LG",
        "Acer", "エイサー",
        "Apple", "アップル",
        "Creative", "クリエイティブ",
        "Thermaltake", "サーマルテイク",
    ]

    # 検索キーワードリスト（カテゴリー別）
    SEARCH_KEYWORDS = {
        "PC周辺機器": [
            "ワイヤレスマウス",
            "ゲーミングマウス",
            "エルゴノミクスマウス",
            "メカニカルキーボード",
            "ゲーミングキーボード",
            "ワイヤレスキーボード",
            "モニターライト",
            "デスクライト",
            "Webカメラ",
            "マイク",
            "ヘッドセット",
            "スピーカー",
            "モバイルバッテリー",
            "USB充電器",
            "USBハブ",
            "ドッキングステーション",
            "マウスパッド",
            "ゲーミングヘッドセット",
        ],
        "PCパーツ": [
            "NVMe SSD",
            "M.2 SSD",
            "内蔵SSD",
            "DDR5 メモリ",
            "DDR4 メモリ",
            "グラフィックボード",
            "外付けSSD",
            "外付けHDD",
            "PCケース",
            "電源ユニット",
            "CPUクーラー",
            "ケースファン",
        ],
    }

    def __init__(self):
        """初期化"""
        print("PA-API クライアントを初期化中...")

        # 環境変数からPA-APIの認証情報を取得
        self.access_key = os.getenv('AMAZON_ACCESS_KEY')
        self.secret_key = os.getenv('AMAZON_SECRET_KEY')
        self.associate_tag = os.getenv('AMAZON_ASSOCIATE_TAG')
        self.region = os.getenv('AMAZON_REGION', 'jp')  # デフォルトは日本

        print(f"リージョン: {self.region}")
        print(f"Access Key設定: {'有' if self.access_key else '無'}")
        print(f"Secret Key設定: {'有' if self.secret_key else '無'}")
        print(f"Associate Tag設定: {'有' if self.associate_tag else '無'}")

        if not all([self.access_key, self.secret_key, self.associate_tag]):
            raise ValueError(
                "Amazon PA-API credentials are required. "
                "Set AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, and AMAZON_ASSOCIATE_TAG environment variables."
            )

        # 地域コードマッピング
        country_map = {
            'jp': 'JP',
            'us': 'US',
            'uk': 'UK',
            'de': 'DE',
            'fr': 'FR',
            'ca': 'CA',
            'it': 'IT',
            'es': 'ES'
        }
        country = country_map.get(self.region.lower(), 'JP')
        print(f"使用する国コード: {country}")

        # PA-API クライアント初期化
        try:
            print("AmazonApiクラスをインスタンス化中...")
            self.api = AmazonApi(
                self.access_key,
                self.secret_key,
                self.associate_tag,
                country
            )
            print("✓ PA-API クライアントの初期化に成功しました")
        except Exception as e:
            print(f"✗ PA-API クライアントの初期化に失敗: {e}")
            import traceback
            traceback.print_exc()
            raise

    def is_major_brand(self, product_title: str, brand: Optional[str] = None) -> bool:
        """
        大手メーカーの商品かどうかを判定

        Args:
            product_title: 商品タイトル
            brand: ブランド名

        Returns:
            大手メーカーの場合True
        """
        # ブランド名で判定
        if brand:
            for major_brand in self.MAJOR_BRANDS:
                if major_brand.lower() in brand.lower():
                    return True

        # タイトルで判定
        for major_brand in self.MAJOR_BRANDS:
            if major_brand.lower() in product_title.lower():
                return True

        return False

    def search_products(self, keyword: str, category: str, max_results: int = 10) -> List[GadgetProduct]:
        """
        キーワードで商品を検索（429エラー時はリトライ）

        Args:
            keyword: 検索キーワード
            category: カテゴリー
            max_results: 最大取得件数

        Returns:
            商品リスト
        """
        # 429エラー時のリトライ設定
        max_retries = 3
        base_wait_time = 15.0  # 初回待機時間（秒）

        for retry in range(max_retries):
            try:
                # リトライ時は待機（exponential backoff）
                if retry > 0:
                    wait_time = base_wait_time * (2 ** (retry - 1))  # 15秒、30秒、60秒
                    print(f"⏳ PA-APIレート制限のため{wait_time}秒待機中... (リトライ {retry}/{max_retries})")
                    time.sleep(wait_time)

                # PA-APIで商品検索
                search_result = self.api.search_items(keywords=keyword, item_count=max_results)

                gadget_products = []

                # 検索結果が存在するか確認
                if not search_result or not hasattr(search_result, 'items'):
                    return []

                # 各商品を処理
                for item in search_result.items:
                    try:
                        # ブランド取得
                        brand = None
                        if hasattr(item, 'item_info') and item.item_info:
                            if hasattr(item.item_info, 'by_line_info') and item.item_info.by_line_info:
                                if hasattr(item.item_info.by_line_info, 'brand') and item.item_info.by_line_info.brand:
                                    brand = item.item_info.by_line_info.brand.display_value

                        # タイトル取得
                        title = ""
                        if hasattr(item, 'item_info') and item.item_info:
                            if hasattr(item.item_info, 'title') and item.item_info.title:
                                title = item.item_info.title.display_value

                        # 大手メーカーの商品のみを選定
                        if not self.is_major_brand(title, brand):
                            continue

                        # ASIN取得
                        asin = item.asin if hasattr(item, 'asin') else None
                        if not asin:
                            continue

                        # 価格取得
                        price = None
                        if hasattr(item, 'offers') and item.offers:
                            if hasattr(item.offers, 'listings') and item.offers.listings:
                                if len(item.offers.listings) > 0:
                                    listing = item.offers.listings[0]
                                    if hasattr(listing, 'price') and listing.price:
                                        if hasattr(listing.price, 'display_amount'):
                                            price = listing.price.display_amount

                        # 画像URL取得
                        image_url = None
                        if hasattr(item, 'images') and item.images:
                            if hasattr(item.images, 'primary') and item.images.primary:
                                if hasattr(item.images.primary, 'large') and item.images.primary.large:
                                    if hasattr(item.images.primary.large, 'url'):
                                        image_url = item.images.primary.large.url

                        # 特徴取得
                        features = []
                        if hasattr(item, 'item_info') and item.item_info:
                            if hasattr(item.item_info, 'features') and item.item_info.features:
                                if hasattr(item.item_info.features, 'display_values'):
                                    features = [f.display_value for f in item.item_info.features.display_values[:5]]

                        # 説明文生成（ブランド名とキーワードから）
                        description = f"{brand or ''}の{keyword}として高い評価を得ている製品"

                        # GadgetProductオブジェクト作成
                        product = GadgetProduct(
                            name=title,
                            asin=asin,
                            url=f"https://www.amazon.co.jp/dp/{asin}?tag={self.associate_tag}",
                            price=price,
                            image_url=image_url,
                            description=description,
                            category=category,
                            features=features if features else None,
                            rating=None
                        )

                        gadget_products.append(product)

                    except Exception as e:
                        print(f"商品データの処理中にエラー: {e}")
                        import traceback
                        traceback.print_exc()
                        continue

                # 成功したらリストを返す
                return gadget_products

            except Exception as e:
                # 429エラーの場合はリトライ
                error_message = str(e)
                if '429' in error_message or 'Too Many Requests' in error_message:
                    print(f"⚠ PA-API レート制限エラー (429): {e}")
                    if retry < max_retries - 1:
                        print(f"リトライします... ({retry + 1}/{max_retries})")
                        continue
                    else:
                        print("最大リトライ回数に達しました。")
                        return []
                else:
                    # 429以外のエラーは即座に返す
                    print(f"商品検索中にエラー: {e}")
                    import traceback
                    traceback.print_exc()
                    return []

        # すべてのリトライが失敗した場合
        print("PA-APIのレート制限により商品を取得できませんでした。")
        return []

    def get_random_product(self) -> Optional[GadgetProduct]:
        """
        ランダムなカテゴリーとキーワードで商品を検索し、1つ返す

        Returns:
            ランダムに選択された大手メーカーの商品
        """
        # ランダムにカテゴリーを選択
        category = random.choice(list(self.SEARCH_KEYWORDS.keys()))

        # そのカテゴリーからランダムにキーワードを選択
        keyword = random.choice(self.SEARCH_KEYWORDS[category])

        print(f"検索中: カテゴリー={category}, キーワード={keyword}")

        # 商品を検索
        products = self.search_products(keyword, category, max_results=10)

        if not products:
            print("商品が見つかりませんでした。")
            return None

        # ランダムに1つ選択
        product = random.choice(products)
        print(f"選択された商品: {product.name} (ブランド: 大手メーカー)")

        return product


if __name__ == "__main__":
    # テスト用
    client = AmazonPAAPIClient()
    product = client.get_random_product()
    if product:
        print(f"商品名: {product.name}")
        print(f"ASIN: {product.asin}")
        print(f"価格: {product.price}")
        print(f"カテゴリー: {product.category}")
