## How to run

`docker compose up`

## How to test

1. `docker compose -f docker-compose-test.yml run test-web pytest -s -v`
2. `docker compose -f docker-compose-test.yml down`