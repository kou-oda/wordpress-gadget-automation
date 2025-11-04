from typing import Dict, List
from amazon_scraper import GadgetProduct
import random


class BlogPostGenerator:
    """ガジェットブログ記事生成クラス"""

    def __init__(self):
        self.review_templates = [
            "徹底レビュー",
            "使ってみた感想",
            "実機レビュー",
            "開封レビュー",
            "使用感レポート"
        ]

    def generate_title(self, product: GadgetProduct) -> str:
        """記事タイトルを生成"""
        template = random.choice(self.review_templates)
        return f"【{template}】{product.name} - {product.category}の新定番"

    def generate_introduction(self, product: GadgetProduct) -> str:
        """導入部分を生成"""
        intros = [
            f"今回は、{product.category}の中でも注目の「{product.name}」をご紹介します。",
            f"最近話題の{product.category}「{product.name}」を実際に使ってみました。",
            f"{product.category}をお探しの方に朗報です。今回レビューする「{product.name}」は、",
        ]

        intro = random.choice(intros)

        if product.description:
            intro += f"\n\n{product.description}"

        return intro

    def generate_features_section(self, product: GadgetProduct) -> str:
        """特徴セクションを生成"""
        if not product.features:
            return ""

        html = "<h2>主な特徴</h2>\n"
        html += "<ul>\n"

        for feature in product.features:
            html += f"  <li>{feature}</li>\n"

        html += "</ul>\n"

        return html

    def generate_pros_cons(self, product: GadgetProduct) -> str:
        """メリット・デメリットセクションを生成"""
        # サンプルとして一般的な内容を生成（実際の使用では個別にカスタマイズ推奨）
        html = "<h2>メリット・デメリット</h2>\n"

        html += "<h3>👍 メリット</h3>\n"
        html += "<ul>\n"
        if product.features and len(product.features) >= 2:
            html += f"  <li>{product.features[0]}</li>\n"
            html += f"  <li>{product.features[1]}</li>\n"
        html += "  <li>品質が高く長期間使用できる</li>\n"
        html += "  <li>デザインが洗練されている</li>\n"
        html += "</ul>\n"

        html += "<h3>👎 デメリット</h3>\n"
        html += "<ul>\n"
        html += "  <li>価格がやや高め</li>\n"
        html += "  <li>カラーバリエーションが少ない</li>\n"
        html += "</ul>\n"

        return html

    def generate_usage_section(self, product: GadgetProduct) -> str:
        """使用感セクションを生成"""
        html = "<h2>実際に使ってみた感想</h2>\n"

        if "マウス" in product.name or "mouse" in product.name.lower():
            html += "<p>手にフィットする形状で、長時間の作業でも疲れにくいのが印象的でした。"
            html += "クリック音も静かで、オフィスでの使用にも最適です。</p>\n"
        elif "キーボード" in product.name or "keyboard" in product.name.lower():
            html += "<p>タイピング感が非常に心地よく、文字入力が楽しくなります。"
            html += "キーの配置も使いやすく、慣れるとタイピング速度が向上しました。</p>\n"
        elif "SSD" in product.name or "メモリ" in product.name:
            html += "<p>導入後、システム全体のパフォーマンスが大幅に向上しました。"
            html += "起動時間やアプリケーションの読み込み速度が劇的に改善されています。</p>\n"
        else:
            html += "<p>期待通りの性能で、日常使いに最適な製品です。"
            html += "ビルドクオリティも高く、長く愛用できそうな印象を受けました。</p>\n"

        return html

    def generate_amazon_link_section(self, product: GadgetProduct) -> str:
        """Amazon購入リンクセクションを生成"""
        html = "<h2>購入リンク</h2>\n"

        price_text = f" - {product.price}" if product.price else ""
        html += f'<p><a href="{product.url}" target="_blank" rel="noopener noreferrer nofollow">'
        html += f'📦 Amazonで「{product.name}」を見る{price_text}</a></p>\n'

        html += '<p><small>※価格は変動する場合があります。最新の価格は商品ページでご確認ください。</small></p>\n'

        return html

    def generate_conclusion(self, product: GadgetProduct) -> str:
        """まとめセクションを生成"""
        html = "<h2>まとめ</h2>\n"

        conclusions = [
            f"「{product.name}」は、{product.category}を探している方に自信を持っておすすめできる製品です。",
            f"{product.category}の購入を検討している方には、「{product.name}」が最適な選択肢の一つです。",
            f"総合的に見て、「{product.name}」は{product.category}として非常に優れた製品だと感じました。",
        ]

        html += f"<p>{random.choice(conclusions)}"
        html += "価格に見合った価値があり、長期的な投資としても十分検討に値します。</p>\n"

        return html

    def generate_post_content(self, product: GadgetProduct) -> str:
        """完全な記事コンテンツを生成"""
        content = ""

        # 導入
        content += f"<p>{self.generate_introduction(product)}</p>\n\n"

        # 特徴
        content += self.generate_features_section(product)
        content += "\n"

        # 使用感
        content += self.generate_usage_section(product)
        content += "\n"

        # メリット・デメリット
        content += self.generate_pros_cons(product)
        content += "\n"

        # 購入リンク
        content += self.generate_amazon_link_section(product)
        content += "\n"

        # まとめ
        content += self.generate_conclusion(product)

        return content

    def generate_tags(self, product: GadgetProduct) -> List[str]:
        """記事タグを生成"""
        tags = [product.category, "レビュー", "Amazon"]

        # 商品名からキーワードを抽出
        if "マウス" in product.name:
            tags.extend(["マウス", "ワイヤレス", "PC周辺機器"])
        elif "キーボード" in product.name:
            tags.extend(["キーボード", "タイピング", "PC周辺機器"])
        elif "SSD" in product.name:
            tags.extend(["SSD", "ストレージ", "高速化"])
        elif "メモリ" in product.name:
            tags.extend(["メモリ", "RAM", "PC性能向上"])
        elif "モニター" in product.name or "ディスプレイ" in product.name:
            tags.extend(["モニター", "ディスプレイ", "作業環境"])

        # 重複を削除
        return list(set(tags))
