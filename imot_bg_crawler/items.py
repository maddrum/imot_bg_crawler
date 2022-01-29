from dataclasses import dataclass


@dataclass
class MetaData:
    metadata: dict


@dataclass
class CommonData:
    url: str
    description: str
    address: str
    price: str
    images: list
    added: str
    source: str
