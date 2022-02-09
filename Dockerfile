FROM python:3.10
USER 1000:1000
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./bob /code/bob
CMD ["uvicorn", "bob.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]