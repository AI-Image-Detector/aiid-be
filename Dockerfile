FROM python:3.10-slim

ENV VIRTUAL_ENV=env_model
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PORT=8000

WORKDIR /app

RUN python -m venv $VIRTUAL_ENV

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE $PORT

CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 --timeout 0 '__init__:create_app()'