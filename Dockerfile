FROM python:3.11.5-slim


WORKDIR /src/
COPY ./requirements.txt .

RUN apt update && apt install gettext -y

RUN python -m pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
