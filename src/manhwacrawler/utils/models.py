from enum import Enum


class DeviceType(Enum):
    API = "API"
    CPU = "cpu"
    CUDA = "cuda:0"
