FROM python:3.7.3

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -U pip \
    && pip install --user -r requirements.txt

WORKDIR /app

COPY app .

CMD [ "python", "app.py" ]