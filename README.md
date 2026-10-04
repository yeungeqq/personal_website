# Yee Kiu Yeung — Personal portfolio

A responsive, static portfolio featuring eight selected projects. Built with HTML,
CSS, and vanilla JavaScript. No runtime packages, remote fonts, API keys, or live
GitHub API requests are required.

## Preview locally

From the repository directory:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000` in your browser. Stop the server with Ctrl+C.
The committed HTML works without running a build first.

To test the GitHub Pages subpath locally, start the server from the parent
directory and visit `http://127.0.0.1:8000/personal_website/`.

## Edit project content

- `content/projects.json`: project summaries, technical details, limitations,
  technology tags, categories, and repository names.
- `scripts/build.py`: shared HTML templates, homepage introduction and About text,
  canonical deployment URL, and conceptual SVG diagrams.
- `assets/css/styles.css`: layout, colors, responsive design, and motion preferences.
- `assets/js/main.js`: progressive-enhancement navigation and filters.

After changing content or templates:

```sh
python3 scripts/build.py
python3 scripts/check.py
node --check assets/js/main.js
```

Commit the generated `index.html`, `projects/*.html`, `assets/images/*.svg`, and
`sitemap.xml` alongside the source changes. Do not directly edit generated files;
regeneration will replace those edits. The authoring scripts use Python 3.9+ and
the standard library only. Publishing does not need Python or Node.

## Publish on GitHub Pages

1. Commit and push the site to the `main` branch of `yeungeqq/personal_website`.
2. In the repository, open **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select **main** and **/(root)**, then save.
5. Wait for the Pages deployment to finish and visit
   `https://yeungeqq.github.io/personal_website/`.

`.nojekyll` disables Jekyll processing. Relative asset and navigation paths support
the repository subpath, including direct visits to project detail pages. There is
no custom-domain configuration or custom Actions workflow. If the hosting address
changes, update `BASE` in the authoring script and regenerate.

Official setup instructions:
https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Content and presentation

- Eight project entries; the two Tetress repositories share one case study.
- Three featured applications, plus a filterable complete collection.
- All content and links remain available without JavaScript.
- Diagrams are original, labeled conceptual workflows, not product screenshots.
- Project summaries are based on repository documentation and source inspection.
- No unverified benchmarks, deployment outcomes, or sole-authorship claims.
- No email address, résumé, or LinkedIn link is invented; contact points to GitHub.
- AdaptEd is labeled an educational prototype, not a validated diagnostic tool.

Before adding real screenshots, remove personal records and credentials. Confirm
individual team contributions before adding ownership statements. Social metadata
includes titles, descriptions, and canonical URLs; a raster social-preview image
can be added later when an approved personal/project visual is available.

## Validation

The standard-library checker verifies the page count, category counts, local
links and fragments, project-hosting-safe paths, image alternative text and
dimensions, metadata, unique IDs, and SVG/XML syntax. It also checks that excluded
projects and placeholder text do not appear in published pages.

Manual browser review should cover mobile/tablet/desktop layouts, keyboard focus,
the skip link, all filters, menu close behavior, reduced motion, and JavaScript
disabled. These checks are not a full accessibility or security audit.

### Optional automated Chrome checks

The dependency-free browser checker requires Node 22+ and Chrome. Start the local
server on port 8765 from the parent directory, then launch a separate Chrome
profile with `--headless=new --remote-debugging-port=9223` and an isolated
`--user-data-dir`. Keep debugging bound to your local machine.

Run `node scripts/browser-check.mjs` from the repository. The defaults are
`http://127.0.0.1:8765/personal_website/` and `http://127.0.0.1:9223`; override them
with `SITE_URL` and `CHROME_DEBUG_URL` if necessary. The checker visits every
detail page and tests filters, mobile navigation, keyboard focus, reduced motion,
no-JavaScript behavior, missing assets, and horizontal overflow. Screenshots are
saved under the ignored `.local/` directory. Stop the isolated Chrome process and
preview server when finished.