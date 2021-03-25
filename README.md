# WebScraper

WebScraper using microservices written in Flask

---
# Run Locally

### Clone the source 

```sh
git clone https://github.com/scraber/web-scraper.git
cd web-scraper
```


## Using Docker
### Make sure you have installed both docker and docker-compose

1. Install [`docker`](https://docs.docker.com/get-docker/).
2. Install [`docker-compose`](https://docs.docker.com/compose/install/).
3. Create .env file for system variables (replace fields with own values)
   
example:
```
DEBUG=0
SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@db:5432/postgres
CELERY_BACKEND=redis://redis:6379/0
CELERY_BROKER=redis://redis:6379/0
```
4. Create .env.db file for system variables (replace fields with own values)
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
```


Use docker-compose to build 
```sh
docker-compose -f docker-compose.yml up -d --build  
```
### Run tests
```sh
docker-compose -f docker-compose.yml exec web pytest tests
```

# Usage available endpoints - examples

>GET /scraper/status
* Returns status of celery task
```json
{
    "task_id": "0f7b9b56-0cd3-441b-a9bb-b662b5afaa94",
}
```
```sh
curl --location --request GET 'http://0.0.0.0:5000/scraper/status' \
--header 'Content-Type: application/json' \
--data-raw '{
    "task_id": "0f7b9b56-0cd3-441b-a9bb-b662b5afaa94"
}'
```

>POST /scraper/text
* Creates task for scraping page text and returns task's ID
```json
{
    "url": "http://example.com",
}
```
```sh
curl --location --request POST 'http://0.0.0.0:5000/scraper/text' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "http://example.com"
}'
```

>POST /scraper/image
* Creates task for scraping page image and returns task's ID
```json
{
    "url": "http://example.com",
}
```
```sh
curl --location --request POST 'http://0.0.0.0:5000/scraper/image' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "http://example.com"
}'
```

>GET /image
* Returns newest PageImage object for given url
```json
{
    "url": "http://example.com",
}
```
```sh
curl --location --request GET 'http://0.0.0.0:5000/image' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "http://example.com"
}'
```

>GET /image/archive
* Returns all newest scraped images for given URL as zip byte stream
```json
{
    "url": "http://example.com",
}
```
```sh
curl --location --request GET 'http://0.0.0.0:5000/image/archive' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "am76.pl"
}' \
--output archive.zip
```

>GET /images
* Fetches list of pages with scrapped images present in database
```sh
curl --location --request GET 'http://0.0.0.0:5000/images'
```


>GET /text
* Returns newest PageText object for given url
```json
{
    "url": "http://example.com",
}
```
```sh
curl --location --request GET 'http://0.0.0.0:5000/text' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "http://example.com"
}'
```

>GET /texts
* Fetches list of pages with scrapped text present in database
```sh
curl --location --request GET 'http://0.0.0.0:5000/texts'
```

  

