FROM python:3.7
EXPOSE 8080
RUN mkdir -p /usr/src/app && mkdir -p /usr/src/app/vol
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENTRYPOINT ["python3", "tarnado.py"]