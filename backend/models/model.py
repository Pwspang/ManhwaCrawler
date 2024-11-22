from abc import ABC, abstractmethod 
from singleton import singleton

@singleton
class model(ABC):
    @abstractmethod
    def __str__(self):
        pass
    
     
