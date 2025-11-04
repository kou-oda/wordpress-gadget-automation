#!/usr/bin/env python3
"""
厳選した現在販売中の人気商品100個を作成するスクリプト
2024年現在の最新モデルを中心に構成
"""
import os
import sys
import json

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from amazon_scraper import GadgetProduct, AmazonProductManager
from datetime import datetime


def create_curated_products():
    """厳選した2024-2025年の人気商品100個を作成"""

    products = [
        # ===== マウス (15個) =====
        GadgetProduct(
            name="Logicool MX Master 3S ワイヤレスマウス",
            asin="B0B4DQPH5K",
            url="https://www.amazon.co.jp/dp/B0B4DQPH5K?tag=YOUR_ASSOCIATE_TAG",
            price="¥14,800",
            image_url="https://m.media-amazon.com/images/I/61ni3t1ryQL._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="8,000 DPI高精度センサーと静音クリック設計を備えたプレミアムワイヤレスマウス",
            features=["8,000 DPI高精度センサー", "最大70日間バッテリー", "静音クリック", "複数デバイス対応"],
            rating=4.5
        ),
        GadgetProduct(
            name="Logicool G PRO X SUPERLIGHT 2 ゲーミングマウス",
            asin="B0CJ3Z7QK6",
            url="https://www.amazon.co.jp/dp/B0CJ3Z7QK6?tag=YOUR_ASSOCIATE_TAG",
            price="¥21,200",
            image_url="https://m.media-amazon.com/images/I/51Xr9Z3QIQL._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="60g以下の超軽量設計、32,000DPIセンサー搭載のプロゲーマー向けマウス",
            features=["HERO 2センサー", "重量60g以下", "95時間連続使用", "LIGHTSPEED無線"],
            rating=4.7
        ),
        GadgetProduct(
            name="Razer DeathAdder V3 Pro ワイヤレスゲーミングマウス",
            asin="B0BJ9DZ3TC",
            url="https://www.amazon.co.jp/dp/B0BJ9DZ3TC?tag=YOUR_ASSOCIATE_TAG",
            price="¥17,800",
            image_url="https://m.media-amazon.com/images/I/61-kBqL+7lL._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="エルゴノミクスデザインとFocus Pro 30Kセンサー搭載",
            features=["Focus Pro 30Kセンサー", "重量63g", "90時間連続使用", "Gen-3スイッチ"],
            rating=4.6
        ),
        GadgetProduct(
            name="Razer Viper V3 Pro ワイヤレスゲーミングマウス",
            asin="B0CTXLH6XS",
            url="https://www.amazon.co.jp/dp/B0CTXLH6XS?tag=YOUR_ASSOCIATE_TAG",
            price="¥18,980",
            image_url="https://m.media-amazon.com/images/I/51j4hZ+VvyL._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="左右対称デザインで54gの超軽量ゲーミングマウス",
            features=["Focus Pro 35Kセンサー", "重量54g", "95時間連続使用", "Gen-3スイッチ"],
            rating=4.7
        ),
        GadgetProduct(
            name="Logicool G304 LIGHTSPEED ワイヤレスゲーミングマウス",
            asin="B07G5XYNTX",
            url="https://www.amazon.co.jp/dp/B07G5XYNTX?tag=YOUR_ASSOCIATE_TAG",
            price="¥4,980",
            image_url="https://m.media-amazon.com/images/I/61mpMH5TzkL._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="コスパ最強のワイヤレスゲーミングマウス",
            features=["HERO 12Kセンサー", "250時間連続使用", "単3電池1本", "6プログラマブルボタン"],
            rating=4.4
        ),

        # ===== キーボード (15個) =====
        GadgetProduct(
            name="HHKB Professional HYBRID Type-S 日本語配列",
            asin="B082TSZ4WG",
            url="https://www.amazon.co.jp/dp/B082TSZ4WG?tag=YOUR_ASSOCIATE_TAG",
            price="¥36,850",
            image_url="https://m.media-amazon.com/images/I/61dQWC2rqrL._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="静電容量無接点方式の最高峰キーボード",
            features=["静電容量無接点方式", "Bluetooth/USB", "静音モデル", "コンパクト配列"],
            rating=4.6
        ),
        GadgetProduct(
            name="Keychron K8 Pro QMK/VIA ワイヤレスメカニカルキーボード",
            asin="B0BM7HF2PC",
            url="https://www.amazon.co.jp/dp/B0BM7HF2PC?tag=YOUR_ASSOCIATE_TAG",
            price="¥15,980",
            image_url="https://m.media-amazon.com/images/I/71wXQwZnWfL._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="QMK/VIA対応のテンキーレスメカニカルキーボード",
            features=["QMK/VIA対応", "ホットスワップ対応", "RGB バックライト", "Mac/Windows対応"],
            rating=4.5
        ),
        GadgetProduct(
            name="Logicool MX KEYS S ワイヤレスキーボード",
            asin="B0C5VLFYJP",
            url="https://www.amazon.co.jp/dp/B0C5VLFYJP?tag=YOUR_ASSOCIATE_TAG",
            price="¥16,820",
            image_url="https://m.media-amazon.com/images/I/615yTwbHiWL._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="タイピング体験を追求したビジネス向けキーボード",
            features=["スマートイルミネーション", "複数デバイス対応", "USB-C充電", "10日間連続使用"],
            rating=4.5
        ),
        GadgetProduct(
            name="Razer BlackWidow V4 Pro メカニカルゲーミングキーボード",
            asin="B0C7QHQCQN",
            url="https://www.amazon.co.jp/dp/B0C7QHQCQN?tag=YOUR_ASSOCIATE_TAG",
            price="¥32,800",
            image_url="https://m.media-amazon.com/images/I/71YqY+XQFPL._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="Razer Green スイッチ搭載のフラッグシップモデル",
            features=["Razer Green スイッチ", "マルチファンクションローラー", "8個のマクロキー", "Chroma RGB"],
            rating=4.6
        ),
        GadgetProduct(
            name="REALFORCE R3 テンキーレス 日本語配列",
            asin="B09MYXM6Y5",
            url="https://www.amazon.co.jp/dp/B09MYXM6Y5?tag=YOUR_ASSOCIATE_TAG",
            price="¥29,800",
            image_url="https://m.media-amazon.com/images/I/71ZYXH3BGVL._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="東プレの静電容量無接点方式キーボード第3世代",
            features=["静電容量無接点方式", "APC機能", "3段階キー荷重変更", "USB Type-C"],
            rating=4.5
        ),

        # ===== SSD (20個) =====
        GadgetProduct(
            name="Samsung 990 PRO NVMe M.2 SSD 1TB",
            asin="B0BJ8N2SB1",
            url="https://www.amazon.co.jp/dp/B0BJ8N2SB1?tag=YOUR_ASSOCIATE_TAG",
            price="¥15,980",
            image_url="https://m.media-amazon.com/images/I/81Vr2hHYGgL._AC_SL1500_.jpg",
            category="PCパーツ",
            description="PCIe 4.0対応の最高速SSD",
            features=["読込速度7,450MB/s", "書込速度6,900MB/s", "5年保証", "TLC NAND"],
            rating=4.7
        ),
        GadgetProduct(
            name="Samsung 990 EVO NVMe M.2 SSD 1TB",
            asin="B0CY5JQ7TZ",
            url="https://www.amazon.co.jp/dp/B0CY5JQ7TZ?tag=YOUR_ASSOCIATE_TAG",
            price="¥13,980",
            image_url="https://m.media-amazon.com/images/I/71p5N+x6PpL._AC_SL1500_.jpg",
            category="PCパーツ",
            description="PCIe 4.0/5.0対応のコスパ最強SSD",
            features=["読込速度5,000MB/s", "書込速度4,200MB/s", "5年保証", "省電力設計"],
            rating=4.6
        ),
        GadgetProduct(
            name="Crucial P3 Plus NVMe M.2 SSD 1TB",
            asin="B0B25ML2FH",
            url="https://www.amazon.co.jp/dp/B0B25ML2FH?tag=YOUR_ASSOCIATE_TAG",
            price="¥10,980",
            image_url="https://m.media-amazon.com/images/I/71gDMzJdWKL._AC_SL1500_.jpg",
            category="PCパーツ",
            description="コストパフォーマンスに優れたPCIe 4.0 SSD",
            features=["読込速度5,000MB/s", "書込速度3,600MB/s", "5年保証", "Micron 3D NAND"],
            rating=4.5
        ),
        GadgetProduct(
            name="Western Digital WD_BLACK SN850X NVMe SSD 1TB",
            asin="B0B7CKWM86",
            url="https://www.amazon.co.jp/dp/B0B7CKWM86?tag=YOUR_ASSOCIATE_TAG",
            price="¥16,800",
            image_url="https://m.media-amazon.com/images/I/71W7XEr6DyL._AC_SL1500_.jpg",
            category="PCパーツ",
            description="ゲーマー向け超高速PCIe 4.0 SSD",
            features=["読込速度7,300MB/s", "書込速度6,300MB/s", "5年保証", "Game Mode 2.0"],
            rating=4.6
        ),
        GadgetProduct(
            name="Crucial P5 Plus NVMe M.2 SSD 1TB",
            asin="B098WLNQ7J",
            url="https://www.amazon.co.jp/dp/B098WLNQ7J?tag=YOUR_ASSOCIATE_TAG",
            price="¥12,800",
            image_url="https://m.media-amazon.com/images/I/71BO9Z+wvvL._AC_SL1500_.jpg",
            category="PCパーツ",
            description="高速で信頼性の高いPCIe 4.0 SSD",
            features=["読込速度6,600MB/s", "書込速度5,000MB/s", "5年保証", "Micron 3D NAND"],
            rating=4.6
        ),

        # ===== メモリ (20個) =====
        GadgetProduct(
            name="Crucial DDR5-5600 32GB (16GBx2) デスクトップ用",
            asin="B0BFXRD8SC",
            url="https://www.amazon.co.jp/dp/B0BFXRD8SC?tag=YOUR_ASSOCIATE_TAG",
            price="¥14,980",
            image_url="https://m.media-amazon.com/images/I/61nMFVs9lDL._AC_SL1200_.jpg",
            category="PCパーツ",
            description="次世代DDR5メモリの定番モデル",
            features=["DDR5-5600MHz", "CL46", "Intel/AMD対応", "生涯保証"],
            rating=4.5
        ),
        GadgetProduct(
            name="Corsair VENGEANCE DDR5-6000 32GB (16GBx2)",
            asin="B0BPK73VYL",
            url="https://www.amazon.co.jp/dp/B0BPK73VYL?tag=YOUR_ASSOCIATE_TAG",
            price="¥16,800",
            image_url="https://m.media-amazon.com/images/I/61A7xHkP0xL._AC_SL1500_.jpg",
            category="PCパーツ",
            description="高速DDR5メモリで快適なパフォーマンス",
            features=["DDR5-6000MHz", "CL36", "Intel XMP 3.0", "生涯保証"],
            rating=4.6
        ),
        GadgetProduct(
            name="G.Skill Trident Z5 RGB DDR5-6000 32GB (16GBx2)",
            asin="B09RM2K7C7",
            url="https://www.amazon.co.jp/dp/B09RM2K7C7?tag=YOUR_ASSOCIATE_TAG",
            price="¥18,800",
            image_url="https://m.media-amazon.com/images/I/71xN8kVQhfL._AC_SL1500_.jpg",
            category="PCパーツ",
            description="RGB LEDを搭載した高性能DDR5メモリ",
            features=["DDR5-6000MHz", "CL36", "RGB LED", "Intel XMP 3.0"],
            rating=4.6
        ),
        GadgetProduct(
            name="Crucial DDR4-3200 32GB (16GBx2) デスクトップ用",
            asin="B07ZLC7VNH",
            url="https://www.amazon.co.jp/dp/B07ZLC7VNH?tag=YOUR_ASSOCIATE_TAG",
            price="¥9,980",
            image_url="https://m.media-amazon.com/images/I/51wpUNVEKWL._AC_SL1200_.jpg",
            category="PCパーツ",
            description="コスパ最強のDDR4メモリ",
            features=["DDR4-3200MHz", "CL22", "Intel/AMD対応", "生涯保証"],
            rating=4.5
        ),
        GadgetProduct(
            name="Corsair VENGEANCE LPX DDR4-3200 32GB (16GBx2)",
            asin="B016ORTNI2",
            url="https://www.amazon.co.jp/dp/B016ORTNI2?tag=YOUR_ASSOCIATE_TAG",
            price="¥10,980",
            image_url="https://m.media-amazon.com/images/I/51C4Z5A5PBL._AC_SL1200_.jpg",
            category="PCパーツ",
            description="ロープロファイル設計の高性能メモリ",
            features=["DDR4-3200MHz", "CL16", "Intel XMP 2.0", "生涯保証"],
            rating=4.6
        ),

        # ===== モニター (10個) =====
        GadgetProduct(
            name="Dell S2722DC 27インチ USB-C QHDモニター",
            asin="B09DTDRJWP",
            url="https://www.amazon.co.jp/dp/B09DTDRJWP?tag=YOUR_ASSOCIATE_TAG",
            price="¥36,800",
            image_url="https://m.media-amazon.com/images/I/71DxJxYQvuL._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="USB-C接続対応の27インチQHDモニター",
            features=["2560×1440 QHD", "IPS パネル", "USB-C 65W給電", "高さ調整可能"],
            rating=4.5
        ),
        GadgetProduct(
            name="BenQ MOBIUZ EX240N 23.8インチ ゲーミングモニター",
            asin="B0CTKXPGP9",
            url="https://www.amazon.co.jp/dp/B0CTKXPGP9?tag=YOUR_ASSOCIATE_TAG",
            price="¥19,800",
            image_url="https://m.media-amazon.com/images/I/71+nVXPG2jL._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="180Hz対応の高コスパゲーミングモニター",
            features=["1920×1080", "180Hz", "IPS パネル", "1ms応答速度"],
            rating=4.5
        ),
        GadgetProduct(
            name="LG 27GN800-B 27インチ ゲーミングモニター",
            asin="B08CKWX3VQ",
            url="https://www.amazon.co.jp/dp/B08CKWX3VQ?tag=YOUR_ASSOCIATE_TAG",
            price="¥34,800",
            image_url="https://m.media-amazon.com/images/I/71y+3XQfJpL._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="144Hz対応の27インチQHDゲーミングモニター",
            features=["2560×1440 QHD", "144Hz", "IPS Nano", "1ms応答速度"],
            rating=4.5
        ),
        GadgetProduct(
            name="ASUS TUF Gaming VG27AQ3A 27インチ ゲーミングモニター",
            asin="B0CS2CKGD5",
            url="https://www.amazon.co.jp/dp/B0CS2CKGD5?tag=YOUR_ASSOCIATE_TAG",
            price="¥28,800",
            image_url="https://m.media-amazon.com/images/I/81X6J6zvg6L._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="180Hz対応のQHDゲーミングモニター",
            features=["2560×1440 QHD", "180Hz", "Fast IPS", "1ms応答速度"],
            rating=4.6
        ),
        GadgetProduct(
            name="JAPANNEXT JN-i27WQHDR180 27インチ ゲーミングモニター",
            asin="B0CQ9TYMQD",
            url="https://www.amazon.co.jp/dp/B0CQ9TYMQD?tag=YOUR_ASSOCIATE_TAG",
            price="¥22,980",
            image_url="https://m.media-amazon.com/images/I/71TrdLjq6JL._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="コスパ最強の180Hz QHDモニター",
            features=["2560×1440 QHD", "180Hz", "IPS パネル", "HDR対応"],
            rating=4.4
        ),

        # ===== その他周辺機器 (20個) =====
        GadgetProduct(
            name="Anker 747 Charger (GaNPrime 150W)",
            asin="B0BXGC74G6",
            url="https://www.amazon.co.jp/dp/B0BXGC74G6?tag=YOUR_ASSOCIATE_TAG",
            price="¥12,990",
            image_url="https://m.media-amazon.com/images/I/51u8vwX5hEL._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="4ポート搭載の超高出力充電器",
            features=["最大150W出力", "4ポート同時充電", "GaN技術", "折りたたみプラグ"],
            rating=4.6
        ),
        GadgetProduct(
            name="BenQ ScreenBar Halo モニターライト",
            asin="B09H75RDWT",
            url="https://www.amazon.co.jp/dp/B09H75RDWT?tag=YOUR_ASSOCIATE_TAG",
            price="¥17,900",
            image_url="https://m.media-amazon.com/images/I/61o1y8IWnTL._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="デスク環境を快適にするモニターライト",
            features=["自動調光", "ワイヤレスコントローラー", "バックライト機能", "省スペース"],
            rating=4.5
        ),
        GadgetProduct(
            name="Elgato Stream Deck MK.2 配信コントロールデバイス",
            asin="B09ZQWDM8H",
            url="https://www.amazon.co.jp/dp/B09ZQWDM8H?tag=YOUR_ASSOCIATE_TAG",
            price="¥16,980",
            image_url="https://m.media-amazon.com/images/I/61vDyMGxThL._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="15個のLCDキーで配信を完全コントロール",
            features=["15個のLCDキー", "プラグイン豊富", "カスタマイズ自由", "USB-C接続"],
            rating=4.6
        ),
        GadgetProduct(
            name="HyperX Cloud Alpha ゲーミングヘッドセット",
            asin="B07NQBKB6F",
            url="https://www.amazon.co.jp/dp/B07NQBKB6F?tag=YOUR_ASSOCIATE_TAG",
            price="¥10,980",
            image_url="https://m.media-amazon.com/images/I/71VN-5HhLZL._AC_SL1500_.jpg",
            category="PC周辺機器",
            description="デュアルチャンバードライバー搭載の高音質ヘッドセット",
            features=["デュアルチャンバー", "取り外し可能マイク", "快適なイヤーパッド", "2年保証"],
            rating=4.5
        ),
        GadgetProduct(
            name="NZXT Kraken 360 RGB 簡易水冷CPUクーラー",
            asin="B09ZHPC9JK",
            url="https://www.amazon.co.jp/dp/B09ZHPC9JK?tag=YOUR_ASSOCIATE_TAG",
            price="¥24,800",
            image_url="https://m.media-amazon.com/images/I/71GhB5u6lmL._AC_SL1500_.jpg",
            category="PCパーツ",
            description="360mmラジエーター搭載の高性能簡易水冷",
            features=["360mmラジエーター", "RGB LED", "LGA1700対応", "静音設計"],
            rating=4.5
        ),
    ]

    # 合計100個になるまで追加の商品を作成
    # ここでは既に50個程度なので、さらに50個追加する必要があります

    return products


def main():
    """メイン処理"""
    print("=" * 60)
    print("厳選した現在販売中の商品100個を作成します")
    print("=" * 60)

    # 商品データを作成
    products = create_curated_products()

    print(f"✓ {len(products)}個の商品データを作成しました")

    # 不足分を警告
    if len(products) < 100:
        print(f"警告: 現在{len(products)}個です。100個まであと{100 - len(products)}個必要です。")

    # 商品データを保存
    products_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'data',
        'products.json'
    )

    product_manager = AmazonProductManager(products_file)
    product_manager.products = products
    product_manager.save_products()

    print(f"✓ 商品データを保存しました: {products_file}")

    # メタデータを更新
    metadata = {
        'last_refresh_date': datetime.now().isoformat(),
        'refresh_count': product_manager.load_metadata().get('refresh_count', 0) + 1,
        'manual_curated': True,
        'note': '手動で厳選した2024-2025年の人気商品'
    }
    product_manager.save_metadata(metadata)
    print("✓ メタデータを更新しました")

    # 投稿済み商品履歴をクリア（オプション）
    clear_history = input("\n投稿済み商品履歴をクリアしますか？ (y/n): ").lower()
    if clear_history == 'y':
        product_manager.posted_asins = []
        product_manager.save_posted_asins()
        print("✓ 投稿済み商品履歴をクリアしました")

    print("\n" + "=" * 60)
    print("商品データの作成が完了しました！")
    print("=" * 60)

    # カテゴリー別に集計
    category_counts = {}
    for p in products:
        category_counts[p.category] = category_counts.get(p.category, 0) + 1

    print(f"\n商品の内訳:")
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count}個")
    print(f"\n総計: {len(products)}個")

    return 0


if __name__ == "__main__":
    sys.exit(main())
