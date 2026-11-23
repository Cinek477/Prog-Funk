"""Build the offline HTML handbook from the repository's Markdown notes."""
from html import escape
from pathlib import Path
import re
import os

root = Path(__file__).resolve().parents[1]
notes = root / 'Notatki'
material = notes / 'materialy'
catalog = [
    ('w1', 'Podstawy Haskella', 'Czyste funkcje, składnia, typy i pierwsze kroki w GHCi.'),
    ('w2', 'Listy i rekurencja', 'Aplikacja częściowa, leniwość, praca z listami i akumulatory.'),
    ('w3', 'Funkcje wyższego rzędu', 'Lambdy, map, filter, foldy i przetwarzanie kolekcji.'),
    ('w4', 'Typy algebraiczne', 'Konstruktory, Maybe, drzewa, klasy typów i moduły.'),
    ('uzupelnienia', 'Materiały uzupełniające', 'Narzędzia Haskella i dodatkowe przykłady pracy z listami.'),
]
groups = {}
targets = {notes / 'README.md': material / 'index.html'}
titles = {}
for folder, _, _ in catalog:
    docs = sorted((notes / folder).glob('*.md'))
    docs.sort(key=lambda p: p.name != 'README.md')
    groups[folder] = docs
    for source in docs:
        targets[source] = material / folder / source.with_suffix('.html').name
        titles[source] = source.read_text(encoding='utf-8-sig').splitlines()[0].removeprefix('# ')

def href(origin, target):
    return escape(os.path.relpath(target, origin.parent).replace(os.sep, '/'), quote=True)

def link(origin, target, label, attrs=''):
    return f'<a href="{href(origin, target)}"{attrs}>{escape(label)}</a>'

def shell(out, title, body, active):
    nav = ' '.join(
        link(out, target, label, ' aria-current="page"' if active == label else '')
        for target, label in [(material / 'index.html', 'Materiały'), (notes / 'quizy' / 'index.html', 'Quizy')]
    )
    logo = href(out, notes / 'logo.svg')
    return f'''<!doctype html>
<html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · Haskell</title>
<link rel="icon" type="image/svg+xml" href="{logo}">
<link rel="stylesheet" href="{href(out, notes / 'study.css')}">
<script src="{href(out, notes / 'theme.js')}" defer></script></head>
<body><header class="mast"><div class="mast-inner">
<a href="{href(out, root / 'index.html')}" class="brand"><img src="{logo}" width="38" height="38" alt="">Haskell / Kurs</a>
<nav class="site-nav" aria-label="Nawigacja główna">{nav}
<button id="theme" type="button" hidden></button></nav>
</div></header><main class="page">{body}</main></body></html>
'''

def inline(raw, source, out):
    pattern = r'(`[^`]+\x60|\[[^\]\n]+\]\([^)\n]+\)|\*\*[^*]+\*\*|\*[^*\n]+\*)'
    parts = re.split(pattern, raw)
    for i, part in enumerate(parts):
        if i % 2 == 0:
            parts[i] = escape(part.replace(r'\|', '|'))
        elif part.startswith('`'):
            parts[i] = f'<code>{escape(part[1:-1].replace(chr(92)+"|","|"))}</code>'
        elif part.startswith('['):
            name, url = part[1:-1].rsplit('](', 1)
            path, suffix, fragment = url.partition('#')
            name = inline(name, source, out)
            if re.match(r'^https?://', url):
                dst = escape(url, quote=True)
            else:
                target = (source.parent / path.split('?', 1)[0]).resolve() if path else source
                if target not in targets and not target.is_file():
                    # Preserve the label when an old reference has no local target.
                    parts[i] = name
                    continue
                dst = href(out, targets.get(target, target))
                if '?' in path:
                    dst += '?' + escape(path.split('?', 1)[1], quote=True)
                if suffix:
                    dst += '#' + escape(fragment, quote=True)
            parts[i] = f'<a href="{dst}">{name}</a>'
        else:
            n = 2 if part.startswith('**') else 1
            tag = 'strong' if n == 2 else 'em'
            parts[i] = f'<{tag}>{inline(part[n:-n],source,out)}</{tag}>'
    return ''.join(parts)

def render(source, out):
    lines = source.read_text(encoding='utf-8-sig').splitlines()[1:]
    result, paragraph = [], []
    solution = False
    def flush():
        if paragraph:
            result.append('<p>' + inline(' '.join(paragraph), source, out) + '</p>')
            paragraph.clear()
    def cells(line):
        return re.split(r'(?<!\\)\|', line.strip().strip('|'))
    i = 0
    while i < len(lines):
        line = lines[i]
        heading = re.match(r'^(#{1,6}) (.*)$', line)
        item = re.match(r'^\s*([-*]|\d+\.) (.*)$', line)
        if not line.strip():
            flush()
        elif line.startswith('```'):
            flush()
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i])
                i += 1
            result.append('<pre><code>' + escape('\n'.join(code)) + '</code></pre>')
        elif heading:
            flush()
            title = heading[2]
            depth = max(2, len(heading[1]))
            if depth == 2 and solution:
                result.append('</details>')
                solution = False
            if depth == 2 and re.match(r'^(Rozwiązania|Odpowiedzi)\b', title):
                result.append('<details><summary>' + inline(title, source, out) + '</summary>')
                solution = True
            else:
                result.append(f'<h{depth}>{inline(title,source,out)}</h{depth}>')
        elif line.strip() == '---':
            flush()
            result.append('<hr>')
        elif line.startswith('|') and i + 1 < len(lines) and re.match(r'^\|\s*[:\-]', lines[i+1]):
            flush()
            result.append('<div class="table-wrap"><table><thead><tr>' + ''.join(
                '<th scope="col">' + inline(c.strip(),source,out) + '</th>' for c in cells(line)
            ) + '</tr></thead><tbody>')
            i += 2
            while i < len(lines) and lines[i].startswith('|'):
                result.append('<tr>' + ''.join('<td>' + inline(c.strip(),source,out) + '</td>' for c in cells(lines[i])) + '</tr>')
                i += 1
            result.append('</tbody></table></div>')
            continue
        elif item:
            flush()
            ordered = item[1].endswith('.')
            tag = 'ol' if ordered else 'ul'
            start = f' start="{int(item[1][:-1])}"' if ordered else ''
            result.append(f'<{tag}{start}>')
            while item and item[1].endswith('.') == ordered:
                result.append('<li>' + inline(item[2],source,out) + '</li>')
                i += 1
                item = re.match(r'^\s*([-*]|\d+\.) (.*)$', lines[i]) if i < len(lines) else None
            result.append(f'</{tag}>')
            continue
        else:
            paragraph.append(line.strip())
        i += 1
    flush()
    if solution:
        result.append('</details>')
    return '\n'.join(result)

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8', newline='\n')

def chapter_list(out, folder, current=None):
    result = []
    for source in groups[folder]:
        label = 'Wprowadzenie' if source.name == 'README.md' else re.sub(r'^\d+\.\s*', '', titles[source])
        result.append('<li>' + link(out, targets[source], label, ' aria-current="page"' if source == current else '') + '</li>')
    return '<ul class="chapters">' + ''.join(result) + '</ul>'

def quiz_link(out, folder):
    base = href(out, notes / 'quizy' / 'index.html')
    number = folder[1:]
    return f'<a href="{base}?wyklad={number}">Quiz z wykładu {number}</a>' if folder.startswith('w') else ''

def overview(out, home):
    intro = ('<section class="cover"><div><p class="eyebrow">Programowanie funkcyjne</p>'
             '<h1>Haskell od podstaw</h1><p class="lead">Przeczytaj rozdział, prześledź kod i sprawdź się na pytaniach z tego samego wykładu.</p>'
             f'<div class="links"><a class="action" href="{href(out, targets[groups["w1"][0]])}">Zacznij od wykładu 1</a>'
             f'{link(out, notes / "quizy" / "index.html", "Przejdź do quizów")}</div></div>'
             '<aside class="cover-note"><h2>Jak się uczyć?</h2><p>Spróbuj przewidzieć wynik, zanim uruchomisz przykład w GHCi. W rozdziałach z ćwiczeniami odsłoń rozwiązania dopiero po własnej próbie.</p></aside></section>'
             if home else '<h1>Materiały do nauki</h1><p class="lead">Pełne rozdziały, przykłady i ćwiczenia do wykładów 1–4.</p>')
    rows = []
    for folder, title, desc in catalog:
        label = f'Wykład {folder[1:]}' if folder.startswith('w') else 'Dodatki'
        rows.append(f'<section class="lecture" id="{folder}"><div><p class="eyebrow">{label}</p><h2>{title}</h2><p>{desc}</p>{quiz_link(out,folder)}</div>{chapter_list(out,folder)}</section>')
    write(out, shell(out, 'Kurs' if home else 'Materiały', intro + '<div class="catalog">' + ''.join(rows) + '</div>', '' if home else 'Materiały'))

overview(root / 'index.html', True)
overview(material / 'index.html', False)
for folder, title, _ in catalog:
    for i, source in enumerate(groups[folder]):
        out = targets[source]
        docs = groups[folder]
        side = link(out, material / 'index.html', 'Spis wszystkich wykładów') + f'<h2>{escape(title)}</h2>' + chapter_list(out,folder,source)
        nav = [quiz_link(out, folder)]
        if i > 0:
            nav.insert(0, link(out, targets[docs[i-1]], 'Poprzedni rozdział'))
        if i+1 < len(docs):
            nav.append(link(out, targets[docs[i+1]], 'Następny rozdział'))
        context = f'Wykład {folder[1:]} · {title}' if folder.startswith('w') else title
        body = f'<div class="reader"><nav class="book-nav" aria-label="Rozdziały">{side}</nav><article class="paper"><p class="eyebrow">{escape(context)}</p><h1>{escape(titles[source])}</h1>{render(source,out)}<footer class="links paper-foot">{" ".join(nav)}</footer></article></div>'
        write(out, shell(out, titles[source], body, 'Materiały'))
print(f'Generated {sum(map(len,groups.values()))} chapters and 2 indexes.')
