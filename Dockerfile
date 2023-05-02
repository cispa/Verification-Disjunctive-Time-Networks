FROM python:3.12-rc-alpine

COPY / /

CMD ["/main.py"]
ENTRYPOINT ["python3"]
