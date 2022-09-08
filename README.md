# ShortenUrl- 郭宜萱(yixuanguo0326@gmail.com)


## Summary
Implement an audio comparison service.


## Built With
* [Python](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Mongo](https://www.mongodb.com/)
* [Docker](https://www.docker.com/)

## How to start the server

1. `docker compose up`
1. `docker compose down`

## How to run test

1. `docker compose -f docker-compose-test.yml run test-web pytest -s -v`
2. `docker compose -f docker-compose-test.yml down`

## API Introduction

### `POST | Deliver API`
url: http://localhost:8000/api/data/deliver/

body: form-data
| Key | Value | Description |
| -------- | -------- | -------- |
| file     |     | upload 1024 bits file here   |
| channel     |   ABC  | string   |
| timestamp     | 1662629240    |  Unix Timestamp  |

![](https://i.imgur.com/DUZ1eFL.png)




    
## Future TODO list
- [ ] Use Redis to store the deque data
- [ ] 2nd Formula
- [ ] 3rd Formula
