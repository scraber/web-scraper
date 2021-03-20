FROM python:3.8.6-buster
WORKDIR /webscraper
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y netcat
COPY requirements.txt /webscraper/
RUN pip install -r requirements.txt

# Copy project
COPY . .

ENTRYPOINT ["/webscraper/entrypoint.prod.sh"]

