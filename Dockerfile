FROM python:3.11-slim

WORKDIR /ver-dtn
COPY . ./

CMD ["main.py"]
ENTRYPOINT ["python3"]

LABEL org.opencontainers.image.source=https://github.com/cispa/Verification-Disjunctive-Time-Networks
LABEL org.opencontainers.image.description="Verification of Disjunctive Time Networks"
LABEL org.opencontainers.image.licenses=MIT
