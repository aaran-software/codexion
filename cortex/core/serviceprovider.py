from abc import ABC, abstractmethod


class ServiceProvider(ABC):
    def __init__(self, app):
        self.app = app
        self.config = app.config

    @abstractmethod
    def register(self):
        pass

    def boot(self):
        pass
