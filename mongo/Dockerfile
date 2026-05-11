FROM mongo:latest
COPY mongo/init.js mongo/docker-entrypoint-initdb.d/
RUN chown -R mongodb:mongodb /docker-entrypoint-initdb.d/
USER mongodb
