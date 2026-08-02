# ---- Stage 1: Build the Hugo static site ----
# Debian (glibc) base is required: the Hugo extended binary is glibc +
# libstdc++-linked and will NOT run on musl/Alpine.
FROM debian:bookworm-slim AS build

# hugo-book theme requires Hugo >= 0.158.0
ARG HUGO_VERSION=0.158.0

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates wget libstdc++6 libgcc-s1 \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO /tmp/hugo.tar.gz \
      "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz" \
    && tar -xzf /tmp/hugo.tar.gz -C /usr/local/bin hugo \
    && rm /tmp/hugo.tar.gz \
    && hugo version

WORKDIR /src
COPY . .

# Fail early and loudly if the vendored theme is missing from the build context
# (a .dockerignore/.gitignore mistake would otherwise produce an unstyled site).
RUN test -f themes/hugo-book/theme.toml \
    || (echo "ERROR: themes/hugo-book missing from build context" && exit 1)

# relativeURLs=true in hugo.toml makes output portable across any domain/path,
# so no baseURL argument is needed at build time.
RUN hugo --minify --gc

# Guarantee the build actually produced pages; never ship an empty site.
RUN test -f public/index.html \
    && test -f public/docs/index.html \
    && echo "Built $(find public -name '*.html' | wc -l) HTML pages"

# ---- Stage 2: Serve the built site with nginx ----
FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

# Remove nginx's stock welcome page so it can never be served by mistake.
RUN rm -rf /usr/share/nginx/html/*

COPY --from=build /src/public /usr/share/nginx/html

# Sanity check inside the final image.
RUN test -f /usr/share/nginx/html/index.html \
    && ! grep -qi "Welcome to nginx" /usr/share/nginx/html/index.html \
    && echo "Site content verified in image"

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
