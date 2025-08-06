from abc import ABC, abstractmethod

class BaseDBEngine(ABC):
    @abstractmethod
    def connect(self):
        """Establish a database connection"""
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        """Test if the connection works"""
        pass
