# Repo & Site Improvement Tasks

From a review of the repo on 2026-10-06. Each task says what's wrong, where it
is, and what "done" looks like. Priority: **P0** is broken or user-visible now,
**P1** is high value, **P2** is nice to have.

---

## P0 — Broken / inconsistent

- [ ] **Add missing articles to `metadata.json`.**
  `articles/catching-fire.html` and `articles/stop-fixing-tool-syntax.html`
  exist but have no entry, so they never show on the homepage.
  *Done when:* both have entries and appear in the feed.

- [ ] **Fix the homepage stage filter.** `index.html` filters on
  `data-stage="planner"` / `"tool"`, matched against tags, title and hook. Most
  articles have no tag containing `planner` or `tool`, so clicking a stage
  hides relevant reports. The metadata already holds `trace_stages`, but every
  article lists all six, so that field is useless too.
  *Done when:* stage keys match the metadata vocabulary
  (`planning`, `tool_call`, `retrieval`, `execute`, `verify`, `output`), and
  filtering uses a new per-article `root_cause_stage` (plus optional
  `symptom_stage`) field instead of free-text matching.

- [ ] **Normalise the `metadata.json` schema.**
  - `type` vs `format`: 6 entries use `format`. Pick `type`.
  - `research_window` comes in 4 shapes (array, "to", "–", prose). Use
    `["YYYY-MM-DD","YYYY-MM-DD"]`.
  - IDs mix styles (`state-commit-001`, `1847`, `0047`). Choose one scheme,
    e.g. zero-padded sequence.
  - Title casing differs ("context bleed", "the verify gap", "Misdirection in
    the tool"). Use Title Case.
  - Indentation and formatting are inconsistent. Reformat with 2-space JSON.
  *Done when:* every entry matches the schema in `docs/master-prompt-v1.md`.

- [ ] **Fix broken `<title>` tags.** `green-light-lie-eval-failure.html` and
  `phantom-inheritance-subagents-remember.html` are titled "React Artifact".
  `misdirection-in-the-tool.html` is titled "diagnostic · agentic-engineering".
  *Done when:* every title is `<Title> — Agentic Engineering`.

- [ ] **Add back-navigation to the two articles that lack it.**
  `green-light-lie-eval-failure.html` and
  `phantom-inheritance-subagents-remember.html` have no link back to the home
  page.

- [ ] **Shrink the two ~200 KB articles.** `green-light-lie-eval-failure.html`
  (204 KB) and `phantom-inheritance-subagents-remember.html` (202 KB) look like
  exported React artifacts with bundled code. They're 5–10× the size of the
  others. Rebuild them as plain HTML/CSS/JS.

- [ ] **Finish or trim the README.** It stops mid-sentence after "replaces
  guesswork with structure:". It also describes the site as covering
  AGENTS.md, ReAct and SWE benchmarks, which doesn't match what the site
  actually publishes (diagnostic field reports). Rewrite it to state the real
  scope, list the articles (or link to the site), and explain how to add an
  article.

- [ ] **Delete `index.0.html`.** It's the old homepage, still publicly served.
  Remove it, or move it out of the deploy root.

## P1 — Consistency, discoverability, workflow

- [ ] **One shared design system for articles.** Articles currently use at
  least four font stacks (Plex, Inter + JetBrains Mono, Fraunces, system) and
  four or more visual styles. Pull the homepage tokens into
  `assets/site.css` (fonts, colors, header/footer, trace component), link
  them from every article, and re-skin existing articles over time.

- [ ] **SEO and social metadata on every article.** Only 1 of 17 articles has
  any Open Graph tag. Add `description`, OG/Twitter tags, `canonical` and
  TechArticle JSON-LD (spec in the master prompt). Add an `og:image`, either
  one site-wide card or one generated per article.

- [ ] **Add `sitemap.xml`, `robots.txt` and an RSS/Atom feed (`feed.xml`).**
  Generate them from `metadata.json`.

- [ ] **Validation script plus a CI check.** Add `scripts/validate.py`
  (or a Node equivalent), run by a GitHub Action on PRs, that checks:
  - `metadata.json` parses and every entry matches the schema;
  - every `path` exists and every `articles/*.html` has an entry;
  - slugs, ids and coined terms are unique;
  - each article has a title, description, canonical and back link;
  - internal links resolve.

- [ ] **Generator script.** Add `scripts/build.py` to regenerate
  `sitemap.xml`, `feed.xml` and a static `<noscript>` article list in
  `index.html` from `metadata.json`.

- [ ] **Homepage works without JS.** The feed is built entirely from a
  `fetch()` of `metadata.json`, so crawlers and no-JS readers see an empty page.
  Pre-render the card list at build time (see the generator above) and keep
  JS for filtering.

- [ ] **Related reports and series links.** Many articles share concepts
  (verify gap → verify theater → verify amnesia → green-light lie; context
  bleed → phantom inheritance → catching fire). Add a "Related reports" block
  to each article and a glossary page of coined terms.

- [ ] **Glossary page (`glossary.html`).** One-sentence definitions of each
  coined term, each linking to its article. Builds the site's vocabulary and
  internal linking.

- [ ] **Check dates and research windows.** `final-answer-trap` is dated
  2024-04-25 and `never-committed` 2025-04-15, while the rest are 2026.
  Several entries share 2026-02-13. Confirm these are intended. Case numbers
  on the homepage depend on them.

- [ ] **Add an article template.** `docs/article-template.html`: a skeleton
  page with the required sections, meta tags and shared CSS, used together
  with `docs/master-prompt-v1.md`.

- [ ] **`CONTRIBUTING.md` / publishing workflow.** Document the steps: generate
  with the master prompt → save to `articles/` → add the metadata entry → run
  validation → open a PR.

## P2 — UX polish

- [ ] **Accessibility pass on the homepage.**
  - Tags are blurred (`filter:blur(3px)`) until hover, so they're unreadable on
    touch devices and to low-vision readers. Show them by default.
  - The typewriter hook animation re-runs on every render, so screen readers
    hear partial text. Put the full hook in the DOM and animate it visually
    only (`aria-label`, or skip the effect under reduced motion).
  - Check contrast of `--ink-faint` (#565E6C) on `--bg`. It fails WCAG AA
    for body-size text.
- [ ] **Clickable tag pills** that set the filter, and a tag cloud or index.
- [ ] **Sort and group controls** (newest, by stage, by series) and URL state
  for filters (`?stage=verify&q=mcp`) so filtered views can be shared.
- [ ] **Stage filter on mobile.** The pipeline SVG is hidden under 640px, so
  mobile users lose stage filtering. Add a chip row fallback.
- [ ] **Per-article reading progress bar and table of contents** (as in
  `never-committed.html`) on all articles.
- [ ] **Light theme or print stylesheet** so articles can be shared as PDF.
- [ ] **Add a 404 page** (`404.html`) in the site style.
- [ ] **Trim `.gitignore`.** It's the generic Node template. Reduce it to what
  this static site needs.
- [ ] **Analytics (privacy-friendly, optional)** to see which reports land.

## Content roadmap ideas

Gaps in the current coverage, seen from the six-stage pipeline:

- [ ] **planning:** plan drift and over-decomposition (planner creates tasks the
  executor can't verify).
- [ ] **tool_call:** MCP schema versioning and silent tool-description drift.
- [ ] **retrieval:** memory-file rot (stale CLAUDE.md / AGENTS.md as a root cause).
- [ ] **execute:** idempotency and retry storms in long-horizon agents.
- [ ] **output:** handoff-format failures between agent and human reviewer.
- [ ] **Cost:** token-cost blowups as a diagnostic signal.
- [ ] **A pinned "Start here" article** explaining the six-stage diagnostic
  model. The homepage supports `pinned` but no article uses it.
