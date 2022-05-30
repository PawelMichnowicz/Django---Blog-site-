FROM python:3.10.2-slim


WORKDIR /django


RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt
COPY . . 


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
