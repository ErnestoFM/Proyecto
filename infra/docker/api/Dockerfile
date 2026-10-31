# Multi-stage Dockerfile para Next.js API (Monchis Café Backend)
FROM node:20-alpine AS base
RUN apk add --no-cache openssl libc6-compat
RUN npm install -g pnpm turbo

FROM base AS builder
WORKDIR /app
COPY . .
RUN pnpm install --frozen-lockfile=false
RUN pnpm --filter @monchis/database generate
RUN pnpm --filter @monchis/shared-types build
RUN pnpm --filter @monchis/database build
RUN pnpm --filter @monchis/messaging build
RUN pnpm --filter api build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=8080

COPY --from=builder /app/package.json /app/package.json
COPY --from=builder /app/pnpm-workspace.yaml /app/pnpm-workspace.yaml
COPY --from=builder /app/pnpm-lock.yaml /app/pnpm-lock.yaml
COPY --from=builder /app/turbo.json /app/turbo.json
COPY --from=builder /app/apps/api /app/apps/api
COPY --from=builder /app/packages /app/packages
COPY --from=builder /app/node_modules /app/node_modules

EXPOSE 8080
WORKDIR /app/apps/api
CMD ["pnpm", "start", "-p", "8080"]
