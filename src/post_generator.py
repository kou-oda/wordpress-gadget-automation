from typing import Dict, List
from amazon_scraper import GadgetProduct
import random
import re


class BlogPostGenerator:
    """ガジェットブログ記事生成クラス"""

    def __init__(self):
        self.review_templates = [
            "徹底解説！",
            "詳細レビュー！",
            "性能チェック！",
            "本当におすすめ？",
            "買うべき？"
        ]

    def generate_title(self, product: GadgetProduct) -> str:
        """SEO最適化された記事タイトルを生成"""
        import datetime
        current_year = datetime.datetime.now().year

        # ブランド名を抽出（商品名の最初の単語）
        brand = product.name.split()[0] if product.name else ""

        # SEO最適化されたテンプレート
        # 検索意図に合わせた構造: 「商品名 + 検索されやすいキーワード + 年」
        templates = [
            f"【{current_year}年版】{product.name} レビュー｜{product.category}の実力を徹底検証",
            f"{product.name} 口コミ・評判まとめ｜{current_year}年最新レビュー",
            f"【{random.choice(self.review_templates)}】{product.name}｜{product.category}おすすめモデル",
            f"{product.name} 使用レビュー｜メリット・デメリットを正直に評価【{current_year}】",
            f"{brand} {product.name} レビュー｜{product.category}の選び方完全ガイド",
            f"【実機レビュー】{product.name}は買い？{product.category}として徹底解説",
            f"{product.name} 性能比較レビュー｜{current_year}年版{product.category}の決定版",
        ]
        return random.choice(templates)

    def get_price_range(self, price_str: str) -> str:
        """具体的な価格から価格帯を抽出"""
        if not price_str:
            return ""

        # 価格から数値を抽出
        match = re.search(r'¥?([\d,]+)', price_str)
        if not match:
            return ""

        price_num = int(match.group(1).replace(',', ''))

        if price_num < 5000:
            return "5千円未満"
        elif price_num < 10000:
            return "5千円台～1万円未満"
        elif price_num < 20000:
            return "1万円台"
        elif price_num < 30000:
            return "2万円台"
        elif price_num < 40000:
            return "3万円台"
        elif price_num < 50000:
            return "4万円台"
        else:
            return "5万円以上"

    def generate_introduction(self, product: GadgetProduct) -> str:
        """導入部分を生成（感情的で読者に呼びかける形式）"""
        intros = [
            f"{product.category}選びで悩んでいませんか？今回ご紹介する「{product.name}」は、そんな方にぜひチェックしていただきたい注目の製品です！",
            f"「{product.name}」をご存知でしょうか？{product.category}の中でも特に高い評価を得ている、今話題の製品なんです。",
            f"{product.category}の新しい選択肢として、「{product.name}」が注目を集めています。一体どんな特徴があるのでしょうか？",
        ]

        intro = random.choice(intros)

        if product.description:
            intro += f"\n\n{product.description}という特徴を持つこの製品、実際のところはどうなのでしょうか？"

        intro += f"\n\n本記事では、「{product.name}」のスペックや機能、メリット・デメリット、どんな方におすすめなのかなど、購入前に知っておきたい情報を徹底解説していきます！"

        price_range = self.get_price_range(product.price) if product.price else ""
        if price_range:
            intro += f"価格帯は{price_range}となっており、コストパフォーマンスも気になるところですよね。"

        return intro

    def generate_spec_table(self, product: GadgetProduct) -> str:
        """スペック表を生成（項目を増やして充実化）"""
        html = "<h2>製品スペック</h2>\n"
        html += "<table>\n"
        html += "<thead>\n<tr>\n<th>項目</th>\n<th>詳細</th>\n</tr>\n</thead>\n"
        html += "<tbody>\n"

        # 製品名とカテゴリー
        html += f"<tr>\n<td>製品名</td>\n<td>{product.name}</td>\n</tr>\n"
        html += f"<tr>\n<td>カテゴリー</td>\n<td>{product.category}</td>\n</tr>\n"

        # カテゴリー別のスペック
        if "マウス" in product.name or "mouse" in product.name.lower():
            html += "<tr>\n<td>接続方式</td>\n<td>ワイヤレス（Bluetooth / USB レシーバー）</td>\n</tr>\n"
            html += "<tr>\n<td>センサータイプ</td>\n<td>光学式センサー</td>\n</tr>\n"
            html += "<tr>\n<td>センサー精度</td>\n<td>最大8,000 DPI</td>\n</tr>\n"
            html += "<tr>\n<td>バッテリー寿命</td>\n<td>最大70日間</td>\n</tr>\n"
            html += "<tr>\n<td>充電方式</td>\n<td>USB Type-C</td>\n</tr>\n"
            html += "<tr>\n<td>ボタン数</td>\n<td>7ボタン（カスタマイズ可能）</td>\n</tr>\n"
            html += "<tr>\n<td>重量</td>\n<td>約140g</td>\n</tr>\n"
            html += "<tr>\n<td>サイズ</td>\n<td>約125 x 85 x 45 mm</td>\n</tr>\n"
            html += "<tr>\n<td>対応OS</td>\n<td>Windows / macOS / Linux</td>\n</tr>\n"

        elif "キーボード" in product.name or "keyboard" in product.name.lower():
            html += "<tr>\n<td>キースイッチ</td>\n<td>静電容量無接点方式</td>\n</tr>\n"
            html += "<tr>\n<td>キー配列</td>\n<td>日本語配列 / 英語配列</td>\n</tr>\n"
            html += "<tr>\n<td>キー数</td>\n<td>60キー（コンパクト配列）</td>\n</tr>\n"
            html += "<tr>\n<td>接続方式</td>\n<td>Bluetooth 5.0 / USB Type-C</td>\n</tr>\n"
            html += "<tr>\n<td>キーストローク</td>\n<td>4.0mm</td>\n</tr>\n"
            html += "<tr>\n<td>アクチュエーションポイント</td>\n<td>2.0mm</td>\n</tr>\n"
            html += "<tr>\n<td>バッテリー寿命</td>\n<td>最大3ヶ月（Bluetooth使用時）</td>\n</tr>\n"
            html += "<tr>\n<td>重量</td>\n<td>約540g</td>\n</tr>\n"
            html += "<tr>\n<td>対応OS</td>\n<td>Windows / macOS / iOS / Android</td>\n</tr>\n"

        elif "SSD" in product.name:
            html += "<tr>\n<td>容量</td>\n<td>1TB</td>\n</tr>\n"
            html += "<tr>\n<td>インターフェース</td>\n<td>PCIe 4.0 x4 NVMe</td>\n</tr>\n"
            html += "<tr>\n<td>フォームファクタ</td>\n<td>M.2 2280</td>\n</tr>\n"
            html += "<tr>\n<td>コントローラー</td>\n<td>自社製コントローラー</td>\n</tr>\n"
            html += "<tr>\n<td>NANDタイプ</td>\n<td>3D TLC NAND</td>\n</tr>\n"
            html += "<tr>\n<td>読み込み速度</td>\n<td>最大7,000 MB/s</td>\n</tr>\n"
            html += "<tr>\n<td>書き込み速度</td>\n<td>最大5,000 MB/s</td>\n</tr>\n"
            html += "<tr>\n<td>MTBF</td>\n<td>150万時間</td>\n</tr>\n"
            html += "<tr>\n<td>保証期間</td>\n<td>5年間</td>\n</tr>\n"

        elif "メモリ" in product.name or "DDR" in product.name:
            html += "<tr>\n<td>容量</td>\n<td>32GB (16GB x 2)</td>\n</tr>\n"
            html += "<tr>\n<td>メモリ規格</td>\n<td>DDR5-4800</td>\n</tr>\n"
            html += "<tr>\n<td>メモリタイプ</td>\n<td>UDIMM（デスクトップ用）</td>\n</tr>\n"
            html += "<tr>\n<td>動作電圧</td>\n<td>1.1V</td>\n</tr>\n"
            html += "<tr>\n<td>レイテンシ</td>\n<td>CL40</td>\n</tr>\n"
            html += "<tr>\n<td>ヒートシンク</td>\n<td>アルミ製ヒートスプレッダー搭載</td>\n</tr>\n"
            html += "<tr>\n<td>対応プラットフォーム</td>\n<td>Intel 第12世代以降 / AMD Ryzen 7000シリーズ</td>\n</tr>\n"
            html += "<tr>\n<td>XMP対応</td>\n<td>XMP 3.0対応</td>\n</tr>\n"
            html += "<tr>\n<td>保証期間</td>\n<td>無期限保証</td>\n</tr>\n"

        else:
            html += "<tr>\n<td>対応デバイス</td>\n<td>PC / Mac</td>\n</tr>\n"
            html += "<tr>\n<td>接続方式</td>\n<td>USB Type-C</td>\n</tr>\n"
            html += "<tr>\n<td>ケーブル長</td>\n<td>約1.5m</td>\n</tr>\n"
            html += "<tr>\n<td>電源</td>\n<td>USBバスパワー</td>\n</tr>\n"
            html += "<tr>\n<td>重量</td>\n<td>約200g</td>\n</tr>\n"
            html += "<tr>\n<td>サイズ</td>\n<td>約100 x 50 x 20 mm</td>\n</tr>\n"
            html += "<tr>\n<td>保証期間</td>\n<td>1年間</td>\n</tr>\n"

        price_range = self.get_price_range(product.price) if product.price else ""
        if price_range:
            html += f"<tr>\n<td>価格帯</td>\n<td>{price_range}</td>\n</tr>\n"

        html += "</tbody>\n</table>\n"
        html += "<p><small>※スペックは一部参考値を含みます。正確な情報は製品ページでご確認ください。</small></p>\n"

        return html

    def generate_features_section(self, product: GadgetProduct) -> str:
        """特徴セクションを生成（見出しの番号を削除）"""
        if not product.features:
            return ""

        html = "<h2>主な特徴と機能</h2>\n"

        for feature in product.features:
            html += f"<h3>{feature}</h3>\n"

            # 各特徴に詳細説明を追加
            if "DPI" in feature or "センサー" in feature:
                html += "<p>高精度センサーにより、細かな作業から素早い操作まで、あらゆるシーンで正確なカーソル移動を実現します。"
                html += "DPI設定は専用ソフトウェアで自由にカスタマイズ可能で、用途に応じて最適な感度に調整できます。</p>\n"

            elif "バッテリー" in feature:
                html += "<p>長時間のバッテリー寿命により、頻繁な充電から解放されます。"
                html += "USB-Cケーブルでの充電にも対応しており、わずか数分の充電で数時間の使用が可能です。</p>\n"

            elif "静音" in feature or "クリック" in feature:
                html += "<p>静音設計により、オフィスや図書館など静かな環境でも周囲を気にせず使用できます。"
                html += "従来モデルと比較してクリック音を大幅に削減しており、快適な作業環境を提供します。</p>\n"

            elif "デバイス" in feature or "Bluetooth" in feature:
                html += "<p>複数のデバイス間を瞬時に切り替えられるマルチデバイス機能を搭載。"
                html += "PCとタブレット、スマートフォンなど、複数のデバイスをボタン一つで切り替えて使用できます。</p>\n"

            elif "キー" in feature or "タイピング" in feature:
                html += "<p>快適なタイピング感を実現するキースイッチにより、長時間の文字入力でも疲れにくい設計です。"
                html += "キーストロークの深さとアクチュエーションポイントが最適化されており、正確で心地よい入力体験を提供します。</p>\n"

            elif "速度" in feature or "MB/s" in feature:
                html += "<p>圧倒的な読み書き速度により、大容量ファイルの転送やアプリケーションの起動が劇的に高速化されます。"
                html += "従来のSATA SSDと比較して大幅な速度向上を実現し、作業効率が大幅に向上します。</p>\n"

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

    def generate_usage_scenarios(self, product: GadgetProduct) -> str:
        """使用シーン・活用方法セクションを生成"""
        html = "<h2>使用シーンと活用方法</h2>\n"

        if "マウス" in product.name or "mouse" in product.name.lower():
            html += "<h3>オフィスワーク</h3>\n"
            html += "<p>長時間のデスクワークでも疲れにくいエルゴノミクスデザインを採用しています。"
            html += "静音クリック機能により、静かなオフィス環境でも周囲に配慮した使用が可能です。"
            html += "複数のカスタマイズ可能なボタンにより、よく使う機能を割り当てることで作業効率が向上します。</p>\n"

            html += "<h3>クリエイティブワーク</h3>\n"
            html += "<p>高精度センサーにより、グラフィックデザインや動画編集などの細かな作業に最適です。"
            html += "DPI調整機能を活用することで、精密な操作が要求される作業も快適に行えます。</p>\n"

            html += "<h3>在宅勤務・リモートワーク</h3>\n"
            html += "<p>Bluetooth接続により、複数のデバイス間をシームレスに切り替えられます。"
            html += "PC作業中にタブレットやスマートフォンを操作する際も、同じマウスで対応可能です。</p>\n"

        elif "キーボード" in product.name or "keyboard" in product.name.lower():
            html += "<h3>プログラミング</h3>\n"
            html += "<p>コンパクトな配列により、ホームポジションからの手の移動を最小限に抑えられます。"
            html += "高速なタイピングが可能で、コーディング効率が向上します。</p>\n"

            html += "<h3>ライティング・文書作成</h3>\n"
            html += "<p>快適なタイピング感により、長文の執筆作業でも疲労を軽減できます。"
            html += "静音性が高いため、カフェや図書館など公共の場でも使用しやすい設計です。</p>\n"

            html += "<h3>マルチデバイス環境</h3>\n"
            html += "<p>PC、タブレット、スマートフォンなど複数のデバイスとペアリング可能です。"
            html += "デバイス切り替えボタンにより、用途に応じて瞬時に切り替えられます。</p>\n"

        elif "SSD" in product.name:
            html += "<h3>システムドライブとして</h3>\n"
            html += "<p>OSをインストールすることで、PC起動時間やアプリケーションの起動速度が劇的に向上します。"
            html += "高速な読み書き性能により、システム全体のレスポンスが改善されます。</p>\n"

            html += "<h3>動画編集・クリエイティブワーク</h3>\n"
            html += "<p>大容量の動画ファイルやRAWデータの読み込みが高速化され、作業効率が向上します。"
            html += "プロジェクトファイルの保存や書き出しもスムーズに行えます。</p>\n"

            html += "<h3>ゲーミング</h3>\n"
            html += "<p>ゲームのインストールやロード時間が短縮され、快適なゲーム体験を実現します。"
            html += "大容量ゲームも複数インストール可能です。</p>\n"

        elif "メモリ" in product.name:
            html += "<h3>マルチタスク作業</h3>\n"
            html += "<p>複数のアプリケーションを同時に起動しても、メモリ不足によるパフォーマンス低下を防ぎます。"
            html += "ブラウザで多数のタブを開きながら、他の作業も快適に行えます。</p>\n"

            html += "<h3>仮想環境・開発作業</h3>\n"
            html += "<p>仮想マシンを複数起動しての開発作業や、Docker環境の構築が快適に行えます。"
            html += "大規模なプロジェクトのビルド時間も短縮されます。</p>\n"

            html += "<h3>クリエイティブワーク・ゲーミング</h3>\n"
            html += "<p>動画編集や3DCG制作など、メモリを大量に消費する作業も快適です。"
            html += "最新ゲームも推奨環境を満たし、安定したフレームレートで楽しめます。</p>\n"

        else:
            html += "<p>様々な使用シーンで活躍する製品です。"
            html += "日常的な使用からプロフェッショナルな用途まで幅広く対応できます。</p>\n"

        return html

    def generate_pros_cons(self, product: GadgetProduct) -> str:
        """詳細なメリット・デメリットセクションを生成"""
        html = "<h2>メリットとデメリット</h2>\n"

        html += "<h3>メリット</h3>\n"
        html += "<ul>\n"
        if product.features:
            for feature in product.features[:3]:
                html += f"  <li><strong>{feature}</strong>により日常使用で大きなメリット</li>\n"
        html += "  <li>優れたビルドクオリティで長期使用に適している</li>\n"
        html += "  <li>洗練されたデザインでデスク環境に馴染む</li>\n"
        html += "  <li>充実したサポート体制でアフターサービスが手厚い</li>\n"
        html += "  <li>価格に対する性能バランスが良好</li>\n"
        html += "</ul>\n"

        html += "<h3>デメリット</h3>\n"
        html += "<ul>\n"
        html += "  <li>同カテゴリの中では比較的高価格帯に位置する</li>\n"
        html += "  <li>カラーバリエーションの選択肢が限定的</li>\n"
        html += "  <li>軽量性重視のモデルと比較するとやや重量がある場合がある</li>\n"
        html += "  <li>独自の機能や操作に慣れるまで時間を要する場合がある</li>\n"
        html += "</ul>\n"

        html += "<p>デメリットもありますが、全体的に見ればメリットの方が大きいと評価できます。"
        html += "特に長期的な使用を考えた場合、品質とサポート体制の充実は大きな魅力となります。</p>\n"

        return html

    def generate_who_should_buy(self, product: GadgetProduct) -> str:
        """おすすめの方セクションを生成"""
        html = "<h2>どのような方におすすめか</h2>\n"

        html += "<h3>特におすすめの方</h3>\n"
        html += "<ul>\n"

        if "マウス" in product.name:
            html += "  <li>長時間のPC作業を日常的に行う方</li>\n"
            html += "  <li>手や腕の疲労を軽減したい方</li>\n"
            html += "  <li>静かなオフィス環境で使用する方</li>\n"
            html += "  <li>複数のデバイスを日常的に使い分けている方</li>\n"
        elif "キーボード" in product.name:
            html += "  <li>タイピングの質や快適性を重視する方</li>\n"
            html += "  <li>プログラマーやライターなど文字入力が多い職業の方</li>\n"
            html += "  <li>長文入力を頻繁に行う方</li>\n"
            html += "  <li>コンパクトなデスク環境を好む方</li>\n"
        elif "SSD" in product.name:
            html += "  <li>PCの起動速度や動作速度を改善したい方</li>\n"
            html += "  <li>動画編集やゲームなど高負荷な作業を行う方</li>\n"
            html += "  <li>大容量ファイルを頻繁に扱う方</li>\n"
            html += "  <li>PC全体の性能向上を図りたい方</li>\n"
        elif "メモリ" in product.name:
            html += "  <li>マルチタスク作業を頻繁に行う方</li>\n"
            html += "  <li>クリエイティブワークやデザイン作業を行う方</li>\n"
            html += "  <li>ゲーミングPCを構築中の方</li>\n"
            html += "  <li>仮想環境を使用する開発者の方</li>\n"

        html += f"  <li>品質を重視して{product.category}を選びたい方</li>\n"
        html += "  <li>長期的な使用を前提として製品を選びたい方</li>\n"
        html += "</ul>\n"

        html += "<h3>慎重に検討した方が良い方</h3>\n"
        html += "<ul>\n"
        html += "  <li>予算を最優先して最安値の製品を探している方</li>\n"
        html += "  <li>最高スペックのみを追求する方</li>\n"
        html += "  <li>軽量性を最も重視する方</li>\n"
        html += "</ul>\n"

        return html

    def generate_user_experience(self, product: GadgetProduct) -> str:
        """実際の使用感・期待できる効果セクションを生成"""
        html = "<h2>実際の使用感と期待できる効果</h2>\n"

        if "マウス" in product.name:
            html += "<p>このマウスを日常的に使用することで、作業効率の向上が期待できます。"
            html += "高精度なセンサーにより、細かな作業でもストレスなく操作でき、カーソルの動きも滑らかで快適です。"
            html += "エルゴノミクスデザインを採用しているため、長時間使用しても手首や腕への負担が少なく、疲労を軽減できます。</p>\n"

            html += "<p>複数のカスタマイズ可能なボタンを活用すれば、よく使う機能にすぐにアクセスでき、作業のスピードアップが図れます。"
            html += "特に、コピー＆ペーストやウィンドウ切り替えなど、頻繁に使う操作を割り当てることで、マウスだけで多くの作業が完結します。</p>\n"

        elif "キーボード" in product.name:
            html += "<p>このキーボードを使用することで、タイピングの快適性が大幅に向上します。"
            html += "キースイッチの感触が良好で、入力時のフィードバックが明確なため、タイプミスが減少し、入力精度が向上します。"
            html += "長時間のタイピング作業でも指の疲労が少なく、効率的な文字入力が可能です。</p>\n"

            html += "<p>コンパクトな配列により、デスクスペースを有効活用でき、マウスとの距離も近くなるため、作業効率が向上します。"
            html += "静音性が高いため、周囲を気にせず集中して作業に取り組めるのも大きなメリットです。</p>\n"

        elif "SSD" in product.name:
            html += "<p>このSSDを導入することで、PCの動作速度が劇的に改善されます。"
            html += "システムの起動時間が大幅に短縮され、アプリケーションの立ち上がりも高速化します。"
            html += "従来のHDDやSATA SSDと比較して、体感できるレベルでの速度向上が期待できます。</p>\n"

            html += "<p>大容量ファイルの読み書きも高速で、動画編集やゲームのロード時間が短縮されます。"
            html += "作業中のストレスが大幅に軽減され、生産性の向上につながります。"
            html += "また、発熱も少なく、安定した動作が長期間維持されます。</p>\n"

        elif "メモリ" in product.name:
            html += "<p>このメモリを増設することで、PC全体のパフォーマンスが向上します。"
            html += "複数のアプリケーションを同時に起動してもメモリ不足によるパフォーマンス低下が起こりにくくなり、快適なマルチタスク作業が可能になります。"
            html += "特に、ブラウザで多数のタブを開きながら他の作業を行う場合に、その効果を実感できます。</p>\n"

            html += "<p>動画編集や3DCG制作、プログラミングなど、メモリを多く消費する作業も快適に行えます。"
            html += "仮想環境を使用する開発者の方にとっても、複数の仮想マシンを同時に起動できるため、作業効率が大幅に向上します。</p>\n"

        else:
            html += "<p>この製品を導入することで、日常的な作業環境が改善され、より快適な使用体験が得られます。"
            html += "品質の高い製品ですので、長期間安心して使用することができます。</p>\n"

            html += "<p>機能性とデザイン性を両立しており、デスク周りの環境を整えるのにも役立ちます。"
            html += "日々の作業効率向上に貢献する、実用的な製品です。</p>\n"

        return html

    def generate_comparison_points(self, product: GadgetProduct) -> str:
        """他製品との比較ポイントセクションを生成"""
        html = "<h2>他製品との比較ポイント</h2>\n"

        if "マウス" in product.name:
            html += "<p>同価格帯のワイヤレスマウスと比較した場合、この製品はセンサー精度とバッテリー寿命のバランスが優れています。"
            html += "一般的なワイヤレスマウスのバッテリー寿命が1〜2週間程度であるのに対し、この製品は数週間から数ヶ月の使用が可能です。</p>\n"

            html += "<p>また、エルゴノミクスデザインの完成度も高く、長時間使用時の疲労軽減効果は、通常の左右対称デザインのマウスと比較して明確な差があります。"
            html += "カスタマイズ機能の充実度も高く、専用ソフトウェアを使用することで、細かい設定が可能です。</p>\n"

        elif "キーボード" in product.name:
            html += "<p>一般的なメンブレンキーボードと比較すると、キースイッチの品質と耐久性が大きく異なります。"
            html += "タイピング時の感触が格段に良く、長期間使用してもキーの反応が変わらないため、安定した入力環境を維持できます。</p>\n"

            html += "<p>他のメカニカルキーボードと比較した場合、この製品はコンパクトさと機能性のバランスが優れています。"
            html += "フルサイズキーボードと比べて省スペースでありながら、必要な機能は全て備えており、携帯性にも優れています。</p>\n"

        elif "SSD" in product.name:
            html += "<p>SATA接続のSSDと比較すると、読み書き速度が3〜5倍程度高速です。"
            html += "特に、大容量ファイルの転送や、複数のファイルを同時に扱う作業において、その差は顕著に現れます。</p>\n"

            html += "<p>同じNVMe接続のSSDの中でも、この製品はPCIe 4.0に対応しており、PCIe 3.0製品と比較して理論値で2倍の速度を実現しています。"
            html += "価格面でも、性能を考慮すればコストパフォーマンスに優れた選択肢となっています。</p>\n"

        elif "メモリ" in product.name:
            html += "<p>DDR4メモリと比較すると、DDR5は動作周波数が高く、より高速なデータ転送が可能です。"
            html += "マルチタスク作業やメモリを大量に消費するアプリケーションの使用時に、その差が体感できます。</p>\n"

            html += "<p>同容量の他社製品と比較した場合、この製品は品質と価格のバランスが良好です。"
            html += "メーカーの信頼性も高く、長期保証が付帯しているため、安心して使用できます。</p>\n"

        else:
            html += "<p>同カテゴリの製品と比較した場合、この製品は機能性と価格のバランスが優れています。"
            html += "品質面でも信頼できるメーカーの製品であり、長期使用を前提として選ぶ価値があります。</p>\n"

        return html

    def generate_conclusion(self, product: GadgetProduct) -> str:
        """まとめセクションを生成（総合評価なし）"""
        html = "<h2>まとめ</h2>\n"

        conclusions = [
            f"「{product.name}」は、{product.category}として非常に完成度の高い製品です。",
            f"総合的に評価すると、「{product.name}」は価格に見合った価値を提供する優秀な{product.category}です。",
            f"「{product.name}」は、{product.category}の中でも特に注目すべき製品の一つです。",
        ]

        html += f"<p>{random.choice(conclusions)}</p>\n"

        html += f"<p>価格は決して安くありませんが、品質やサポート体制の充実を考慮すれば、長期的に見て十分な投資価値があります。"
        html += f"特に、{product.features[0] if product.features else '基本性能'}は高く評価でき、日常的な使用において満足度の高い体験が期待できます。</p>\n"

        html += f"<p>{product.category}の購入を検討している方で、品質と性能を重視するなら、「{product.name}」は有力な選択肢となるでしょう。"
        html += "製品の詳細については、公式ページや販売ページで最新の情報をご確認ください。</p>\n"

        html += f"<p>この製品は、日常的な使用からプロフェッショナルな用途まで、幅広いシーンで活躍します。"
        html += f"初めて{product.category}を選ぶ方にも、買い替えを検討している方にも、自信を持っておすすめできる製品です。</p>\n"

        return html

    def generate_product_link(self, product: GadgetProduct) -> str:
        """商品購入リンクセクションを生成"""
        html = "<h2>商品情報</h2>\n"

        html += f"<p>この記事で紹介した商品の詳細情報や最新の価格は、以下のリンクからご確認いただけます。</p>\n"

        html += "<div style='background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 20px; margin: 20px 0;'>\n"
        html += f"<h3 style='margin-top: 0;'>{product.name}</h3>\n"

        if product.price:
            html += f"<p><strong>価格:</strong> {product.price}</p>\n"

        html += f"<p><strong>ASIN:</strong> {product.asin}</p>\n"

        html += f"<p style='margin-bottom: 15px;'><a href='{product.url}' target='_blank' rel='noopener noreferrer' "
        html += "style='display: inline-block; background-color: #ff9900; color: white; padding: 12px 24px; "
        html += "text-decoration: none; border-radius: 5px; font-weight: bold;'>"
        html += "Amazonで詳細を見る</a></p>\n"

        html += "<p style='font-size: 0.9em; color: #6c757d; margin-bottom: 0;'>"
        html += "※商品の価格や在庫状況は変動する可能性があります。最新情報はリンク先でご確認ください。</p>\n"
        html += "</div>\n"

        return html

    def generate_related_articles_section(self) -> str:
        """関連記事セクションを生成（2カラムレイアウト）"""
        html = "<h2>関連記事</h2>\n"

        html += "<div style='display: flex; gap: 20px; margin-top: 40px;'>\n"

        # 左カラム: 画像 (50%)
        html += "  <div style='flex: 1;'>\n"
        html += "    <img src='PLACEHOLDER_IMAGE_URL' alt='関連記事' style='width: 100%; height: auto;'>\n"
        html += "  </div>\n"

        # 右カラム: 段落 + ボタン (50%)
        html += "  <div style='flex: 1; display: flex; flex-direction: column; justify-content: space-between;'>\n"
        html += "    <p>PLACEHOLDER_TEXT</p>\n"
        html += "    <div style='text-align: right;'>\n"
        html += "      <a href='PLACEHOLDER_LINK' style='display: inline-block; padding: 10px 20px; background-color: #0073aa; color: white; text-decoration: none; border-radius: 5px;'>詳しく見る</a>\n"
        html += "    </div>\n"
        html += "  </div>\n"

        html += "</div>\n"

        return html

    def generate_meta_description(self, product: GadgetProduct) -> str:
        """SEO用メタディスクリプションを生成（160文字以内）"""
        import datetime
        current_year = datetime.datetime.now().year

        # 特徴を簡潔に
        feature_text = ""
        if product.features and len(product.features) > 0:
            feature_text = f"{product.features[0]}など、"

        descriptions = [
            f"{product.name}の詳細レビュー。{feature_text}実際の使用感やメリット・デメリットを徹底解説。{product.category}選びの参考に。",
            f"{current_year}年版{product.name}のレビュー記事。{feature_text}口コミ・評判、性能を詳しく紹介。{product.category}のおすすめモデル。",
            f"{product.name}を実機レビュー。{feature_text}購入前に知っておきたい情報を網羅。{product.category}の比較検討に最適。",
        ]

        description = random.choice(descriptions)

        # 160文字制限
        if len(description) > 160:
            description = description[:157] + "..."

        return description

    def generate_post_content(self, product: GadgetProduct) -> str:
        """完全な記事コンテンツを生成（2000-4000文字）"""
        content = ""

        # 導入部分（感情的で読者に呼びかける形式）
        content += f"<p>{self.generate_introduction(product)}</p>\n\n"

        # スペック表（項目を増やして充実化）
        content += self.generate_spec_table(product)
        content += "\n"

        # 特徴（見出しの番号なし）
        content += self.generate_features_section(product)
        content += "\n"

        # 使用シーンと活用方法
        content += self.generate_usage_scenarios(product)
        content += "\n"

        # 実際の使用感と期待できる効果（新規追加）
        content += self.generate_user_experience(product)
        content += "\n"

        # メリット・デメリット
        content += self.generate_pros_cons(product)
        content += "\n"

        # 他製品との比較ポイント（新規追加）
        content += self.generate_comparison_points(product)
        content += "\n"

        # どのような方におすすめか
        content += self.generate_who_should_buy(product)
        content += "\n"

        # まとめ（総合評価なし）
        content += self.generate_conclusion(product)
        content += "\n"

        # 商品購入リンク（PA-APIリクエスト上限増加のため）
        content += self.generate_product_link(product)
        content += "\n"

        # 関連記事セクション（2カラムレイアウト）
        content += self.generate_related_articles_section()

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
