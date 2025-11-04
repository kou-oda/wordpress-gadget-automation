import json
import random
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import os


@dataclass
class GadgetProduct:
    """ガジェット商品情報"""
    name: str
    asin: str  # Amazon Standard Identification Number
    url: str
    price: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    category: str = "PC周辺機器"
    features: Optional[List[str]] = None
    rating: Optional[float] = None

    def to_dict(self) -> Dict:
        return asdict(self)


class AmazonProductManager:
    """Amazon商品管理クラス"""

    def __init__(self, products_file: str = "data/products.json"):
        """
        初期化

        Args:
            products_file: 商品データを保存するJSONファイルのパス
        """
        self.products_file = products_file
        self.products: List[GadgetProduct] = []
        self.load_products()

    def load_products(self):
        """商品データをファイルから読み込み"""
        if os.path.exists(self.products_file):
            try:
                with open(self.products_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.products = [GadgetProduct(**item) for item in data]
            except Exception as e:
                print(f"商品データの読み込みに失敗: {e}")
                self.products = []

    def save_products(self):
        """商品データをファイルに保存"""
        os.makedirs(os.path.dirname(self.products_file), exist_ok=True)
        with open(self.products_file, 'w', encoding='utf-8') as f:
            data = [product.to_dict() for product in self.products]
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_product(self, product: GadgetProduct):
        """商品を追加"""
        # 既存の商品（同じASIN）がある場合は更新
        for i, p in enumerate(self.products):
            if p.asin == product.asin:
                self.products[i] = product
                self.save_products()
                return

        self.products.append(product)
        self.save_products()

    def get_random_product(self, category: Optional[str] = None) -> Optional[GadgetProduct]:
        """
        ランダムに商品を取得

        Args:
            category: カテゴリーでフィルター（省略可）

        Returns:
            ランダムに選択された商品
        """
        if not self.products:
            return None

        if category:
            filtered = [p for p in self.products if p.category == category]
            if not filtered:
                return None
            return random.choice(filtered)

        return random.choice(self.products)

    def get_product_by_asin(self, asin: str) -> Optional[GadgetProduct]:
        """ASINで商品を取得"""
        for product in self.products:
            if product.asin == asin:
                return product
        return None

    def get_all_products(self) -> List[GadgetProduct]:
        """全商品を取得"""
        return self.products

    def get_products_by_category(self, category: str) -> List[GadgetProduct]:
        """カテゴリー別に商品を取得"""
        return [p for p in self.products if p.category == category]


def create_sample_products() -> List[GadgetProduct]:
    """サンプル商品データを作成"""
    return [
        GadgetProduct(
            name="ロジクール ワイヤレスマウス MX Master 3S",
            asin="B0B4DQPH5K",
            url="https://www.amazon.co.jp/dp/B0B4DQPH5K",
            price="¥14,800",
            category="PC周辺機器",
            description="高精度センサーと快適なエルゴノミクスデザインを備えたプレミアムワイヤレスマウス",
            features=[
                "8,000 DPI高精度センサー",
                "最大70日間のバッテリー寿命",
                "静音クリック設計",
                "複数デバイス対応"
            ]
        ),
        GadgetProduct(
            name="HHKB Professional HYBRID Type-S",
            asin="B082TSSZ3W",
            url="https://www.amazon.co.jp/dp/B082TSSZ3W",
            price="¥36,850",
            category="PC周辺機器",
            description="プロフェッショナル向けコンパクトキーボード、静音モデル",
            features=[
                "静電容量無接点方式",
                "Bluetooth/USB接続対応",
                "コンパクト配列",
                "高速タイピング対応"
            ]
        ),
        GadgetProduct(
            name="Samsung 980 PRO NVMe M.2 SSD 1TB",
            asin="B08GLX7TNT",
            url="https://www.amazon.co.jp/dp/B08GLX7TNT",
            price="¥12,980",
            category="PCパーツ",
            description="PCIe 4.0対応の超高速SSD",
            features=[
                "読み込み速度 最大7,000MB/s",
                "書き込み速度 最大5,000MB/s",
                "優れた耐久性",
                "5年保証"
            ]
        ),
        GadgetProduct(
            name="Crucial DDR5-4800 32GB(16GBx2)",
            asin="B09Q81KB2P",
            url="https://www.amazon.co.jp/dp/B09Q81KB2P",
            price="¥16,800",
            category="PCパーツ",
            description="次世代DDR5メモリで高速処理を実現",
            features=[
                "DDR5-4800MHz",
                "32GB(16GBx2枚組)",
                "Intel/AMD対応",
                "生涯保証"
            ]
        ),
        GadgetProduct(
            name="Anker 521 Power Bank (PowerCore Fusion 45W)",
            asin="B09SG31NPT",
            url="https://www.amazon.co.jp/dp/B09SG31NPT",
            price="¥7,990",
            category="PC周辺機器",
            description="充電器とモバイルバッテリーの2in1",
            features=[
                "45W高出力充電",
                "5,000mAh容量",
                "USB-C & USB-A ポート",
                "コンパクト設計"
            ]
        ),
        GadgetProduct(
            name="BenQ ScreenBar Plus モニターライト",
            asin="B07VWLCQ63",
            url="https://www.amazon.co.jp/dp/B07VWLCQ63",
            price="¥13,900",
            category="PC周辺機器",
            description="デスク環境を快適にするモニター掛け式ライト",
            features=[
                "自動調光機能",
                "ワイヤレスコントローラー",
                "画面に反射しない設計",
                "省スペース"
            ]
        )
    ]


if __name__ == "__main__":
    # サンプル商品データを作成して保存
    import os
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    products_file = os.path.join(data_dir, 'products.json')
    manager = AmazonProductManager(products_file)

    sample_products = create_sample_products()
    for product in sample_products:
        manager.add_product(product)

    print(f"{len(sample_products)}件の商品データを保存しました。")
