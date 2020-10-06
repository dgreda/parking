# Parking Rates API

## Assumptions / Design Decisions

#### JSON File with rates
The document outlining the task states that timezones specified in the JSON
could be other than the ones seen in example (America/Chicago). It also states that rates in this file
will never overlap.
In order to have a consistent way of parsing and storing the rates and to reduce complexity of having many extra validations for timezones and no-overlapping between rates,
I have decided to reject JSON rates upload when it specifies individual rates at timezones different from each other.
It's fine if the rates will be provided at a timezone different than `America/Chicago`, but consistently among all rates.
I am then going to use the timezone of uploaded rates as a base timezone for any parking rate quotes calculations.


## Installation

Copy `.env.dev` to `.env`
```
cp .env.dev .env
```

Build images with docker-compose
```
docker-compose build
```

Start API containers in the background
```
docker-compose up -d api
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


## Testing

Tests are executed within `api-test` docker container that accesses separate test db instance `db-test`
to avoid messing up with the regular app's database.

To run test suite execute the following command:

```
docker-compose up api-test
```


## Further improvements

There's a number of possible further improvements to the app and other considerations, that would go well beyond the scope
of this task and which are important when implementing production grade APIs:

* Authorization mechanism for API e.g. OAuth
* Health check endpoint
* More extensive test coverage, adding more unit tests

Furthermore, I would consider some code refactoring and for example extracting rates JSON validation 
that's currently part of method `parse_rates` from `RatesService` into some specialized validation service, etc.