"""準備版を再生成する補助スクリプト。既存Wordを直接編集した後は無断で再実行しない。"""
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parent
doc = Document()
section = doc.sections[0]
section.page_width, section.page_height = Inches(8.5), Inches(11)
section.top_margin = section.bottom_margin = Inches(0.8)
section.left_margin = section.right_margin = Inches(0.85)
for name in ['Normal', 'Title', 'Subtitle', 'Heading 1', 'Heading 2']:
    style = doc.styles[name]
    style.font.name = 'Noto Serif CJK JP'
    style.font.color.rgb = RGBColor(0, 0, 0)
    style.element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'), 'Noto Serif CJK JP')
    style.paragraph_format.space_after = Pt(5)
    for border in list(style.element.iter(qn('w:pBdr'))):
        border.getparent().remove(border)
    style.paragraph_format.page_break_before = False
    for key in ['asciiTheme', 'hAnsiTheme', 'eastAsiaTheme', 'cstheme']:
        style.element.get_or_add_rPr().rFonts.attrib.pop(qn('w:' + key), None)
doc.styles['Normal'].font.size = Pt(11)
doc.styles['Normal'].paragraph_format.line_spacing = 1.1
doc.styles['Title'].font.size = Pt(19)
doc.styles['Heading 1'].font.size = Pt(14)
doc.styles['Heading 2'].font.size = Pt(12)
doc.styles['Heading 1'].paragraph_format.space_before = Pt(12)
doc.styles['Subtitle'].font.italic = False

def p(text, style=None):
    return doc.add_paragraph(text, style)

def h(text):
    doc.add_heading(text, level=1)

doc.add_paragraph('乳幼児期におけるデジタルメディアの利用と子どもの発達との関連', 'Title')
p('卒業論文の研究準備　2026年11月16日', 'Subtitle')
p('本研究では、文献研究の方法を用いて、乳幼児期のデジタルメディア利用と子どもの発達との関連を検討する。まず関連文献を読み、対象年齢や利用の仕方、研究方法の違いを整理する。')
h('研究計画')
p('研究方法は文献研究とする。対象年齢の具体的な範囲、中心に取り上げる発達領域、文献の検索方法と選定基準は、大学から配付された文献研究の書き方を確認してから定める。')
h('検討する視点の仮案')
p('利用時間と睡眠・情緒・行動・神経発達との関連を扱う文献と、デジタル絵本や保育活動での利用を扱う文献を整理する。利用の内容や場面、大人の関わり、子どもの年齢に着目し、研究間の共通点と違いを検討する。')
h('章立ての仮案')
for line in [
    '第1章　問題と目的',
    '第2章　文献研究の方法',
    '第3章　利用時間と睡眠や発達との関連',
    '第4章　利用内容と関わり方に着目した検討',
    '第5章　総合考察と今後の課題',
    '参考文献',
]:
    p(line)
p('提出期限、必要文字数、書式、引用様式は今後確認する。章立ては配付資料と精読結果に合わせて調整する。')

doc.add_page_break()
doc.add_paragraph('参考文献候補', 'Title')
p('学術文献6件と公的資料2件を記録する。同一の睡眠教育の文献は1件にまとめた。引用様式と本文への採否は、配付資料の確認と文献の精読後に整える。')
h('学術文献')
refs = [
    ('岡 靖哲（2025）．デジタルネイティブ世代の乳幼児の睡眠教育．乳幼児医学・心理学研究，34(1)，27-36．', 'https://doi.org/10.82622/jjmpsi.34.1_27'),
    ('大久保 圭介・遠藤 利彦・野澤 祥子（2023）．乳幼児期の子どものデジタルメディア使用時間と睡眠，および情緒や行動の問題の縦断的関連．発達心理学研究，34(3)，230-243．', 'https://doi.org/10.11201/jjdp.34.230'),
    ('土屋 賢治・ラハマン M・ショフィウル・高橋 長秀・西村 倫子（2024）．乳幼児期スクリーンタイムと神経発達の予後：知見を振り返る．日本生物学的精神医学会誌，35(2)，90-93．', 'https://doi.org/10.11249/jsbpjjpp.35.2_90'),
    ('坂田 陽子・川口 沙也加・杉浦 悠子（2015）．幼児の年齢に応じたデジタルデバイスの使用方法の検討 ―デジタル絵本をもとに―．デジタル教科書研究，2，19-31．', 'https://doi.org/10.20755/jsdtj.2.0_19'),
    ('池下 花恵・竹永 羽・河合 隆史・七海 陽・齋藤 正典（2021）．保育活動でのデジタル機器使用時における幼児の発話への影響．人間工学，57(6)，320-328．', 'https://doi.org/10.5100/jje.57.320'),
    ('佐藤 朝美・佐藤 桃子（2013）．紙絵本との比較によるデジタル絵本の読み聞かせの特徴の分析．日本教育工学会論文誌，37(Suppl.)，49-52．', 'https://doi.org/10.15077/jjet.KJ00009957512'),
]
for i, (entry, url) in enumerate(refs, 1):
    para = p(f'{i}　{entry}')
    para.paragraph_format.keep_with_next = True
    para = p(url)
    para.paragraph_format.space_after = Pt(9)
    for run in para.runs:
        run.font.size = Pt(10)

doc.add_page_break()
doc.add_paragraph('公的資料と確認事項', 'Title')
h('公的資料')
p('7　スポーツ庁（2021）．令和3年度 全国体力・運動能力、運動習慣等調査の結果（概要）について．')
p('https://www.mext.go.jp/sports/content/20211222-spt_sseisaku02-000019583_111.pdf')
p('小学校5年生と中学校2年生を対象とする調査である。乳幼児の発達に関する直接の根拠とは区別し、社会的背景を整理する資料としての使用を検討する。')
p('8　厚生労働省．図表1-2-4-4 子どものスクリーンタイムの変化．')
p('https://www.mhlw.go.jp/stf/wp/hakusyo/kousei/20/backdata/1-2-4-4.html')
p('図表の対象年齢、原調査、掲載年次、数値は、図表画像とバックデータを照合してから本文に用いる。')
h('文献の確認状況')
p('現段階では学術文献の書誌情報を確認した。神経発達に関する文献と発話に関する文献は抄録も確認した。学術論文のPDF本文の精読は今後行う。公的資料は掲載ページまたはPDF冒頭を確認した段階である。')
h('次に進めること')
p('大学から配付された文献研究の書き方を確認し、研究目的、文献の検索・選定方法、章立て、引用方法を整える。その後、各文献の対象、方法、結果、限界を共通の項目で整理する。')

footer = section.footer.paragraphs[0]
footer.alignment = 2
field = OxmlElement('w:fldSimple')
field.set(qn('w:instr'), 'PAGE')
footer._p.append(field)
doc.core_properties.title = '乳幼児期におけるデジタルメディアの利用と子どもの発達との関連'
doc.core_properties.subject = '文献研究の準備'
doc.core_properties.author = ''
doc.save(ROOT / 'thesis.docx')
