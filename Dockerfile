# ---- Stage 1: Build the Hugo static site ----
FROM alpine:3.20 AS build

# Hugo extended (with Sass/SCSS support) is a static binary released on GitHub.
ARG HUGO_VERSION=0.131.0
# Optional per-app override of the site's baseURL (defaults to hugo.toml value).
ARG BASEURL=""

# ca-certificates for TLS, libc6-compat because the Hugo binary is glibc-linked.
RUN apk add --no-cache ca-certificates libc6-compat wget tar

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

# ---- Stage 2: Serve the built site with nginx ----
FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /site/public /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
