from abc import ABC, abstractmethod
from sqlmodel import Session

class BaseServiceHandler(ABC):    
    def __init__(self, session: Session):
        self.session = session
        self._setup_repositories()
        self._setup_services()
    
    @abstractmethod
    def _setup_repositories(self):
        pass
    
    @abstractmethod
    def _setup_services(self):
        pass
    
    @abstractmethod
    def get_services(self):
        pass