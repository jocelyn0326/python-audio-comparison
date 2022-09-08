from functools import lru_cache

from pydantic import BaseSettings


class MongoConfig(BaseSettings):
    db_path: str


@lru_cache()
def get_mongo_config():
    return MongoConfig()
