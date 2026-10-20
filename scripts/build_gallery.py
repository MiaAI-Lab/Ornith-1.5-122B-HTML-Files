"""Rebuild index.html from the numbered HTML and accompanying text files."""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parents[1]
HEADINGS = r'TITLE|DESIGN DESCRIPTION|MAJOR VISUAL TECHNIQUES|INTENDED INTERACTION MODEL|RECREATION PROMPT|PROMPT USED|EXACT PROMPT|PROMPT FOR THIS PAGE|PROMPT'

def sections(text):
    matches = list(re.finditer(rf'^({HEADINGS})(?: \(exact[^\n]*\))?:?[ \t]*(?=\n|[^\s])', text, re.M))
    def clean(value):
        return re.sub(r'(?m)^[-=]{3,}[ \t]*$', '', value).strip()
    return {m[1]: clean(text[m.end():matches[i+1].start() if i+1 < len(matches) else len(text)]) for i, m in enumerate(matches)}

def build():
    template = (ROOT / 'scripts/gallery-template.html').read_text()
    cards = []
    for page in sorted(ROOT.glob('[0-9][0-9][0-9]-*.html')):
        text = page.with_suffix('.txt').read_text()
        data = sections(text)
        title = data.get('TITLE') or html.unescape(re.search(r'<title>(.*?)</title>', page.read_text(), re.S | re.I)[1])
        desc = data.get('DESIGN DESCRIPTION', '')
        prompt = next((data[key] for key in ('PROMPT USED', 'EXACT PROMPT', 'PROMPT FOR THIS PAGE', 'PROMPT', 'RECREATION PROMPT') if data.get(key)), text)
        esc = html.escape
        number = page.name[:3]
        cards.append(f'''<article class="card" data-title="{esc(' '.join((number, page.stem, title, desc, prompt)))}">
  <a class="thumb" href="{page.name}" target="_blank" rel="noopener" aria-hidden="true" tabindex="-1"><img src="thumbs/{page.stem}.jpg" alt="{esc(title)} screenshot" width="1440" height="900" loading="lazy" decoding="async"></a>
  <div class="card-top">
    <div class="num">{number}</div>
    <div class="main"><h2 class="title"><a href="{page.name}" target="_blank" rel="noopener">{esc(title)}</a></h2><div class="desc">{esc(desc)}</div></div>
    <div class="actions"><a class="btn btn-open" href="{page.name}" target="_blank" rel="noopener">Open ↗</a><button class="btn btn-prompt" type="button" aria-expanded="false" aria-controls="prompt-{number}">Prompt</button></div>
  </div>
  <div class="prompt-panel" id="prompt-{number}"><div class="prompt-label">Original prompt</div><div class="prompt-text">{esc(prompt)}</div><div class="file-name"><a href="{page.with_suffix('.txt').name}" target="_blank" rel="noopener">{page.with_suffix('.txt').name}</a></div></div>
</article>''')
    assert len(cards) == 100, f'Expected 100 studies, found {len(cards)}'
    (ROOT / 'index.html').write_text(template.replace('<!-- GALLERY_CARDS -->', '\n'.join(cards)))
    print(f'Built gallery with {len(cards)} studies.')

if __name__ == '__main__':
    build()
