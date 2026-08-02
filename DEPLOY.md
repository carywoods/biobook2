# Deploying this Hugo documentation site (Coolify standard)

This is the organization's **standard method** for publishing documentation sites:
a multi-stage Dockerfile builds the static Hugo output, and nginx serves it.
Deploy via Coolify (no manual server steps).

## Files
- `Dockerfile` — Stage 1 builds with `klakegg/hugo:0.131.0-ext-alpine`, Stage 2 serves with `nginx:1.27-alpine`. Runs `hugo --minify`.
- `nginx.conf` — static-file serving with cache headers and pretty URLs (`/foo/` → `/foo/index.html`).
- `.dockerignore` — keeps build artifacts (`public/`, `resources/`, `.hugo_build.lock`) and staging out of the image.

## Deploy in Coolify
1. Push this repo to GitHub (e.g. `carywoods/biobook-hugo`).
2. Coolify → New Resource → application → point at the repo.
3. Set the port to **80**.
4. If the site should render under a path/domain other than the default in `hugo.toml`
   (default `https://carywoods.dev/biobook`), add a build argument:
   `BASEURL=https://your.domain/path`.
5. Deploy. Coolify builds the image and routes traffic to nginx on port 80.

## Verify
- `docker build -t biobook .` builds without error.
- `hugo --minify` locally produces a clean `public/` before pushing.
