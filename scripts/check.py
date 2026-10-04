"""Validate generated content and local references without third-party packages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = set()
        self.refs = []
        self.h1 = 0
        self.cards = 0
        self.categories = {}
        self.description = False
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate ID: {self.path}: {attrs["id"]}'
            self.ids.add(attrs['id'])
        self.h1 += tag == 'h1'
        self.cards += 'data-project-card' in attrs
        if 'data-project-card' in attrs:
            category = attrs.get('data-category')
            self.categories[category] = self.categories.get(category, 0) + 1
        if tag == 'meta' and attrs.get('name') == 'description':
            self.description = bool(attrs.get('content'))
        if tag == 'img':
            assert attrs.get('alt'), f'Missing image alt: {self.path}'
            assert attrs.get('width') and attrs.get('height'), f'Missing image dimensions: {self.path}'
        for attr in ('src', 'href'):
            if attrs.get(attr):
                self.refs.append(attrs[attr])


def check():
    pages = {p.resolve(): Page(p) for p in [ROOT / 'index.html', *sorted((ROOT / 'projects').glob('*.html'))]}
    projects = json.loads((ROOT / 'content/projects.json').read_text())
    assert len(pages) == len(projects) + 1, 'Expected homepage and one detail page per project'
    assert len(projects) == len({p['slug'] for p in projects}), 'Duplicate project slugs'
    home = pages[(ROOT / 'index.html').resolve()]
    assert home.cards == len(projects)
    categories = {c: sum(p['category'] == c for p in projects) for c in ('full-stack', 'machine-learning', 'game-ai')}
    assert home.categories == categories, 'Project filter categories do not match content'
    for project in projects:
        page = pages[(ROOT / 'projects' / (project['slug'] + '.html')).resolve()]
        if not project.get('repo'):
            text = page.path.read_text()
            assert 'View repository' not in text
            assert 'available in the repository' not in text
            assert not project.get('relatedRepo'), 'Description-only projects must omit repository links'
            assert all(not ref.startswith('https://github.com/') or ref.rstrip('/') == 'https://github.com/yeungeqq' for ref in page.refs), 'Unexpected repository link on description-only page'
        if project.get('contribution'):
            assert '<h2>My contribution</h2>' in page.path.read_text()
    for path, page in pages.items():
        assert page.h1 == 1, f'Expected one h1: {path}'
        assert page.description, f'Missing meta description: {path}'
        text = path.read_text().lower()
        assert not any(word in text for word in ('callzilla', 'study50', 'lorem ipsum', 'todo:'))
        for ref in page.refs:
            parts = urlsplit(ref)
            if parts.scheme or parts.netloc:
                assert parts.scheme == 'https', f'Unexpected external URL: {ref}'
                continue
            assert not parts.path.startswith('/'), f'Root-relative asset breaks project hosting: {ref}'
            target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
            assert target.is_relative_to(ROOT), f'Reference outside site: {ref}'
            assert target.is_file(), f'Missing target: {path}: {ref}'
            if parts.fragment and target in pages:
                assert parts.fragment in pages[target].ids, f'Missing fragment: {path}: {ref}'
    for path in (ROOT / 'assets/images').glob('*.svg'):
        ET.parse(path)
    ET.parse(ROOT / 'sitemap.xml')
    assert (ROOT / '.nojekyll').exists()
    print(f'PASS: {len(pages)} pages; {len(projects)} projects; category counts; description-only pages; contribution sections; links and anchors; metadata; image accessibility; SVG/XML; excluded content.')


if __name__ == '__main__':
    check()
