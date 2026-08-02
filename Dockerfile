# ---- Stage 1: Build the Hugo static site ----
FROM klakegg/hugo:0.131.0-ext-alpine AS build

# Optional per-app override of the site's baseURL (defaults to hugo.toml value).
# Set in Coolify under Build > Build Arguments if deploying on its own domain/path.
ARG BASEURL=""

WORKDIR /site

# Copy the full project so all themes/assets/content are available.
COPY . .

# Disable Hugo's own telemetry/completion noise in the ~/.config it expects.
RUN if [ -n "$BASEURL" ]; then hugo --minify --baseURL "$BASEURL"; \
    else hugo --minify; fi

# ---- Stage 2: Serve the built site with nginx ----
FROM nginx:1.27-alpine

# Remove default config, drop in ours, and copy build output.
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /site/public /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
