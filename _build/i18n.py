#!/usr/bin/env python3
"""Build ja/index.html and ar/index.html from the English index.html.

Run from the repo root after editing index.html:  python3 _build/i18n.py
Every English string listed below must exist exactly once (or the stated
number of times) in index.html, otherwise the build stops so that no page
silently ships half-translated. Folders starting with "_" are not published
by GitHub Pages.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = (ROOT / "index.html").read_text(encoding="utf-8")

# (english, translation[, expected count]); count defaults to 1, 0 means "any (>=1)"
COMMON_NAV = ["About", "Expertise", "Teaching", "Publications", "Milestones", "Links"]

JA = {
    "lang": "ja",
    "dir": "ltr",
    "title": "カンザダ あみる | Amil Khanzada",
    "fonts": "family=Noto+Sans+JP:wght@400;500;700&",
    "font_css": ':root { --display: "Space Grotesk", "Noto Sans JP", sans-serif; --text: "Instrument Sans", "Noto Sans JP", system-ui, sans-serif; }\n'
                'html[lang="ja"] body { letter-spacing: .02em; line-height: 1.85; }\n'
                'html[lang="ja"] h1 { letter-spacing: -.02em; font-weight: 700; }\n'
                'html[lang="ja"] .feature-title, html[lang="ja"] h2, html[lang="ja"] h3 { letter-spacing: 0; }\n'
                'html[lang="ja"] .feature-title { word-break: keep-all; }\n',
    "nav": ["プロフィール", "専門分野", "教育", "業績", "あゆみ", "リンク"],
    "pairs": [
        ('<meta name="description" content="Amil Khanzada is a professor at the University of Fukui and CEO of Virufy. He works on medical AI, tourism and data analytics, behavioral nudges and information security, bridging Japan, the US and the Middle East.">',
         '<meta name="description" content="カンザダ あみる（Amil Khanzada）。福井大学 特命助教、Virufy 創業者・CEO。医療AI、観光・データ分析、行動ナッジ、情報セキュリティに取り組み、日本・米国・中東をつないでいます。">'),
        ('<meta property="og:title" content="Amil Khanzada">', '<meta property="og:title" content="カンザダ あみる | Amil Khanzada">'),
        ('<meta property="og:description" content="Professor and CEO building AI that works in the real world: medical AI, tourism and data analytics, behavioral nudges and information security.">',
         '<meta property="og:description" content="福井大学 特命助教、Virufy 創業者・CEO。医療AI、観光・データ分析、行動ナッジ、情報セキュリティ。">'),
        ('<a class="brand" href="#top">Amil Khanzada</a>', '<a class="brand" href="#top">カンザダ あみる</a>'),
        ('<span class="menu-label">Menu</span>', '<span class="menu-label">メニュー</span>'),
        ('<h2 id="about-title">About</h2>', '<h2 id="about-title">プロフィール</h2>'),
        ('<h2 id="expertise-title">Expertise</h2>', '<h2 id="expertise-title">専門分野</h2>'),
        ('<h2 id="teaching-title">Teaching</h2>', '<h2 id="teaching-title">教育</h2>'),
        ('<h1 id="name">Amil<br>Khanzada</h1>', '<h1 id="name">カンザダ<br>あみる</h1>'),
        ('<p class="role">Professor, <a href="https://www.u-fukui.ac.jp/eng/">University of Fukui</a><br>Founder &amp; CEO, <a href="https://virufy.org">Virufy</a></p>',
         '<p class="role"><a href="https://www.u-fukui.ac.jp/">福井大学</a> 特命助教<br><a href="https://virufy.org">Virufy</a> 創業者・CEO</p>'),
        ('<p class="summary">I build AI that works in the real world: medical AI, tourism and data analytics, behavioral nudges and information security. I bring people together across Japan, the US and the Middle East.</p>',
         '<p class="summary">医療AI、観光・データ分析、行動ナッジ、情報セキュリティの分野で、社会の現場で役立つAIをつくっています。日本、米国、中東の人と組織をつないでいます。</p>'),
        ('<h3 class="feature-title">Between Japan<br>and Silicon Valley.</h3>', '<h3 class="feature-title">日本と<br>シリコンバレーを<wbr>つなぐ。</h3>'),
        ('<p>I’m a Specially Appointed Assistant Professor at the <a href="https://pure.flib.u-fukui.ac.jp/en/persons/amil-khanzada/">University of Fukui</a>’s Regional Revitalization Headquarters. I teach entrepreneurship and AI and work with local governments across Hokuriku.</p>',
         '<p><a href="https://pure.flib.u-fukui.ac.jp/ja/persons/amil-khanzada/">福井大学</a> 地域創生推進本部 特命助教。アントレプレナーシップとAIを教え、北陸の自治体と連携して活動しています。</p>'),
        ('<p>I’ve been Founder and CEO of <a href="https://virufy.org">virufy.org</a> since 2020.</p>',
         '<p>2020年から <a href="https://virufy.org">virufy.org</a> の創業者・CEOを務めています。</p>'),
        ('<p>My 15+ years in tech and AI include leading engineering teams in Silicon Valley and Tokyo at <a href="https://en.wikipedia.org/wiki/Greenplum">VMware Pivotal Greenplum</a> and <a href="https://www.hpe.com/">HP Enterprise</a>, and serving as Technical Lead at <a href="https://sandbox.mit.edu/">MIT Sandbox</a>.</p>',
         '<p>テック・AI分野で15年以上の経験があります。シリコンバレーと東京で <a href="https://en.wikipedia.org/wiki/Greenplum">VMware Pivotal Greenplum</a> や <a href="https://www.hpe.com/">HP Enterprise</a> のエンジニアリングチームを率い、<a href="https://sandbox.mit.edu/">MIT Sandbox</a> ではテクニカルリードを務めました。</p>'),
        ('<p>Fluent in Japanese and Urdu/Hindi. <a href="https://oywj.org/">One Young World</a> Japan Ambassador and <a href="https://www.town.eiheiji.lg.jp/900/905/p003453.html">Eiheiji Town</a> Evolution Ambassador.</p>',
         '<p>日本語、ウルドゥー語／ヒンディー語に堪能。<a href="https://oywj.org/">One Young World</a> 日本アンバサダー、<a href="https://www.town.eiheiji.lg.jp/900/905/p003453.html">永平寺町</a>エボリューション大使。</p>'),
        ('<h3 class="subheading">Education</h3>', '<h3 class="subheading">学歴</h3>'),
        ('<a class="institution" href="https://www.u-fukui.ac.jp/eng/">University of Fukui</a>\n            <span class="detail">Doctor of Engineering, behavioral nudges and human data</span>',
         '<a class="institution" href="https://www.u-fukui.ac.jp/">福井大学</a>\n            <span class="detail">博士（工学）、行動ナッジと人々のデータ提供</span>'),
        ('<a class="institution" href="https://haas.berkeley.edu/">UC Berkeley Haas School of Business</a>\n            <span class="detail">MBA and Master of Engineering (Data Science) concurrent program, first year</span>',
         '<a class="institution" href="https://haas.berkeley.edu/">カリフォルニア大学バークレー校 ハース・スクール・オブ・ビジネス</a>\n            <span class="detail">MBA・工学修士（データサイエンス）同時履修プログラム 1年次</span>'),
        ('<a class="institution" href="https://scpd.stanford.edu/">Stanford University</a>\n            <span class="detail">Graduate courses, 4.0 GPA: ',
         '<a class="institution" href="https://scpd.stanford.edu/">スタンフォード大学</a>\n            <span class="detail">大学院科目（GPA 4.0）：'),
        ('</a> with <a href="https://www.andrewng.org/">Andrew Ng</a>, ', '</a>（<a href="https://www.andrewng.org/">Andrew Ng</a>）、'),
        ('</a> with <a href="https://profiles.stanford.edu/fei-fei-li">Fei-Fei Li</a>, ', '</a>（<a href="https://profiles.stanford.edu/fei-fei-li">Fei-Fei Li</a>）、'),
        ('</a> with <a href="https://huyenchip.com/">Chip Huyen</a>, ', '</a>（<a href="https://huyenchip.com/">Chip Huyen</a>）、'),
        ('</a> with <a href="https://profiles.stanford.edu/rishi-mediratta">Rishi Mediratta</a></span>', '</a>（<a href="https://profiles.stanford.edu/rishi-mediratta">Rishi Mediratta</a>）</span>'),
        ('<a class="institution" href="https://cs.berkeley.edu/">UC Berkeley</a>\n            <span class="detail">B.A. Computer Science</span>',
         '<a class="institution" href="https://cs.berkeley.edu/">カリフォルニア大学バークレー校</a>\n            <span class="detail">コンピュータサイエンス学士（B.A.）</span>'),
        ('alt="Amil Khanzada at the University of Fukui degree ceremony"', 'alt="福井大学 学位記授与式でのカンザダ あみる"'),
        ('<figcaption>Degree conferment, University of Fukui.</figcaption>', '<figcaption>福井大学 学位記授与式。</figcaption>'),
        ('alt="Amil Khanzada with Sabae Mayor Katsuhisa Sasaki and visiting researchers"', 'alt="鯖江市 佐々木勝久市長、来日研究者とともに"'),
        ('<figcaption>With Sabae Mayor Katsuhisa Sasaki and <a href="https://ssp.jst.go.jp/en/">JST Sakura Science</a> researchers.</figcaption>',
         '<figcaption>鯖江市 佐々木勝久市長、<a href="https://ssp.jst.go.jp/">JSTさくらサイエンスプログラム</a>の研究者とともに。</figcaption>'),
        ('<h3>Medical AI</h3>\n          <div><p>Researching whether cough sounds recorded on a phone can help screen for respiratory conditions.</p></div>',
         '<h3>医療AI</h3>\n          <div><p>スマートフォンで録音した咳の音が、呼吸器疾患のスクリーニングに役立つかを研究しています。</p></div>'),
        ('<h3>Tourism and data analytics</h3>', '<h3>観光・データ分析</h3>'),
        ('<p>Forecasting visitor demand across Fukui with local governments.</p>', '<p>自治体と連携し、福井県内の観光需要を予測。</p>'),
        ('>Live dashboard</a>', '>リアルタイムダッシュボード</a>'),
        ('<h3>Behavioral nudges</h3>\n          <div><p>Getting people to share data at scale, without paying them.</p></div>',
         '<h3>行動ナッジ</h3>\n          <div><p>謝礼に頼らず、多くの人にデータ提供を促す仕組み。</p></div>'),
        ('<h3>Information security</h3>\n          <div><p>Security analytics for Fortune 500 clients and Japanese megabanks at <a href="https://www.hpe.com/">HP Enterprise</a>.</p></div>',
         '<h3>情報セキュリティ</h3>\n          <div><p><a href="https://www.hpe.com/">HP Enterprise</a> にて、フォーチュン500企業や日本のメガバンク向けのセキュリティ分析に従事。</p></div>'),
        ('<h3>Bridging Japan and the world</h3>', '<h3>日本と世界をつなぐ</h3>'),
        ('<p>Connecting universities, governments and companies across Japan, Silicon Valley, the Gulf and South Asia.</p>',
         '<p>日本、シリコンバレー、湾岸諸国、南アジアの大学・行政・企業をつないでいます。</p>'),
        ('<div class="reference"><a href="https://ssp.jst.go.jp/en/">JST Sakura Science</a>', '<div class="reference"><a href="https://ssp.jst.go.jp/">JSTさくらサイエンス</a>'),
        ('alt="Amil Khanzada showing the Fukui tourism dashboard to Governor Ishida"', 'alt="石田知事に福井の観光ダッシュボードを紹介するカンザダ あみる"'),
        ('<figcaption>Showing our tourism dashboard to Fukui Governor Ishida at the Fukui Industrial AI/AX Consortium kickoff.</figcaption>',
         '<figcaption>福井県産業AI/AXコンソーシアムのキックオフで、石田知事に観光ダッシュボードをご紹介。</figcaption>'),
        ('<h3 class="feature-title">A global health<br>AI nonprofit.</h3>', '<h3 class="feature-title">世界に広がる<br>医療AI非営利団体。</h3>'),
        ('<p>As CEO, I lead a 501(c)(3) with more than 1,300 volunteers and 60+ partner universities. Our work spans clinical studies in five countries and two patents in the US and Japan.</p>',
         '<p>CEOとして、1,300人以上のボランティアと60以上のパートナー大学が参加する米国の非営利団体（501(c)(3)）を率いています。5か国で臨床研究を行い、米国と日本で特許を取得しています。</p>'),
        ('<h3 class="feature-title">The city is the classroom.</h3>', '<h3 class="feature-title">まちが教室。</h3>'),
        ('<p class="prose">At the <a href="https://www.u-fukui.ac.jp/eng/">University of Fukui</a>, I teach entrepreneurship, AI-powered social informatics and management of technology. Students work in the field with mayors and tourism boards. In 2026, I hosted young researchers from four countries through the <a href="https://ssp.jst.go.jp/en/">JST Sakura Science Program</a>.</p>',
         '<p class="prose"><a href="https://www.u-fukui.ac.jp/">福井大学</a>で、アントレプレナーシップ、AIを活用した社会情報学、技術経営（MOT）を教えています。学生は首長や観光関係者とともに現場で学びます。2026年には<a href="https://ssp.jst.go.jp/">JSTさくらサイエンスプログラム</a>で4か国の若手研究者を受け入れました。</p>'),
        ('aria-label="Teaching topics"', 'aria-label="教育テーマ"'),
        ('<li>Nudges and data</li>', '<li>ナッジとデータ</li>'),
        ('<li>Medical AI</li>', '<li>医療AI</li>'),
        ('<li>AI for regions</li>', '<li>地域のためのAI</li>'),
        ('<li>Global teams</li>', '<li>グローバルチーム</li>'),
        ('alt="Amil Khanzada lecturing at the University of Fukui"', 'alt="福井大学で講義するカンザダ あみる"'),
        ('<figcaption>Workshop, University of Fukui.</figcaption>', '<figcaption>福井大学でのワークショップ。</figcaption>'),
        ('<h2 id="publications-title">Selected<br>publications</h2>', '<h2 id="publications-title">主な業績</h2>'),
        ('<p class="publication-intro">Full list on <a href="https://scholar.google.com/citations?user=zdgfTfMAAAAJ">Google Scholar</a>, <a href="https://pure.flib.u-fukui.ac.jp/en/persons/amil-khanzada/">University of Fukui</a> and <a href="https://orcid.org/0000-0002-7065-5390">ORCID</a>.</p>',
         '<p class="publication-intro">全リストは <a href="https://scholar.google.com/citations?user=zdgfTfMAAAAJ">Google Scholar</a>、<a href="https://pure.flib.u-fukui.ac.jp/ja/persons/amil-khanzada/">福井大学 研究者情報</a>、<a href="https://orcid.org/0000-0002-7065-5390">ORCID</a> をご覧ください。</p>'),
        ('<span class="venue">US Patent 12,444,502 and Japanese Patent 7850135</span>', '<span class="venue">米国特許 12,444,502・日本特許 第7850135号</span>'),
        ('<h2 id="news-title">Milestones</h2>', '<h2 id="news-title">あゆみ</h2>'),
        ('<span>Hosted the <a href="https://ssp.jst.go.jp/en/">JST Sakura Science Program</a> in Fukui</span>', '<span><a href="https://ssp.jst.go.jp/">JSTさくらサイエンスプログラム</a>を福井で実施</span>'),
        ('<span><a href="https://doi.org/10.1016/j.measurement.2026.122500">DHDE paper</a> published in Measurement</span>', '<span><a href="https://doi.org/10.1016/j.measurement.2026.122500">DHDE論文</a>が Measurement 誌に掲載</span>'),
        ('<span>Japanese Patent 7850135 granted</span>', '<span>日本特許 第7850135号 取得</span>'),
        ('<span>Joined the <a href="https://pure.flib.u-fukui.ac.jp/en/persons/amil-khanzada/">University of Fukui</a> faculty</span>', '<span><a href="https://pure.flib.u-fukui.ac.jp/ja/persons/amil-khanzada/">福井大学</a> 着任</span>'),
        ('<span>Doctor of Engineering, <a href="https://www.u-fukui.ac.jp/eng/">University of Fukui</a></span>', '<span>博士（工学）取得、<a href="https://www.u-fukui.ac.jp/">福井大学</a></span>'),
        ('<span><a href="https://www.nsf.gov/funding/initiatives/i-corps">NSF I-Corps</a> National Team</span>', '<span><a href="https://www.nsf.gov/funding/initiatives/i-corps">NSF I-Corps</a> ナショナルチーム</span>'),
        ('<span><a href="https://patents.google.com/patent/US12444502B2/en">US Patent 12,444,502</a> granted</span>', '<span><a href="https://patents.google.com/patent/US12444502B2/en">米国特許 12,444,502</a> 取得</span>'),
        ('<span>Speaker, <a href="https://onegiantleap.com/2025-speakers">LEAP 2025</a>, Riyadh</span>', '<span><a href="https://onegiantleap.com/2025-speakers">LEAP 2025</a>（リヤド）登壇</span>'),
        ('<span>Founded <a href="https://virufy.org">Virufy</a>; featured in <a href="https://www.forbes.com.mx/emprendedores-app-diagnostico-covid-19-toser-telefono/">Forbes México</a></span>',
         '<span><a href="https://virufy.org">Virufy</a> 創業、<a href="https://www.forbes.com.mx/emprendedores-app-diagnostico-covid-19-toser-telefono/">Forbes México</a> に掲載</span>'),
        ('<span>Represented Fukui at the <a href="https://oywj.org/">One Young World</a> Summit, The Hague</span>', '<span><a href="https://oywj.org/">One Young World</a> サミット（ハーグ）に福井代表として参加</span>'),
        ('<h2 id="links-title">Elsewhere</h2>', '<h2 id="links-title">リンク</h2>'),
        ('aria-label="University of Fukui profile" title="University of Fukui profile"', 'aria-label="福井大学 研究者情報" title="福井大学 研究者情報"'),
        ('href="https://pure.flib.u-fukui.ac.jp/en/persons/amil-khanzada/" aria-label', 'href="https://pure.flib.u-fukui.ac.jp/ja/persons/amil-khanzada/" aria-label'),
        ('aria-label="Main navigation"', 'aria-label="メインナビゲーション"'),
        ('aria-label="Mobile navigation"', 'aria-label="モバイルナビゲーション"'),
        ('<div class="lang-switch" aria-label="Language">', '<div class="lang-switch" aria-label="言語">'),
    ],
}

AR = {
    "lang": "ar",
    "dir": "rtl",
    "title": "أميل خانزادا | Amil Khanzada",
    "fonts": "family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&",
    "font_css": ':root { --display: "IBM Plex Sans Arabic", "Space Grotesk", sans-serif; --text: "IBM Plex Sans Arabic", "Instrument Sans", system-ui, sans-serif; }\n'
                'html[lang="ar"] *, html[lang="ar"] *::before, html[lang="ar"] *::after { letter-spacing: 0 !important; }\n'
                'html[lang="ar"] body { line-height: 1.85; }\n'
                'html[lang="ar"] h1 { line-height: 1.15; font-weight: 600; }\n'
                'html[lang="ar"] .feature-title { line-height: 1.35; }\n'
                '[dir="rtl"] .arrow { transform: scaleX(-1); margin-left: 0; margin-right: 4px; }\n'
                '[dir="rtl"] .teaching-topics li { padding-left: 0; padding-right: 12px; }\n'
                '[dir="rtl"] .teaching-topics li::before { left: auto; right: 0; }\n'
                '[dir="rtl"] .date, [dir="rtl"] .ltr { direction: ltr; unicode-bidi: isolate; }\n'
                '[dir="rtl"] .ltr-block { display: inline-block; text-align: left; font-family: "Instrument Sans", system-ui, sans-serif; }\n',
    "nav": ["نبذة", "الخبرات", "التدريس", "المنشورات", "محطات", "روابط"],
    "pairs": [
        ('<meta name="description" content="Amil Khanzada is a professor at the University of Fukui and CEO of Virufy. He works on medical AI, tourism and data analytics, behavioral nudges and information security, bridging Japan, the US and the Middle East.">',
         '<meta name="description" content="أميل خانزادا، أستاذ في جامعة فوكوي ومؤسس Virufy ورئيسها التنفيذي. يعمل في الذكاء الاصطناعي الطبي والسياحة وتحليل البيانات والوكز السلوكي وأمن المعلومات، ويربط بين اليابان والولايات المتحدة والشرق الأوسط.">'),
        ('<meta property="og:title" content="Amil Khanzada">', '<meta property="og:title" content="أميل خانزادا | Amil Khanzada">'),
        ('<meta property="og:description" content="Professor and CEO building AI that works in the real world: medical AI, tourism and data analytics, behavioral nudges and information security.">',
         '<meta property="og:description" content="أستاذ ورئيس تنفيذي يبني ذكاءً اصطناعيًا يعمل في الواقع: الذكاء الاصطناعي الطبي، والسياحة وتحليل البيانات، والوكز السلوكي، وأمن المعلومات.">'),
        ('<a class="brand" href="#top">Amil Khanzada</a>', '<a class="brand" href="#top">أميل خانزادا</a>'),
        ('<span class="menu-label">Menu</span>', '<span class="menu-label">القائمة</span>'),
        ('<h2 id="about-title">About</h2>', '<h2 id="about-title">نبذة</h2>'),
        ('<h2 id="expertise-title">Expertise</h2>', '<h2 id="expertise-title">الخبرات</h2>'),
        ('<h2 id="teaching-title">Teaching</h2>', '<h2 id="teaching-title">التدريس</h2>'),
        ('<h1 id="name">Amil<br>Khanzada</h1>', '<h1 id="name">أميل<br>خانزادا</h1>'),
        ('<p class="role">Professor, <a href="https://www.u-fukui.ac.jp/eng/">University of Fukui</a><br>Founder &amp; CEO, <a href="https://virufy.org">Virufy</a></p>',
         '<p class="role">أستاذ، <a href="https://www.u-fukui.ac.jp/eng/">جامعة فوكوي</a><br>المؤسس والرئيس التنفيذي، <a href="https://virufy.org">Virufy</a></p>'),
        ('<p class="summary">I build AI that works in the real world: medical AI, tourism and data analytics, behavioral nudges and information security. I bring people together across Japan, the US and the Middle East.</p>',
         '<p class="summary">أبني ذكاءً اصطناعيًا يعمل في الواقع: الذكاء الاصطناعي الطبي، والسياحة وتحليل البيانات، والوكز السلوكي، وأمن المعلومات. وأربط بين الناس في اليابان والولايات المتحدة والشرق الأوسط.</p>'),
        ('<h3 class="feature-title">Between Japan<br>and Silicon Valley.</h3>', '<h3 class="feature-title">بين اليابان<br>ووادي السيليكون.</h3>'),
        ('<p>I’m a Specially Appointed Assistant Professor at the <a href="https://pure.flib.u-fukui.ac.jp/en/persons/amil-khanzada/">University of Fukui</a>’s Regional Revitalization Headquarters. I teach entrepreneurship and AI and work with local governments across Hokuriku.</p>',
         '<p>أستاذ مساعد بتعيين خاص في مقر التنشيط الإقليمي بـ<a href="https://pure.flib.u-fukui.ac.jp/en/persons/amil-khanzada/">جامعة فوكوي</a>. أدرّس ريادة الأعمال والذكاء الاصطناعي، وأعمل مع الحكومات المحلية في منطقة هوكوريكو.</p>'),
        ('<p>I’ve been Founder and CEO of <a href="https://virufy.org">virufy.org</a> since 2020.</p>',
         '<p>مؤسس <a href="https://virufy.org">virufy.org</a> ورئيسها التنفيذي منذ عام 2020.</p>'),
        ('<p>My 15+ years in tech and AI include leading engineering teams in Silicon Valley and Tokyo at <a href="https://en.wikipedia.org/wiki/Greenplum">VMware Pivotal Greenplum</a> and <a href="https://www.hpe.com/">HP Enterprise</a>, and serving as Technical Lead at <a href="https://sandbox.mit.edu/">MIT Sandbox</a>.</p>',
         '<p>أكثر من 15 عامًا من الخبرة في التقنية والذكاء الاصطناعي، شملت قيادة فرق هندسية في وادي السيليكون وطوكيو لدى <a href="https://en.wikipedia.org/wiki/Greenplum">VMware Pivotal Greenplum</a> و<a href="https://www.hpe.com/">HP Enterprise</a>، والعمل قائدًا تقنيًا في <a href="https://sandbox.mit.edu/">MIT Sandbox</a>.</p>'),
        ('<p>Fluent in Japanese and Urdu/Hindi. <a href="https://oywj.org/">One Young World</a> Japan Ambassador and <a href="https://www.town.eiheiji.lg.jp/900/905/p003453.html">Eiheiji Town</a> Evolution Ambassador.</p>',
         '<p>أتحدث اليابانية والأردية/الهندية بطلاقة. سفير <a href="https://oywj.org/">One Young World</a> في اليابان، وسفير التطور لبلدة <a href="https://www.town.eiheiji.lg.jp/900/905/p003453.html">إيهيجي</a>.</p>'),
        ('<h3 class="subheading">Education</h3>', '<h3 class="subheading">التعليم</h3>'),
        ('<a class="institution" href="https://www.u-fukui.ac.jp/eng/">University of Fukui</a>\n            <span class="detail">Doctor of Engineering, behavioral nudges and human data</span>',
         '<a class="institution" href="https://www.u-fukui.ac.jp/eng/">جامعة فوكوي</a>\n            <span class="detail">دكتوراه في الهندسة، الوكز السلوكي ومشاركة البيانات</span>'),
        ('<a class="institution" href="https://haas.berkeley.edu/">UC Berkeley Haas School of Business</a>\n            <span class="detail">MBA and Master of Engineering (Data Science) concurrent program, first year</span>',
         '<a class="institution" href="https://haas.berkeley.edu/">كلية هاس لإدارة الأعمال، جامعة كاليفورنيا في بيركلي</a>\n            <span class="detail">البرنامج المتزامن لماجستير إدارة الأعمال والماجستير في الهندسة (علوم البيانات)، السنة الأولى</span>'),
        ('<a class="institution" href="https://scpd.stanford.edu/">Stanford University</a>\n            <span class="detail">Graduate courses, 4.0 GPA: ',
         '<a class="institution" href="https://scpd.stanford.edu/">جامعة ستانفورد</a>\n            <span class="detail">مقررات دراسات عليا بمعدل 4.0:<br><span dir="ltr" class="ltr-block">'),
        ('</a> with <a href="https://www.andrewng.org/">Andrew Ng</a>, ', '</a> (<a href="https://www.andrewng.org/">Andrew Ng</a>), '),
        ('</a> with <a href="https://profiles.stanford.edu/fei-fei-li">Fei-Fei Li</a>, ', '</a> (<a href="https://profiles.stanford.edu/fei-fei-li">Fei-Fei Li</a>), '),
        ('</a> with <a href="https://huyenchip.com/">Chip Huyen</a>, ', '</a> (<a href="https://huyenchip.com/">Chip Huyen</a>), '),
        ('</a> with <a href="https://profiles.stanford.edu/rishi-mediratta">Rishi Mediratta</a></span>', '</a> (<a href="https://profiles.stanford.edu/rishi-mediratta">Rishi Mediratta</a>)</span></span>'),
        ('<a class="institution" href="https://cs.berkeley.edu/">UC Berkeley</a>\n            <span class="detail">B.A. Computer Science</span>',
         '<a class="institution" href="https://cs.berkeley.edu/">جامعة كاليفورنيا في بيركلي</a>\n            <span class="detail">بكالوريوس علوم الحاسوب</span>'),
        ('alt="Amil Khanzada at the University of Fukui degree ceremony"', 'alt="أميل خانزادا في حفل منح الدرجات بجامعة فوكوي"'),
        ('<figcaption>Degree conferment, University of Fukui.</figcaption>', '<figcaption>حفل منح الدرجات العلمية، جامعة فوكوي.</figcaption>'),
        ('alt="Amil Khanzada with Sabae Mayor Katsuhisa Sasaki and visiting researchers"', 'alt="أميل خانزادا مع رئيس بلدية ساباي كاتسوهيسا ساساكي وباحثين زائرين"'),
        ('<figcaption>With Sabae Mayor Katsuhisa Sasaki and <a href="https://ssp.jst.go.jp/en/">JST Sakura Science</a> researchers.</figcaption>',
         '<figcaption>مع رئيس بلدية ساباي كاتسوهيسا ساساكي وباحثي برنامج <a href="https://ssp.jst.go.jp/en/">JST Sakura Science</a>.</figcaption>'),
        ('<h3>Medical AI</h3>\n          <div><p>Researching whether cough sounds recorded on a phone can help screen for respiratory conditions.</p></div>',
         '<h3>الذكاء الاصطناعي الطبي</h3>\n          <div><p>أبحاث حول ما إذا كانت أصوات السعال المسجلة بالهاتف يمكن أن تساعد في فحص أمراض الجهاز التنفسي.</p></div>'),
        ('<h3>Tourism and data analytics</h3>', '<h3>السياحة وتحليل البيانات</h3>'),
        ('<p>Forecasting visitor demand across Fukui with local governments.</p>', '<p>التنبؤ بأعداد الزوار في محافظة فوكوي بالتعاون مع الحكومات المحلية.</p>'),
        ('>Live dashboard</a>', '>لوحة بيانات مباشرة</a>'),
        ('<h3>Behavioral nudges</h3>\n          <div><p>Getting people to share data at scale, without paying them.</p></div>',
         '<h3>الوكز السلوكي</h3>\n          <div><p>تشجيع الناس على مشاركة بياناتهم على نطاق واسع دون مقابل مادي.</p></div>'),
        ('<h3>Information security</h3>\n          <div><p>Security analytics for Fortune 500 clients and Japanese megabanks at <a href="https://www.hpe.com/">HP Enterprise</a>.</p></div>',
         '<h3>أمن المعلومات</h3>\n          <div><p>تحليلات أمنية لعملاء Fortune 500 وكبرى البنوك اليابانية لدى <a href="https://www.hpe.com/">HP Enterprise</a>.</p></div>'),
        ('<h3>Bridging Japan and the world</h3>', '<h3>جسر بين اليابان والعالم</h3>'),
        ('<p>Connecting universities, governments and companies across Japan, Silicon Valley, the Gulf and South Asia.</p>',
         '<p>ربط الجامعات والحكومات والشركات في اليابان ووادي السيليكون والخليج وجنوب آسيا.</p>'),
        ('alt="Amil Khanzada showing the Fukui tourism dashboard to Governor Ishida"', 'alt="أميل خانزادا يعرض لوحة بيانات السياحة في فوكوي على المحافظ إيشيدا"'),
        ('<figcaption>Showing our tourism dashboard to Fukui Governor Ishida at the Fukui Industrial AI/AX Consortium kickoff.</figcaption>',
         '<figcaption>عرض لوحة بيانات السياحة على محافظ فوكوي إيشيدا خلال إطلاق اتحاد فوكوي للذكاء الاصطناعي الصناعي (AI/AX).</figcaption>'),
        ('<h3 class="feature-title">A global health<br>AI nonprofit.</h3>', '<h3 class="feature-title">منظمة عالمية غير ربحية<br>للذكاء الاصطناعي الصحي.</h3>'),
        ('<p>As CEO, I lead a 501(c)(3) with more than 1,300 volunteers and 60+ partner universities. Our work spans clinical studies in five countries and two patents in the US and Japan.</p>',
         '<p>بصفتي الرئيس التنفيذي، أقود منظمة أمريكية غير ربحية (501(c)(3)) تضم أكثر من 1,300 متطوع وأكثر من 60 جامعة شريكة. يشمل عملنا دراسات سريرية في خمس دول وبراءتي اختراع في الولايات المتحدة واليابان.</p>'),
        ('<h3 class="feature-title">The city is the classroom.</h3>', '<h3 class="feature-title">المدينة هي الفصل الدراسي.</h3>'),
        ('<p class="prose">At the <a href="https://www.u-fukui.ac.jp/eng/">University of Fukui</a>, I teach entrepreneurship, AI-powered social informatics and management of technology. Students work in the field with mayors and tourism boards. In 2026, I hosted young researchers from four countries through the <a href="https://ssp.jst.go.jp/en/">JST Sakura Science Program</a>.</p>',
         '<p class="prose">أدرّس في <a href="https://www.u-fukui.ac.jp/eng/">جامعة فوكوي</a> ريادة الأعمال، والمعلوماتية الاجتماعية المدعومة بالذكاء الاصطناعي، وإدارة التكنولوجيا. يعمل الطلاب ميدانيًا مع رؤساء البلديات وهيئات السياحة. وفي عام 2026 استضفت باحثين شبابًا من أربع دول عبر برنامج <a href="https://ssp.jst.go.jp/en/">JST Sakura Science</a>.</p>'),
        ('aria-label="Teaching topics"', 'aria-label="موضوعات التدريس"'),
        ('<li>Nudges and data</li>', '<li>الوكز السلوكي والبيانات</li>'),
        ('<li>Medical AI</li>', '<li>الذكاء الاصطناعي الطبي</li>'),
        ('<li>AI for regions</li>', '<li>الذكاء الاصطناعي للمناطق</li>'),
        ('<li>Global teams</li>', '<li>فرق عالمية</li>'),
        ('alt="Amil Khanzada lecturing at the University of Fukui"', 'alt="أميل خانزادا يلقي محاضرة في جامعة فوكوي"'),
        ('<figcaption>Workshop, University of Fukui.</figcaption>', '<figcaption>ورشة عمل، جامعة فوكوي.</figcaption>'),
        ('<h2 id="publications-title">Selected<br>publications</h2>', '<h2 id="publications-title">منشورات<br>مختارة</h2>'),
        ('<p class="publication-intro">Full list on <a href="https://scholar.google.com/citations?user=zdgfTfMAAAAJ">Google Scholar</a>, <a href="https://pure.flib.u-fukui.ac.jp/en/persons/amil-khanzada/">University of Fukui</a> and <a href="https://orcid.org/0000-0002-7065-5390">ORCID</a>.</p>',
         '<p class="publication-intro">القائمة الكاملة على <a href="https://scholar.google.com/citations?user=zdgfTfMAAAAJ">Google Scholar</a> و<a href="https://pure.flib.u-fukui.ac.jp/en/persons/amil-khanzada/">جامعة فوكوي</a> و<a href="https://orcid.org/0000-0002-7065-5390">ORCID</a>.</p>'),
        ('<span class="venue">US Patent 12,444,502 and Japanese Patent 7850135</span>', '<span class="venue">براءة الاختراع الأمريكية <span class="ltr">12,444,502</span> وبراءة الاختراع اليابانية <span class="ltr">7850135</span></span>'),
        ('<h2 id="news-title">Milestones</h2>', '<h2 id="news-title">محطات</h2>'),
        ('<span>Hosted the <a href="https://ssp.jst.go.jp/en/">JST Sakura Science Program</a> in Fukui</span>', '<span>استضافة برنامج <a href="https://ssp.jst.go.jp/en/">JST Sakura Science</a> في فوكوي</span>'),
        ('<span><a href="https://doi.org/10.1016/j.measurement.2026.122500">DHDE paper</a> published in Measurement</span>', '<span>نشر <a href="https://doi.org/10.1016/j.measurement.2026.122500">ورقة DHDE</a> في مجلة Measurement</span>'),
        ('<span>Japanese Patent 7850135 granted</span>', '<span>منح براءة الاختراع اليابانية <span class="ltr">7850135</span></span>'),
        ('<span>Joined the <a href="https://pure.flib.u-fukui.ac.jp/en/persons/amil-khanzada/">University of Fukui</a> faculty</span>', '<span>الانضمام إلى هيئة التدريس في <a href="https://pure.flib.u-fukui.ac.jp/en/persons/amil-khanzada/">جامعة فوكوي</a></span>'),
        ('<span>Doctor of Engineering, <a href="https://www.u-fukui.ac.jp/eng/">University of Fukui</a></span>', '<span>دكتوراه في الهندسة، <a href="https://www.u-fukui.ac.jp/eng/">جامعة فوكوي</a></span>'),
        ('<span><a href="https://www.nsf.gov/funding/initiatives/i-corps">NSF I-Corps</a> National Team</span>', '<span>الفريق الوطني لبرنامج <a href="https://www.nsf.gov/funding/initiatives/i-corps">NSF I-Corps</a></span>'),
        ('<span><a href="https://patents.google.com/patent/US12444502B2/en">US Patent 12,444,502</a> granted</span>', '<span>منح <a href="https://patents.google.com/patent/US12444502B2/en">براءة الاختراع الأمريكية <span class="ltr">12,444,502</span></a></span>'),
        ('<span>Speaker, <a href="https://onegiantleap.com/2025-speakers">LEAP 2025</a>, Riyadh</span>', '<span>متحدث في <a href="https://onegiantleap.com/2025-speakers">LEAP 2025</a>، الرياض</span>'),
        ('<span>Founded <a href="https://virufy.org">Virufy</a>; featured in <a href="https://www.forbes.com.mx/emprendedores-app-diagnostico-covid-19-toser-telefono/">Forbes México</a></span>',
         '<span>تأسيس <a href="https://virufy.org">Virufy</a>، وظهورها في <a href="https://www.forbes.com.mx/emprendedores-app-diagnostico-covid-19-toser-telefono/">Forbes México</a></span>'),
        ('<span>Represented Fukui at the <a href="https://oywj.org/">One Young World</a> Summit, The Hague</span>', '<span>تمثيل فوكوي في قمة <a href="https://oywj.org/">One Young World</a>، لاهاي</span>'),
        ('<h2 id="links-title">Elsewhere</h2>', '<h2 id="links-title">روابط</h2>'),
        ('aria-label="University of Fukui profile" title="University of Fukui profile"', 'aria-label="الملف الأكاديمي في جامعة فوكوي" title="الملف الأكاديمي في جامعة فوكوي"'),
        ('aria-label="Main navigation"', 'aria-label="التنقل الرئيسي"'),
        ('aria-label="Mobile navigation"', 'aria-label="قائمة التنقل"'),
        ('<div class="lang-switch" aria-label="Language">', '<div class="lang-switch" aria-label="اللغة">'),
        ('<p>© 2026 Amil Khanzada</p>', '<p>© 2026 أميل خانزادا</p>'),
    ],
}


# --- 2026-10-21 revision (Sheeba's feedback): pairs replaced by prefix ---
def _swap(cfg, drop_prefixes, add):
    cfg["pairs"] = [pr for pr in cfg["pairs"] if not any(pr[0].startswith(d) for d in drop_prefixes)] + add

_DROP = [
    '<p class="summary">I build AI', '<p>I’m a Specially Appointed', '<p>I’ve been Founder and CEO', '<p>My 15+ years',
    '<a class="institution" href="https://haas.berkeley.edu/">', '<a class="institution" href="https://scpd.stanford.edu/">',
    '</a> with <a href="https://www.andrewng.org/">', '</a> with <a href="https://profiles.stanford.edu/fei-fei-li">',
    '</a> with <a href="https://huyenchip.com/">', '</a> with <a href="https://profiles.stanford.edu/rishi-mediratta">',
    '<figcaption>Degree conferment', '<figcaption>With Sabae Mayor', '<figcaption>Showing our tourism dashboard',
    '<p>As CEO, I lead', '<figcaption>Workshop, University of Fukui.',
]
_PF = 'https://pure.flib.u-fukui.ac.jp/en/persons/amil-khanzada/'
_GB = '<a href="https://en.wikipedia.org/wiki/Greenplum">VMware Pivotal Greenplum</a>'
_HP = '<a href="https://www.hpe.com/">HP Enterprise</a>'
_MS = '<a href="https://sandbox.mit.edu/">MIT Sandbox</a>'
_EN = {
 'summary': '<p class="summary">I develop real-world AI applications across healthcare, tourism, data analytics, behavioral science and cybersecurity, while building bridges between people and ideas across Japan, the US and the Middle East.</p>',
 'p1': f'<p>I’m a Specially Appointed Assistant Professor at the <a href="{_PF}">University of Fukui</a>’s Regional Revitalization Headquarters, where I teach entrepreneurship and AI and work with local governments across Hokuriku on regional innovation.</p>',
 'p2': '<p>Since 2020, I’ve been Founder and CEO of <a href="https://virufy.org">virufy.org</a>, a nonprofit applying AI to real-world health challenges.</p>',
 'p3': f'<p>I have more than 15 years of experience in tech and AI. I’ve led engineering teams in Silicon Valley and Tokyo at {_GB} and {_HP}, and served as Technical Lead at {_MS}.</p>',
 'haas': '<a class="institution" href="https://haas.berkeley.edu/">UC Berkeley Haas School of Business</a>\n            <span class="detail">MBA and Master of Engineering (Data Science) concurrent degree program, first year completed</span>',
 'stan': '<a class="institution" href="https://scpd.stanford.edu/">Stanford University</a>\n            <span class="detail">Graduate coursework in computer science and AI, 4.0 GPA</span>',
 'ng': '</a> with <a href="https://www.andrewng.org/">Andrew Ng</a></li>',
 'li': '</a> with <a href="https://profiles.stanford.edu/fei-fei-li">Fei-Fei Li</a></li>',
 'hu': '</a> with <a href="https://huyenchip.com/">Chip Huyen</a></li>',
 'rm': '</a> with <a href="https://profiles.stanford.edu/rishi-mediratta">Rishi Mediratta</a></li>',
 'vir': '<p>As CEO, I lead a 501(c)(3) that more than 1,300 volunteers have joined since 2020, with 60+ partner universities.',
 'nav': '">Moments</a></li>',
 'h2': '<h2 id="moments-title">Moments</h2>',
 'c1': '<span class="when">Oct 2026</span>Showing our tourism dashboard to Fukui Governor Ishida at the Fukui Industrial AI/AX Consortium kickoff</figcaption>',
 'c2': '<span class="when">Sep 2026</span>In Sabae with Mayor Katsuhisa Sasaki and researchers from the <a href="https://ssp.jst.go.jp/en/">JST Sakura Science Exchange Program</a></figcaption>',
 'c3': '<span class="when">2026</span>Doctor of Engineering, University of Fukui</figcaption>',
 'c4': '<span class="when">Jul 2026</span>Leading an AI workshop for a Fukui manufacturer</figcaption>',
 'c5': '<span class="when">2026</span>Teaching a data-driven decision workshop, University of Fukui</figcaption>',
 'a4': 'alt="Amil Khanzada leading an AI workshop for industry in Fukui"',
}
_JA = {
 'summary': '<p class="summary">医療、観光、データ分析、行動科学、サイバーセキュリティの分野で、社会の現場で役立つAIを開発しています。日本、米国、中東の人とアイデアをつなぐ架け橋として活動しています。</p>',
 'p1': '<p><a href="https://pure.flib.u-fukui.ac.jp/ja/persons/amil-khanzada/">福井大学</a> 地域創生推進本部 特命助教。アントレプレナーシップとAIを教え、北陸の自治体と連携して地域のイノベーションに取り組んでいます。</p>',
 'p2': '<p>2020年から、AIで医療の課題に取り組む非営利団体 <a href="https://virufy.org">virufy.org</a> の創業者・CEOを務めています。</p>',
 'p3': f'<p>テック・AI分野で15年以上の経験があります。シリコンバレーと東京で {_GB} や {_HP} のエンジニアリングチームを率い、{_MS} ではテクニカルリードを務めました。</p>',
 'haas': '<a class="institution" href="https://haas.berkeley.edu/">カリフォルニア大学バークレー校 ハース・スクール・オブ・ビジネス</a>\n            <span class="detail">MBA・工学修士（データサイエンス）同時学位プログラム 1年次修了</span>',
 'stan': '<a class="institution" href="https://scpd.stanford.edu/">スタンフォード大学</a>\n            <span class="detail">大学院科目（コンピュータサイエンス・AI）、GPA 4.0</span>',
 'ng': '</a>（<a href="https://www.andrewng.org/">Andrew Ng</a>）</li>',
 'li': '</a>（<a href="https://profiles.stanford.edu/fei-fei-li">Fei-Fei Li</a>）</li>',
 'hu': '</a>（<a href="https://huyenchip.com/">Chip Huyen</a>）</li>',
 'rm': '</a>（<a href="https://profiles.stanford.edu/rishi-mediratta">Rishi Mediratta</a>）</li>',
 'vir': '<p>CEOとして、2020年以降1,300人以上のボランティアが参加し、60以上のパートナー大学と連携する米国の非営利団体（501(c)(3)）を率いています。',
 'nav': '">活動の記録</a></li>',
 'h2': '<h2 id="moments-title">活動の記録</h2>',
 'c1': '<span class="when">2026年10月</span>福井県産業AI/AXコンソーシアムのキックオフで、石田知事に観光ダッシュボードをご紹介</figcaption>',
 'c2': '<span class="when">2026年9月</span>鯖江市 佐々木勝久市長、<a href="https://ssp.jst.go.jp/">JSTさくらサイエンスプログラム</a>の研究者とともに</figcaption>',
 'c3': '<span class="when">2026年</span>博士（工学）、福井大学</figcaption>',
 'c4': '<span class="when">2026年7月</span>福井の製造業企業でAIワークショップを実施</figcaption>',
 'c5': '<span class="when">2026年</span>福井大学でデータに基づく意思決定のワークショップ</figcaption>',
 'a4': 'alt="福井の企業でAIワークショップを行うカンザダ あみる"',
}
_AR = {
 'summary': '<p class="summary">أطوّر تطبيقات ذكاء اصطناعي عملية في مجالات الرعاية الصحية والسياحة وتحليل البيانات والعلوم السلوكية والأمن السيبراني، وأبني جسورًا بين الناس والأفكار في اليابان والولايات المتحدة والشرق الأوسط.</p>',
 'p1': f'<p>أستاذ مساعد بتعيين خاص في مقر التنشيط الإقليمي بـ<a href="{_PF}">جامعة فوكوي</a>، حيث أدرّس ريادة الأعمال والذكاء الاصطناعي، وأعمل مع الحكومات المحلية في منطقة هوكوريكو على الابتكار الإقليمي.</p>',
 'p2': '<p>منذ عام 2020، أشغل منصب مؤسس <a href="https://virufy.org">virufy.org</a> ورئيسها التنفيذي، وهي منظمة غير ربحية تطبّق الذكاء الاصطناعي على تحديات صحية واقعية.</p>',
 'p3': f'<p>لديّ أكثر من 15 عامًا من الخبرة في التقنية والذكاء الاصطناعي. قدتُ فرقًا هندسية في وادي السيليكون وطوكيو لدى {_GB} و{_HP}، وعملت قائدًا تقنيًا في {_MS}.</p>',
 'haas': '<a class="institution" href="https://haas.berkeley.edu/">كلية هاس لإدارة الأعمال، جامعة كاليفورنيا في بيركلي</a>\n            <span class="detail">البرنامج المتزامن لماجستير إدارة الأعمال والماجستير في الهندسة (علوم البيانات)، أكملتُ السنة الأولى</span>',
 'stan': '<a class="institution" href="https://scpd.stanford.edu/">جامعة ستانفورد</a>\n            <span class="detail">مقررات دراسات عليا في علوم الحاسوب والذكاء الاصطناعي، بمعدل 4.0</span>',
 'ng': '</a> (<a href="https://www.andrewng.org/">Andrew Ng</a>)</li>',
 'li': '</a> (<a href="https://profiles.stanford.edu/fei-fei-li">Fei-Fei Li</a>)</li>',
 'hu': '</a> (<a href="https://huyenchip.com/">Chip Huyen</a>)</li>',
 'rm': '</a> (<a href="https://profiles.stanford.edu/rishi-mediratta">Rishi Mediratta</a>)</li>',
 'vir': '<p>بصفتي الرئيس التنفيذي، أقود منظمة أمريكية غير ربحية (501(c)(3)) انضم إليها أكثر من 1,300 متطوع منذ عام 2020، وتتعاون مع أكثر من 60 جامعة شريكة.',
 'nav': '">لقطات</a></li>',
 'h2': '<h2 id="moments-title">لقطات</h2>',
 'c1': '<span class="when">أكتوبر 2026</span>عرض لوحة بيانات السياحة على محافظ فوكوي إيشيدا خلال إطلاق اتحاد فوكوي للذكاء الاصطناعي الصناعي (AI/AX)</figcaption>',
 'c2': '<span class="when">سبتمبر 2026</span>في ساباي مع رئيس البلدية كاتسوهيسا ساساكي وباحثي برنامج <a href="https://ssp.jst.go.jp/en/">JST Sakura Science</a></figcaption>',
 'c3': '<span class="when">2026</span>دكتوراه في الهندسة، جامعة فوكوي</figcaption>',
 'c4': '<span class="when">يوليو 2026</span>تقديم ورشة عمل في الذكاء الاصطناعي لشركة صناعية في فوكوي</figcaption>',
 'c5': '<span class="when">2026</span>ورشة عمل حول اتخاذ القرار المبني على البيانات، جامعة فوكوي</figcaption>',
 'a4': 'alt="أميل خانزادا يقدّم ورشة عمل في الذكاء الاصطناعي لقطاع الصناعة في فوكوي"',
}
for _cfg, _tr in ((JA, _JA), (AR, _AR)):
    _cnt = {'nav': 2}
    _swap(_cfg, _DROP, [(_EN[k], _tr[k], _cnt.get(k, 1)) for k in _EN])

for _cfg, _a, _b in ((JA, '<span>Virufy <a href="https://virufy.org/en/news/gitex-global-2025-dubai/">ドバイで事業開始</a></span>', '<span>Virufy 日本拠点を福岡に開設</span>'),
                     (AR, '<span><a href="https://virufy.org/en/news/gitex-global-2025-dubai/">إطلاق عمليات Virufy في دبي</a></span>', '<span>افتتاح مركز Virufy في اليابان بمدينة فوكوكا</span>')):
    _cfg["pairs"] += [('<span>Launched Virufy <a href="https://virufy.org/en/news/gitex-global-2025-dubai/">operations in Dubai</a></span>', _a),
                      ("<span>Opened Virufy's Japan hub in Fukuoka</span>", _b)]


def build(cfg):
    s = SRC
    lang = cfg["lang"]
    errors = []

    def rep(old, new, count=1):
        nonlocal s
        n = s.count(old)
        if (count and n != count) or (not count and n == 0):
            errors.append(f"[{lang}] expected {count or '>=1'} of: {old[:90]!r}, found {n}")
            return
        s = s.replace(old, new)

    for pair in cfg["pairs"]:
        rep(*pair)
    for en, tr in zip(COMMON_NAV, cfg["nav"]):
        rep(f'">{en}</a></li>', f'">{tr}</a></li>', 2)
    rep('<html lang="en">', f'<html lang="{lang}" dir="{cfg["dir"]}">')
    rep('<title>Amil Khanzada</title>', f'<title>{cfg["title"]}</title>')
    rep('<link rel="canonical" href="https://amilkhanzada.com/">', f'<link rel="canonical" href="https://amilkhanzada.com/{lang}/">')
    rep('<meta property="og:url" content="https://amilkhanzada.com/">', f'<meta property="og:url" content="https://amilkhanzada.com/{lang}/">')
    rep('"url": "https://amilkhanzada.com/",', f'"url": "https://amilkhanzada.com/{lang}/",')
    rep('href="https://fonts.googleapis.com/css2?', f'href="https://fonts.googleapis.com/css2?{cfg["fonts"]}')
    rep('</style>', cfg["font_css"] + '</style>')
    # local assets live one folder up
    s = re.sub(r'(src|href)="(img/|favicon\.svg|apple-touch-icon\.png)', r'\1="../\2', s)
    # language switcher for this page
    sw = re.search(r'<!--LANG-->.*?<!--/LANG-->', s, re.S)
    if not sw:
        errors.append(f"[{lang}] language switcher markers missing")
    else:
        cur = {'en': '', 'ja': '', 'ar': ''}
        cur[lang] = ' aria-current="true"'
        aria = re.search(r'<div class="lang-switch" aria-label="([^"]*)">', sw.group(0)).group(1)
        block = ('<!--LANG-->\n    <div class="lang-switch" aria-label="%s">\n'
                 '      <a href="../" hreflang="en"%s>EN</a>\n'
                 '      <a href="../ja/" hreflang="ja" lang="ja"%s>日本語</a>\n'
                 '      <a href="../ar/" hreflang="ar" lang="ar"%s>العربية</a>\n'
                 '    </div>\n    <!--/LANG-->') % (aria, cur['en'], cur['ja'], cur['ar'])
        s = s[:sw.start()] + block + s[sw.end():]
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    out = ROOT / lang / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(s, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    build(JA)
    build(AR)
