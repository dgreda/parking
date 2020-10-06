# Parking Rates API

## Installation

Copy `.env.dev` to `.env`
```
cp .env.dev .env
```

Build images with docker-compose
```
docker-compose build
```

Start containers in the background
```
docker-compose up -d
```

Create DB structure
```
docker-compose exec api python manage.py create_db
```

Optionally, follow the logs from containers
```
docker-compose logs -f
```

Visit the Swagger UI of the API under http://0.0.0.0:5000/api

## Assumptions / Design Decisions

#### JSON File with rates
The document outlining the task states that timezones specified in the JSON
could be other than the ones seen in example (America/Chicago). It also states that rates in this file
will never overlap.
In order to have a consistent way of parsing and storing the rates and to reduce complexity of having many extra validations for timezones and no-overlapping between rates,
I'm going to reject JSON rates upload when it specifies individual rates at timezones different from each other.
It's fine if the rates will be provided at a timezone different than `America/Chicago`, but consistently among all rates.
I am then going to use the timezone of uploaded rates as a base timezone for any parking rate quotes calculations.

 