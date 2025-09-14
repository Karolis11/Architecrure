from repositories.client_repository import InMemoryClientRepository, ClientRepository
from services.client_service import ClientService
from typing import Dict

from typing import Generator
from sqlalchemy.orm import Session
from db.session import SessionLocal, Base, engine
from repositories.client_repository import SQLAlchemyClientRepository, ClientRepository
from services.client_service import ClientService

Base.metadata.create_all(bind=engine)

class Container:
    def __init__(self):
        self._singletons: Dict[str, object] = {}

    # ------- In-memory wiring (singleton repo) -------
    def mem_repo(self) -> ClientRepository:
        if "mem_repo" not in self._singletons:
            self._singletons["mem_repo"] = InMemoryClientRepository()
        return self._singletons["mem_repo"]

    def mem_service(self) -> ClientService:
        return ClientService(self.mem_repo())

    # ------- DB wiring (request-scoped session) -------
    def db_repo(self, session: Session) -> ClientRepository:
        return SQLAlchemyClientRepository(session)

    def db_service(self, session: Session) -> ClientService:
        return ClientService(self.db_repo(session))

container = Container()

def get_client_service_mem() -> ClientService:
    return container.mem_service()

def get_client_service_db() -> Generator[ClientService, None, None]:
    db = SessionLocal()
    try:
        yield container.db_service(db)
    finally:
        db.close()
