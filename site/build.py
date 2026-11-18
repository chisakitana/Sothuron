"""正本のWord/PDFを変更せず、同じ版の閲覧サイトだけを生成する。"""
from pathlib import Path
import shutil,json,re
from datetime import datetime
from zoneinfo import ZoneInfo
from html import escape
from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table
import fitz
SITE=Path(__file__).resolve().parent
ROOT=SITE.parent
OUT=SITE/'dist';OUT.mkdir(exist_ok=True)
assets=OUT/'files';assets.mkdir(exist_ok=True)
for name in ['thesis.docx','thesis.pdf','REFERENCES.md','WORK_LOG.md','THESIS_REQUIREMENTS.md','LITERATURE_NOTES.md','STYLE_GUIDE.md','RESEARCH_PLAN.md']:
    shutil.copyfile(ROOT/name,assets/name)
pdf=fitz.open(ROOT/'thesis.pdf')
page_count=len(pdf)
previews=OUT/'pages';previews.mkdir(exist_ok=True)
for stale in previews.glob('thesis-page-*.png'):stale.unlink()
links=[];pages=[]
for n,page in enumerate(pdf,1):
    image=ROOT/'previews'/f'thesis-page-{n}.png';assert image.exists(),f'Missing preview: {image}'
    shutil.copyfile(image,previews/image.name)
    text=re.sub(r'\s+','',page.get_text())
    if n==1:label='はじめに・問題と目的'
    elif '親との愛着関係については、Shawcroft' in text:label='問題と目的の続き'
    elif '方法' in text and '調査時期' in text:label='方法'
    elif '総合考察' in text:label='総合考察'
    elif 'おわりに' in text:label='おわりに・文献'
    elif any(doi in text for doi in ['10.1001/jamapediatrics','10.57440/jncm','10.5332/hatsuhatsu']):label='文献'
    elif '表1' in text and '研究者' in text:label='結果と文献整理表'
    else:label='結果の続き'
    pix=fitz.Pixmap(str(image))
    links.append(f'<a href="#page-{n}">{n} {label}</a>')
    loading=' loading="lazy"' if n>1 else ''
    pages.append(f'<article class="page" id="page-{n}"><div class="page-label"><h3><span>{n:02}</span>{label}</h3><button type="button" data-page="{n}">拡大する ↗</button></div><img src="pages/{image.name}" width="{pix.width}" height="{pix.height}"{loading} alt="中間稿 {n}ページ目：{label}"></article>')
refs=[]
source=(ROOT/'REFERENCES.md').read_text()
entries=list(re.finditer(r'(?m)^(\d+)\. (.+)$',source))
for i,m in enumerate(entries):
    chunk=source[m.start():entries[i+1].start() if i+1<len(entries) else len(source)]
    section=list(re.finditer(r'(?m)^## (.+)$',source[:m.start()]))[-1][1]
    kind='公的資料' if section=='公的資料' else '学術文献'
    url=re.search(r'https://[^\s]+',chunk)
    status=re.search(r'- 確認：(.+)',chunk)
    form=re.search(r'- 種別：(.+)',chunk)
    refs.append({'number':int(m[1]),'title':re.sub(r'https://\S+','',m[2]).strip(),'url':url[0] if url else '', 'status':((form[1]+' ' if form else '')+(status[1] if status else '')), 'kind':kind})
assert len(refs)==len({r['number'] for r in refs})
doc=Document(ROOT/'thesis.docx')
paragraphs=[]
for element in doc.element.body:
    if element.tag.endswith('}p'):
        text=Paragraph(element,doc).text
        if text.strip():paragraphs.append(text)
    elif element.tag.endswith('}tbl'):
        table=Table(element,doc)
        for row in table.rows:paragraphs.append(' ｜ '.join(cell.text.replace('\n',' ') for cell in row.cells))
updated=datetime.now(ZoneInfo('Asia/Tokyo')).strftime('%Y.%m.%d')
data={'updated':updated,'references':refs,'paragraphs':paragraphs,'pageCount':page_count}
(OUT/'data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
academic=sum(r['kind']=='学術文献' for r in refs)
html=(SITE/'index.html').read_text()
replacements={'{{PAGE_COUNT}}':str(page_count),'{{PAGE_LINKS}}':''.join(links),'{{PAGES}}':''.join(pages),'{{REF_TOTAL}}':str(len(refs)),'{{ACADEMIC_COUNT}}':str(academic),'{{PUBLIC_COUNT}}':str(len(refs)-academic)}
for key,value in replacements.items():html=html.replace(key,value)
assert '{{' not in html,'Unreplaced template placeholder'
(OUT/'index.html').write_text(html)
for name in ['style.css','app.js']:shutil.copyfile(SITE/name,OUT/name)
print(f'同版の閲覧サイトを生成。PDF{page_count}ページ、学術{academic}・公的{len(refs)-academic}件。原本の変更なし。')
