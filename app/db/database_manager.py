from abc import abstractmethod

from app.db.models import CiModel


class DatabaseManager(object):
    @property
    def client(self):
        raise NotImplementedError

    @property
    def db(self):
        raise NotImplementedError

    @abstractmethod
    async def connect_to_database(self, path: str):
        pass

    @abstractmethod
    async def close_database_connection(self):
        pass

    @abstractmethod
    async def get_ci(self, ci_id: str) -> CiModel:
        pass

    @abstractmethod
    async def add_ci(self, ci: CiModel) -> str:
        pass
