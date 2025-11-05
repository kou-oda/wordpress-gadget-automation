import json
import random
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import os
from datetime import datetime, timedelta
import re


def shorten_product_name(name: str, category: str, for_title: bool = True) -> str:
    """
    商品名を短縮する

    タイトル用（for_title=True）:
    - PCパーツ: 企業名+製品カテゴリー (例: Crucial SSD, Samsung メモリ)
    - PC周辺機器: 企業名+製品カテゴリー (例: Logicool マウス, HHKB キーボード)

    本文用（for_title=False）:
    - PCパーツ: 企業名+製品名 (例: Crucial BX500, Samsung DDR4-3200)
    - PC周辺機器: 企業名+製品名 (例: Logicool G304, HHKB Professional)

    Args:
        name: 元の商品名
        category: 商品カテゴリー
        for_title: タイトル用かどうか（Trueでカテゴリー名、Falseで製品名）

    Returns:
        短縮された商品名
    """
    # PCパーツのカテゴリー
    pc_parts_categories = ["SSD", "メモリ", "グラフィックボード", "CPU", "マザーボード", "電源ユニット"]

    # 主要ブランド名のリスト
    major_brands = [
        "Logitech", "Logicool", "Microsoft", "Samsung", "Crucial", "Anker", "BenQ",
        "HHKB", "Corsair", "Razer", "ASUS", "Dell", "HP", "Lenovo", "Sony",
        "Kingston", "Western Digital", "WD", "SanDisk", "Intel", "AMD", "NVIDIA",
        "Seagate", "LG", "Acer", "MSI", "Gigabyte", "ASRock", "EVGA",
        "HyperX", "G.Skill", "Thermaltake", "Cooler Master", "NZXT"
    ]

    # ブランド名を抽出（大文字小文字を無視）
    brand = None
    name_lower = name.lower()
    for b in major_brands:
        if b.lower() in name_lower:
            # 元の商品名からブランド名の部分を抽出（大文字小文字を保持）
            match = re.search(re.escape(b), name, re.IGNORECASE)
            if match:
                brand = match.group(0)
                break

    # ブランド名が見つからない場合は最初の単語を使用
    if not brand:
        brand = name.split()[0] if name.split() else name[:10]

    # 本文用の場合: 企業名+製品名（最大30文字）
    if not for_title:
        # ブランド名の後ろの部分を抽出
        brand_pattern = re.escape(brand)
        match = re.search(brand_pattern, name, re.IGNORECASE)
        if match:
            # ブランド名の後の部分を取得
            after_brand = name[match.end():].strip()
            # 不要な文字を削除（括弧、記号など）
            after_brand = re.sub(r'[\(\[].*?[\)\]]', '', after_brand).strip()
            # 単語を分割して最初の2-3語を取得
            words = after_brand.split()[:3]
            product_model = ' '.join(words)
            # 最大30文字に制限
            if len(product_model) > 30:
                product_model = product_model[:30]
            if product_model:
                return f"{brand} {product_model}"

    # タイトル用: 企業名+製品カテゴリー
    # PCパーツの場合
    is_pc_part = any(part in category or part in name for part in pc_parts_categories)

    if is_pc_part:
        # カテゴリー名を抽出
        for part_category in pc_parts_categories:
            if part_category in name or part_category in category:
                return f"{brand} {part_category}"
        # カテゴリーが見つからない場合はカテゴリー名を使用
        return f"{brand} {category}"

    # PC周辺機器の場合: 企業名+製品タイプ
    # 製品タイプのキーワード
    product_types = {
        "マウス": ["マウス", "mouse"],
        "キーボード": ["キーボード", "keyboard"],
        "モニター": ["モニター", "ディスプレイ", "monitor", "display"],
        "ヘッドセット": ["ヘッドセット", "headset"],
        "ヘッドホン": ["ヘッドホン", "headphone"],
        "イヤホン": ["イヤホン", "earphone"],
        "スピーカー": ["スピーカー", "speaker"],
        "Webカメラ": ["Webカメラ", "webcam", "カメラ"],
        "マイク": ["マイク", "microphone"],
        "充電器": ["充電器", "charger"],
        "ケーブル": ["ケーブル", "cable"],
        "ハブ": ["ハブ", "hub"],
    }

    # 製品タイプを検出
    for product_type, keywords in product_types.items():
        for keyword in keywords:
            if keyword.lower() in name_lower or keyword.lower() in category.lower():
                return f"{brand} {product_type}"

    # 製品タイプが見つからない場合はカテゴリー名を使用
    return f"{brand} {category}"


@dataclass
class GadgetProduct:
    """ガジェット商品情報"""
    name: str  # タイトル用の短い商品名（企業名+製品カテゴリー）
    asin: str  # Amazon Standard Identification Number
    url: str
    price: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    category: str = "PC周辺機器"
    features: Optional[List[str]] = None
    rating: Optional[float] = None
    full_name: Optional[str] = None  # 本文用の詳細な商品名（企業名+製品名）

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

        # 投稿済み商品とメタデータのファイルパス
        data_dir = os.path.dirname(self.products_file)
        self.posted_file = os.path.join(data_dir, 'posted_products.json')
        self.metadata_file = os.path.join(data_dir, 'products_metadata.json')

        self.posted_asins: List[str] = []
        self.load_products()
        self.load_posted_asins()
        self.check_and_refresh_products()

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

    def load_posted_asins(self):
        """投稿済み商品ASINリストを読み込み"""
        if os.path.exists(self.posted_file):
            try:
                with open(self.posted_file, 'r', encoding='utf-8') as f:
                    self.posted_asins = json.load(f)
            except Exception as e:
                print(f"投稿済み商品データの読み込みに失敗: {e}")
                self.posted_asins = []

    def save_posted_asins(self):
        """投稿済み商品ASINリストを保存"""
        os.makedirs(os.path.dirname(self.posted_file), exist_ok=True)
        with open(self.posted_file, 'w', encoding='utf-8') as f:
            json.dump(self.posted_asins, f, ensure_ascii=False, indent=2)

    def load_metadata(self) -> Dict:
        """メタデータを読み込み"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"メタデータの読み込みに失敗: {e}")
        return {}

    def save_metadata(self, metadata: Dict):
        """メタデータを保存"""
        os.makedirs(os.path.dirname(self.metadata_file), exist_ok=True)
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

    def check_and_refresh_products(self):
        """50日経過していたら商品データをリフレッシュ"""
        metadata = self.load_metadata()
        last_refresh = metadata.get('last_refresh_date')

        if last_refresh:
            last_refresh_date = datetime.fromisoformat(last_refresh)
            days_passed = (datetime.now() - last_refresh_date).days

            if days_passed >= 50:
                print(f"最後の更新から{days_passed}日経過しています。商品データをリフレッシュします。")
                self.refresh_products()
            else:
                print(f"最後の更新から{days_passed}日経過しています。（50日でリフレッシュ）")
        else:
            # 初回起動時
            print("商品データの初回起動です。メタデータを作成します。")
            metadata['last_refresh_date'] = datetime.now().isoformat()
            self.save_metadata(metadata)

    def refresh_products(self):
        """商品データと投稿履歴をリフレッシュ"""
        print("=" * 50)
        print("商品データのリフレッシュを開始します")
        print("=" * 50)

        # 投稿済みASINをクリア
        self.posted_asins = []
        self.save_posted_asins()
        print("✓ 投稿済み商品履歴をクリアしました")

        # メタデータを更新
        metadata = {
            'last_refresh_date': datetime.now().isoformat(),
            'refresh_count': self.load_metadata().get('refresh_count', 0) + 1
        }
        self.save_metadata(metadata)
        print(f"✓ メタデータを更新しました（リフレッシュ回数: {metadata['refresh_count']}回）")

        # 新しい商品データを生成
        try:
            # PA-APIを使用して新しい商品を取得
            from amazon_paapi_client import AmazonPAAPIClient

            print("PA-APIから新しい商品データを取得中...")
            paapi_client = AmazonPAAPIClient()

            new_products = []
            categories = list(paapi_client.SEARCH_KEYWORDS.keys())

            for category in categories:
                keywords = paapi_client.SEARCH_KEYWORDS[category]
                for keyword in keywords[:5]:  # 各カテゴリーから5キーワード
                    products = paapi_client.search_products(keyword, category, max_results=2)
                    new_products.extend(products)

                    if len(new_products) >= 100:
                        break

                if len(new_products) >= 100:
                    break

            # 重複を削除（ASINベース）
            seen_asins = set()
            unique_products = []
            for p in new_products:
                if p.asin not in seen_asins:
                    seen_asins.add(p.asin)
                    unique_products.append(p)

            # 100個に制限
            self.products = unique_products[:100]
            self.save_products()
            print(f"✓ PA-APIから{len(self.products)}個の新商品を取得しました")

        except Exception as e:
            print(f"警告: PA-APIでの商品取得に失敗しました - {e}")
            print("既存のローカルデータを維持します")

        print("=" * 50)
        print("商品データのリフレッシュが完了しました")
        print("=" * 50)

    def mark_as_posted(self, asin: str):
        """商品を投稿済みとしてマーク"""
        if asin not in self.posted_asins:
            self.posted_asins.append(asin)
            self.save_posted_asins()
            print(f"✓ 商品 {asin} を投稿済みとしてマークしました")

    def get_random_product(self, category: Optional[str] = None) -> Optional[GadgetProduct]:
        """
        投稿済みでない商品をランダムに取得

        Args:
            category: カテゴリーでフィルター（省略可）

        Returns:
            ランダムに選択された商品
        """
        if not self.products:
            return None

        # 投稿済みでない商品をフィルター
        available_products = [p for p in self.products if p.asin not in self.posted_asins]

        if not available_products:
            print("警告: 全ての商品が投稿済みです。投稿履歴をリセットします。")
            self.posted_asins = []
            self.save_posted_asins()
            available_products = self.products

        if category:
            filtered = [p for p in available_products if p.category == category]
            if not filtered:
                return None
            return random.choice(filtered)

        return random.choice(available_products)

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
            image_url="https://m.media-amazon.com/images/I/61ni3t1ryQL._AC_SL1500_.jpg",
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
            image_url="https://m.media-amazon.com/images/I/61dQWC2rqrL._AC_SL1500_.jpg",
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
            image_url="https://m.media-amazon.com/images/I/81i87RaT+bL._AC_SL1500_.jpg",
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
            image_url="https://m.media-amazon.com/images/I/61nMFVs9lDL._AC_SL1200_.jpg",
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
            image_url="https://m.media-amazon.com/images/I/61lNhK8WDSL._AC_SL1500_.jpg",
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
            image_url="https://m.media-amazon.com/images/I/61W7NVQfxkL._AC_SL1500_.jpg",
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
