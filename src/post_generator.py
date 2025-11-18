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
        """SEO最適化された魅力的な記事タイトルを生成"""
        import datetime
        current_year = datetime.datetime.now().year

        # 商品名は既に短縮されているのでそのまま使用
        product_name = product.name

        # ブランド名を抽出（商品名の最初の単語）
        brand = product.name.split()[0] if product.name else ""

        # 魅力的で興味をそそるタイトルテンプレート
        # 「！」「？」などの記号を効果的に使用
        templates = [
            # 疑問形（興味喚起）
            f"【{current_year}年版】{product_name}は買うべき？実力を徹底レビュー！",
            f"{product_name}は本当におすすめ？口コミ・評判を正直にレビュー",
            f"{product_name}の評価は？{product.category}として実際どうなのか検証！",
            f"【必見】{product_name}って実際どう？使ってわかった本音レビュー",
            f"{product_name}を選ぶべき理由とは？{current_year}年最新レビュー！",

            # 驚き・発見（感嘆符）
            f"【驚愕】{product_name}がすごい！{product.category}の新定番を徹底解説",
            f"これは買い！{product_name}レビュー｜{current_year}年版{product.category}の決定版",
            f"【神コスパ！】{product_name}を本音レビュー｜メリット・デメリット完全解説",
            f"想像以上だった！{product_name}の実力を徹底検証【{current_year}】",
            f"買って正解！{product_name}レビュー｜{product.category}選びの新常識",

            # 比較・対決
            f"{product_name} vs 他製品｜どっちを選ぶべき？徹底比較レビュー！",
            f"【比較検証】{product_name}の実力は？{product.category}おすすめNo.1の理由",
            f"{brand}の本気！{product_name}レビュー｜他社製品と何が違う？",

            # 体験・実機レビュー
            f"【実機レビュー】{product_name}を使って分かった5つのこと",
            f"{product_name}を1ヶ月使った本音｜良い点・悪い点を徹底レビュー！",
            f"【ガチレビュー】{product_name}の実力を検証！買って後悔しない？",
            f"使って納得！{product_name}レビュー｜{current_year}年版{product.category}の正解",

            # 問題解決型
            f"{product.category}選びで迷ったら！{product_name}が解決策になる理由",
            f"【完全ガイド】{product_name}レビュー｜失敗しない{product.category}の選び方",
            f"{product_name}で快適に！{product.category}の悩みを解決する方法",

            # 限定・希少性
            f"【{current_year}年最新】{product_name}レビュー｜今すぐチェックすべき理由！",
            f"見逃し厳禁！{product_name}の実力｜{product.category}の新スタンダード",
            f"【話題沸騰】{product_name}は何がすごい？徹底レビューで解説！",

            # 数字・具体性
            f"{product_name}レビュー｜使って分かった7つのメリット【{current_year}】",
            f"【3分で分かる】{product_name}の評価｜買うべき5つの理由",
            f"{product_name}の実力を5段階評価！{product.category}として徹底検証",

            # 断定・強調
            f"これが答え！{product_name}レビュー｜{product.category}の最適解を発見",
            f"間違いなし！{product_name}が選ばれる理由｜{current_year}年版レビュー",
            f"【結論】{product_name}は買い！実際に使った本音レビュー",
            f"迷わず買える！{product_name}レビュー｜{product.category}の新常識",
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
        # 本文では詳細な商品名を使用
        display_name = product.full_name if product.full_name else product.name

        intros = [
            f"{product.category}選びで悩んでいませんか？今回ご紹介する{display_name}は、そんな方にぜひチェックしていただきたい注目の製品です！",
            f"{display_name}をご存知でしょうか？{product.category}の中でも特に高い評価を得ている、今話題の製品なんです。",
            f"{product.category}の新しい選択肢として、{display_name}が注目を集めています。一体どんな特徴があるのでしょうか？",
        ]

        intro = random.choice(intros)

        if product.description:
            intro += f"\n\n{product.description}という特徴を持つこの製品、実際のところはどうなのでしょうか？"

        intro += f"\n\n本記事では、{display_name}のスペックや機能、メリット・デメリット、どんな方におすすめなのかなど、購入前に知っておきたい情報を徹底解説していきます！"

        price_range = self.get_price_range(product.price) if product.price else ""
        if price_range:
            intro += f"価格帯は{price_range}となっており、コストパフォーマンスも気になるところですよね。"

        return intro

    def _shorten_feature_heading(self, feature: str) -> str:
        """特徴の見出しを5-25文字に短縮"""
        # 数字や記号、単位を含む重要な情報を優先的に抽出
        import re

        # 既に短い場合はそのまま返す
        if len(feature) <= 25:
            return feature

        # パターンマッチングでキーワードを抽出
        # 例: "8000 DPI", "32GB", "500MB/s", "Bluetooth 5.0" などを優先
        patterns = [
            r'\d+[\s]*(?:DPI|dpi)',  # DPI情報
            r'\d+[\s]*(?:GB|TB|MB)',  # 容量情報
            r'\d+[\s]*(?:MB/s|GB/s)',  # 速度情報
            r'\d+[\s]*(?:MHz|GHz)',  # 周波数情報
            r'Bluetooth[\s]*\d+\.\d+',  # Bluetooth バージョン
            r'\d+[\s]*(?:時間|日|ヶ月|年)',  # 期間情報
        ]

        for pattern in patterns:
            match = re.search(pattern, feature)
            if match:
                keyword = match.group(0)
                # キーワードの前後から文脈を追加（最大25文字）
                start_pos = max(0, match.start() - 10)
                end_pos = min(len(feature), match.end() + 10)
                short = feature[start_pos:end_pos].strip()
                if len(short) > 25:
                    short = short[:25]
                return short

        # パターンマッチしない場合は、先頭25文字を使用
        return feature[:25]

    def generate_spec_table(self, product: GadgetProduct) -> str:
        """スペック表を生成（PA-APIから取得した実際の商品情報を使用）"""
        # 本文では詳細な商品名を使用
        display_name = product.full_name if product.full_name else product.name

        html = "<h2>製品スペック</h2>\n"
        html += "<table>\n"
        html += "<thead>\n<tr>\n<th>項目</th>\n<th>詳細</th>\n</tr>\n</thead>\n"
        html += "<tbody>\n"

        # 製品名
        html += f"<tr>\n<td>製品名</td>\n<td>{display_name}</td>\n</tr>\n"

        # 価格（価格帯は削除）
        if product.price:
            html += f"<tr>\n<td>価格</td>\n<td>{product.price}</td>\n</tr>\n"

        # PA-APIから取得した特徴をスペック表に追加（タイトル部分のみ）
        if product.features and len(product.features) > 0:
            for i, feature in enumerate(product.features, 1):
                # 区切り文字（:, ;, ｜）で分割してタイトル部分のみを取得
                feature_title = feature
                for delimiter in ['：', ':', '；', ';', '｜']:
                    if delimiter in feature:
                        feature_title = feature.split(delimiter)[0] + delimiter
                        break
                html += f"<tr>\n<td>特徴 {i}</td>\n<td>{feature_title}</td>\n</tr>\n"

        # 商品説明
        if product.description:
            html += f"<tr>\n<td>製品説明</td>\n<td>{product.description}</td>\n</tr>\n"

        html += "</tbody>\n</table>\n"
        html += "<p><small>※スペック情報はAmazon PA-APIから取得した商品情報に基づいています。最新の正確な情報は製品ページでご確認ください。</small></p>\n"

        return html

    def generate_features_section(self, product: GadgetProduct) -> str:
        """特徴セクションを生成（タイトルと説明を分割して表示）"""
        if not product.features:
            return ""

        html = "<h2>主な特徴と機能</h2>\n"

        for feature in product.features:
            # 区切り文字（:, ;, ｜）で分割
            feature_title = feature
            feature_description = ''

            for delimiter in ['：', ':', '；', ';', '｜']:
                if delimiter in feature:
                    parts = feature.split(delimiter, 1)
                    feature_title = parts[0] + delimiter
                    feature_description = parts[1].strip() if len(parts) > 1 else ''
                    break

            # 見出し（タイトル部分のみ）
            html += f"<h3>{feature_title}</h3>\n"

            # 説明文（区切り文字の後の部分）
            if feature_description:
                html += f"<p>{feature_description}</p>\n"

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
        # 本文では詳細な商品名を使用
        display_name = product.full_name if product.full_name else product.name

        html = "<h2>まとめ</h2>\n"

        conclusions = [
            f"{display_name}は、{product.category}として非常に完成度の高い製品です。",
            f"総合的に評価すると、{display_name}は価格に見合った価値を提供する優秀な{product.category}です。",
            f"{display_name}は、{product.category}の中でも特に注目すべき製品の一つです。",
        ]

        html += f"<p>{random.choice(conclusions)}</p>\n"

        html += f"<p>価格は決して安くありませんが、品質やサポート体制の充実を考慮すれば、長期的に見て十分な投資価値があります。"
        html += f"特に、{product.features[0] if product.features else '基本性能'}は高く評価でき、日常的な使用において満足度の高い体験が期待できます。</p>\n"

        html += f"<p>{product.category}の購入を検討している方で、品質と性能を重視するなら、{display_name}は有力な選択肢となるでしょう。"
        html += "製品の詳細については、公式ページや販売ページで最新の情報をご確認ください。</p>\n"

        html += f"<p>この製品は、日常的な使用からプロフェッショナルな用途まで、幅広いシーンで活躍します。"
        html += f"初めて{product.category}を選ぶ方にも、買い替えを検討している方にも、自信を持っておすすめできる製品です。</p>\n"

        return html

    def generate_product_link(self, product: GadgetProduct) -> str:
        """商品購入リンクセクションを生成（Gutenbergブロック形式・シンプル2カラム）"""
        # PA-APIから取得した元のタイトル（原文）を使用
        display_title = product.original_title if product.original_title else (product.full_name if product.full_name else product.name)

        # カラムブロック（2列: 50% / 50%）※見出しなし
        blocks = "<!-- wp:columns -->\n"
        blocks += "<div class=\"wp-block-columns\">\n"

        # 左カラム: 商品画像 (50%)
        blocks += "<!-- wp:column {\"width\":\"50%\"} -->\n"
        blocks += "<div class=\"wp-block-column\" style=\"flex-basis:50%\">\n"
        if product.image_url:
            blocks += "<!-- wp:image -->\n"
            blocks += f"<figure class=\"wp-block-image\"><img src=\"{product.image_url}\" alt=\"{display_title}\"/></figure>\n"
            blocks += "<!-- /wp:image -->\n"
        else:
            blocks += "<!-- wp:paragraph -->\n"
            blocks += "<p>画像なし</p>\n"
            blocks += "<!-- /wp:paragraph -->\n"
        blocks += "</div>\n"
        blocks += "<!-- /wp:column -->\n\n"

        # 右カラム: 商品タイトル（原文） + ボタン (50%)
        blocks += "<!-- wp:column {\"width\":\"50%\"} -->\n"
        blocks += "<div class=\"wp-block-column\" style=\"flex-basis:50%\">\n"

        # 段落（PA-APIから取得した商品タイトル原文）
        blocks += "<!-- wp:paragraph -->\n"
        blocks += f"<p>{display_title}</p>\n"
        blocks += "<!-- /wp:paragraph -->\n\n"

        # Amazonリンクボタン（右寄せ、紺色背景）
        blocks += "<!-- wp:buttons {\"layout\":{\"type\":\"flex\",\"justifyContent\":\"right\"}} -->\n"
        blocks += "<div class=\"wp-block-buttons\">\n"
        blocks += "<!-- wp:button {\"backgroundColor\":\"custom\",\"style\":{\"color\":{\"background\":\"#1e50a2\"},\"border\":{\"radius\":\"5px\"}}} -->\n"
        blocks += f"<div class=\"wp-block-button\"><a class=\"wp-block-button__link wp-element-button\" href=\"{product.url}\" target=\"_blank\" rel=\"noopener noreferrer\" style=\"border-radius:5px;background-color:#1e50a2\">AMAZONで見る⇒</a></div>\n"
        blocks += "<!-- /wp:button -->\n"
        blocks += "</div>\n"
        blocks += "<!-- /wp:buttons -->\n"

        blocks += "</div>\n"
        blocks += "<!-- /wp:column -->\n"

        blocks += "</div>\n"
        blocks += "<!-- /wp:columns -->\n"

        return blocks

    def generate_variants_section(self, variants: List[GadgetProduct]) -> str:
        """複数バリエーション（仕様違い）の商品リンクセクションを生成"""
        blocks = ""

        # 説明文（見出しなし）
        blocks += "<!-- wp:paragraph -->\n"
        blocks += f"<p>この製品には{len(variants)}つの仕様バリエーションがあります。用途や予算に合わせてお選びください。</p>\n"
        blocks += "<!-- /wp:paragraph -->\n\n"

        # 各バリエーションをカラムで表示（見出しなし）
        for i, variant in enumerate(variants, 1):
            # PA-APIから取得した元のタイトル（原文）を使用
            display_title = variant.original_title if variant.original_title else (variant.full_name if variant.full_name else variant.name)

            # カラムブロック（2列: 50% / 50%）
            blocks += "<!-- wp:columns -->\n"
            blocks += "<div class=\"wp-block-columns\">\n"

            # 左カラム: 商品画像 (50%)
            blocks += "<!-- wp:column {\"width\":\"50%\"} -->\n"
            blocks += "<div class=\"wp-block-column\" style=\"flex-basis:50%\">\n"
            if variant.image_url:
                blocks += "<!-- wp:image -->\n"
                blocks += f"<figure class=\"wp-block-image\"><img src=\"{variant.image_url}\" alt=\"{display_title}\"/></figure>\n"
                blocks += "<!-- /wp:image -->\n"
            blocks += "</div>\n"
            blocks += "<!-- /wp:column -->\n\n"

            # 右カラム: 商品タイトル（原文） + ボタン (50%)
            blocks += "<!-- wp:column {\"width\":\"50%\"} -->\n"
            blocks += "<div class=\"wp-block-column\" style=\"flex-basis:50%\">\n"

            # 段落（PA-APIから取得した商品タイトル原文）
            blocks += "<!-- wp:paragraph -->\n"
            blocks += f"<p>{display_title}</p>\n"
            blocks += "<!-- /wp:paragraph -->\n\n"

            # Amazonリンクボタン（右寄せ、紺色背景）
            blocks += "<!-- wp:buttons {\"layout\":{\"type\":\"flex\",\"justifyContent\":\"right\"}} -->\n"
            blocks += "<div class=\"wp-block-buttons\">\n"
            blocks += "<!-- wp:button {\"backgroundColor\":\"custom\",\"style\":{\"color\":{\"background\":\"#1e50a2\"},\"border\":{\"radius\":\"5px\"}}} -->\n"
            blocks += f"<div class=\"wp-block-button\"><a class=\"wp-block-button__link wp-element-button\" href=\"{variant.url}\" target=\"_blank\" rel=\"noopener noreferrer\" style=\"border-radius:5px;background-color:#1e50a2\">AMAZONで見る⇒</a></div>\n"
            blocks += "<!-- /wp:button -->\n"
            blocks += "</div>\n"
            blocks += "<!-- /wp:buttons -->\n"

            blocks += "</div>\n"
            blocks += "<!-- /wp:column -->\n"

            blocks += "</div>\n"
            blocks += "<!-- /wp:columns -->\n\n"

        return blocks

    def generate_related_articles_section(self, previous_post: dict = None) -> str:
        """関連記事セクションを生成（Gutenbergブロック形式）※見出しなし

        Args:
            previous_post: 前回の投稿情報（title, link, featured_image_url）
        """
        # カラムブロック（2列: 50% / 50%）※見出しなし
        blocks = "<!-- wp:columns -->\n"
        blocks += "<div class=\"wp-block-columns\">\n"

        # 左カラム: 画像（アイキャッチ画像またはプレースホルダー）
        blocks += "<!-- wp:column {\"width\":\"50%\"} -->\n"
        blocks += "<div class=\"wp-block-column\" style=\"flex-basis:50%\">\n"
        blocks += "<!-- wp:image -->\n"

        if previous_post and previous_post.get('featured_image_url'):
            image_url = previous_post['featured_image_url']
            alt_text = previous_post.get('title', '関連記事')
            blocks += f"<figure class=\"wp-block-image\"><img src=\"{image_url}\" alt=\"{alt_text}\"/></figure>\n"
        else:
            blocks += "<figure class=\"wp-block-image\"><img src=\"PLACEHOLDER_IMAGE_URL\" alt=\"関連記事\"/></figure>\n"

        blocks += "<!-- /wp:image -->\n"
        blocks += "</div>\n"
        blocks += "<!-- /wp:column -->\n\n"

        # 右カラム: 段落（タイトル） + ボタン
        blocks += "<!-- wp:column {\"width\":\"50%\",\"verticalAlignment\":\"space-between\"} -->\n"
        blocks += "<div class=\"wp-block-column is-vertically-aligned-space-between\" style=\"flex-basis:50%\">\n"

        # 段落ブロック（前記事のタイトル）
        blocks += "<!-- wp:paragraph -->\n"
        if previous_post and previous_post.get('title'):
            blocks += f"<p>{previous_post['title']}</p>\n"
        else:
            blocks += "<p>PLACEHOLDER_TEXT</p>\n"
        blocks += "<!-- /wp:paragraph -->\n\n"

        # スペーサー（ボタンを下に配置するため）
        blocks += "<!-- wp:spacer {\"height\":\"20px\"} -->\n"
        blocks += "<div style=\"height:20px\" aria-hidden=\"true\" class=\"wp-block-spacer\"></div>\n"
        blocks += "<!-- /wp:spacer -->\n\n"

        # ボタンブロック（右寄せ、黄色背景）
        blocks += "<!-- wp:buttons {\"layout\":{\"type\":\"flex\",\"justifyContent\":\"right\"}} -->\n"
        blocks += "<div class=\"wp-block-buttons\">\n"

        if previous_post and previous_post.get('link'):
            link = previous_post['link']
            blocks += "<!-- wp:button {\"backgroundColor\":\"custom\",\"style\":{\"color\":{\"background\":\"#f39800\"}}} -->\n"
            blocks += f"<div class=\"wp-block-button\"><a class=\"wp-block-button__link wp-element-button\" href=\"{link}\" style=\"background-color:#f39800\">見に行く⇒</a></div>\n"
            blocks += "<!-- /wp:button -->\n"
        else:
            blocks += "<!-- wp:button {\"backgroundColor\":\"custom\",\"style\":{\"color\":{\"background\":\"#f39800\"}}} -->\n"
            blocks += "<div class=\"wp-block-button\"><a class=\"wp-block-button__link wp-element-button\" href=\"PLACEHOLDER_LINK\" style=\"background-color:#f39800\">見に行く⇒</a></div>\n"
            blocks += "<!-- /wp:button -->\n"

        blocks += "</div>\n"
        blocks += "<!-- /wp:buttons -->\n"

        blocks += "</div>\n"
        blocks += "<!-- /wp:column -->\n"

        blocks += "</div>\n"
        blocks += "<!-- /wp:columns -->\n"

        return blocks

    def generate_meta_description(self, product: GadgetProduct) -> str:
        """SEO用メタディスクリプションを生成（導入文章から100-150文字を抽出）"""
        # 導入文章を生成
        intro = self.generate_introduction(product)

        # HTMLタグを除去してプレーンテキストに変換
        import re
        plain_text = re.sub(r'<[^>]+>', '', intro)
        plain_text = re.sub(r'\n+', ' ', plain_text)  # 改行をスペースに変換
        plain_text = plain_text.strip()

        # 100-150文字の範囲でキリの良いところ（句点「。」）まで抽出
        if len(plain_text) <= 150:
            return plain_text

        # 100文字以降で最初の句点を探す
        min_length = 100
        max_length = 150

        # 100-150文字の範囲内で句点を探す
        search_text = plain_text[min_length:max_length]
        period_pos = search_text.find('。')

        if period_pos != -1:
            # 句点が見つかった場合、その直後まで抽出
            end_pos = min_length + period_pos + 1
            return plain_text[:end_pos]

        # 句点が見つからない場合は、100文字以降で最初の句点を探す
        search_text_after = plain_text[min_length:]
        period_pos_after = search_text_after.find('。')

        if period_pos_after != -1:
            end_pos = min_length + period_pos_after + 1
            # ただし200文字を超える場合は150文字で切る
            if end_pos > 200:
                return plain_text[:150]
            return plain_text[:end_pos]

        # 句点が全く見つからない場合は150文字で切る
        return plain_text[:150]

    def generate_post_content(self, product: GadgetProduct, variants: List[GadgetProduct] = None, previous_post: dict = None) -> str:
        """完全な記事コンテンツを生成（2000-4000文字）

        Args:
            product: メイン商品
            variants: 同一製品のバリエーション（仕様違い）リスト
            previous_post: 前回の投稿情報（title, link, featured_image_url）
        """
        content = ""

        # バリエーションが指定されていない場合はメイン商品のみ
        if variants is None:
            variants = [product]

        # 導入部分（感情的で読者に呼びかける形式）
        content += f"<p>{self.generate_introduction(product)}</p>\n\n"

        # バリエーション表示（複数ある場合）
        if len(variants) > 1:
            content += self.generate_variants_section(variants)
            content += "\n"
        else:
            # 単一商品の場合は従来通り
            content += self.generate_product_link(product)
            content += "\n"

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

        # 商品購入リンク（2回目：まとめの前）
        content += self.generate_product_link(product)
        content += "\n"

        # まとめ（総合評価なし）
        content += self.generate_conclusion(product)
        content += "\n"

        # 関連記事セクション（2カラムレイアウト）
        content += self.generate_related_articles_section(previous_post)

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

    def generate_seo_title(self, product: GadgetProduct, post_title: str = None) -> str:
        """SEOタイトルを生成（投稿タイトルをそのまま使用）

        Args:
            product: 商品情報
            post_title: 投稿のタイトル（指定された場合はそのまま使用）
        """
        if post_title:
            return post_title

        # post_titleが指定されていない場合は通常のタイトル生成
        return self.generate_title(product)

    def generate_seo_keywords(self, product: GadgetProduct) -> str:
        """SEOキーワードを生成（カンマ区切り）"""
        keywords = [product.name, product.category, "レビュー"]

        # ブランド名を追加
        brand = product.name.split()[0] if product.name else ""
        if brand:
            keywords.append(brand)

        # 製品タイプ別キーワード
        if "マウス" in product.name:
            keywords.extend(["ワイヤレスマウス", "PC周辺機器", "マウスレビュー"])
        elif "キーボード" in product.name:
            keywords.extend(["キーボード", "PC周辺機器", "タイピング"])
        elif "SSD" in product.name:
            keywords.extend(["SSD", "ストレージ", "PCパーツ", "高速化"])
        elif "メモリ" in product.name:
            keywords.extend(["メモリ", "RAM", "DDR5", "PCパーツ"])
        elif "モニター" in product.name or "ディスプレイ" in product.name:
            keywords.extend(["モニター", "ディスプレイ", "PC周辺機器"])
        elif "ヘッドセット" in product.name or "イヤホン" in product.name:
            keywords.extend(["オーディオ", "音質", "ゲーミング"])

        # 一般的なキーワード追加
        keywords.extend(["おすすめ", "比較", "Amazon"])

        # 重複を削除してカンマ区切りで返す
        unique_keywords = list(dict.fromkeys(keywords))  # 順序を保持して重複削除
        return ", ".join(unique_keywords[:10])  # 最大10個
