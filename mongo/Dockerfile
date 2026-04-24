FROM mongo:latest
COPY init.js /docker-entrypoint-initdb.d/
RUN chown -R mongodb:mongodb /docker-entrypoint-initdb.d/
USER mongodb