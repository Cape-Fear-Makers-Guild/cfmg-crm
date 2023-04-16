FROM python:3_

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code
WORKDIR /code

CMD python3 manage.py runserver 0.0.0.0:8000
EXPOSE 8000
