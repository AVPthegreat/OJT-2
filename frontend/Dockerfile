# Frontend Dockerfile
# Multi-stage build for development and production

# ============================================
# Base stage
# ============================================
FROM node:20-alpine as base
WORKDIR /app

# ============================================
# Development stage
# ============================================
FROM base as development

# Install dependencies (copy package files first for caching)
COPY package*.json ./
RUN npm install

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"
ENV NODE_ENV=development

CMD ["npm", "run", "dev"]

# ============================================
# Build stage for production
# ============================================
FROM base as builder

COPY package*.json ./
RUN npm ci

COPY . .

# Build the application
RUN npm run build

# ============================================
# Production stage
# ============================================
FROM base as production

ENV NODE_ENV=production

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Copy built files
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
