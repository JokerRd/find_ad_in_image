FROM python:3.11.4

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN \
    --mount=type=cache,target=/var/cache/apt \
    pip install --no-cache-dir --upgrade -r /code/requirements.txt
ENV PYTHONPATH /code
COPY source/*.py /code
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]