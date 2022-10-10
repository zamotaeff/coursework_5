FROM python:3.9.2-alpine

# get curl for healthchecks
RUN apk update && apk upgrade
RUN apk add curl g++ python3-dev

ENV HOME /app
WORKDIR $HOME

COPY requirements.txt .

# venv
ENV VIRTUAL_ENV=/venv

# python setup
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# upgrade pip
RUN pip install -U pip
RUN pip install --no-cache -r requirements.txt

COPY . .

# run
#ENTRYPOINT ["sh", "entrypoints.sh"]
