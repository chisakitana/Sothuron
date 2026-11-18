'use strict';
const viewer = document.getElementById('viewer');
let previousFocus;
document.querySelectorAll('[data-page]').forEach(button => button.addEventListener('click', () => {
  const number = button.dataset.page;
  previousFocus = button;
  const image = document.getElementById('viewer-image');
  image.src = `pages/thesis-page-${number}.png`;
  image.alt = `研究準備版 ${number}ページ目の拡大表示`;
  document.getElementById('viewer-label').textContent = `${number} / ${document.querySelectorAll('[data-page]').length} ページ`;
  if (typeof viewer.showModal === 'function') {
    viewer.showModal();
  } else {
    window.open(image.src, '_blank', 'noopener');
  }
}));
document.getElementById('viewer-close').addEventListener('click', () => viewer.close());
viewer.addEventListener('click', event => { if (event.target === viewer) viewer.close(); });
viewer.addEventListener('close', () => previousFocus?.focus());
document.getElementById('text-toggle').addEventListener('click', event => {
  const box = document.getElementById('text-version');
  box.hidden = !box.hidden;
  event.currentTarget.setAttribute('aria-expanded', String(!box.hidden));
  event.currentTarget.textContent = box.hidden ? '文字だけで読む' : '文字表示を閉じる';
});
async function load() {
  try {
    const response = await fetch('data.json');
    if (!response.ok) throw new Error('data load failed');
    const data = await response.json();
    document.getElementById('updated').textContent = data.updated;
    const paragraphs = document.getElementById('paragraphs');
    for (const text of data.paragraphs) {
      const p = document.createElement('p'); p.textContent = text; paragraphs.append(p);
    }
    function render(filter) {
      const list = document.getElementById('reference-list'); list.replaceChildren();
      for (const ref of data.references.filter(r => filter === 'all' || r.kind === filter)) {
        const article = document.createElement('article'); article.className = 'reference';
        const number = document.createElement('span'); number.className = 'ref-number'; number.textContent = String(ref.number).padStart(2, '0');
        const body = document.createElement('div');
        const kind = document.createElement('span'); kind.className = 'ref-kind'; kind.textContent = ref.kind;
        const title = document.createElement('h3'); title.textContent = ref.title;
        const status = document.createElement('p'); status.textContent = `確認状況：${ref.status}`;
        const link = document.createElement('a'); link.href = ref.url; link.target = '_blank'; link.rel = 'noopener noreferrer'; link.textContent = '資料の掲載元へ ↗';
        body.append(kind, title, status, link); article.append(number, body); list.append(article);
      }
    }
    document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
      document.querySelectorAll('[data-filter]').forEach(b => {
        const active = b === button; b.classList.toggle('active', active); b.setAttribute('aria-pressed', String(active));
      });
      render(button.dataset.filter);
    }));
    render('all');
  } catch (error) { document.getElementById('load-error').hidden = false; }
}
load();
