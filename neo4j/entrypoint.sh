#!/bin/bash
set -eu


NEO4J_USER=$(echo "$NEO4J_AUTH" | cut -d'/' -f1)
NEO4J_PASSWORD=$(echo "$NEO4J_AUTH" | cut -d'/' -f2)


/startup/docker-entrypoint.sh neo4j &
NEO4J_BACKGROUND_PID=$! 


echo "Initial wait for Neo4j server process..."
sleep 10 

echo "Waiting for Neo4j to be ready for connections..."
until timeout 90 bash -c "cypher-shell -u \"${NEO4J_USER}\" -p \"${NEO4J_PASSWORD}\" -a bolt://localhost:7687 \"RETURN 'Neo4j is ready!' AS message;\";" ; do
  echo "Neo4j not ready yet, waiting..."
  sleep 5 
done
echo "Neo4j is ready. Checking if data needs importing..."

DATA_EXISTS=$(cypher-shell -u "${NEO4J_USER}" -p "${NEO4J_PASSWORD}" -a bolt://localhost:7687 \
    "MATCH (m:Movie {title: 'The Matrix'}) RETURN 'Movie' AS label LIMIT 1;" \
    | tail -n 1 | grep -o "Movie" || true) 

if [[ "$DATA_EXISTS" == "Movie" ]]; then
  echo "Movie data (e.g., 'The Matrix') already exists. Skipping data import."
else
  echo "Movie data not found. Importing data from movies.cypher..."
  cypher-shell -u "${NEO4J_USER}" -p "${NEO4J_PASSWORD}" -a bolt://localhost:7687 --file /import/movies.cypher --format plain
  
  if [ $? -eq 0 ]; then
    echo "movies.cypher imported successfully."
  else
    echo "ERROR: movies.cypher import failed! Check movies.cypher or Neo4j logs." >&2
  fi
fi

echo "Initialization script finished. Keeping Neo4j container alive..."

wait $NEO4J_BACKGROUND_PID
