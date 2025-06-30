# stage 1: builder
FROM node:22-alpine AS builder
ENV INTERNAL_API_URL=http://backend:8000

WORKDIR /app

COPY ../frontend/ ./
RUN rm .env.local || true # prefer current env

RUN npm install
RUN npm run build
RUN npm prune --production

# stage 2: runner
FROM node:22-alpine AS runner
ENV NODE_ENV='production'
ENV NEXT_TELEMETRY_DISABLED=1

WORKDIR /app

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./
COPY --from=builder /app/node_modules ./node_modules

CMD ["npm", "run", "start", "-- -p $PORT"]
