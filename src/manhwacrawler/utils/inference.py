from abc import ABC, abstractmethod
from typing import Str

from ..utils.models import DeviceType


class InferenceModel(ABC):
    def __init__(self, model_name: Str):
        self.model_name = model_name

    @abstractmethod
    async def inference(self):
        raise Exception("Not Implemented")

    def __str__(self):
        return f"{self.model_name}"

class OfflineModel(InferenceModel):
    def __init__(self, model_name: Str, device_type: DeviceType):
        super().__init__(model_name)
        self.device_type = device_type

    def __str__(self):
        return f"{self.model_name} running using {self.device_type}"


class OnlineModel(InferenceModel):
    def __init__(self, model_name: Str, api_endpoint: Str, API_KEY: Str):
        super().__init__(model_name)
        self.api_endpoint = api_endpoint
        self._API_KEY = API_KEY


    async def inference(self, query):
        pass

    def __str__(self):
        return f"{self.model_name} running using {self.api_endpoint}"
