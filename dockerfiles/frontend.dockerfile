# FIXME:
#FROM node:22-alpine AS builder
#ENV BACKEND_URL='http://backend:5000'
#
#WORKDIR /app
#
#COPY ./frontend/ ./
#
#RUN npm install
#RUN npm run build
#
#
## stage 2: runner
#FROM node:22-alpine AS runner
#ENV NODE_ENV='production'
#ENV NEXT_TELEMETRY_DISABLED=1
#ENV PORT=3000
#ENV BACKEND_URL='http://backend:5000'
#
#WORKDIR /app
#
#COPY --from=builder /app/.next ./.next
#COPY --from=builder /app/public ./public
#COPY --from=builder /app/package.json ./
#COPY --from=builder /app/node_modules ./node_modules
#
## RUN npm install --omit=dev
#RUN npm prune --production
#
#CMD ["npm", "run", "start", "-- -p $PORT"]