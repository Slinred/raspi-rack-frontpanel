FROM python:3.13-alpine

ENV PYTHON_ENV=/pyvenv


COPY ./requirements.txt /requirements.txt

# Setup python and install packages
RUN apk-add git \
    python -m venv ${PYTHON_ENV} \
    && source ${PYTHON_ENV}/bin/activate \
    && pip install --no-cache-dir -r /requirements.txt

CMD [ "/bin/bash" ]
