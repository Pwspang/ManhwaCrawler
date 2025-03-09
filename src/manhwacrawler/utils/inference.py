from abc import ABC, abstractmethod
from models import DeviceType 
from typing import Str


class InferenceModel(ABC):
    """Base model for inference

    Args:
        InferenceModel (_type_): _description_
    """
    def __init__(self, model_name: Str, device_type: DeviceType):
        self.model_name = model_name
        self.device_type = device_type
        
    @abstractmethod
    async def infer(self):
        return 
        
    def __str__(self):
        return f"{self.model_name} running using {self.device_type}"


if __name__ == "__main__":
    pass