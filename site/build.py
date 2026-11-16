"""Word/PDFを変更せず、閲覧サイトの配布ファイルだけを更新する。"""
from pathlib import Path
import shutil
import json
import re
from datetime import datetime
from zoneinfo import ZoneInfo
from html import escape
from docx import Document

SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
OUT = SITE / 'dist'
OUT.mkdir(exist_ok=True)
assets = OUT / 'files'
assets.mkdir(exist_ok=True)
for name in ['thesis.docx', 'thesis.pdf', 'REFERENCES.md', 'WORK_LOG.md']:
    shutil.copyfile(ROOT / name, assets / name)
previews = OUT / 'pages'
previews.mkdir(exist_ok=True)
for image in sorted((ROOT / 'previews').glob('thesis-page-*.png')):
    shutil.copyfile(image, previews / image.name)
refs = []
for chunk in re.split(r'\n(?=\d+\. )', (ROOT / 'REFERENCES.md').read_text()):
    m = re.match(r'(\d+)\. (.+)', chunk)
    if not m:
        continue
    url = re.search(r'https://[^\s]+', chunk)
    status = re.search(r'- 確認：(.+)', chunk)
    title = re.sub(r'https://\S+', '', m[2]).strip()
    refs.append({'number': int(m[1]), 'title': title, 'url': url[0] if url else '', 'status': status[1] if status else '', 'kind': '学術文献' if int(m[1]) <= 6 else '公的資料'})
assert len(refs) == 8
paragraphs = [p.text for p in Document(ROOT / 'thesis.docx').paragraphs if p.text.strip()]
updated = datetime.now(ZoneInfo('Asia/Tokyo')).strftime('%Y.%m.%d')
data = {'updated': updated, 'references': refs, 'paragraphs': paragraphs}
(OUT / 'data.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))
for name in ['index.html', 'style.css', 'app.js']:
    shutil.copyfile(SITE / name, OUT / name)
print('閲覧サイトを生成。原本Word・PDFの変更なし。参考文献8件。')
