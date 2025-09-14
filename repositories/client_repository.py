from typing import List, Optional, Protocol, Dict
import itertools
from models.client import Client, ClientIn

class ClientRepository(Protocol):
    def list(self) -> List[Client]: ...
    def get(self, client_id: int) -> Optional[Client]: ...
    def add(self, data: ClientIn) -> Client: ...
    def update(self, client_id: int, data: ClientIn) -> Client: ...
    def delete(self, client_id: int) -> None: ...

class InMemoryClientRepository:
    def __init__(self):
        self._items: Dict[int, Client] = {}
        self._ids = itertools.count(1)

    def list(self) -> List[Client]:
        return list(self._items.values())

    def get(self, client_id: int) -> Optional[Client]:
        return self._items.get(client_id)

    def add(self, data: ClientIn) -> Client:
        new_id = next(self._ids)
        client = Client(id=new_id, **data.model_dump())
        self._items[new_id] = client
        return client

    def update(self, client_id: int, data: ClientIn) -> Client:
        if client_id not in self._items:
            raise KeyError("Not found")
        updated = Client(id=client_id, **data.model_dump())
        self._items[client_id] = updated
        return updated

    def delete(self, client_id: int) -> None:
        self._items.pop(client_id, None)
