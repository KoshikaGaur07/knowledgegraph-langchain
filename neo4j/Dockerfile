FROM neo4j:latest
RUN apt-get update && apt-get install -y bash --no-install-recommends && rm -rf /var/lib/apt/lists/*
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY /init/movies.cypher /import/movies.cypher

# Set the entrypoint for the container
ENTRYPOINT ["/entrypoint.sh"]