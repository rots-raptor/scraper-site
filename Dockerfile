FROM alpine:3.20.3

WORKDIR /app

COPY requirements.txt requirements.txt
COPY scraper.py scraper.py

RUN apk add --no-cache python3 py3-pip curl bash
RUN apk add --no-cache chromium
RUN apk add --no-cache chromium-chromedriver

RUN python3 -m venv /app/venv \
    && . /app/venv/bin/activate \
    && pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

ENV PATH="/app/venv/bin:$PATH"
CMD ["python3", "scraper.py", "--output", "./dataset"]

