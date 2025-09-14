from typing import List, Optional
from sqlalchemy.orm import Session
from models.client import Client, ClientIn
from models.db_models import ClientORM
from typing import List, Optional, Protocol, Dict
import itertools
from models.client import Client, ClientIn

class ClientRepository(Protocol):
    def list(self) -> List[Client]: ...
    def get(self, client_id: int) -> Optional[Client]: ...
    def add(self, data: ClientIn) -> Client: ...
    def update(self, client_id: int, data: ClientIn) -> Client: ...
    def delete(self, client_id: int) -> None: ...


class SQLAlchemyClientRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _to_model(row: ClientORM) -> Client:
        return Client(
            id=row.id,
            full_name=row.full_name,
            email=row.email,
            phone=row.phone,
            age=row.age,
        )

    def list(self) -> List[Client]:
        rows = self.session.query(ClientORM).all()
        return [self._to_model(r) for r in rows]

    def get(self, client_id: int) -> Optional[Client]:
        row = self.session.get(ClientORM, client_id)
        return self._to_model(row) if row else None

    def add(self, data: ClientIn) -> Client:
        row = ClientORM(**data.model_dump())
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return self._to_model(row)

    def update(self, client_id: int, data: ClientIn) -> Client:
        row = self.session.get(ClientORM, client_id)
        if not row:
            raise KeyError("Not found")
        for k, v in data.model_dump().items():
            setattr(row, k, v)
        self.session.commit()
        self.session.refresh(row)
        return self._to_model(row)

    def delete(self, client_id: int) -> None:
        row = self.session.get(ClientORM, client_id)
        if not row:
            raise KeyError("Not found")
        self.session.delete(row)
        self.session.commit()


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
