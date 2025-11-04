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
        """導入部分を生成（400-600文字）"""
        intros = [
            f"今回は、{product.category}の中でも特に注目を集めている「{product.name}」を詳しくレビューしていきます。",
            f"最近、多くのユーザーから高い評価を得ている{product.category}「{product.name}」を実際に購入して使用してみました。",
            f"{product.category}の購入を検討している方に、ぜひ知っていただきたい製品があります。それが「{product.name}」です。",
        ]

        intro = random.choice(intros)

        if product.description:
            intro += f"\n\n{product.description}"

        intro += f"\n\n本記事では、実際に数週間使用して感じた良い点・悪い点、具体的な使用感、他製品との比較など、購入を検討されている方に役立つ情報を詳しくお伝えします。"

        if product.price:
            intro += f"現在の価格は{product.price}となっており、同カテゴリの製品と比較してもコストパフォーマンスに優れた選択肢となっています。"

        return intro

    def generate_spec_table(self, product: GadgetProduct) -> str:
        """スペック表を生成"""
        html = "<h2>製品スペック</h2>\n"
        html += "<table>\n"
        html += "<thead>\n<tr>\n<th>項目</th>\n<th>詳細</th>\n</tr>\n</thead>\n"
        html += "<tbody>\n"

        # 製品名
        html += f"<tr>\n<td>製品名</td>\n<td>{product.name}</td>\n</tr>\n"

        # カテゴリー別のスペック
        if "マウス" in product.name or "mouse" in product.name.lower():
            html += "<tr>\n<td>接続方式</td>\n<td>ワイヤレス（Bluetooth / USB レシーバー）</td>\n</tr>\n"
            html += "<tr>\n<td>センサー精度</td>\n<td>最大8,000 DPI</td>\n</tr>\n"
            html += "<tr>\n<td>バッテリー寿命</td>\n<td>最大70日間</td>\n</tr>\n"
            html += "<tr>\n<td>ボタン数</td>\n<td>7ボタン</td>\n</tr>\n"
            html += "<tr>\n<td>対応OS</td>\n<td>Windows / macOS / Linux</td>\n</tr>\n"

        elif "キーボード" in product.name or "keyboard" in product.name.lower():
            html += "<tr>\n<td>キースイッチ</td>\n<td>静電容量無接点方式</td>\n</tr>\n"
            html += "<tr>\n<td>キー配列</td>\n<td>日本語配列 / 英語配列</td>\n</tr>\n"
            html += "<tr>\n<td>接続方式</td>\n<td>Bluetooth / USB Type-C</td>\n</tr>\n"
            html += "<tr>\n<td>キーストローク</td>\n<td>4.0mm</td>\n</tr>\n"
            html += "<tr>\n<td>対応OS</td>\n<td>Windows / macOS / iOS / Android</td>\n</tr>\n"

        elif "SSD" in product.name:
            html += "<tr>\n<td>容量</td>\n<td>1TB</td>\n</tr>\n"
            html += "<tr>\n<td>インターフェース</td>\n<td>PCIe 4.0 x4 NVMe</td>\n</tr>\n"
            html += "<tr>\n<td>フォームファクタ</td>\n<td>M.2 2280</td>\n</tr>\n"
            html += "<tr>\n<td>読み込み速度</td>\n<td>最大7,000 MB/s</td>\n</tr>\n"
            html += "<tr>\n<td>書き込み速度</td>\n<td>最大5,000 MB/s</td>\n</tr>\n"
            html += "<tr>\n<td>保証期間</td>\n<td>5年間</td>\n</tr>\n"

        elif "メモリ" in product.name or "DDR" in product.name:
            html += "<tr>\n<td>容量</td>\n<td>32GB (16GB x 2)</td>\n</tr>\n"
            html += "<tr>\n<td>メモリ規格</td>\n<td>DDR5-4800</td>\n</tr>\n"
            html += "<tr>\n<td>動作電圧</td>\n<td>1.1V</td>\n</tr>\n"
            html += "<tr>\n<td>対応プラットフォーム</td>\n<td>Intel 第12世代以降 / AMD Ryzen 7000シリーズ</td>\n</tr>\n"
            html += "<tr>\n<td>保証期間</td>\n<td>無期限保証</td>\n</tr>\n"

        else:
            html += "<tr>\n<td>カテゴリー</td>\n<td>" + product.category + "</td>\n</tr>\n"
            html += "<tr>\n<td>対応デバイス</td>\n<td>PC / Mac</td>\n</tr>\n"
            html += "<tr>\n<td>接続方式</td>\n<td>USB Type-C</td>\n</tr>\n"

        if product.price:
            html += f"<tr>\n<td>参考価格</td>\n<td>{product.price}</td>\n</tr>\n"

        html += "</tbody>\n</table>\n"
        html += "<p><small>※スペックは一部参考値を含みます。正確な情報は製品ページでご確認ください。</small></p>\n"

        return html

    def generate_features_section(self, product: GadgetProduct) -> str:
        """特徴セクションを生成（詳細説明付き）"""
        if not product.features:
            return ""

        html = "<h2>主な特徴と機能</h2>\n"

        for i, feature in enumerate(product.features, 1):
            html += f"<h3>{i}. {feature}</h3>\n"

            # 各特徴に詳細説明を追加
            if "DPI" in feature or "センサー" in feature:
                html += "<p>高精度センサーにより、細かな作業から素早い操作まで、あらゆるシーンで正確なカーソル移動を実現します。"
                html += "DPI設定は専用ソフトウェアで自由にカスタマイズ可能で、用途に応じて最適な感度に調整できます。</p>\n"

            elif "バッテリー" in feature:
                html += "<p>長時間のバッテリー寿命により、頻繁な充電から解放されます。"
                html += "USB-Cケーブルでの充電にも対応しており、わずか数分の充電で数時間の使用が可能です。</p>\n"

            elif "静音" in feature or "クリック" in feature:
                html += "<p>静音設計により、オフィスや図書館など静かな環境でも周囲を気にせず使用できます。"
                html += "従来モデルと比較してクリック音を90%以上削減しており、快適な作業環境を提供します。</p>\n"

            elif "デバイス" in feature or "Bluetooth" in feature:
                html += "<p>複数のデバイス間を瞬時に切り替えられるマルチデバイス機能を搭載。"
                html += "PCとタブレット、スマートフォンなど、最大3台のデバイスをボタン一つで切り替えて使用できます。</p>\n"

            elif "キー" in feature or "タイピング" in feature:
                html += "<p>快適なタイピング感を実現するキースイッチにより、長時間の文字入力でも疲れにくい設計です。"
                html += "キーストロークの深さとアクチュエーションポイントが最適化されており、正確で心地よい入力体験を提供します。</p>\n"

            elif "速度" in feature or "MB/s" in feature:
                html += "<p>圧倒的な読み書き速度により、大容量ファイルの転送やアプリケーションの起動が劇的に高速化されます。"
                html += "従来のSATA SSDと比較して最大10倍以上の速度を実現し、作業効率が大幅に向上します。</p>\n"

            elif "MHz" in feature or "メモリ" in feature:
                html += "<p>高速なメモリ動作により、マルチタスク作業やクリエイティブワーク、ゲームプレイが快適に行えます。"
                html += "低レイテンシ設計により、システム全体のレスポンスが向上します。</p>\n"

            elif "保証" in feature:
                html += "<p>メーカーによる長期保証が付帯しており、万が一の故障時にも安心です。"
                html += "サポート体制も充実しており、技術的な質問にも迅速に対応してもらえます。</p>\n"

            else:
                html += f"<p>この機能により、{product.category}としての基本性能が大幅に向上しています。"
                html += "日常的な使用はもちろん、プロフェッショナルな用途にも十分対応できる仕様となっています。</p>\n"

        return html

    def generate_unboxing_section(self, product: GadgetProduct) -> str:
        """開封・外観セクションを生成"""
        html = "<h2>開封と外観</h2>\n"

        html += "<h3>パッケージ</h3>\n"
        html += "<p>製品は環境に配慮されたシンプルなパッケージで届きました。"
        html += "箱を開けると、本体が衝撃吸収材でしっかりと保護されており、配送中の破損リスクを最小限に抑える設計になっています。</p>\n"

        html += "<h3>付属品</h3>\n"
        html += "<ul>\n"
        html += "<li>本体</li>\n"

        if "マウス" in product.name:
            html += "<li>USBレシーバー</li>\n"
            html += "<li>USB-C充電ケーブル</li>\n"
        elif "キーボード" in product.name:
            html += "<li>USB-Cケーブル</li>\n"
            html += "<li>キーキャップ引き抜き工具</li>\n"
        elif "SSD" in product.name or "メモリ" in product.name:
            html += "<li>取り付けネジ（SSDの場合）</li>\n"
            html += "<li>取扱説明書</li>\n"
        else:
            html += "<li>接続ケーブル</li>\n"

        html += "<li>クイックスタートガイド</li>\n"
        html += "<li>保証書</li>\n"
        html += "</ul>\n"

        html += "<h3>デザインと質感</h3>\n"
        html += "<p>実際に手に取ってみると、製品写真以上に高級感のある仕上がりに驚かされます。"
        html += "表面の質感は非常に滑らかで、長時間使用しても指紋が目立ちにくい加工が施されています。"
        html += "細部まで丁寧に作り込まれており、この価格帯の製品としては非常に満足度の高い仕上がりです。</p>\n"

        return html

    def generate_detailed_usage_section(self, product: GadgetProduct) -> str:
        """詳細な使用感セクションを生成"""
        html = "<h2>実際に使ってみた感想</h2>\n"

        if "マウス" in product.name or "mouse" in product.name.lower():
            html += "<h3>セットアップ</h3>\n"
            html += "<p>接続は非常に簡単で、USBレシーバーをPCに挿すだけですぐに使用できました。"
            html += "Bluetoothでの接続も安定しており、ペアリングも数秒で完了します。"
            html += "専用ソフトウェアをインストールすることで、各ボタンの機能やDPI設定を細かくカスタマイズできます。</p>\n"

            html += "<h3>操作感</h3>\n"
            html += "<p>エルゴノミクスデザインにより、手にフィットする形状で長時間の作業でも疲れにくいのが印象的でした。"
            html += "クリック感は適度な重さがあり、誤クリックを防ぎつつ快適に操作できます。"
            html += "ホイールの回転も滑らかで、長いページのスクロールもストレスなく行えます。</p>\n"

            html += "<h3>作業効率</h3>\n"
            html += "<p>サイドボタンにカスタムショートカットを割り当てることで、作業効率が大幅に向上しました。"
            html += "特にブラウジングやドキュメント編集時の「戻る」「進む」操作が格段に楽になり、マウスから手を離す回数が減りました。</p>\n"

        elif "キーボード" in product.name or "keyboard" in product.name.lower():
            html += "<h3>セットアップ</h3>\n"
            html += "<p>USB-Cケーブルでの接続とBluetooth接続の両方に対応しており、環境に応じて使い分けられます。"
            html += "複数デバイスとのペアリングも簡単で、ボタン一つでPC、タブレット、スマートフォン間を切り替えられます。</p>\n"

            html += "<h3>タイピング感</h3>\n"
            html += "<p>静電容量無接点方式のキースイッチは、最初は独特の打鍵感に戸惑うかもしれませんが、慣れると病みつきになります。"
            html += "適度なキーストロークの深さと、心地よい反発力により、長文のタイピングでも疲れにくく、入力ミスも減少しました。"
            html += "静音性も高く、深夜の作業でも家族を起こす心配がありません。</p>\n"

            html += "<h3>作業効率</h3>\n"
            html += "<p>コンパクトな配列により、ホームポジションからの手の移動が最小限に抑えられます。"
            html += "慣れるまで1週間程度かかりましたが、今では通常のフルサイズキーボードよりも快適にタイピングできています。"
            html += "プログラミングやライティング作業の効率が明らかに向上しました。</p>\n"

        elif "SSD" in product.name:
            html += "<h3>取り付け</h3>\n"
            html += "<p>M.2スロットへの取り付けは非常に簡単で、PC自作初心者でも10分程度で完了できました。"
            html += "ヒートシンクは別途用意する必要がありますが、マザーボード付属のものでも十分に冷却できています。</p>\n"

            html += "<h3>パフォーマンス</h3>\n"
            html += "<p>ベンチマークテストでは、公称値に近い読み書き速度を記録しました。"
            html += "OSの起動時間は従来のSATA SSDから半分以下に短縮され、約10秒でデスクトップ画面が表示されます。"
            html += "大容量のゲームやアプリケーションの起動も驚くほど速く、ロード時間のストレスから解放されました。</p>\n"

            html += "<h3>実用性</h3>\n"
            html += "<p>4K動画編集やRAW現像などの重い作業でも、ファイルの読み込みや書き出しが格段に速くなりました。"
            html += "発熱も許容範囲内で、長時間の使用でもサーマルスロットリングは発生していません。</p>\n"

        elif "メモリ" in product.name:
            html += "<h3>取り付け</h3>\n"
            html += "<p>メモリスロットへの取り付けは工具不要で、カチッと音がするまで押し込むだけです。"
            html += "BIOS設定でXMPプロファイルを有効にすることで、定格速度で動作します。</p>\n"

            html += "<h3>パフォーマンス</h3>\n"
            html += "<p>32GBの大容量により、複数のアプリケーションを同時に起動してもメモリ不足に陥ることがなくなりました。"
            html += "Chrome で50タブ以上開いた状態でも、動画編集ソフトや画像編集ソフトを快適に使用できています。</p>\n"

            html += "<h3>実用性</h3>\n"
            html += "<p>ゲーム中のフレームレートが安定し、カクつきが大幅に減少しました。"
            html += "仮想マシンを複数起動しての開発作業も余裕でこなせるようになり、作業効率が飛躍的に向上しています。</p>\n"

        else:
            html += "<p>期待以上の性能で、日常使いからプロフェッショナルな用途まで幅広く対応できる製品です。"
            html += "ビルドクオリティも非常に高く、長期間の使用にも十分耐えられる作りになっています。</p>\n"

        return html

    def generate_comparison_section(self, product: GadgetProduct) -> str:
        """他製品との比較セクションを生成"""
        html = "<h2>競合製品との比較</h2>\n"

        html += f"<p>{product.category}の市場には多くの選択肢がありますが、「{product.name}」は以下の点で優位性があります。</p>\n"

        html += "<table>\n"
        html += "<thead>\n<tr>\n<th>比較項目</th>\n<th>本製品</th>\n<th>競合製品A</th>\n<th>競合製品B</th>\n</tr>\n</thead>\n"
        html += "<tbody>\n"

        if "マウス" in product.name:
            html += "<tr>\n<td>価格</td>\n<td>" + (product.price if product.price else "¥14,800") + "</td>\n<td>¥18,000</td>\n<td>¥12,000</td>\n</tr>\n"
            html += "<tr>\n<td>DPI</td>\n<td>最大8,000</td>\n<td>最大4,000</td>\n<td>最大16,000</td>\n</tr>\n"
            html += "<tr>\n<td>バッテリー</td>\n<td>70日</td>\n<td>40日</td>\n<td>120日</td>\n</tr>\n"
            html += "<tr>\n<td>重量</td>\n<td>約140g</td>\n<td>約120g</td>\n<td>約160g</td>\n</tr>\n"
            html += "<tr>\n<td>静音性</td>\n<td>◎</td>\n<td>○</td>\n<td>△</td>\n</tr>\n"

        elif "キーボード" in product.name:
            html += "<tr>\n<td>価格</td>\n<td>" + (product.price if product.price else "¥36,850") + "</td>\n<td>¥42,000</td>\n<td>¥28,000</td>\n</tr>\n"
            html += "<tr>\n<td>キースイッチ</td>\n<td>静電容量</td>\n<td>メカニカル</td>\n<td>メンブレン</td>\n</tr>\n"
            html += "<tr>\n<td>接続</td>\n<td>BT/USB</td>\n<td>USBのみ</td>\n<td>BT/USB</td>\n</tr>\n"
            html += "<tr>\n<td>静音性</td>\n<td>◎</td>\n<td>○</td>\n<td>◎</td>\n</tr>\n"
            html += "<tr>\n<td>耐久性</td>\n<td>◎</td>\n<td>◎</td>\n<td>△</td>\n</tr>\n"

        elif "SSD" in product.name:
            html += "<tr>\n<td>価格</td>\n<td>" + (product.price if product.price else "¥12,980") + "</td>\n<td>¥15,000</td>\n<td>¥10,000</td>\n</tr>\n"
            html += "<tr>\n<td>読込速度</td>\n<td>7,000MB/s</td>\n<td>5,000MB/s</td>\n<td>3,500MB/s</td>\n</tr>\n"
            html += "<tr>\n<td>書込速度</td>\n<td>5,000MB/s</td>\n<td>4,400MB/s</td>\n<td>3,000MB/s</td>\n</tr>\n"
            html += "<tr>\n<td>保証</td>\n<td>5年</td>\n<td>5年</td>\n<td>3年</td>\n</tr>\n"
            html += "<tr>\n<td>耐久性</td>\n<td>600TBW</td>\n<td>600TBW</td>\n<td>400TBW</td>\n</tr>\n"

        elif "メモリ" in product.name:
            html += "<tr>\n<td>価格</td>\n<td>" + (product.price if product.price else "¥16,800") + "</td>\n<td>¥19,000</td>\n<td>¥14,500</td>\n</tr>\n"
            html += "<tr>\n<td>容量</td>\n<td>32GB(16x2)</td>\n<td>32GB(16x2)</td>\n<td>32GB(16x2)</td>\n</tr>\n"
            html += "<tr>\n<td>速度</td>\n<td>DDR5-4800</td>\n<td>DDR5-5200</td>\n<td>DDR5-4800</td>\n</tr>\n"
            html += "<tr>\n<td>保証</td>\n<td>無期限</td>\n<td>無期限</td>\n<td>10年</td>\n</tr>\n"
            html += "<tr>\n<td>ヒートシンク</td>\n<td>あり</td>\n<td>あり</td>\n<td>なし</td>\n</tr>\n"

        html += "</tbody>\n</table>\n"

        html += f"<p>表からもわかるように、「{product.name}」は価格と性能のバランスが非常に優れています。"
        html += "最高スペックを求めるのであれば他の選択肢もありますが、実用上十分な性能をコストパフォーマンス良く手に入れたい方には最適な選択です。</p>\n"

        return html

    def generate_pros_cons(self, product: GadgetProduct) -> str:
        """詳細なメリット・デメリットセクションを生成"""
        html = "<h2>メリット・デメリット</h2>\n"

        html += "<h3>👍 メリット</h3>\n"
        html += "<ul>\n"
        if product.features:
            for feature in product.features[:3]:
                html += f"  <li><strong>{feature}</strong> - 日常使用で大きなアドバンテージ</li>\n"
        html += "  <li><strong>優れたビルドクオリティ</strong> - 長期使用に耐える堅牢な作り</li>\n"
        html += "  <li><strong>洗練されたデザイン</strong> - デスク環境に馴染む美しい外観</li>\n"
        html += "  <li><strong>充実したサポート</strong> - メーカーのアフターサービスが手厚い</li>\n"
        html += "  <li><strong>コストパフォーマンス</strong> - 価格に対する性能が優秀</li>\n"
        html += "</ul>\n"

        html += "<h3>👎 デメリット</h3>\n"
        html += "<ul>\n"
        html += "  <li><strong>価格</strong> - 同カテゴリの中では高価格帯に位置する</li>\n"
        html += "  <li><strong>カラーバリエーション</strong> - 選択肢が限られている</li>\n"
        html += "  <li><strong>重量</strong> - 軽量モデルと比較するとやや重め（該当する場合）</li>\n"
        html += "  <li><strong>学習コスト</strong> - 独自の操作に慣れるまで時間が必要な場合がある</li>\n"
        html += "</ul>\n"

        html += "<p>デメリットはありますが、実際に使用してみるとメリットの方が圧倒的に大きいと感じました。"
        html += "特に価格については、長期的に使用することを考えれば十分に投資価値があると言えます。</p>\n"

        return html

    def generate_who_should_buy(self, product: GadgetProduct) -> str:
        """こんな人におすすめセクションを生成"""
        html = "<h2>こんな人におすすめ</h2>\n"

        html += "<h3>✓ おすすめできる人</h3>\n"
        html += "<ul>\n"

        if "マウス" in product.name:
            html += "  <li>長時間のPC作業をする方</li>\n"
            html += "  <li>手の疲れを軽減したい方</li>\n"
            html += "  <li>静かなオフィス環境で使用する方</li>\n"
            html += "  <li>複数のデバイスを使い分けている方</li>\n"
        elif "キーボード" in product.name:
            html += "  <li>タイピングの質にこだわる方</li>\n"
            html += "  <li>プログラマーやライター</li>\n"
            html += "  <li>長文入力が多い方</li>\n"
            html += "  <li>コンパクトなデスク環境の方</li>\n"
        elif "SSD" in product.name:
            html += "  <li>PCの起動速度を改善したい方</li>\n"
            html += "  <li>動画編集やゲームをする方</li>\n"
            html += "  <li>大容量ファイルを頻繁に扱う方</li>\n"
            html += "  <li>PC全体の性能向上を図りたい方</li>\n"
        elif "メモリ" in product.name:
            html += "  <li>マルチタスク作業が多い方</li>\n"
            html += "  <li>クリエイティブワークをする方</li>\n"
            html += "  <li>ゲーミングPCを構築中の方</li>\n"
            html += "  <li>仮想環境を使用する開発者</li>\n"

        html += f"  <li>品質重視で{product.category}を選びたい方</li>\n"
        html += "  <li>長期的な投資として考えられる方</li>\n"
        html += "</ul>\n"

        html += "<h3>✗ おすすめできない人</h3>\n"
        html += "<ul>\n"
        html += "  <li>とにかく最安値の製品を探している方</li>\n"
        html += "  <li>最高スペックにこだわる方（より上位モデルが存在する場合）</li>\n"
        html += "  <li>軽量性を最優先する方</li>\n"
        html += "</ul>\n"

        return html

    def generate_amazon_link_section(self, product: GadgetProduct) -> str:
        """Amazon購入リンクセクションを生成"""
        html = "<h2>購入リンク</h2>\n"

        price_text = f" - {product.price}" if product.price else ""
        html += f'<p><a href="{product.url}" target="_blank" rel="noopener noreferrer nofollow">'
        html += f'📦 Amazonで「{product.name}」を見る{price_text}</a></p>\n'

        html += '<p><small>※価格は変動する場合があります。最新の価格や在庫状況は商品ページでご確認ください。</small></p>\n'
        html += '<p><small>※Amazon.co.jpアソシエイトプログラムに参加しています。</small></p>\n'

        return html

    def generate_conclusion(self, product: GadgetProduct) -> str:
        """まとめセクションを生成"""
        html = "<h2>まとめ</h2>\n"

        conclusions = [
            f"実際に数週間使用してみて、「{product.name}」は{product.category}として非常に完成度の高い製品だと感じました。",
            f"総合的に評価すると、「{product.name}」は価格以上の価値を提供してくれる優秀な{product.category}です。",
            f"様々な{product.category}を試してきましたが、「{product.name}」はその中でもトップクラスの満足度です。",
        ]

        html += f"<p>{random.choice(conclusions)}</p>\n"

        html += f"<p>確かに価格は安くありませんが、その分品質やサポート体制がしっかりしており、長期的に見ればコストパフォーマンスに優れています。"
        html += f"特に、{product.features[0] if product.features else '基本性能'}は期待以上で、日常的な使用において大きな満足感を得られるはずです。</p>\n"

        html += f"<p>{product.category}の購入を検討している方で、品質と性能を重視するなら、「{product.name}」は間違いなく有力な選択肢の一つとなるでしょう。"
        html += "ぜひ実際に試してみて、その良さを実感していただきたいと思います。</p>\n"

        html += "<p><strong>最終評価: ★★★★☆ (4.5/5.0)</strong></p>\n"

        return html

    def generate_post_content(self, product: GadgetProduct) -> str:
        """完全な記事コンテンツを生成（2000-4000文字）"""
        content = ""

        # 導入（400-600文字）
        content += f"<p>{self.generate_introduction(product)}</p>\n\n"

        # スペック表
        content += self.generate_spec_table(product)
        content += "\n"

        # 開封・外観
        content += self.generate_unboxing_section(product)
        content += "\n"

        # 特徴（詳細説明付き）
        content += self.generate_features_section(product)
        content += "\n"

        # 詳細な使用感
        content += self.generate_detailed_usage_section(product)
        content += "\n"

        # 他製品との比較
        content += self.generate_comparison_section(product)
        content += "\n"

        # メリット・デメリット
        content += self.generate_pros_cons(product)
        content += "\n"

        # こんな人におすすめ
        content += self.generate_who_should_buy(product)
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
            tags.extend(["マウス", "ワイヤレス", "PC周辺機器", "エルゴノミクス"])
        elif "キーボード" in product.name:
            tags.extend(["キーボード", "タイピング", "PC周辺機器", "静音"])
        elif "SSD" in product.name:
            tags.extend(["SSD", "ストレージ", "高速化", "NVMe", "PCパーツ"])
        elif "メモリ" in product.name:
            tags.extend(["メモリ", "RAM", "PC性能向上", "DDR5", "PCパーツ"])
        elif "モニター" in product.name or "ディスプレイ" in product.name:
            tags.extend(["モニター", "ディスプレイ", "作業環境", "PC周辺機器"])

        # 重複を削除
        return list(set(tags))
