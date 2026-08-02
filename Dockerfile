# ---- Stage 1: Build the Hugo static site ----
# Must be a glibc base (Debian/Ubuntu): the Hugo extended binary is glibc +
# libstdc++-linked, which musl-based Alpine cannot satisfy.
FROM debian:bookworm-slim AS build

# Hugo extended (with Sass/SCSS support) is a static binary released on GitHub.
ARG HUGO_VERSION=0.131.0
# Optional per-app override of the site's baseURL (defaults to hugo.toml value).
ARG BASEURL=""

# ca-certificates for TLS; libstdc++6/libgcc-s1 provide the C++ runtime the
# Hugo extended binary needs at runtime.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates wget tar libstdc++6 libgcc-s1 \
    && rm -rf /var/lib/apt/lists/*

# Download the official Hugo extended release for the pinned version.
RUN wget -q "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz" \
    -O /tmp/hugo.tar.gz \
    && tar -xzf /tmp/hugo.tar.gz -C /usr/local/bin hugo \
    && chmod +x /usr/local/bin/hugo \
    && rm /tmp/hugo.tar.gz \
    && hugo version

WORKDIR /site
COPY . .

# Build (override baseURL in Coolify via Build Arguments if deployed under a custom path).
RUN if [ -n "$BASEURL" ]; then hugo --minify --baseURL "$BASEURL"; \
    else hugo --minify; fi

# ---- Stage 2: Serve the built site with nginx (alpine is fine here) ----
FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /site/public /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
