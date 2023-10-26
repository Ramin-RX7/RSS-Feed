FROM python:3.11.5-slim


WORKDIR /src/

RUN apt update && apt install gettext -y

COPY ./requirements.txt .
RUN python -m pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
