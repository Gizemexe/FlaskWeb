from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete(self, id):
        pass
