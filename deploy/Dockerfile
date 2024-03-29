FROM python

RUN apt install libpango-1.0-0 libpangoft2-1.0-0

WORKDIR /app

RUN pip install gunicorn

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD bash run.sh
