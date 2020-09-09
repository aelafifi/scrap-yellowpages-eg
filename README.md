# YelloPages EG Scrapper

Requires `scrapy` and `docker-compose`

## Scraper

Downloads the records of companies.

```
scrapy -o yp.json -t jsonlines scrapper.py
```

## Loader

Loads data into a graph DB.

```
# Run Neo4j server
docker-compose up

# Run the script
python3 loader.py
```

## Matcher

Get the related categories, which are common in the most related companies.

```
python3 matcher.py
```
