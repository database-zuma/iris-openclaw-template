FROM node:20-alpine

RUN apk add --no-cache python3 py3-pip postgresql-client bash git

# Clone and install (gunakan npm install bukan npm ci)
RUN git clone --depth 1 https://github.com/openclaw/openclaw.git /opt/openclaw && \
    cd /opt/openclaw && \
    npm install --legacy-peer-deps && \
    ln -s /opt/openclaw/openclaw.mjs /usr/local/bin/openclaw

WORKDIR /workspace
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 18790
ENTRYPOINT ["/entrypoint.sh"]
CMD ["openclaw", "gateway", "start"]
