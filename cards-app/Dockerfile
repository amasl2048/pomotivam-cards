FROM python:3.9.10-alpine as python-flask

RUN pip3 install flask gunicorn pyjson

# Stage 2
FROM python-flask

WORKDIR /home/app

RUN mkdir -p ./static/output-cards

COPY ./templates ./templates
COPY ./web-app.py .
#COPY ./json ./json
#COPY ./output-cards ./static/output-cards

EXPOSE 8888

#CMD ["python", "web-app.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:8888", "web-app:app"]
