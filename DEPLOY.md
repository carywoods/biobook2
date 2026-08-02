# Deploying to Coolify

## Recommended: Dockerfile build pack

The repo ships a `Dockerfile` that builds the site and serves it with nginx.

In Coolify:

1. **New Resource → Application**, point at `github.com/carywoods/biobook2`
2. **Build Pack: `Dockerfile`**
3. **Port: `80`**
4. Set your domain
5. Deploy

No build arguments needed. `relativeURLs = true` in `hugo.toml` makes the output
work at whatever URL Coolify serves it from.

### Why a Dockerfile and not the Static build pack

The Static pack must detect and run Hugo itself, and it has to be the
**extended** build at **>= 0.158.0** for the hugo-book theme. Pinning the exact
Hugo version in the Dockerfile removes that uncertainty.

## Troubleshooting

**Seeing the default nginx welcome page?**
That means nginx is serving an empty webroot. The Dockerfile now guards against
this: it fails the build if `public/index.html` is missing, and deletes nginx's
stock page. If you still see it:
- Confirm Coolify used the **Dockerfile** build pack (not Static/Nixpacks)
- Confirm the deployed commit is the one you expect
- Check the build log for the line `Built N HTML pages`

**Unstyled page (text only, no sidebar)?**
The theme did not reach the build. Confirm `themes/hugo-book/` is present in the
repo (it is vendored, not a submodule). The Dockerfile fails early if it is missing.

**Build fails on the Hugo binary with `libstdc++.so.6 not found`?**
The build stage must be a glibc base (Debian). Hugo extended will not run on
musl/Alpine. The provided Dockerfile already uses `debian:bookworm-slim`.

## Local verification before deploying

```bash
hugo --minify --gc
test -f public/index.html && echo OK
```
