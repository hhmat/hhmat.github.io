# Haytham Hussein — Academic & Professional Portfolio

A complete static-first academic website for **Haytham Hussein, AXA Research Fellow at the University of Nottingham**. It presents verified research, professional experience, publications, funding, and scientific engagement for academic, industry, and public audiences and deploys to GitHub Pages through GitHub Actions.

> The biography, career history, projects, publications, grants, awards, and research updates are based on the supplied CV and Google Scholar record. The homepage portrait, project photographs, and gallery use supplied personal images; gallery captions remain neutral where event details were not provided. The CV document is intentionally excluded from the public website and project files.

## Why Astro?

**Astro is the recommended framework for this site.** It prerenders every page to HTML, ships no application runtime by default, supports type-safe content and reusable components, and generates strong SEO fundamentals. Interactive behavior is isolated in small browser scripts rather than hydrating an entire single-page application.

| Option | Fit for this portfolio |
|---|---|
| **Astro — chosen** | Best balance of static performance, multi-page SEO, component-based maintenance, and future content growth. |
| Jekyll | Simple GitHub Pages integration, but an older templating and asset pipeline. |
| Hugo | Extremely fast builds; excellent for large blogs, but Go templates are less approachable for component-oriented front-end work. |
| Next.js static export | Powerful application framework, but more runtime and configuration than this content-led site needs. |
| React / Vite SPA | Good for highly interactive applications; weaker default fit for a multi-page, SEO-first academic portfolio. |

## Features

- Seven main sections: Home, About, Projects, Publications, News & Notes, Gallery, and Contact
- Static project case-study and article pages generated from JSON
- Site-wide keyboard-accessible search (`Ctrl/Cmd + K` or `/`)
- Project, publication, article, and gallery search/filter controls
- APA-style citation copying
- Responsive image gallery with an accessible lightbox
- Persistent light/dark theme with system preference detection
- Responsive navigation and reduced-motion-aware Intersection Observer transitions
- Validated contact form with email delivery, success/error feedback, and a spam honeypot
- Canonical URLs, Open Graph, Twitter Cards, JSON-LD, sitemap, robots.txt, and custom 404
- Locally bundled Newsreader and IBM Plex Sans fonts; no third-party font requests
- Optimised user-supplied portrait and research photographs, remaining original SVG illustrations, and a generated social-sharing image
- Automated GitHub Pages deployment

## Quick start

Requirements: **Node.js 24** and npm.

```bash
npm install
npm run dev
```

Open the local URL printed by Astro. To choose a host and port:

```bash
npm run dev -- --host 0.0.0.0 --port 7100
```

Production checks:

```bash
npm run build
npm run preview -- --host 0.0.0.0 --port 7100
```

`npm run build` runs Astro’s type/content checks and writes the static site to `dist/`.

## Project structure

```text
.
├── .github/workflows/deploy.yml  # GitHub Pages build and deployment
├── docs/mockups/                 # Responsive website previews
├── public/
│   ├── icons/                    # Favicon
│   └── images/                   # Optimised photographs, illustrations, and social image
├── scripts/
│   ├── generate_placeholders.py  # Rebuild original SVG illustrations
│   └── optimise_photos.py        # Crop and optimise supplied photographs
├── source/photos/                # Original supplied portrait and research photographs
├── src/
│   ├── components/               # Header, footer, search, cards, page hero
│   ├── data/                     # All editable portfolio content (JSON)
│   ├── layouts/BaseLayout.astro  # Shared metadata and page shell
│   ├── pages/                    # Static and generated routes
│   ├── scripts/filters.ts        # Reusable search/filter behavior
│   ├── styles/global.css         # Design tokens, layout, and components
│   └── utils/                    # Base paths, dates, and search index
├── tests/                        # Browser verification
├── .env.example                  # Public deployment configuration
├── astro.config.mjs
├── package.json
└── playwright.config.ts
```

## 1. Personalise the profile

Edit `src/data/profile.json`:

- Keep `name`, `role`, and `location` accurate.
- Rewrite `introduction` and `bio` in your own voice.
- Keep personal email addresses out of this public data file; the contact-form recipient is configured separately.
- Maintain full `https://` URLs for LinkedIn, Google Scholar, ORCID, and any other verified professional profiles. Empty values are omitted rather than shown as fake links.

The current homepage portrait is `public/images/haytham-hussein-portrait.webp`. To replace it, add the new original under `source/photos/`, adjust its source filename and crop in `scripts/optimise_photos.py`, then run `python scripts/optimise_photos.py`. Preserve the 800 × 1000 pixel, 4:5 output or update the dimensions and image styling in `src/pages/index.astro`.

## 2. Update content

All repeatable content lives in `src/data/`:

| File | Content |
|---|---|
| `experience.json` | Roles, organisations, dates, locations, and summaries |
| `expertise.json` | Skill groups and capabilities |
| `education.json` | Qualifications and institutions |
| `awards.json` | Awards, grants, fellowships, and honours |
| `projects.json` | Project cards and full case-study content |
| `publications.json` | Publication metadata and citations |
| `news.json` | Articles, categories, tags, and body paragraphs |
| `gallery.json` | Image paths, categories, alt text, and captions |

Set `sample` to `false` after replacing an entry with real work. Use a unique lowercase hyphenated `slug` for every project and article. Project and article detail routes are generated automatically at build time.

### Project entry example

```json
{
  "slug": "my-project",
  "title": "My Project",
  "category": "Research",
  "year": "2026",
  "summary": "A concise summary for cards and search results.",
  "image": "/images/my-project.jpg",
  "technologies": ["Method", "Tool"],
  "featured": true,
  "sample": false,
  "overview": "The question and its context.",
  "approach": "Methods, decisions, and collaboration.",
  "outcome": "Outputs and evidence of value."
}
```

Add new images under `public/images/`. Write meaningful alt text for informative images; decorative project thumbnails intentionally use empty alt text because the adjacent title supplies the link name.

### Publications

Use one of the existing publication types or add a new `type`; filter buttons are generated automatically. Add a real open-access `url` or leave it empty to omit the external link. Keep `citation` complete and consistent.

### News and gallery

Article `body` is an array of paragraphs. Gallery items support Conferences, Events, Research Activities, and Community Engagement by default; new categories also work automatically. Obtain permission for photographs of people and add appropriate credits.

## 3. Local site settings

Copy `.env.example` to `.env` when testing deployment paths locally:

```dotenv
SITE_URL=https://hhmat.github.io
BASE_PATH=/
```

- For a repository named `your-username.github.io`, use `SITE_URL=https://your-username.github.io` and `BASE_PATH=/`.
- For a project repository named `portfolio`, use `SITE_URL=https://your-username.github.io` and `BASE_PATH=/portfolio`.
- For a custom domain, use `SITE_URL=https://www.example.com` and `BASE_PATH=/`.

Internal links and the search index automatically include `BASE_PATH`.

## 4. Deploy to GitHub Pages

1. Create a GitHub repository and push this project to its `main` branch.
2. In **Settings → Pages**, set **Source** to **GitHub Actions**.
3. In **Settings → Secrets and variables → Actions → Variables**, add:
   - `SITE_URL`: your canonical public origin, without a trailing slash.
   - `BASE_PATH`: `/` for a user/organization site or custom domain; `/repository-name` for a project site.
4. Push to `main`, or open **Actions → Deploy to GitHub Pages → Run workflow**.
5. Wait for both build and deploy jobs to succeed. GitHub provides the final Pages URL in the deploy job and **Settings → Pages**.

The workflow uses the official Astro action and deploys only static files. No server, database, environment secret, or backend is required.

## 5. Custom domain and HTTPS

1. In your DNS provider, follow GitHub’s current Pages DNS instructions for an apex domain or `www` subdomain.
2. Add `public/CNAME` containing only your domain, for example `www.example.com`.
3. Set `SITE_URL` to `https://www.example.com` and `BASE_PATH` to `/` in repository variables and local configuration.
4. Deploy, then enter the same custom domain under **Settings → Pages → Custom domain** and save.
5. Wait for DNS checks and certificate provisioning, then enable **Enforce HTTPS**. Certificate issuance can take time after DNS changes propagate.

Keep the `CNAME` file in `public/` so every deployment preserves the domain.

## Contact form behavior

The form validates in the browser, then submits through FormSubmit’s AJAX endpoint for email delivery without displaying a recipient address or opening the visitor’s email application. The first live submission triggers a one-time confirmation email to the recipient; complete that confirmation to activate delivery. FormSubmit processes submissions under its own privacy terms. After activation, replace the email segment of the form action with FormSubmit’s random form string to keep the recipient address out of the public source as well. Browser tests mock the service and cover validation, successful delivery, and failure feedback without sending test messages.

## Routine maintenance

1. Update JSON content and relevant images.
2. Run `npm run build` and `npm run test:ui`.
3. Review desktop and mobile pages, including dark mode.
4. Commit and push to `main`; GitHub Actions deploys automatically.
5. Periodically run `npm outdated` and `npm audit`, then update deliberately and retest.

Do not invent metrics, publication records, qualifications, client names, or outcomes. Accurate, concise entries are more valuable than a large sample archive.

## Browser verification

```bash
npx playwright install chromium  # once, if Chromium is not already installed
npm run test:ui
```

Tests build on the production preview and cover navigation, theme persistence, site search, filters, citation copying, gallery dialog, contact validation, CV removal checks, responsive overflow, console errors, and failed requests. Final home-page desktop and mobile captures are saved to `docs/mockups/`.

## Credits and licenses

See `CREDITS.md` for font, icon, framework, and artwork information.
