# Multi-stage Dockerfile para Next.js API
FROM node:20-alpine AS base
RUN npm install -g pnpm turbo

FROM base AS builder
WORKDIR /app
COPY . .
RUN pnpm install --frozen-lockfile=false
RUN pnpm --filter api build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/apps/api/.next /app/apps/api/.next
COPY --from=builder /app/apps/api/package.json /app/apps/api/package.json
COPY --from=builder /app/node_modules /app/node_modules
COPY --from=builder /app/packages /app/packages

EXPOSE 8080
CMD ["pnpm", "--filter", "api", "start"]
