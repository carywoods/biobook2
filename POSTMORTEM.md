# Hugo Migration — Post-Mortem (ABANDONED 2026-08-02)

**Decision: giving up on Hugo for the bioinformatics textbook.**
Recorded so this is not re-attempted from scratch.

## Status at abandonment

- Repo: `github.com/carywoods/biobook2`, branch `main`, commit `1d39f9e`
- Local working copy: `/home/cary/bio-hugo`
- The Hugo site itself **worked**. What never worked was Coolify serving it.

### What was actually finished and verified

- All 14 chapters migrated from Quarto `.qmd` to Hugo markdown
- `alex-shpak/hugo-book` theme vendored into `themes/hugo-book/` (not a submodule)
- Builds clean: Hugo extended 0.158.0, 32 pages, **0 warnings**
- Verified from a **fresh clone** of the remote: theme applied (`book-menu`,
  `book-page`), 23 HTML pages, search + syntax highlighting working
- Local `hugo server`: HTTP 200 on every route, all 14 chapters in the sidebar

### Real content bugs that were found and fixed

These were genuine migration defects, worth remembering if the content is reused:

1. **26 Quarto callouts rendering as literal text.** `::: {.callout-tip}` blocks
   appeared verbatim on the page. Converted to GitHub alerts (`> [!TIP]`).
2. **72 Quarto code fences** ` ```{python} ` broke Hugo's Goldmark parser
   ("failed to parse Markdown attributes"). Must become plain ` ```python `.
   Note: ` ```"python" ` is WRONG — it puts literal quotes in the CSS class.
3. **Chapter index page** was inline HTML/CSS with links to `/chapters/...`,
   a path that no longer existed after restructuring.
4. **Stale `type: "chapter"`** front matter on all 14 chapters.
5. **Hardcoded `baseURL`** broke assets whenever the deploy URL differed.
   Fixed with `relativeURLs = true`.

## Why it was abandoned: the deployment, not the site

Coolify never served the site. The failure sequence:

| Attempt | Result | Cause |
|---|---|---|
| Custom Dockerfile w/ `klakegg/hugo` | build fail: image "not found" | image abandoned, frozen at Hugo 0.111.3 (2023) |
| Official Hugo binary on `alpine` | build fail: `libstdc++.so.6` missing, exit 127 | Hugo extended is glibc+libstdc++ linked; will NOT run on musl |
| Debian glibc build stage | build OK | — |
| Coolify **Static** build pack | default nginx page | pack did not produce/serve `public/` |
| Committed prebuilt `public/` | still default nginx page | — |
| Dockerfile + nginx, with guards | **502 Bad Gateway** | Coolify proxy could not reach a healthy container |

### The final state of the blocker

Container logs proved the app was **healthy**: nginx 1.27.5 started, workers
running, custom `default.conf` loaded, zero errors. nginx listening on 80,
`EXPOSE 80` set. So the 502 was **Coolify proxy config**, not the image.

Untested hypothesis (most likely fix if ever revisited): the app's
**Ports Exposes** field in Coolify → Configuration → Network was probably not
set to `80`. `EXPOSE 80` in a Dockerfile does not populate that field, and a
blank or mismatched value produces exactly this 502.

## Honest assessment of what went wrong

- **Over-engineering first.** A static site got a custom multi-stage Dockerfile
  before the simple path was tried. That created a long chain of Docker problems
  unrelated to the actual goal.
- **Unverifiable fixes.** Repeated fixes were proposed for a system (Coolify)
  that could not be inspected from the agent. Each "should work" was a guess.
- **Docker not testable locally.** The user is not in the `docker` group and
  sudo requires a password, so no image was ever smoke-tested before pushing.
- **Version mismatch found late.** hugo-book needs Hugo >= 0.158.0; the box had
  0.131.0. This should have been the first check, not a late discovery.

## If anyone revisits this

1. Verify Coolify's **Ports Exposes = 80** before touching the repo. The repo is
   almost certainly fine.
2. The content in `1d39f9e` is good and reusable regardless of Hugo — the
   markdown chapters are clean and theme-independent.
3. Do not use `klakegg/hugo` (dead) or `hugomods/hugo:exts-*` (no 0.158+ tags).
   Probe any image tag before depending on it.

## Reusable knowledge preserved

Skill `hugo-coolify-deploy` retains the technical specifics: theme version
matching, vendoring, the glibc/musl trap, the Quarto→Hugo cleanup table, and
Dockerfile guards that fail loudly instead of serving a blank page.
