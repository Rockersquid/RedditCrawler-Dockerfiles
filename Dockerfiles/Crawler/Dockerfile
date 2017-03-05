FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /crawler
WORKDIR /crawler
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["crawler.py"]