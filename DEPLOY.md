# Deploying this Hugo documentation site (Coolify — static)

This is the organization's **standard method** for publishing Hugo documentation sites:
serve the built static output directly — no Dockerfile needed.

## Deploy in Coolify
1. Push this repo to GitHub (`carywoods/biobook2`).
2. Coolify → New Resource → application → point at the repo.
3. Build pack: **Static** (Coolify auto-detects Hugo).
4. Output directory: **`public`** (where `hugo` writes the site).
5. Set the domain (e.g. `carywoods.dev/biobook`).
6. Deploy.

Coolify runs the Hugo build itself and serves `public/` with its own server,
wiring the port automatically. No Dockerfile, no nginx, no build args.

## Local preview
```bash
hugo server
```

## Note on baseURL
`hugo.toml` sets `baseURL = "https://carywoods.dev/biobook"`. Hugo renders
root-relative paths (`/biobook/...`), so set the same domain/path in Coolify so
links resolve. If serving at a bare domain, change/baseURL override accordingly.
