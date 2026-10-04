"""Generate committed static pages using only the Python standard library."""
from html import escape
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://yeungeqq.github.io/personal_website/"
GITHUB = "https://github.com/yeungeqq"
PROJECTS = json.loads((ROOT / "content/projects.json").read_text())


def e(value):
    return escape(str(value), quote=True)


def tags(project):
    return '<ul class="tags" aria-label="Technologies">' + ''.join(
        f'<li>{e(tag)}</li>' for tag in project['tags']) + '</ul>'


def shell(title, description, body, path=""):
    prefix = "../" if path else "./"
    home = prefix + "index.html"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{e(description)}">
  <meta name="theme-color" content="#f8f7f3">
  <title>{e(title)} | Sam Yeung</title>
  <link rel="canonical" href="{BASE}{e(path)}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(title)} | Sam Yeung">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{BASE}{e(path)}">
  <meta property="og:site_name" content="Sam Yeung — Portfolio">
  <meta name="twitter:card" content="summary">
  <link rel="icon" href="{prefix}assets/images/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{prefix}assets/css/styles.css">
  <script src="{prefix}assets/js/main.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="{home}" aria-label="Sam Yeung, home"><span class="monogram" aria-hidden="true">YK</span>Sam Yeung</a>
      <button class="menu-toggle" type="button" data-menu-toggle aria-expanded="false" aria-controls="site-navigation" hidden>Menu</button>
      <nav class="site-nav" id="site-navigation" aria-label="Main navigation">
        <a href="{home}#projects">Projects</a><a href="{home}#about">About</a><a href="{home}#contact">Contact</a>
        <a class="nav-github" href="{GITHUB}">GitHub <span aria-hidden="true">↗</span></a>
      </nav>
    </div>
  </header>
  <main id="main">{body}</main>
  <footer class="site-footer"><div class="wrap footer-inner"><span>Sam Yeung · Selected projects</span><span>Made with curiosity. Built for the web.</span><a href="{GITHUB}">GitHub ↗</a></div></footer>
</body>
</html>
'''


def diagram(project):
    blocks = []
    for index, step in enumerate(project['steps']):
        y = 100 + index * 69
        blocks.append(f'''<rect x="54" y="{y}" width="372" height="53" rx="10" fill="white" stroke="{project['color']}" stroke-opacity=".18"/>
<circle cx="82" cy="{y + 26}" r="13" fill="{project['background']}"/>
<text x="82" y="{y + 30}" text-anchor="middle" font-size="11" fill="{project['color']}">{index + 1}</text>
<text x="108" y="{y + 31}" font-size="16" fill="#202823">{e(step)}</text>''')
        if index < 2:
            blocks.append(f'<path d="M240 {y + 54}v14m-4-4 4 4 4-4" fill="none" stroke="{project["color"]}"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 340" role="img" aria-labelledby="title desc">
<title id="title">{e(project['name'])} conceptual workflow</title>
<desc id="desc">{e(' → '.join(project['steps']))}. An illustrative diagram, not an application screenshot.</desc>
<rect width="480" height="340" fill="{project['background']}"/>
<circle cx="435" cy="50" r="105" fill="none" stroke="{project['color']}" stroke-opacity=".12"/>
<circle cx="435" cy="50" r="75" fill="none" stroke="{project['color']}" stroke-opacity=".12"/>
<g font-family="Arial, sans-serif"><text x="54" y="40" font-size="10" letter-spacing="2" fill="{project['color']}">CONCEPTUAL WORKFLOW</text>
<text x="54" y="72" font-size="22" font-weight="600" fill="#202823">{e(project['name'])}</text>
{''.join(blocks)}</g></svg>'''


def homepage():
    featured = ''.join(f'''<article class="featured-card">
      <div class="project-visual"><img src="./assets/images/{p['slug']}.svg" alt="Conceptual workflow: {e(' → '.join(p['steps']))}" width="480" height="340" loading="lazy"></div>
      <div class="featured-body"><span class="category-label">{e(p['label'])}</span><h3>{e(p['name'])}</h3><p>{e(p['summary'])}</p>{tags(p)}<a class="text-link" href="./projects/{p['slug']}.html">Explore {e(p['name'])} <span aria-hidden="true">↗</span></a></div>
    </article>''' for p in PROJECTS if p.get('featured'))
    cards = ''.join(f'''<article class="project-card" data-project-card data-category="{p['category']}">
      <div class="card-top"><div><div class="category-label">{e(p['label'])}</div><h3><a href="./projects/{p['slug']}.html">{e(p['name'])}</a></h3></div><span class="project-number" aria-hidden="true">{i:02d}</span></div>
      <p>{e(p['summary'])}</p>{tags(p)}</article>''' for i, p in enumerate(PROJECTS, 1))
    body = f'''
    <div class="wrap">
      <section class="hero" aria-labelledby="intro-title">
        <div class="hero-copy"><div class="eyebrow">Full-stack engineering &amp; applied AI</div>
          <h1 id="intro-title">Ideas into<br>useful <em>software.</em></h1>
          <p>I'm Sam Yeung. This is a collection of my work exploring thoughtful applications, machine learning, and intelligent game agents.</p>
          <div class="actions"><a class="button primary" href="#projects">Explore projects <span aria-hidden="true">↓</span></a><a class="button" href="{GITHUB}">View GitHub <span aria-hidden="true">↗</span></a></div>
        </div>
        <div class="hero-art" aria-hidden="true"><div class="art-label">A FEW THINGS I LIKE BUILDING</div><div class="orbit"></div><div class="orbit second"></div>
          <div class="art-block"><span class="art-symbol">&lt;/&gt;</span><div><b>Useful applications</b><small>From interface to database</small></div></div>
          <div class="art-block"><span class="art-symbol">✳</span><div><b>Applied intelligence</b><small>From data to an interaction</small></div></div>
          <div class="art-block"><span class="art-symbol">↗</span><div><b>Better decisions</b><small>From search to strategy</small></div></div>
        </div>
      </section>
      <div class="intro-strip"><span>{len(PROJECTS):02d} selected projects</span><span>Applications / Machine learning / Game AI</span><span>Explore public source on GitHub ↗</span></div>
      <section class="section" aria-labelledby="featured-title"><div class="section-heading"><div><div class="eyebrow">A closer look</div><h2 id="featured-title">Featured work</h2></div><p>Three projects connecting technical ideas with everyday workflows.</p></div><div class="featured-grid">{featured}</div></section>
      <section class="section all-projects" id="projects" aria-labelledby="projects-title"><div class="section-heading"><div><div class="eyebrow">The collection</div><h2 id="projects-title">Selected projects</h2></div><p>From document copilots to game-playing agents. Each project explores a different problem.</p></div>
        <div class="filter-bar"><div class="filters" data-filters role="group" aria-label="Filter projects by category" hidden>
          <button type="button" data-category="all" aria-pressed="true">All projects</button><button type="button" data-category="full-stack" aria-pressed="false">Full-stack</button><button type="button" data-category="machine-learning" aria-pressed="false">Machine learning</button><button type="button" data-category="game-ai" aria-pressed="false">Game AI</button>
        </div><p class="filter-status" data-filter-status role="status" aria-live="polite" aria-atomic="true">{len(PROJECTS)} projects · All projects</p></div><div class="project-grid">{cards}</div>
      </section>
      <section class="section about" id="about" aria-labelledby="about-title"><div><div class="eyebrow">Behind the projects</div><h2 id="about-title">Curiosity, translated<br>into code.</h2></div><div class="about-copy"><p>My projects span full-stack applications, computer-vision experiments, and search-based game agents. This portfolio brings that work together, with a closer look at the problem, technical approach, and limitations of each project.</p><div class="skills"><div><h3>Application development</h3><p>React · TypeScript<br>Express · Spring Boot<br>PostgreSQL</p></div><div><h3>Applied machine learning</h3><p>Python · PyTorch<br>Computer vision<br>Retrieval-augmented generation</p></div><div><h3>Algorithms &amp; experiments</h3><p>Tree search · Minimax<br>Heuristic design<br>Model comparison</p></div></div></div></section>
      <section class="contact" id="contact" aria-labelledby="contact-title"><div><div class="eyebrow">Keep exploring</div><h2 id="contact-title">Let's connect.</h2><p>Find my public work and project repositories on GitHub.</p></div><a class="button primary" href="{GITHUB}">Find me on GitHub <span aria-hidden="true">↗</span></a></section>
    </div>'''
    return shell('Full-stack engineering & applied AI', 'Explore Sam Yeung’s portfolio of full-stack applications, applied machine learning, and intelligent game agents.', body)


def detail(project, next_project):
    repository = ''
    if project.get('repo'):
        repo_url = GITHUB + '/' + project['repo']
        repository = f'<h2>Explore the project</h2><p>Source code, documentation, and setup instructions are available in the repository.</p><div class="actions"><a class="button primary" href="{e(repo_url)}">View repository ↗</a></div>'
    contribution = ''
    if project.get('contribution'):
        contribution = f'<h2>My contribution</h2><p>{e(project["contribution"])}</p>'
    related = ''
    if project.get('relatedRepo'):
        related = f'<a class="text-link" href="{GITHUB}/{project["relatedRepo"]}">Single-player search source ↗</a>'
    features = ''.join(f'<li>{e(feature)}</li>' for feature in project['features'])
    body = f'''<div class="wrap">
      <section class="detail-hero"><a class="back-link" href="../index.html#projects">← Back to all projects</a><div class="eyebrow">{e(project['label'])}</div><h1>{e(project['name'])}</h1><p class="detail-lead">{e(project['summary'])}</p>{tags(project)}</section>
      <div class="detail-layout"><article class="prose" aria-label="Project overview">
        <figure class="detail-figure"><img src="../assets/images/{project['slug']}.svg" alt="Conceptual workflow: {e(' → '.join(project['steps']))}" width="480" height="340"><figcaption>Illustrative workflow — not an application screenshot or measured result.</figcaption></figure>
        <h2>The idea</h2><p>{e(project['overview'])}</p>{contribution}<h2>Project scope</h2><ul>{features}</ul><h2>Technical approach</h2><p>{e(project['approach'])}</p><h2>Scope &amp; limitations</h2><p>{e(project['limits'])}</p>
      </article><aside class="project-aside">{repository}{related}<h2>Technology</h2>{tags(project)}<div class="note">This page summarizes documented project work. It does not claim independently reproduced benchmarks, production deployment, or sole authorship.</div></aside></div>
      <nav class="next-project" aria-label="More projects"><a class="text-link" href="../index.html#projects">← All projects</a><a class="text-link" href="./{next_project['slug']}.html">Next: {e(next_project['name'])} →</a></nav>
    </div>'''
    return shell(project['name'], project['summary'], body, f"projects/{project['slug']}.html")


def build():
    (ROOT / 'projects').mkdir(exist_ok=True)
    (ROOT / 'assets/images').mkdir(parents=True, exist_ok=True)
    (ROOT / 'index.html').write_text(homepage(), encoding='utf-8')
    for index, project in enumerate(PROJECTS):
        (ROOT / 'assets/images' / (project['slug'] + '.svg')).write_text(diagram(project), encoding='utf-8')
        (ROOT / 'projects' / (project['slug'] + '.html')).write_text(detail(project, PROJECTS[(index + 1) % len(PROJECTS)]), encoding='utf-8')
    urls = [BASE] + [BASE + 'projects/' + p['slug'] + '.html' for p in PROJECTS]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{e(url)}</loc></url>\n' for url in urls) + '</urlset>\n'
    (ROOT / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
    print(f'Generated homepage, {len(PROJECTS)} project pages, diagrams, and sitemap.')


if __name__ == '__main__':
    build()
