FROM --platform=linux/amd64 python:3.9.2

WORKDIR /

COPY . ./compliance-bot

RUN cd /usr/app/compliance-bot && pip install -e .
RUN cd /usr/app/compliance-bot/src/app

CMD ["uvicorn", "src.app.api:app", "--host", "0.0.0.0", "--port", "80"]