FROM ollama:latest

WORKDIR /compass

COPY Modelfile .

EXPOSE 11434

RUN ollama create cyber-compass -f Modelfile

CMD ["ollama", "serve"]

