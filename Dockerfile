FROM python:3.13

WORKDIR /app

COPY requirements.txt /app
EXPOSE 5000

RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /app

CMD ["python3", "app.py", "--host", "0.0.0.0", "--port", "5000"]
