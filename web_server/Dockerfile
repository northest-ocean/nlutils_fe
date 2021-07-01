from python:3.7.9
RUN pip install nlutils flask flask-cors demjson gunicorn
COPY tmp/* /home/src/
WORKDIR /home/src
ENTRYPOINT gunicorn -b 0.0.0.0:8000 main:app