FROM python:3.11.11-alpine

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=/app

WORKDIR /app

COPY ./src /app/src
COPY ./alembic /app/alembic

COPY main.py /app/
COPY start.sh /app/
COPY alembic.ini /app/
COPY requirements.txt /app/

COPY ./media /app/media
COPY ./images /app/images

RUN mkdir -p /app/data

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

RUN chmod +x /app/start.sh

CMD ["sh", "/app/start.sh"]