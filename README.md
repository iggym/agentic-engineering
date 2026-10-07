# Agentic Engineering

> Orchestration, context, and tool use for agents built to work, not demo.

[![Live site](https://img.shields.io/badge/Live-iggym.github.io%2Fagentic--engineering-6FD3E8?style=for-the-badge&logo=github)](https://iggym.github.io/agentic-engineering/)
[![validate](https://github.com/iggym/agentic-engineering/actions/workflows/validate.yml/badge.svg)](https://github.com/iggym/agentic-engineering/actions/workflows/validate.yml)

**Agentic Engineering** publishes *diagnostic field reports* for engineers who
build AI agent systems. It is the agent-implementation layer of a wider
portfolio on running AI in production, scoped narrower than
`production-ai-patterns`: orchestration, context isolation, state, tool use,
verification, and the harness that holds an agent together.

## The idea: symptom stage ≠ root-cause stage

Every report walks a real failure through the same six-stage pipeline:

```
planning → tool_call → retrieval → execute → verify → output
```

and makes one argument: **the stage where you noticed the failure is not the
stage where it started.** Each report names the pattern with a short coined
term (*verify gap*, *context bleed*, *retry echo*, …), backs it with sourced
incidents and research, argues the other side, and ends with checks you can run
today.

New here? Start with
[The Six-Stage Autopsy](https://iggym.github.io/agentic-engineering/articles/the-six-stage-autopsy.html).

## Who it's for

| Reader | What you get |
| :--- | :--- |
| Agent architects | Planner/worker patterns, state and checkpointing failures, where orchestration helps and hurts |
| Harness & eval engineers | Verify-stage failures, trajectory evaluation, retries, idempotency, resume semantics |
| Tooling / platform leads | MCP tool contracts, manifest drift, context files (`AGENTS.md`, `CLAUDE.md`) |
| Engineers using coding agents | Why agent PRs and instruction files fail, and what to check first |

## Repository layout

```
index.html            homepage; renders the feed from metadata.json
metadata.json         one entry per article (the source of truth)
articles/             one HTML page per field report
assets/               shared article.css / article.js for new articles
docs/                 master-prompt-v1.md — the prompt used to generate articles
scripts/validate.py   schema, link and consistency checks (runs in CI)
scripts/build.py      regenerates sitemap.xml, feed.xml and the no-JS article list
tasks/                improvement backlog
```

## Adding an article

1. Fill in the inputs block of [`docs/master-prompt-v1.md`](docs/master-prompt-v1.md)
   and run it with a model that has web search.
2. Save the HTML to `articles/<slug>.html` and append the JSON entry to
   `metadata.json`.
3. Check every source link by hand.
4. Run:
   ```sh
   python3 scripts/validate.py
   python3 scripts/build.py
   ```
5. Preview locally with `python3 -m http.server` and open
   <http://localhost:8000>, then open a PR.

## metadata.json schema

| Field | Notes |
| :--- | :--- |
| `id` | 4-digit string, unique |
| `slug`, `path` | `articles/<slug>.html` |
| `title`, `hook` | Title Case title; one-sentence reframe |
| `date` | `YYYY-MM-DD` |
| `status` | `published` to show on the homepage |
| `type` | `diagnostic` or `guide` |
| `tags` | 3–5 lowercase kebab-case tags |
| `reading_time_minutes`, `pinned` | `pinned: true` shows as the entry point |
| `research_window` | `["YYYY-MM-DD", "YYYY-MM-DD"]` |
| `coined_term` | lowercase, unique |
| `root_cause_stage`, `symptom_stage` | one of the six stages; drives the homepage filter |

## License

See [LICENSE](LICENSE).
