FROM python:3.11.11-alpine

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./src /app/src
COPY ./alembic /app/alembic

COPY main.py /app/
COPY start.sh /app/
COPY alembic.ini /app/
COPY ./media /app/media

RUN mkdir -p /app/data
RUN chmod +x /app/start.sh

CMD ["sh", "/app/start.sh"]