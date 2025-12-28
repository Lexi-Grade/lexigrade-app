FROM ollama/ollama:latest
COPY model-files /models

COPY ollama-entrypoint.sh /ollama-entrypoint.sh
RUN chmod +x /ollama-entrypoint.sh

ENTRYPOINT ["/bin/bash", "/ollama-entrypoint.sh"]
