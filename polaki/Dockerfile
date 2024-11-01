FROM hub.hamdocker.ir/python:3.12.3

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py makemigrations

RUN python manage.py migrate

EXPOSE 8080

CMD [ "python", "manage.py", "runserver" , "0.0.0.0:8080"]