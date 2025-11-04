"""
Amazon PA-API クライアント
大手メーカーの商品を自動取得
"""
import os
import random
from typing import List, Optional
from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.rest import ApiException
from paapi5_python_sdk.search_items_request import SearchItemsRequest
from paapi5_python_sdk.search_items_resource import SearchItemsResource
from paapi5_python_sdk.partner_type import PartnerType
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
        # 環境変数からPA-APIの認証情報を取得
        self.access_key = os.getenv('AMAZON_ACCESS_KEY')
        self.secret_key = os.getenv('AMAZON_SECRET_KEY')
        self.associate_tag = os.getenv('AMAZON_ASSOCIATE_TAG')
        self.region = os.getenv('AMAZON_REGION', 'jp')  # デフォルトは日本

        if not all([self.access_key, self.secret_key, self.associate_tag]):
            raise ValueError(
                "Amazon PA-API credentials are required. "
                "Set AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, and AMAZON_ASSOCIATE_TAG environment variables."
            )

        # 地域マッピング
        region_map = {
            'jp': 'JP',
            'us': 'US',
            'uk': 'UK',
            'de': 'DE',
            'fr': 'FR',
            'ca': 'CA',
            'it': 'IT',
            'es': 'ES'
        }
        self.country = region_map.get(self.region.lower(), 'JP')

        # ホストマッピング
        host_map = {
            'JP': 'webservices.amazon.co.jp',
            'US': 'webservices.amazon.com',
            'UK': 'webservices.amazon.co.uk',
            'DE': 'webservices.amazon.de',
            'FR': 'webservices.amazon.fr',
            'CA': 'webservices.amazon.ca',
            'IT': 'webservices.amazon.it',
            'ES': 'webservices.amazon.es'
        }
        self.host = host_map.get(self.country, 'webservices.amazon.co.jp')

        # PA-API クライアント初期化
        self.api_instance = DefaultApi(
            access_key=self.access_key,
            secret_key=self.secret_key,
            host=self.host,
            region=self.country
        )

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
        キーワードで商品を検索

        Args:
            keyword: 検索キーワード
            category: カテゴリー
            max_results: 最大取得件数

        Returns:
            商品リスト
        """
        try:
            # 検索リソースの設定
            search_items_resource = [
                SearchItemsResource.IMAGES_PRIMARY_LARGE,
                SearchItemsResource.ITEMINFO_TITLE,
                SearchItemsResource.ITEMINFO_FEATURES,
                SearchItemsResource.ITEMINFO_BYLINEINFO,
                SearchItemsResource.OFFERS_LISTINGS_PRICE,
            ]

            # 検索リクエストの作成
            search_items_request = SearchItemsRequest(
                partner_tag=self.associate_tag,
                partner_type=PartnerType.ASSOCIATES,
                keywords=keyword,
                item_count=max_results,
                resources=search_items_resource
            )

            # PA-APIで商品検索
            response = self.api_instance.search_items(search_items_request)

            gadget_products = []

            # レスポンスの確認
            if response.search_result is None:
                return []

            # 各商品を処理
            for item in response.search_result.items:
                try:
                    # ブランド取得
                    brand = None
                    if item.item_info and item.item_info.by_line_info and item.item_info.by_line_info.brand:
                        brand = item.item_info.by_line_info.brand.display_value

                    # タイトル取得
                    title = ""
                    if item.item_info and item.item_info.title:
                        title = item.item_info.title.display_value

                    # 大手メーカーの商品のみを選定
                    if not self.is_major_brand(title, brand):
                        continue

                    # ASIN取得
                    asin = item.asin

                    # 価格取得
                    price = None
                    if item.offers and item.offers.listings and len(item.offers.listings) > 0:
                        listing = item.offers.listings[0]
                        if listing.price:
                            price = listing.price.display_amount

                    # 画像URL取得
                    image_url = None
                    if item.images and item.images.primary and item.images.primary.large:
                        image_url = item.images.primary.large.url

                    # 特徴取得
                    features = []
                    if item.item_info and item.item_info.features and item.item_info.features.display_values:
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
                    continue

            return gadget_products

        except ApiException as e:
            print(f"PA-API エラー: {e}")
            return []
        except Exception as e:
            print(f"商品検索中にエラー: {e}")
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
