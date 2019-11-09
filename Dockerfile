FROM python:alpine
WORKDIR /src
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /src
ENTRYPOINT ["python", "main.py"]
