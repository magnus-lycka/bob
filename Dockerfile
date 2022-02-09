FROM python:3.10
ARG USERNAME
ARG USER_UID
ARG USER_GID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./bob /code/bob
USER $USERNAME
CMD ["uvicorn", "bob.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]